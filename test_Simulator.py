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
from SimulatorV1 import Simulator
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


def draw_axes(shader_program):
    # Define vertices and colors for the axes
    axes_vertices = np.array([
        0.0, 0.0, 0.0,  # X-axis start point (origin)
        1.0, 0.0, 0.0,  # X-axis end point
        0.0, 0.0, 0.0,  # Y-axis start point (origin)
        0.0, 1.0, 0.0,  # Y-axis end point
        0.0, 0.0, 0.0,  # Z-axis start point (origin)
        0.0, 0.0, 1.0   # Z-axis end point
    ], dtype=np.float32)

    axes_colors = np.array([
        1.0, 0.0, 0.0,  # Red for X-axis
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,  # Green for Y-axis
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,  # Blue for Z-axis
        0.0, 0.0, 1.0
    ], dtype=np.float32)

    # Create VBO and VAO
    vbo = glGenBuffers(2)
    vao = glGenVertexArrays(1)

    # Bind VAO
    glBindVertexArray(vao)

    # Bind vertex VBO, upload vertex data
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, axes_vertices.nbytes, axes_vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # Bind color VBO, upload color data
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, axes_colors.nbytes, axes_colors, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # Draw the axes
    glDrawArrays(GL_LINES, 0, 6)

    # Unbind VAO and VBO
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glDeleteBuffers(2, vbo)

# def draw_axes(shader_program):
#     # 定義坐標軸的頂點和顏色
#     scale = 1.39
#     # axes_vertices = np.array([
#     #     0.0, 0.0, 0.0,  # X-axis start point (origin)
#     #     0.78, 0.0, 0.0, # X-axis end point
#     #     0.0, 0.0, 0.0,  # Y-axis start point (origin)
#     #     0.0, 0.78, 0.0, # Y-axis end point
#     #     0.0, 0.0, 0.0,  # Z-axis start point (origin)
#     #     0.0, 0.0, 0.78  # Z-axis end point
#     # ], dtype=np.float32)

#     axes_vertices = np.array([
#         0.0, 0.0, 0.0,  # X-axis start point (origin)
#         1.0, 0.0, 0.0, # X-axis end point
#         0.0, 0.0, 0.0,  # Y-axis start point (origin)
#         0.0, 1.0, 0.0, # Y-axis end point
#         0.0, 0.0, 0.0,  # Z-axis start point (origin)
#         0.0, 0.0, 1.0  # Z-axis end point
#     ], dtype=np.float32)

#     axes_colors = np.array([
#         1.0, 0.0, 0.0,
#         1.0, 0.0, 0.0,
#         0.0, 1.0, 0.0,
#         0.0, 1.0, 0.0,
#         0.0, 0.0, 1.0,
#         0.0, 0.0, 1.0
#     ], dtype=np.float32)

#     # 創建 VBO 和 VAO
#     vbo = glGenBuffers(2)
#     vao = glGenVertexArrays(1)

#     # 綁定 VAO
#     glBindVertexArray(vao)

#     # 綁定頂點 VBO，上傳頂點數據
#     glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
#     glBufferData(GL_ARRAY_BUFFER, axes_vertices.nbytes, axes_vertices, GL_STATIC_DRAW)
#     glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
#     glEnableVertexAttribArray(0)

#     # 綁定顏色 VBO，上傳顏色數據
#     glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
#     glBufferData(GL_ARRAY_BUFFER, axes_colors.nbytes, axes_colors, GL_STATIC_DRAW)
#     glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
#     glEnableVertexAttribArray(1)

#     # 畫出坐標軸
#     glDrawArrays(GL_LINES, 0, 6)

#     # 解綁 VAO 和 VBO
#     glBindVertexArray(0)
#     glBindBuffer(GL_ARRAY_BUFFER, 0)
#     glDeleteBuffers(2, vbo)

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


def cosineTheorem(a, b, c):
    """餘弦定理 給三邊長求最長邊角度
    """
    if a+b>c and a+c>b and b+c>a:
        cosC = (a**2 + b**2 - c**2) / (2 * a * b)
        cAngle = np.degrees(np.arccos(cosC))
    else:
        print("不是三角形")

    return cAngle



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
    floor_vao,floor_lens,floor_vertices, floor_normals, floor_colors = create_floor_grid(20, 20, 1,0)



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

        # 畫地板
        draw_object(floor_vao,floor_lens,np.eye(4).T,view,projection)

        # color
        red = [1.0, 0.0, 0.0]
        orange = [1.0, 0.6, 0.0]
        yellow = [1.0, 1.0, 0]
        green = [0.0, 1.0, 0.0]
        blue = [0.0, 0.0, 1.0]
        Purple = [0.62, 0.125, 0.941]
        
        """
        RR manipulator simulator (Static force)
        """
        # # Fk
        # d2r = np.deg2rad
        # cos = np.cos
        # sin = np.sin

        # base = np.eye(4)
        # base_v = np.array([[1],
        #                      [0],
        #                      [0],
        #                      [1]])
        # baseToJ1 = Mat.RotaZ(d2r(30)) 
        # baseToJ1_v = baseToJ1 @ base_v
        # J1 = base @ baseToJ1
        # J1_v = J1 @ base_v
        # draw_vector(baseToJ1_v, 2, yellow)

        # J1ToJ2 = Mat.TransXYZ(4,1,0) @ Mat.RotaZ(d2r(75)) 

        
        
        
        # J2 = J1 @ J1ToJ2

        # J2ToJ3 = Mat.TransXYZ(4,1,0) 
        # J3 = J2 @ J2ToJ3

        
        
        # Sim.draw_axis(base, 0.8)
        # Sim.draw_axis(J1, 0.8)
        # Sim.draw_axis(J2, 0.8)
        # Sim.draw_axis(J3, 0.8)


        # static force
        # fx, fy = -2, 8
        # _3f3 = np.array([[fx],
        #                  [fy],
        #                  [0],
        #                  [1]])
        # _3n3 = np.array([[0],
        #                  [0],
        #                  [0],
        #                  [1]])
        # _2f2 = _3f3.T @ np.linalg.inv(J2ToJ3)
        # _2n2 = _3n3.T @ np.linalg.inv(J2ToJ3) + cross(J2ToJ3, _3f3.T)
        # print(_2n2)
        # _2n2_ = _3n3.T @ np.linalg.inv(J2ToJ3) + cross(J2ToJ3, _2f2)
        # print(_2n2_)

        # color
        # red = [1.0, 0.0, 0.0]
        # orange = [1.0, 0.6, 0.0]
        # yellow = [1.0, 1.0, 0]
        # green = [0.0, 1.0, 0.0]
        # blue = [0.0, 0.0, 1.0]
        # Purple = [0.62, 0.125, 0.941]

        """
        向量與向量投影
        """
        # # Vector test
        # k = [0.0, 0.0, 1.0]
        # v = [0, 0.707, 0.707]
        # v_ = np.cross(k, v)
        # draw_vector(k, 2, blue)
        # draw_vector(v, 2, green)
        # draw_vector(v_, 2, yellow)
        
        # # Vector projection
        # Raxis = np.array(([0.0, 0.0, 1.0]))
        # v = np.array(([0.707, 0, 0.707]))
        # v_parallel = dot(Raxis, v)*Raxis
        # v_vertical = v-v_parallel

        # w = cross(Raxis, v)
        # Vrot_vertical = cos(d2r(160))*v_vertical + sin(d2r(160))*w
        # Vrot = v_parallel + Vrot_vertical
        # draw_vector(v, 10, red)
        # draw_vector(Raxis, 5, blue)
        # draw_vector(v_parallel, 10, green)
        # draw_vector(v_vertical, 10, yellow)
        # draw_vector(w, 10, Purple)
        # draw_vector(Vrot_vertical, 10, yellow)
        # draw_vector(Vrot, 10, orange)

        

        """
        Rodrigues' rotation formula
        """
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

        """
        叉積測試
        """
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

        """
        Quatrtnion
        """
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

        """
        單位向量
        """
        # u = np.array(([1,4,5]))
        # u_norm = norm(u)
        # unit_v = u/u_norm
        # print(unit_v)
        # ans =  unit_v[1]**2 + unit_v[2]**2
        # x2 =  unit_v[0]**2
        # print("x2", x2)
        # print(ans)

        """
        mh12 IK 幾何向量解
        """
        worldCoordinate = np.eye(4)
        θ = d2r(np.zeros((6,1)))
        θ[0, 0] =  d2r(0)
        θ[1, 0] =  d2r(0)
        θ[2, 0] =  d2r(0)
        θ[3, 0] =  d2r(0)
        θ[4, 0] =  d2r(0)
        θ[5, 0] =  d2r(0)
        Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = Kin.Mh12_FK\
                        (worldCoordinate,
                        θ[0],
                        θ[1],
                        θ[2],
                        θ[3],
                        θ[4],
                        θ[5],
                        1)
        GoalEnd6x1 = np.array([485.271, -1.229, 234.314, 179.9856, 20.224, 1.6763])
        GoalEnd4x4 = np.eye(4)
        GoalEnd4x4 = GoalEnd4x4 @ Mat.TransXYZ(GoalEnd6x1[0], GoalEnd6x1[1], GoalEnd6x1[2]) @ Mat.RotaXYZ(d2r(GoalEnd6x1[3]), d2r(GoalEnd6x1[4]), d2r(GoalEnd6x1[5]))
        # 基座到末端的向量大小
        BtoTvector = Taxis[:3,3]-Saxis[:3,3]
        # S軸法向量與BtoTvector叉積
        roll = np.cross(BtoTvector, Saxis[:3, 2])
        # 利用餘弦定理求出roll的角度
        a = np.sqrt(614**2+155**2)
        b = np.sqrt(200**2+640**2)
        rollDeg = cosineTheorem(a,b,np.linalg.norm(BtoTvector))

        draw_vector(BtoTvector, 5, red)
        draw_vector(Base[:3, 2], 5, blue)
        draw_vector(roll, 5, green)
        
        # print(EndEffector-Base)
        
        
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
