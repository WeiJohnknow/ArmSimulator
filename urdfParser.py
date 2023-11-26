import xml.etree.ElementTree as ET
import math
import numpy as np
import pygame
from pygame.locals import *
import glm  # 安装PyGLM库 pip install PyGLM
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileProgram, compileShader
import stl

# 定义顶点着色器和片元着色器
vertex_shader = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec4 aColor;

out vec4 vertexColor;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    vertexColor = aColor;
}
"""

fragment_shader = """
#version 330 core
in vec4 vertexColor;
out vec4 FragColor;

void main()
{
    FragColor = vertexColor;
}
"""
shader_program = None


# 解析URDF文件，获取关节和链接信息
def parse_urdf(urdf_file):
    tree = ET.parse(urdf_file)
    
    root = tree.getroot()
    links = {}
    joints = {}
    materials ={}
    for material in root.findall('material'):
        color = material.find('color')
        materials[material.get('name')] =  np.array( color.get('rgba').split(), dtype=float)
    
    
    
    for link in root.findall('link'):
        link_name = link.get('name')
        links[link_name] = {'visual': {}}
        visual = link.find('visual')
        geometry = visual.find('geometry')
        origin = visual.find('origin')
        material = visual.find('material')
        links[link_name]['visual']['material'] = materials[material.get('name')]
        links[link_name]['visual']['origin']={'origin': {}}
        
        xyz = origin.get('xyz')
        rpy = origin.get('rpy')
        if  type(rpy)==type(None):
            links[link_name]['visual']['origin']['rpy'] = np.array( [0,0,0], dtype=float)
        else:
            links[link_name]['visual']['origin']['rpy'] = np.array( origin.get('rpy').split(), dtype=float)

        if  type(xyz)==type(None):
            links[link_name]['visual']['origin']['xyz'] = np.array( [0,0,0], dtype=float)
        else:
            links[link_name]['visual']['origin']['xyz'] = np.array( origin.get('xyz').split(), dtype=float)

        mesh = geometry.find('mesh')
        links[link_name]['visual']['mesh'] = {'mesh': {}}
        links[link_name]['visual']['mesh']['filename'] = mesh.get('filename')[10:]
        links[link_name]['visual']['mesh']['scale'] =np.array( mesh.get('scale').split(), dtype=float)

        vertices,normals,colors = create_STL(links[link_name]['visual']['mesh']['filename'],links[link_name]['visual']['material'] ,links[link_name]['visual']['mesh']['scale'])

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        # 创建和绑定顶点缓冲对象
        vbo_vertices = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)

        # 创建和绑定法线缓冲对象
        vbo_normals = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)

        # 创建和绑定颜色缓冲对象
        vbo_colors = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_colors)
        glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        links[link_name]['visual']['mesh']['vao'] = vao
        links[link_name]['visual']['mesh']['lens'] = len(vertices) 
        links[link_name]['visual']['mesh']['vertices']  = vertices
        links[link_name]['visual']['mesh']['normals']  = normals
        links[link_name]['visual']['mesh']['colors']  = colors
    


    for joint in root.findall('joint'):
        joint_name = joint.get('name')
        parent = joint.find('parent').get('link')
        child = joint.find('child').get('link')

        origin = joint.find('origin')
        axis =  joint.find('axis')
        limit = joint.find('limit')

        joints[joint_name] = {'parent': parent, 'child': child}
        joints[joint_name]['rad']=0.0
        joints[joint_name]['origin'] = {'origin': {}}
        xyz = origin.get('xyz')
        rpy = origin.get('rpy')
        if  type(rpy)==type(None):
            joints[joint_name]['origin']['rpy'] = np.array( [0,0,0], dtype=float)
        else:
            joints[joint_name]['origin']['rpy'] = np.array( origin.get('rpy').split(), dtype=float)

        if  type(xyz)==type(None):
            joints[joint_name]['origin']['xyz'] = np.array( [0,0,0], dtype=float)
        else:
            joints[joint_name]['origin']['xyz'] = np.array( origin.get('xyz').split(), dtype=float)

        xyz = axis.get('xyz')
        if  type(xyz)==type(None):
            joints[joint_name]['axis'] = np.array( [0,0,0], dtype=float)
        else:
            joints[joint_name]['axis'] = np.array( axis.get('xyz').split(), dtype=float)
        
        joints[joint_name]['limmit'] = {'limmit': {}}
        joints[joint_name]['limmit']['effort'] =np.array(  limit.get('effort'), dtype=float)
        joints[joint_name]['limmit']['lower'] =np.array(  limit.get('lower'), dtype=float)
        joints[joint_name]['limmit']['upper'] =np.array(  limit.get('upper'), dtype=float)
        
    return links, joints


# # 绘制URDF模型
# def draw_urdf(links, joints):
#     for joint_name, joint_info in joints.items():
#         parent_link = joint_info['parent']
#         child_link = joint_info['child']
#         parent_link_info = links[parent_link]
#         child_link_info = links[child_link]
#         parent_mesh = parent_link_info['visual']['mesh']
#         child_mesh = child_link_info['visual']['mesh']
#         # 在此处计算关节变换并绘制链接的模型

def create_STL(your_stl_file = 'motoman_mh12_support\meshes\visual\mh12_base_link.stl',material=[1,0,0,0.5],scale=1.0):
    # 載入 STL 模型
    stl_mesh = stl.Mesh.from_file(your_stl_file)
    vertices = (np.array(stl_mesh.vectors.reshape(-1,3)) *scale).reshape(-1)
    normals = np.repeat(stl_mesh.normals, 3, axis=0).reshape(-1)
    colors = np.ones(len(stl_mesh.normals)*3*4)
    colors[0::4] = material[0]
    colors[1::4] = material[1]
    colors[2::4] = material[2]
    colors[3::4] = material[3]

    return np.array(vertices, dtype=np.float32), np.array(normals, dtype=np.float32), np.array(colors, dtype=np.float32)

def draw_stl_with_color(vertices, normals, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(4, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)

    glDrawArrays(GL_TRIANGLES, 0, len(vertices)//3)  #len(vertices)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

def draw_object(vao,lens,mat,view,projection):
    global shader_program
    glUseProgram(shader_program)
    glm_mat = glm.mat4(*mat.flatten())

    # 获取着色器中Uniform变量的位置
    

    # 使用glUniformMatrix4fv将矩阵传递到着色器
    
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, 'view')
    projection_loc = glGetUniformLocation(shader_program, 'projection')
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(glm_mat))
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection))
    
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, lens)
    glBindVertexArray(0)
    glUseProgram(0)


def draw_floor_with_color(vertices, normals, colors):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(4, GL_FLOAT, 0, colors)
    glNormalPointer(GL_FLOAT, 0, normals)

    glDrawArrays(GL_QUADS, 0, len(vertices))  #len(vertices)

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_COLOR_ARRAY)

# 定義地板的頂點和法向量
def create_floor_grid(rows, cols, size):
    vertices = []
    normals = []
    colors = []
    
    for row in range(-rows,rows):
        for col in range(-cols,cols):
            vertices.append([col * size,  row * size,0])
            vertices.append([(col+1) * size, row * size,0])
            vertices.append([(col+1) * size, (row+1) * size,0])
            vertices.append([col * size,  row * size,0])
            vertices.append([(col+1) * size, (row+1) * size,0])
            vertices.append([col * size, (row+1) * size,0])
            normals.append([0, 0, 1.0])
            normals.append([0, 0, 1.0])
            normals.append([0, 0, 1.0])
            normals.append([0, 0, 1.0])
            normals.append([0, 0, 1.0])
            normals.append([0, 0, 1.0])
            
            # 黑白交替的顏色
            color = [1.0,1.0,1.0,0.5] if (row + col) % 2 == 0 else [0.5,0.5,0.5,0.5]
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
            colors.append(color)
    
    vertices = np.array(vertices, dtype=np.float32).reshape(-1)
    normals = np.array(normals, dtype=np.float32).reshape(-1)
    colors = np.array(colors, dtype=np.float32).reshape(-1)
    
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    # 创建和绑定顶点缓冲对象
    vbo_vertices = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # 创建和绑定法线缓冲对象
    vbo_normals = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_normals)
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # 创建和绑定颜色缓冲对象
    vbo_colors = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_colors)
    glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
    glVertexAttribPointer(2, 4, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(2)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    return vao,len(vertices),vertices,normals,colors

def draw_urdf(links, joints,view,projection):
    glPushMatrix()  # 保存当前模型视图矩阵

    H_ = np.eye(4)
    #test
    for joint_name, joint_info in joints.items():
        parent_link = joint_info['parent']
        child_link = joint_info['child']
        joint_origin = joint_info['origin']
        parent_link_info = links[parent_link]
        child_link_info = links[child_link]
        parent_mesh = parent_link_info['visual']['mesh']
        parent_origin = parent_link_info['visual']['origin']
        child_mesh = child_link_info['visual']['mesh']
        child_origin = child_link_info['visual']['origin']

        #scale = parent_link_info['visual']['mesh']['scale']

        # 获取关节类型和关节角度
        joint_type = 'revolute'  # 假设关节类型为旋转关节
        joint_angle = joint_info['rad']

        # 绘制链接的模型
        glPushMatrix()  # 保存当前链接的模型视图矩阵

        H__ =H_ @ rpy_to_homogeneous(parent_origin['xyz'],parent_origin['rpy'])
        # glLoadMatrixf(H__.T)

        H_ =H_ @ rpy_to_homogeneous(joint_origin['xyz'],joint_origin['rpy'])
        H_ =H_ @ rpy_to_homogeneous([0,0,0],joint_info['axis']*joint_angle)
        # if joint_type == 'revolute':
        #     # 根据关节类型和角度进行变换
        #     axis = joint_info['axis']
        #     glRotatef(math.degrees(joint_angle), 0, 0, 1)  # 以Z轴为旋转轴进行旋转
        # 绘制链接的模型，此处需要加载并渲染STL模型
        # 例如，可以使用PyOpenGL的glutSolidCube等函数绘制基本几何体
        # 或者使用第三方库（如trimesh）加载和绘制STL模型
        draw_object(parent_mesh['vao'],parent_mesh['lens'],H__.T,view,projection)
        # draw_stl_with_color(parent_mesh['vertices'],parent_mesh['normals'],parent_mesh['colors'] )
        glPopMatrix()  # 恢复到链接前的模型视图矩阵

        if joint_name=='j6':
            glPushMatrix()  # 保存当前链接的模型视图矩阵

            H__ =H_ @ rpy_to_homogeneous(child_origin['xyz'],child_origin['rpy'])
            # glLoadMatrixf(H__.T)
            draw_object(child_mesh['vao'],child_mesh['lens'],H__.T,view,projection)
            # draw_stl_with_color(child_mesh['vertices'],child_mesh['normals'],child_mesh['colors'] )
            glPopMatrix()  # 恢复到链接前的模型视图矩阵

        # glPushMatrix()  # 保存当前链接的模型视图矩阵

        # H_ = rpy_to_homogeneous(child_origin['xyz'],child_origin['rpy'])
        # glLoadMatrixf(H_.T)
        # # if joint_type == 'revolute':
        # #     # 根据关节类型和角度进行变换
        # #     axis = joint_info['axis']
        # #     glRotatef(math.degrees(joint_angle), 0, 0, 1)  # 以Z轴为旋转轴进行旋转
        # # 绘制链接的模型，此处需要加载并渲染STL模型
        # # 例如，可以使用PyOpenGL的glutSolidCube等函数绘制基本几何体
        # # 或者使用第三方库（如trimesh）加载和绘制STL模型

        # draw_stl_with_color(child_mesh['vertices'],child_mesh['normals'],child_mesh['colors'] )
        # glPopMatrix()  # 恢复到链接前的模型视图矩阵

        # 计算关节的变换矩阵
        # if joint_type == 'revolute':
        #     joint_matrix = np.identity(4)
        #     joint_matrix[:3, :3] = np.array([
        #         [math.cos(joint_angle), -math.sin(joint_angle), 0],
        #         [math.sin(joint_angle), math.cos(joint_angle), 0],
        #         [0, 0, 1]
        #     ])
        # 使用关节的变换矩阵，将子链接的模型变换到关节坐标系下
        # 这里需要根据关节类型、关节轴等信息进行变换
        # 然后将子链接的模型绘制到关节坐标系中

    glPopMatrix()  # 恢复到最初的模型视图矩阵

def rpy_to_homogeneous(xyz,rpy):

    Px= xyz[0]
    Py= xyz[1]
    Pz= xyz[2]
    r= rpy[0]
    p= rpy[1]
    y= rpy[2]
    # Roll
    R_x = np.array([[1,         0,          0],
                    [0, np.cos(r), -np.sin(r)],
                    [0, np.sin(r),  np.cos(r)]])

    # Pitch
    R_y = np.array([[np.cos(p), 0, np.sin(p)],
                    [0,         1,         0],
                    [-np.sin(p), 0, np.cos(p)]])

    # Yaw
    R_z = np.array([[np.cos(y), -np.sin(y), 0],
                    [np.sin(y),  np.cos(y), 0],
                    [0,         0,         1]])

    # Combined rotation matrix
    #R = np.dot(R_z, np.dot(R_y, R_x))
    R = R_z @ R_y @ R_x
    # Homogeneous transformation matrix
    H = np.eye(4)
    H[:3, :3] = R
    H[0,3] = Px
    H[1,3] = Py
    H[2,3] = Pz
    return H
# 主循环
def main(urdf_file):
    global shader_program
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    shader_program = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )
    floor_vao,floor_lens,floor_vertices, floor_normals, floor_colors = create_floor_grid(20, 20, 0.5)
    links, joints = parse_urdf(urdf_file)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)


    camera_alpha = 45
    camera_angle = 0.0  # 旋轉角度
    camera_dis = 2.0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_q]:
            camera_angle += 1  # 旋轉攝影機角度
        if keys[pygame.K_e]:
            camera_angle -= 1  # 旋轉攝影機角度
        
        if keys[pygame.K_w]:
            camera_alpha -= 1  # 旋轉攝影機角度
        if keys[pygame.K_s]:
            camera_alpha += 1  # 旋轉攝影機角度
        
        if keys[pygame.K_1]:
            camera_dis += 0.1  # 旋轉攝影機角度
        if keys[pygame.K_2]:
            camera_dis -= 0.1  # 旋轉攝影機角度

        # # puma560
        # if keys[pygame.K_4]:
        #     joints['j1']['rad'] += 0.01
        # if keys[pygame.K_r]:
        #     joints['j1']['rad'] -= 0.01
        # if keys[pygame.K_5]:
        #     joints['j2']['rad'] += 0.01
        # if keys[pygame.K_t]:
        #     joints['j2']['rad'] -= 0.01
        # if keys[pygame.K_6]:
        #     joints['j3']['rad'] += 0.01
        # if keys[pygame.K_y]:
        #     joints['j3']['rad'] -= 0.01
        # if keys[pygame.K_7]:
        #     joints['j4']['rad'] += 0.01
        # if keys[pygame.K_u]:
        #     joints['j4']['rad'] -= 0.01
        # if keys[pygame.K_8]:
        #     joints['j5']['rad'] += 0.01
        # if keys[pygame.K_i]:
        #     joints['j5']['rad'] -= 0.01
        # if keys[pygame.K_9]:
        #     joints['j6']['rad'] += 0.01
        # if keys[pygame.K_o]:
        #     joints['j6']['rad'] -= 0.01

        # mh12
        if keys[pygame.K_4]:
            joints['joint_1_s']['rad'] += 0.01
        if keys[pygame.K_r]:
            joints['joint_1_s']['rad'] -= 0.01
        if keys[pygame.K_5]:
            joints['joint_2_l']['rad'] += 0.01
        if keys[pygame.K_t]:
            joints['joint_2_l']['rad'] -= 0.01
        if keys[pygame.K_6]:
            joints['joint_3_u']['rad'] += 0.01
        if keys[pygame.K_y]:
            joints['joint_3_u']['rad'] -= 0.01
        if keys[pygame.K_7]:
            joints['joint_4_r']['rad'] += 0.01
        if keys[pygame.K_u]:
            joints['joint_4_r']['rad'] -= 0.01
        if keys[pygame.K_8]:
            joints['joint_5_b']['rad'] += 0.01
        if keys[pygame.K_i]:
            joints['joint_5_b']['rad'] -= 0.01
        if keys[pygame.K_9]:
            joints['joint_6_t']['rad'] += 0.01
        if keys[pygame.K_o]:
            joints['joint_6_t']['rad'] -= 0.01

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        projection = glm.perspective(45, (display[0] / display[1]), 0.1, 50.0)

        x = camera_dis * math.sin(math.radians(camera_angle))* math.sin(math.radians(camera_alpha))  # 計算攝影機x位置
        y = camera_dis * math.cos(math.radians(camera_angle))* math.sin(math.radians(camera_alpha))  # 計算攝影機y位置
        z = camera_dis * math.cos(math.radians(camera_alpha))
        gluLookAt(x,y,z,0,0,0,0,0,1)
        view = glm.lookAt(glm.vec3(x,y,z), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 1.0))

        # # 创建模型、视图和投影矩阣
        # model = glm.mat4(1.0)  # 单位矩阵
        # projection_np = np.array(projection).T  # glm矩阵和NumPy矩阵的存储顺序不同，所以需要转置
        # view_np = np.array(view).T
        
       
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # 繪製地板
        # draw_floor_with_color(floor_vertices, floor_normals, floor_colors)
        draw_urdf(links, joints,view,projection)

        glPushMatrix()
        draw_object(floor_vao,floor_lens,np.eye(4).T,view,projection)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    urdf_file = 'puma560_description/urdf/puma560_robot.urdf'
    urdf_file = 'motoman_mh12_support/urdf/mh12_robot.urdf'

    main(urdf_file)
