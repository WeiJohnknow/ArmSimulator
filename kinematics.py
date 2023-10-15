import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cv2 
from Matrix import *




pi = np.pi
display = (800, 600)

def init():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # 設定攝影機視角
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# cube
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
)

def draw_cube():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_axes(Mats):
    glPushMatrix()

    glTranslatef(Mats[0,3], Mats[1,3], Mats[2,3])
    EularAngle = Mat.MatToAngle(Mats)

    glRotatef(r2d(EularAngle[5]),0,0,1)
    glRotatef(r2d(EularAngle[4]),0,1,0)
    glRotatef(r2d(EularAngle[3]),1,0,0)

    glLineWidth(2)
    # 開始指令
    glBegin(GL_LINES)

    # X轴红色
    glColor3f(1, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0.5, 0, 0)
    # Y轴绿色
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0.5, 0)
    # Z轴蓝色
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 0.5)

    # 結束指令
    glEnd()
    glPopMatrix()

def draw_chessboard():
    size = 20
    step = 1
    is_gray = True 

    glPushMatrix()

    # # 畫出棋盤格(邊線)
    # glLineWidth(1)
    # glColor3f(1, 1, 1)  # 设置线条颜色为白色
    # glBegin(GL_LINES)

    # for i in range(-size, size + 1, step):
    #     glVertex3f(i, -size, 0)
    #     glVertex3f(i, size, 0)
    #     glVertex3f(-size, i, 0)
    #     glVertex3f(size, i, 0)

    # 畫棋盤格(有著色)
    glBegin(GL_QUADS)
    for i in range(-size, size, step):
        is_gray = not is_gray
        for j in range(-size, size, step):
            if is_gray:
                glColor3f(0.4, 0.4, 0.4)  # 灰色
            else:
                glColor3f(0.5, 0.5, 0.5)  # 白色
            glVertex3f(i, j, 0)
            glVertex3f(i + step, j, 0)
            glVertex3f(i + step, j + step, 0)
            glVertex3f(i, j + step, 0)
            is_gray = not is_gray
    glEnd()
    glPopMatrix()



def draw_Link(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6):
    vertices = (
        (BasePoint[0, 3], BasePoint[1, 3], BasePoint[2, 3]),
        (Joint1[0, 3], Joint1[1, 3], Joint1[2, 3]),
        (Joint2[0, 3], Joint2[1, 3], Joint2[2, 3]),
        (Joint3[0, 3], Joint3[1, 3], Joint3[2, 3]),
        (Joint4[0, 3], Joint4[1, 3], Joint4[2, 3]),
        (Joint5[0, 3], Joint5[1, 3], Joint5[2, 3]),
        (Joint6[0, 3], Joint6[1, 3], Joint6[2, 3]),
    )

    edges = (
        (0,1),
        (1,2),
        (2,3),
        (3,4),
        (4,5)
    )
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    
def Arm_FK(World_Point,θ1,θ2,θ3,θ4,θ5,θ6):
    # Please Input Radine
    BasePoint = World_Point 

    BaseToJ1 = Mat.TransXYZ(0,0,3) @ Mat.RotaZ(θ1)
    Joint1 = BasePoint @ BaseToJ1  
    
    J1ToJ2 =  Mat.RotaX(d2r(-90)) @ Mat.RotaZ(θ2)
    Joint2 = Joint1 @ J1ToJ2

    J2ToJ3 = Mat.TransXYZ(2,0,0) @ Mat.RotaZ(θ3)
    Joint3 = Joint2 @ J2ToJ3

    J3ToJ4 = Mat.TransXYZ(0,1,0) @ Mat.RotaX(d2r(-90))  @ Mat.RotaZ(θ4)
    Joint4 = Joint3 @ J3ToJ4

    J4ToJ5 = Mat.TransXYZ(0,0,0) @ Mat.RotaX(d2r(90)) @ Mat.RotaZ(θ5)
    Joint5 = Joint4 @ J4ToJ5

    J5ToJ6 = Mat.TransXYZ(0,0,0) @ Mat.RotaX(d2r(-90))  @ Mat.RotaZ(θ6)
    Joint6 = Joint5 @ J5ToJ6

    End_Effector = Joint6
    
    return Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector

def draw_Arm(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6):

    draw_axes(Joint1)
    draw_axes(Joint2)
    draw_axes(Joint3)
    draw_axes(Joint4)
    draw_axes(Joint5)
    draw_axes(Joint6)

    draw_Link(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6)


def Jacobian(Joint1, Joint2, Joint3, Joint4, Joint5, Joint6):
    JacMat = np.eye(6)

    # 線速度
    v1 = np.cross(Joint1[:3,2],Joint6[:3,3]-Joint1[:3,3])
    v2 = np.cross(Joint2[:3,2],Joint6[:3,3]-Joint2[:3,3])
    v3 = np.cross(Joint3[:3,2],Joint6[:3,3]-Joint3[:3,3])
    v4 = np.cross(Joint4[:3,2],Joint6[:3,3]-Joint4[:3,3])
    v5 = np.cross(Joint5[:3,2],Joint6[:3,3]-Joint5[:3,3])
    v6 = np.cross(Joint6[:3,2],Joint6[:3,3]-Joint6[:3,3])

    # 角速度(轉軸多為Z軸，故取Z軸的x、y、z分量)
    w1 = Joint1[:3,2] @ Joint1[:3,:3]
    w2 = Joint1[:3,2] @ Joint2[:3,:3]
    w3 = Joint1[:3,2] @ Joint3[:3,:3]
    w4 = Joint1[:3,2] @ Joint4[:3,:3]
    w5 = Joint1[:3,2] @ Joint5[:3,:3]
    w6 = Joint1[:3,2] @ Joint6[:3,:3]
    # w1 = Joint1[:3,2]
    # w2 = Joint2[:3,2]
    # w3 = Joint3[:3,2]
    # w4 = Joint4[:3,2]
    # w5 = Joint5[:3,2]
    # w6 = Joint6[:3,2]

    # 將角速度、線速度放入Jacobian matrix中
    JacMat[:3,0] = v1
    JacMat[:3,1] = v2
    JacMat[:3,2] = v3
    JacMat[:3,3] = v4
    JacMat[:3,4] = v5
    JacMat[:3,5] = v6

    JacMat[3:6,0] = w1
    JacMat[3:6,1] = w2
    JacMat[3:6,2] = w3
    JacMat[3:6,3] = w4
    JacMat[3:6,4] = w5
    JacMat[3:6,5] = w6

    return JacMat


def IK(GoalEnd, NowEnd):

    World_Point = np.eye(4)
    # 初始疊代角度
    θ = np.array([
        [10],
        [0],
        [10],
        [0],
        [10],
        [0]
    ])

    θ = d2r(θ)

    # Base_GoalEnd = [x,y,z,rx,ry,rz] 
    # Base_NowEnd = [x,y,z,rx,ry,rz]
    # V=Jw
    # V = GoalEnd - NowEnd

    # 跌代次數
    iter = 10

    # 學習率
    alpha = 0.98
    beta = 0.01 

    while iter > 0 :
        iter -= 1

        # FK
        Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = \
            Arm_FK(World_Point,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
        
        # 現在q 回傳的是角度 須改 可參考家欣的IKHead
        q = Mat.MatToAngle(End_Effector)
        # q[3:6] = d2r(q[3:6])

        # 取現在位置
        NowEnd = np.array([q]).reshape(6,1)

        V = GoalEnd - NowEnd

        # 收斂條件
        if np.sum(np.sqrt(V ** 2))  < 0.01:
            break
          
        # 計算角速度
        JacMat = Jacobian(Joint1, Joint2, Joint3, Joint4, Joint5, Joint6)

        # detJ = np.linalg.det(JacMat)
        # if detJ == 0:
        #     print("奇異點")
        #     return None
        
        # Inv
        J_1 = np.linalg.pinv(JacMat)
        w = J_1 @ V

        # 更新角度
        θ += w * alpha
    print("iter :", iter)

    return θ

def TrajectoryPlanning_434(θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t1, t2, t3,nowTime=0):
    # Inital
    # Lift-off
    # Set_down
    # Final
    # y = C*x   =>   x = inv(c)*y

    sampleIntervals = 0.01
    samplePoint = [int(t1/sampleIntervals), int(t2/sampleIntervals), int(t3/sampleIntervals)]
    
    # X = [a13, a14, a21, a22, a23, a33, a34]
    P1 = θlift_off - θinit
    P2 = θset_down - θlift_off
    P3 = θfinal - θset_down

    X =  np.array([0, 0, 0, 0, 0, 0, 0])
    C =  np.array([[1, 1, 0, 0, 0, 0, 0],
                [3/t1, 4/t1, -1/t2, 0, 0, 0, 0],
                [6/t1**2, 12/t1**2, 0, -2/t2**2, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1/t2, 2/t2, 3/t2, -3/t3, 4/t3],
                [0, 0, 0, 2/t2**2, 6/t2**2, 6/t3**2, -12/t3**2],
                [0, 0, 0, 0, 0, 1, -1]])

    Y = np.array([P1-(Ainit*t1**2)/2-Vinit*t1,
                    -Ainit*t1-Vinit,
                    -Ainit/t1,
                    P2,
                    Vfinal-Afinal*t3,
                    Afinal,
                    P3-Vfinal*t3-(Afinal*t3**2)/2])
    
    c_1 = np.linalg.inv(C)

    
    # X = np.array([[Afinal*t1**2*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(-2*t1**2*t2*t3**2 - 6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(-t1**2*t3**2 - 6*t1*t2**3 + 3*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(2*t1**2*t2**3 - t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(-t1**3*t3**2 - 4*t1**2*t2**3 + 2*t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (6*t1**2*t2**2 - 4*t1**2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(4*t1**2*t3**2 + 16*t1*t2**3 - 4*t1*t2*t3**2 + 12*t2**4 - 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [-Afinal*t1**2*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(2*t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(t1**2*t3**2 + 6*t1*t2**3 - 3*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(-2*t1**2*t2**3 + t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(t1**3*t3**2 + 4*t1**2*t2**3 - 2*t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-6*t1**2*t2**2 + 4*t1**2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(-3*t1**2*t3**2 - 12*t1*t2**3 + 4*t1*t2*t3**2 - 6*t2**4 + 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [-Afinal*t1**2*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(2*t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(t1**2*t3**2 + 6*t1*t2**3 - 3*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(-2*t1**2*t2**3 + t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(-2*t1**2*t2*t3**2 - 6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-6*t1**2*t2**2 + 4*t1**2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(4*t1*t2*t3**2 + 12*t2**4 - 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [-Afinal*t1*t2**3*t3**2/(2*t1**2*t3**2 + 8*t1*t2**3 + 12*t2**4 - 6*t2**2*t3**2) - Ainit*(-t1**2*t2*t3**2 - 4*t1*t2**4 + 2*t1*t2**2*t3**2)/(t1*(2*t1**2*t3**2 + 8*t1*t2**3 + 12*t2**4 - 6*t2**2*t3**2)) + P2*(3*t1*t2*t3**2 + 18*t2**4 - 9*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(-6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(3*t1**2*t2*t3**2 + 12*t1*t2**4 - 6*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-18*t1*t2**3 + 12*t1*t2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(-6*t1*t2*t3**2 - 24*t2**4 + 12*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [Afinal*(t1**2*t2**2*t3**2 + 3*t1*t2**3*t3**2)/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(-2*t1*t2**3 - 12*t2**4 + 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(2*t1**2*t2**3 - t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(-t1**2*t2*t3**2 - 6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3**2/2 + P3 - Vfinal*t3)*(6*t1**2*t2**2 - 4*t1**2*t3**2 + 18*t1*t2**3 - 12*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(2*t1*t2*t3**2 + 12*t2**4 - 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [Afinal*(-2*t1*t2**3*t3**2 - 3*t2**4*t3**2)/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) + P2*(-t1*t2*t3**2 - 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) - t1*t2**2*t3**2*(-Ainit*t1 - Vinit)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + 2*t2**2*t3**2*(-Ainit*t1**2/2 + P1 - Vinit*t1**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(t1**2*t2*t3**2 + 2*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3**2/2 + P3 - Vfinal*t3)*(4*t1**2*t3**2 + 4*t1*t2**3 + 8*t1*t2*t3**2 + 6*t2**4)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [Afinal*(-2*t1*t2**3*t3**2 - 3*t2**4*t3**2)/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) + P2*(-t1*t2*t3**2 - 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + t1*t2**2*t3**2*(-Ainit*t1 - Vinit)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + 2*t2**2*t3**2*(-Ainit*t1**2/2 + P1 - Vinit*t1**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(t1**2*t2*t3**2 + 2*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3**2/2 + P3 - Vfinal*t3)*(3*t1**2*t3**2 + 8*t1*t2*t3**2 + 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)]])
    
    # a10 = θinit
    # a11 = Vinit*t1
    # a12 = (Ainit*t1**2)/2
    # a13 = X[0, 0]
    # a14 = X[1, 0]
    # a20 = θlift_off
    # a21 = X[2, 0]
    # a22 = X[3, 0]
    # a23 = X[4, 0]
    # a30 = θfinal
    # a31 = Vfinal*t3
    # a32 = (Afinal*t3**2)/2
    # a33 = X[5, 0]
    # a34 = X[6, 0]
    X = c_1 @ Y

    a10 = θinit
    a11 = Vinit*t1
    a12 = (Ainit*t1**2)/2
    a13 = X[0]
    a14 = X[1]
    a20 = θlift_off
    a21 = X[2]
    a22 = X[3]
    a23 = X[4]
    a30 = θfinal
    a31 = Vfinal*t3
    a32 = (Afinal*t3**2)/2
    a33 = X[5]
    a34 = X[6]

    PosList = []
    VelList = []
    AccList = []
    # 多項式
    # h1 = a10 + a11*t1 + a12*t1**2 + a13*t1**3 + a14*t1**4
    # h2 = a20 + a21*t2 + a22*t2**2 + a23*t2**3
    # h3 = a30 + a31*t3 + a32*t3**2 + a33*t3**3 + a34*t3**4
    TimeList=[nowTime]
    for dt in range(100):
        t = dt/100
        TimeList.append(TimeList[-1]+0.01*t1)
        P = a10 + a11*t + a12*t**2 + a13*t**3 + a14*t**4
        V = a11 + 2*a12*t + 3*a13*t**2 + 4*a14*t**3
        A = 2*a12 + 6*a13*t + 12*a14*t**2
        PosList.append(P)
        VelList.append(V)
        AccList.append(A)

    for dt in range(100):
        t = dt/100
        TimeList.append(TimeList[-1]+0.01*t2)
        P = a20 + a21*t + a22*t**2 + a23*t**3
        V = a21 + 2*a22*t + 3*a23*t**2
        A = 2*a22 + 6*a23*t
        PosList.append(P)
        VelList.append(V)
        AccList.append(A)

    for dt in range(-100,1):
        t = dt/100
        TimeList.append(TimeList[-1]+0.01*t3)
        P = a30 + a31*t + a32*t**2 + a33*t**3 + a34*t**4
        V = a31 + 2*a32*t + 3*a33*t**2 + 4*a34*t**3
        A = 2*a32 + 6*a33*t + 12*a34*t**2
        PosList.append(P)
        VelList.append(V)
        AccList.append(A)

    del TimeList[0]
    return TimeList, PosList , VelList, AccList, samplePoint

def main():
    init()
    Mat = Matrix4x4()
    # 世界坐標系原點
    World_coordinate = np.eye(4)

    # 設定camera
    '''
    forward -> 相機Z軸，看向物體的方向。
    Right -> 相機x軸
    Top -> 相機上方，與右手坐標系Y軸反向
    ''' 
    camera =  Mat.TransXYZ(10,0,10) @ Mat.RotaY(d2r(-135)) @ Mat.RotaZ(d2r(90))

    # # 計算camera姿態與方向向量
    # cammat = World_coordinate
    # campos = cammat @ Mat.TransXYZ(10,0,10)
    # camlook = np.array([0,0,0])
    # P = camera[:3,3]
    # A = camlook
    
    # forward = (A-P)
    # Zaxis = np.array([0,0,1])

    # forward = forward / np.linalg.norm(forward) # vector
    # right = np.cross(forward,Zaxis) # 
    # right = right / np.linalg.norm(right)
    # Top = np.cross(right,forward)
    # Top = Top / np.linalg.norm(Top)

    # cammat[:3,0] = right
    # cammat[:3,1] = -Top
    # cammat[:3,2] = forward

    # Input Radian
    θ1 = 0
    θ2 = 0 
    θ3 = 0
    θ4 = 0
    θ5 = 0
    θ6 = 0

    MotorPosIteration = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    camera = camera @ Mat.TransXYZ(0,-1,0) 
                    # print(camera)
                elif event.key == pygame.K_DOWN:
                    camera = camera @ Mat.TransXYZ(0,1,0)
                    # print(camera)
                elif event.key == pygame.K_LEFT:
                    camera = camera @ Mat.TransXYZ(-1,0,0)
                    # print(camera)
                elif event.key == pygame.K_RIGHT:
                    camera = camera @ Mat.TransXYZ(1,0,0)
                    # print(camera)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    camera = camera @ Mat.TransXYZ(0, 0, 0.25)
                    # print(camera)
                elif event.button == 5:
                    camera = camera @ Mat.TransXYZ(0, 0, -0.25)
                    # print(camera)
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        '''
        glMatrixMode(參數)
        參數:
        GL_PROJECTION 投影
        GL_MODELVIEW 模型视图
        GL_TEXTURE 纹理
        '''
        # 將目前的矩陣指定為投影矩陣
        glMatrixMode(GL_PROJECTION)
        # 將矩陣設為單位矩陣
        glLoadIdentity()

        aspect = display[0] / float(display[1])
        gluPerspective(45, aspect, 0.1, 50.0)
        
        # camlook = np.array([0,0,0])
        # P = camera[:3,3]
        # A = camlook
        

        # forward = (A-P)
        # # print(forward)
        # Zaxis = np.array([0,0,1])

        # forward = forward / np.linalg.norm(forward) # vector
        # right = np.cross(forward,Zaxis) 
        # right = right / np.linalg.norm(right)
        # Top = np.cross(right,forward)
        # Top = Top / np.linalg.norm(Top)

        # gluLookAt(P[0],P[1],P[2],A[0],A[1],A[2],Top[0],Top[1],Top[2])

        gluLookAt(camera[0,3], camera[1,3], camera[2,3],
                World_coordinate[0,3], World_coordinate[1,3], World_coordinate[2,3], 
                -camera[0,1], -camera[1,1], -camera[2,1])
        

        # gluLookAt(-camera[0,3], -camera[1,3], -camera[2,3],
        #           World_coordinate[0,3], World_coordinate[1,3], World_coordinate[2,3],
        #           camera[0,1], camera[1,1], camera[2,1])

        # 對視景模型操作
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # 繪製地板
        draw_chessboard()

        # 繪製世界坐標系原點
        draw_axes(World_coordinate)

        # # 434TrajectoryPlan test(Once Motor)
        # θinit = 0
        # Vinit = 0
        # Ainit = 0
        # # 馬達目標角度(弳度)
        # θfinal = pi
        # Vfinal = 0
        # Afinal = 0
        
        # rate = 0.25
        # θlift_off = θfinal*rate
        # θset_down = θfinal*(1-rate)
        # t = [0.1, 0.1, 0.1]

        # TimeList, PosList , VelList, AccList, samplePoint = TrajectoryPlanning_434(θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t[0], t[1], t[2],nowTime=0)
        # if MotorPosIteration == (len(PosList)-1):
        #     print("Motor已達目標位置")
        # else:
        #     MotorPosIteration += 1
        #     NextPos = PosList[MotorPosIteration] - PosList[MotorPosIteration-1]
        # World_coordinate = World_coordinate @ Mat.RotaZ(NextPos)
        
        # # Arm test
        # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = Arm_FK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        # draw_Arm(World_coordinate, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6)
        # print(End_Effector)

        # IK test
        # NowEnd = np.array([[3, 3, 3, 0, 0, 0]]).reshape(6,1)
        Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = Arm_FK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        NowEnd = End_Effector
        GoalEnd =np.array([[1, 1, 3, d2r(0), 0, 0]]).reshape(6,1)
        θ = IK(GoalEnd, NowEnd)
        print('θ', θ)
        if θ is not None:
            Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = Arm_FK(World_coordinate,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
            print("End: ",End_Effector)
            draw_Arm(World_coordinate, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6)


        # Eular test
        # testBase = np.eye(4) @ Mat.TransXYZ(0,2,0)
        # tBTt1 = Mat.RotaXYZ(d2r(30),d2r(60),d2r(30))
        # test = testBase @ tBTt1
        # # test1 = testBase @ tBTt1
        # qMat1test = Mat.MatToAngle(test)
        # qMat1test[3:6] = r2d(qMat1test[3:6]) 
        # qMat1 = MatToAngle(test1)

        # print(q[0])
        # print(q[1])
        # print(q[2])
        # print(qMat1[3])
        # print(qMat1[4])
        # print("test", qMat1test)

        # draw_axes(testBase)
        # draw_axes(test)
        # draw_axes(test2)

        # 線性插值test
        # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = Arm_FK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        # NowEnd = np.array([[End_Effector[0,3], End_Effector[1,3], End_Effector[2,3], d2r(0), 0, 0]]).reshape(6,1)
        # GoalEnd =np.array([[1, -1, 3, d2r(0), 0, 0]]).reshape(6,1)
        # Point = linearInterpolation(NowEnd, GoalEnd, 0.01)

        pygame.display.flip()
        pygame.time.wait(10)
        # θ1 += 1
        # if θ2 >=45 or θ2>=125:
        #     θ2 += 1
        # else:
        #     θ2 -= 1
        # θ3 += 1
        # θ4 += 1
        # θ5 += 1
        # θ6 += 1



if __name__ == "__main__":
    main()