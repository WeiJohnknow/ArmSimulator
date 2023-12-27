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
from Kinematics import Kinematics
from Simulator import Simulator
from Matrix import Matrix4x4

# 運算子
dot = np.dot
cross = np.cross
norm = np.linalg.norm
sin = np.sin
cos = np.cos
acos = np.arccos
d2r = np.deg2rad
r2d = np.rad2deg

shader_program = None
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

d2r = np.deg2rad
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
def create_floor_grid(rows, cols, size, height=0):
    vertices = []
    normals = []
    colors = []
    
    
    for row in range(-rows,rows):
        for col in range(-cols,cols):
            vertices.append([col * size,  row * size, height])
            vertices.append([(col+1) * size, row * size, height])
            vertices.append([(col+1) * size, (row+1) * size, height])
            vertices.append([col * size,  row * size, height])
            vertices.append([(col+1) * size, (row+1) * size, height])
            vertices.append([col * size, (row+1) * size, height])
            normals.append([0, 0, 1])
            normals.append([0, 0, 1])
            normals.append([0, 0, 1])
            normals.append([0, 0, 1])
            normals.append([0, 0, 1])
            normals.append([0, 0, 1])
            
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

def draw_chessboard(Worldcoordinate,TatamiNumber=40, TatamiSize=1):
    '''
    TatamiNumber 地板組成(塌塌米數量)
    TatamiSize 單格塌塌米大小(n*n)
    '''
    Unit = 0.01
    is_gray = True 
    z = Worldcoordinate @ Matrix4x4().TransXYZ(0,0,0)
    Height = z[2,3]
    glPushMatrix()
    glBegin(GL_QUADS)
    for i in range(-TatamiNumber, TatamiNumber, TatamiSize):
        is_gray = not is_gray
        for j in range(-TatamiNumber, TatamiNumber, TatamiSize):
            if is_gray:
                glColor3f(0.4, 0.4, 0.4)  # 灰色
            else:
                glColor3f(0.5, 0.5, 0.5)  # 白色
            glVertex3f(i, j, Height)
            glVertex3f(i + TatamiSize, j, Height)
            glVertex3f(i + TatamiSize, j + TatamiSize, Height)
            glVertex3f(i, j + TatamiSize, Height)
            is_gray = not is_gray
    glEnd()
    glPopMatrix()

def draw_axes(shader_program):
    # 定義坐標軸的頂點和顏色
    scale = 1.39
    axes_vertices = np.array([
        0.0, 0.0, 0.0,
        0.78, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.78, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.78
    ], dtype=np.float32)

    axes_colors = np.array([
        1.0, 0.0, 0.0,
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0
    ], dtype=np.float32)

    # 創建 VBO 和 VAO
    vbo = glGenBuffers(2)
    vao = glGenVertexArrays(1)

    # 綁定 VAO
    glBindVertexArray(vao)

    # 綁定頂點 VBO，上傳頂點數據
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, axes_vertices.nbytes, axes_vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # 綁定顏色 VBO，上傳顏色數據
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, axes_colors.nbytes, axes_colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # 畫出坐標軸
    glDrawArrays(GL_LINES, 0, 6)

    # 解綁 VAO 和 VBO
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glDeleteBuffers(2, vbo)

def draw_vector(vector, line_width, color):
    vector = [vector[0], vector[1], vector[2]]
    glLineWidth(line_width)
    glBegin(GL_LINES)
    glColor3f(color[0], color[1], color[2])  # 设置颜色为红色
    glVertex3f(0.0, 0.0, 0.0)  # 向量起点
    glVertex3fv(vector)  # 向量终点
    glEnd()



def calculate_angle(vector1, vector2):

    cosθ = dot(vector1,vector2)/(norm(vector1)*norm(vector2))
    angle = r2d(acos(cosθ))
    

    return angle


def main():
    global shader_program

    Kin = Kinematics()
    Mat = Matrix4x4()
    Sim = Simulator()

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    shader_program = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )
    floor_vao,floor_lens,floor_vertices, floor_normals, floor_colors = create_floor_grid(20, 20, 0.2,0)



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
        
        if keys[pygame.K_a]:
            camera_angle += 1  # 旋轉攝影機角度
        if keys[pygame.K_d]:
            camera_angle -= 1  # 旋轉攝影機角度
        
        if keys[pygame.K_w]:
            camera_alpha -= 1  # 旋轉攝影機角度
        if keys[pygame.K_s]:
            camera_alpha += 1  # 旋轉攝影機角度
        
        if keys[pygame.K_1]:
            camera_dis += 0.1  # 旋轉攝影機角度
        if keys[pygame.K_2]:
            camera_dis -= 0.1  # 旋轉攝影機角度

        
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        projection = glm.perspective(45, (display[0] / display[1]), 0.1, 50.0)

        x = camera_dis * math.sin(math.radians(camera_angle))* math.sin(math.radians(camera_alpha))  # 計算攝影機x位置
        y = camera_dis * math.cos(math.radians(camera_angle))* math.sin(math.radians(camera_alpha))  # 計算攝影機y位置
        z = camera_dis * math.cos(math.radians(camera_alpha))
        gluLookAt(x,y,z,0,0,0,0,0,1)
        view = glm.lookAt(glm.vec3(x,y,z), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 0.0, 1.0))

        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        glPushMatrix()
        

        
        # color
        red = [1.0, 0.0, 0.0]
        orange = [1.0, 0.6, 0.0]
        yellow = [1.0, 1.0, 0]
        green = [0.0, 1.0, 0.0]
        blue = [0.0, 0.0, 1.0]
        Purple = [0.62, 0.125, 0.941]


        # # Vector test
        # k = [0.0, 0.0, 1.0]
        # v = [0, 0.707, 0.707]
        # v_ = np.cross(k, v)
        # draw_vector(k, 2, blue)
        # draw_vector(v, 2, green)
        # draw_vector(v_, 2, yellow)
        
        # # Vector projection
        Raxis = np.array(([0.0, 0.0, 1.0]))
        v = np.array(([0.707, 0, 0.707]))
        v_parallel = dot(Raxis, v)*Raxis
        v_vertical = v-v_parallel

        w = cross(Raxis, v)
        Vrot_vertical = cos(d2r(160))*v_vertical + sin(d2r(160))*w
        Vrot = v_parallel + Vrot_vertical

        draw_vector(v, 10, red)
        draw_vector(Raxis, 5, blue)
        draw_vector(v_parallel, 10, green)
        draw_vector(v_vertical, 10, yellow)
        draw_vector(w, 10, Purple)
        draw_vector(Vrot_vertical, 10, yellow)
        draw_vector(Vrot, 10, orange)


        # # # Rodrigues' rotation formula
        # k = np.array(([0.0, 0.0, 1.0]))
        # v = np.array(([0.0, 0.707, 0.707]))
        # v_parallel = (dot(v,k)/norm(k))*(k/norm(k))
        # v_vertical = v - v_parallel
        # θ = d2r(60)
        # vrot_ = cos(θ)*v_vertical + sin(θ)*cross(k,v_vertical)
        # vrot = cos(θ)*v + (1-cos(θ))*(dot(k,v))*k + sin(θ)*cross(k,v)
        # vrot_parallel = (dot(vrot,k)/norm(k))*(k/norm(k))
        # vrot_vertical = vrot - vrot_parallel
        # draw_vector(k, 2, blue)
        # draw_vector(v, 2, green)
        # draw_vector(v_parallel, 5, red)
        # draw_vector(v_vertical, 5, red)
        # draw_vector(vrot, 2, orange)
        # draw_vector(vrot_parallel, 5, Purple)
        # draw_vector(vrot_vertical, 5, Purple)
        # print(calculate_angle(v_vertical, vrot_vertical))

        # # 測試叉積
        # a = [3.0, 0.0, 0.0]
        # b = [0.0, 2.0, 0.0]
        # c = cross(a,b)
        # c_ = norm(a)*norm(b)*sin(d2r(90))
        # c_norm = norm(c)
        # draw_vector(a, 5, green)
        # draw_vector(b, 5, red)
        # draw_vector(c, 5, blue)
        # print("|c| = ", c_)
        # print("|w| = ",c_norm)

        # Quatrtnion
        # x = np.array(([1,0,0]))
        # y = np.array(([0,1,0]))
        # z = np.array(([0,0,1]))
        # θ = d2r(45)
        # v = np.array(([0.707, 0.707, 0.707]))
        # q = [cos(θ/2), sin(θ/2)*v]
        # θ_ = d2r(90)
        # q_ = [cos(θ_/2), sin(θ_/2)*v]
        # draw_vector(x, 2, red)
        # draw_vector(y, 2, green)
        # draw_vector(z, 2, blue)
        # draw_vector(q[1], 5, orange)
        # draw_vector(q_[1], 5, yellow)

        # # 單位向量
        # u = np.array(([1,4,5]))
        # u_norm = norm(u)
        # unit_v = u/u_norm
        # print(unit_v)
        # ans =  unit_v[1]**2 + unit_v[2]**2
        # x2 =  unit_v[0]**2
        # print("x2", x2)
        # print(ans)



        draw_object(floor_vao,floor_lens,np.eye(4).T,view,projection)
        
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
