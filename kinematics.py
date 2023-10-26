import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import cv2 
from Matrix import *
import matplotlib
import matplotlib.pyplot as plt
import datetime



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

def draw_axis(Mats, Axislength):
    '''
    Axislenth 單位: OpenGL Unit
    '''
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
    glVertex3f(Axislength, 0, 0)
    # Y轴绿色
    glColor3f(0, 1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, Axislength, 0)
    # Z轴蓝色
    glColor3f(0, 0, 1)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, Axislength)

    # 結束指令
    glEnd()
    glPopMatrix()

def draw_chessboard():
    size = 40
    step = 2
    is_gray = True 

    glPushMatrix()
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

def draw_Link(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector):

    vertices = (
        (BasePoint[0, 3], BasePoint[1, 3], BasePoint[2, 3]),
        (Joint1[0, 3], Joint1[1, 3], Joint1[2, 3]),
        (Joint2[0, 3], Joint2[1, 3], Joint2[2, 3]),
        (Joint3[0, 3], Joint3[1, 3], Joint3[2, 3]),
        (Joint4[0, 3], Joint4[1, 3], Joint4[2, 3]),
        (Joint5[0, 3], Joint5[1, 3], Joint5[2, 3]),
        (Joint6[0, 3], Joint6[1, 3], Joint6[2, 3]),
        (EndEffector[0, 3], EndEffector[1, 3], EndEffector[2, 3])
    )

    edges = (
        (0,1),
        (1,2),
        (2,3),
        (3,4),
        (4,5),
        (5,6),
        (6,7)
    )
    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(1, 1, 0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def YASKAWA_MA1440_ArmFK(Base, Saxisθ, Laxisθ, Uaxisθ, Raxisθ, Baxisθ, Taxisθ):
    '''
    輸入請注意角度單位: 度、mm
    OpenGL Unit = 0.01(10cm)
    注意各轉軸角度限制(單位:度):
    S軸 : ±170
    L軸 : -90 / +155
    U軸 : -175 / +240
    R軸 : ±150
    B軸 : -135 / +90
    T軸 : ±210
    Payload : 6 kg
    '''
    Unit = 0.01
    

    BtoS = Mat.RotaX(d2r(-180)) @ Mat.TransXYZ(0,0,-299*Unit) @ Mat.RotaZ(Saxisθ) 
    Saxis = Base @ BtoS

    StoL = Mat.RotaY(d2r(90)) @ Mat.RotaX(d2r(-90)) @ Mat.TransXYZ(151*Unit,-155*Unit,0) @ Mat.RotaZ(Laxisθ)
    Laxis = Saxis @ StoL

    LtoU = Mat.TransXYZ(614*Unit,0,0) @ Mat.RotaZ(Uaxisθ)
    Uaxis = Laxis @ LtoU

    UtoR = Mat.RotaX(d2r(90)) @ Mat.TransXYZ(200*Unit,0,z=255*Unit) @ Mat.RotaZ(Raxisθ)
    Raxis = Uaxis @ UtoR

    RtoB = Mat.TransXYZ(0,0,385*Unit) @ Mat.RotaX(d2r(90)) @   Mat.RotaZ(Baxisθ)
    Baxis = Raxis @ RtoB

    BtoT = Mat.TransXYZ(0,100*Unit,0) @ Mat.RotaX(d2r(-90))  @ Mat.RotaZ(Taxisθ)
    Taxis = Baxis @ BtoT

    # 末端法蘭面 to 銲槍末端
    # TtoWeldingGun = Mat.TransXYZ(-15.461*Unit, 0, 323.762*Unit) @ Mat.RotaX(d2r(-90))
    # EndEffector = Taxis @ TtoWeldingGun
    EndEffector = Taxis
    return Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector
    
def PUMA_Arm_FK(Base,θ1,θ2,θ3,θ4,θ5,θ6):
    '''
    輸入單位: rad
    手臂實際單位(inch)
    '''
    
    Unit = 0.1
    BasePoint = Base 

    BaseToJ1 = Mat.TransXYZ(0,0,44*Unit) @ Mat.RotaZ(θ1)
    Joint1 = BasePoint @ BaseToJ1  
    
    J1ToJ2 =  Mat.RotaX(d2r(-90)) @ Mat.RotaZ(θ2)
    Joint2 = Joint1 @ J1ToJ2

    J2ToJ3 = Mat.TransXYZ(25.6*Unit,0,0) @ Mat.RotaZ(θ3)
    Joint3 = Joint2 @ J2ToJ3

    J3ToJ4 = Mat.TransXYZ(0,23.6*Unit,0) @ Mat.RotaX(d2r(-90))  @ Mat.RotaZ(θ4)
    Joint4 = Joint3 @ J3ToJ4

    J4ToJ5 = Mat.RotaY(d2r(90)) @ Mat.RotaZ(θ5)
    Joint5 = Joint4 @ J4ToJ5

    J5ToJ6 = Mat.RotaX(d2r(-90))  @ Mat.RotaZ(θ6)
    Joint6 = Joint5 @ J5ToJ6

    End_Effector = Joint6
    
    return Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector

def draw_Arm(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector):
    length = 1
    draw_axis(BasePoint, length)
    draw_axis(Joint1, length)
    draw_axis(Joint2, length)
    draw_axis(Joint3, length)
    draw_axis(Joint4, length)
    draw_axis(Joint5, length)
    draw_axis(Joint6, length)
    draw_axis(EndEffector, length)

    draw_Link(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector)
    

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
    w1 = Joint1[:3,2] @ Joint6[:3,:3]
    w2 = Joint2[:3,2] @ Joint6[:3,:3]
    w3 = Joint3[:3,2] @ Joint6[:3,:3]
    w4 = Joint4[:3,2] @ Joint6[:3,:3]
    w5 = Joint5[:3,2] @ Joint6[:3,:3]
    w6 = Joint6[:3,2] @ Joint6[:3,:3]
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
    '''
    姿態請輸入角度
    使用此IK，請確認function內部的FK參數!!!
    '''
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

        # PumaFK
        # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = \
        #     PUMA_Arm_FK(World_Point,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
        
        # Yaskawa MA1440 FK
        Base, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = \
            YASKAWA_MA1440_ArmFK(World_Point,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
        
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
    # normθ = norm_deg(θ)
    # print(θ)
    normθ = Normdeg(θ)

    return normθ

def norm_deg(rads:np.array,mode = 1):
    # [0,2pi]
    # [-pi,pi]
    # 3* pi mode 1 4*pi

    if mode == 1:
        rads = (rads + np.pi)  - rads // (2 * np.pi) * 2 * np.pi - np.pi
        # [-pi,pi]
    else:
        rads = rads -  rads // (2 * np.pi) * 2 * np.pi
        # [0,2pi]
    
    return rads

def Normdeg(Mat):
    for i in range(6):
        while(Mat[i,0]>pi or Mat[i,0]<-pi):
            if Mat[i,0] >= pi:
                Mat[i,0] -= pi
                # print(Mat[i,0])
            elif Mat[i,0] <= -pi:
                Mat[i,0] += pi
                # print(Mat[i,0])
            else:
                pass
                # print(Mat[i,0])
    return Mat

def TrajectoryPlanning_434(θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t1, t2, t3, StartTime=0):
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

    sampleIntervals = 0.01
    samplePoint = [int(t1/sampleIntervals), int(t2/sampleIntervals), int(t3/sampleIntervals)]
    reciprocal = 1/sampleIntervals
    
    DataSize = samplePoint[0]+samplePoint[1]+samplePoint[2]
    TimeList = np.zeros((DataSize))
    PosList = np.zeros((DataSize))
    VelList = np.zeros((DataSize))
    AccList = np.zeros((DataSize))

    # 記憶前一段軌跡的時間節點
    PreviousNode = 0

    for _u in range(0,1*samplePoint[0]+1):
        u = _u/samplePoint[0]
        TimeList[_u] = StartTime + t1*u

        P = a10 + a11*u + a12*u**2 + a13*u**3 + a14*u**4
        V = a11 + 2*a12*u + 3*a13*u**2 + 4*a14*u**3
        A = 2*a12 + 6*a13*u + 12*a14*u**2

        PosList[_u] = P
        VelList[_u] = V
        AccList[_u] = A
    
    PreviousNode += samplePoint[0]

    for _u in range(0,1*samplePoint[1]):
        u = _u/samplePoint[1]
        TimeList[PreviousNode+_u] = TimeList[PreviousNode] + t2*u

        P = a20 + a21*u + a22*u**2 + a23*u**3
        V = a21 + 2*a22*u + 3*a23*u**2
        A = 2*a22 + 6*a23*u

        PosList[PreviousNode+_u] = P
        VelList[PreviousNode+_u] = V
        AccList[PreviousNode+_u] = A

    PreviousNode += samplePoint[1]

    # 第三段真實時間
    ut = 0
    counter = 0
    for _u in range(-1*samplePoint[2],1):
        u = _u/samplePoint[2]
        ut += sampleIntervals
        TimeList[PreviousNode+counter] = TimeList[PreviousNode-1] + ut


        P = a30 + a31*u + a32*u**2 + a33*u**3 + a34*u**4
        V = a31 + 2*a32*u + 3*a33*u**2 + 4*a34*u**3
        A = 2*a32 + 6*a33*u + 12*a34*u**2

        PosList[PreviousNode+counter] = P
        VelList[PreviousNode+counter] = V
        AccList[PreviousNode+counter] = A
        if counter == samplePoint[1]-1:
            counter = samplePoint[1]-1
        else:
            counter += 1
    
    # del TimeList[0]

    return TimeList, PosList , VelList, AccList, samplePoint

def GetTime():
    current_datetime = datetime.datetime.now()
    seconds_str = int(current_datetime.strftime("%S"))

    return seconds_str

def draw_Point(coordinateMat):
    # 設定點的大小，單位(Pixel)
    glPointSize(3.0) 

    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 1.0)  
    glVertex3f(coordinateMat[0], coordinateMat[1], coordinateMat[2])  # 在(0,0,0)处绘制点
    glEnd()

def draw_WorkPlatform():
    vertices = (
    (4, -2, 0),
    (4, 2, 0),
    (8, 2, 0),
    (8, -2, 0),
    (4, -2, 4),
    (4, 2, 4),
    (8, 2, 4),
    (8, -2, 4),
    )

    edges = (
        (0,1),
        (1,2),
        (2,3),
        (3,0),
        (4,5),
        (5,6),
        (6,7),
        (7,4),
        (0,4),
        (1,5),
        (2,6),
        (3,7)
    )

    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 1.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    # glBegin(GL_QUADS)
    # glColor3fv((1, 1, 1))
    # for surface in enumerate(edges):
    #     for vertex in surface:
    #         glVertex3fv(vertices[vertex])
    # glEnd()

def main():
    init()
    Mat = Matrix4x4()
    # 世界坐標系原點
    World_coordinate = np.eye(4)
    TestPoint = np.array([[1, 0, 0, 0],
                                [0 ,1 ,0, 0],
                                [0, 0 ,1 ,5],
                                [0, 0, 0, 1]])
    # 設定camera
    '''
    forward -> 相機Z軸，看向物體的方向。
    Right -> 相機x軸
    Top -> 相機上方，與右手坐標系Y軸反向
    ''' 
    camera =  Mat.TransXYZ(20,0,20) @ Mat.RotaY(d2r(-135)) @ Mat.RotaZ(d2r(90))

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

    
    # # IK + TrajectoryPlanning
    # # Arm 現在姿態與位置
    # MotorPosIteration = 0
    # # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = PUMA_Arm_FK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
    # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = YASKAWA_MA1440_ArmFK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
    # NowEnd = EndEffector

    # # 目標位置與姿態
    # GoalEnd =np.array([[10, 0, 4.5, 0, 0, 0]]).reshape(6,1)

    # # Jacbian IK
    # θ = IK(GoalEnd, NowEnd)
    # print('θ', θ)
    
    # # TP parameter
    # θinit = 0
    # Vinit = 0
    # Ainit = 0
    # Vfinal = 0
    # Afinal = 0

    # t = [1, 1, 1]
    # rate = 0.25
    # # Joint1 motor parameter
    # J1θfinal = θ[0, 0]
    # J1θlift_off = J1θfinal*rate
    # J1θset_down = J1θfinal*(1-rate)
    # # Joint2 motor parameter
    # J2θfinal = θ[1, 0]
    # J2θlift_off = J2θfinal*rate
    # J2θset_down = J2θfinal*(1-rate)
    # # Joint3 motor parameter
    # J3θfinal = θ[2, 0]
    # J3θlift_off = J3θfinal*rate
    # J3θset_down = J3θfinal*(1-rate)
    # # Joint4 motor parameter
    # J4θfinal = θ[3, 0]
    # J4θlift_off = J4θfinal*rate
    # J4θset_down = J4θfinal*(1-rate)
    # # Joint5 motor parameter
    # J5θfinal = θ[4, 0]
    # J5θlift_off = J5θfinal*rate
    # J5θset_down = J5θfinal*(1-rate)
    # # Joint6 motor parameter
    # J6θfinal = θ[5, 0]
    # J6θlift_off = J6θfinal*rate
    # J6θset_down = J6θfinal*(1-rate)

    # # 加減速規劃
    # TimeList, PosList1 , VelList1, AccList1, samplePoint1 = TrajectoryPlanning_434(θinit, Vinit, Ainit, J1θlift_off, J1θset_down, J1θfinal, Vfinal, Afinal, t[0], t[1], t[2],0)
    # TimeList, PosList2 , VelList2, AccList2, samplePoint2 = TrajectoryPlanning_434(θinit, Vinit, Ainit, J2θlift_off, J2θset_down, J2θfinal, Vfinal, Afinal, t[0], t[1], t[2],0)
    # TimeList, PosList3 , VelList3, AccList3, samplePoint3 = TrajectoryPlanning_434(θinit, Vinit, Ainit, J3θlift_off, J3θset_down, J3θfinal, Vfinal, Afinal, t[0], t[1], t[2],0)
    # TimeList, PosList4 , VelList4, AccList4, samplePoint4 = TrajectoryPlanning_434(θinit, Vinit, Ainit, J4θlift_off, J4θset_down, J4θfinal, Vfinal, Afinal, t[0], t[1], t[2],0)
    # TimeList, PosList5 , VelList5, AccList5, samplePoint5 = TrajectoryPlanning_434(θinit, Vinit, Ainit, J5θlift_off, J5θset_down, J5θfinal, Vfinal, Afinal, t[0], t[1], t[2],0)
    # TimeList, PosList6 , VelList6, AccList6, samplePoint6 = TrajectoryPlanning_434(θinit, Vinit, Ainit, J6θlift_off, J6θset_down, J6θfinal, Vfinal, Afinal, t[0], t[1], t[2],0)
    
    # J1NextPos = 0
    # J2NextPos = 0
    # J3NextPos = 0
    # J4NextPos = 0
    # J5NextPos = 0
    # J6NextPos = 0
    # # 末端點座標資料庫
    # EndEffectorList = np.zeros((10000, 3))
    teachθ = [0, 0, 0, 0, 0, 0]
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
                elif event.key == pygame.K_1:
                    teachθ[0] += d2r(1)
                elif event.key == pygame.K_KP1:
                    teachθ[0] -= d2r(1)
                elif event.key == pygame.K_2:
                    teachθ[1] += d2r(1)
                elif event.key == pygame.K_KP2:
                    teachθ[1] -= d2r(1)
                elif event.key == pygame.K_3:
                    teachθ[2] += d2r(1)
                elif event.key == pygame.K_KP3:
                    teachθ[2] -= d2r(1)
                elif event.key == pygame.K_4:
                    teachθ[3] += d2r(1)
                elif event.key == pygame.K_KP4:
                    teachθ[3] -= d2r(1)
                elif event.key == pygame.K_5:
                    teachθ[4] += d2r(1)
                elif event.key == pygame.K_KP5:
                    teachθ[4] -= d2r(1)
                elif event.key == pygame.K_6:
                    teachθ[5] += d2r(1)
                elif event.key == pygame.K_KP6:
                    teachθ[5] -= d2r(1)
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
        
        
        # # 繪製世界坐標系原點
        # draw_axis(World_coordinate, 1)
        # draw_axis(TestPoint, 1)
        
        
        # # 434TrajectoryPlanning 疊代test
        # if MotorPosIteration == (len(PosList1)-1):
        #     print("Motor已達目標位置")

        # else:
        #     MotorPosIteration += 1
        #     NextPos1 = PosList1[MotorPosIteration] - PosList1[MotorPosIteration-1]
        #     NextPos2 = PosList2[MotorPosIteration] - PosList2[MotorPosIteration-1]

            
        #     # WtoT = Mat.TransXYZ(0,0,2) @ Mat.RotaX(d2r(90)) @ Mat.RotaZ(NextPos2)
        #     # TestPoint = World_coordinate @ WtoT
        # World_coordinate = World_coordinate  @ Mat.RotaZ(NextPos1)
        # TestPoint = TestPoint  @ Mat.RotaZ(NextPos2)

        # # glPushMatrix()
        # draw_axis(World_coordinate, 1)
        # # glPopMatrix()
        # # glPushMatrix()
        # draw_axis(TestPoint, 1)
        # # glPopMatrix()
        

        # Arm FK test
        # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = PUMA_Arm_FK(World_coordinate,d2r(90),d2r(45),θ3,θ4,θ5,θ6)
        # draw_Arm(World_coordinate, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector)
        Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = YASKAWA_MA1440_ArmFK(World_coordinate,teachθ[0],teachθ[1],teachθ[2],teachθ[3],teachθ[4],teachθ[5])
        draw_Arm(Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector)
        print(EndEffector)


        # IK test
        # NowEnd = np.array([[10, -6, 10, 0, 0, 0]]).reshape(6,1)
        # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = PUMA_Arm_FK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = YASKAWA_MA1440_ArmFK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        # NowEnd = EndEffector
        # GoalEnd =np.array([[4, 2, 4, d2r(0), 0, 0]]).reshape(6,1)
        # θ = IK(GoalEnd, NowEnd)
        # print('θ', θ)
        # if θ is not None:
        #     # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = PUMA_Arm_FK(World_coordinate,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
        #     Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = YASKAWA_MA1440_ArmFK(World_coordinate,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
        #     print("End: ",EndEffector)
        #     # draw_Arm(World_coordinate, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector)
        #     draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)


        # # 軌跡 iteration
        # if MotorPosIteration == (len(PosList1)-1):
        #     print("Motor已達目標位置")
        # else:
        #     J1NextPos = PosList1[MotorPosIteration] 
        #     J2NextPos = PosList2[MotorPosIteration] 
        #     J3NextPos = PosList3[MotorPosIteration] 
        #     J4NextPos = PosList4[MotorPosIteration] 
        #     J5NextPos = PosList5[MotorPosIteration] 
        #     J6NextPos = PosList6[MotorPosIteration] 
        #     MotorPosIteration += 1

        # # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = PUMA_Arm_FK(World_coordinate,J1NextPos,J2NextPos,J3NextPos,J4NextPos,J5NextPos,J6NextPos)
        # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = YASKAWA_MA1440_ArmFK(World_coordinate,J1NextPos,J2NextPos,J3NextPos,J4NextPos,J5NextPos,J6NextPos)
        
        # # 畫軌跡
        # EndEffectorList[MotorPosIteration,0] = EndEffector[0,3]
        # EndEffectorList[MotorPosIteration,1] = EndEffector[1,3]
        # EndEffectorList[MotorPosIteration,2] = EndEffector[2,3]
        # for i in range(MotorPosIteration):
        #     draw_Point(EndEffectorList[i])
        # print("End: ", EndEffector)
        # print("434疊代次數", MotorPosIteration)
        # # draw_Arm(World_coordinate, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector)
        # draw_Arm(Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
        draw_WorkPlatform()

        # # Position curve
        # plt.subplot(6, 1, 1)
        # plt.plot(TimeList,PosList1, label='Pos', color='red')
        # plt.subplot(6, 1, 2)
        # plt.plot(TimeList,PosList2, label='Pos', color='orange')
        # plt.subplot(6, 1, 3)
        # plt.plot(TimeList,PosList3, label='Pos', color='yellow')
        # plt.subplot(6, 1, 4)
        # plt.plot(TimeList,PosList4, label='Pos', color='green')
        # plt.subplot(6, 1, 5)
        # plt.plot(TimeList,PosList5, label='Pos', color='blue')
        # plt.subplot(6, 1, 6)
        # plt.plot(TimeList,PosList6, label='Pos', color='black')
        
        # plt.tight_layout()

        # Veloicty curve
        # plt.plot(TimeList,VelList1, label='Vel', color='red')
        # plt.plot(TimeList,VelList2, label='Vel', color='orange')
        # plt.plot(TimeList,VelList3, label='Vel', color='yellow')
        # plt.plot(TimeList,VelList4, label='Vel', color='green')
        # plt.plot(TimeList,VelList5, label='Vel', color='blue')
        # plt.plot(TimeList,VelList6, label='Vel', color='black')

        # Acc curve
        # plt.plot(TimeList,AccList1, label='Acc', color='red')
        # plt.plot(TimeList,AccList2, label='Acc', color='orange')
        # plt.plot(TimeList,AccList3, label='Acc', color='yellow')
        # plt.plot(TimeList,AccList4, label='Acc', color='green')
        # plt.plot(TimeList,AccList5, label='Acc', color='blue')
        # plt.plot(TimeList,AccList6, label='Acc', color='black')

        # plt.show()

        # # Arm test
        # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = YASKAWA_MA1440_ArmFK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        # # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = PUMA_Arm_FK(World_coordinate,θ1,θ2,θ3,θ4,θ5,θ6)
        # # draw_Arm(World_coordinate, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6)
        # draw_Arm(Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
        # print(EndEffector)
        # draw_WorkPlatform()

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

        # draw_axis(testBase, 1)
        # draw_axis(test, 1)
        # draw_axis(test2, 1)


        pygame.display.flip()
        pygame.time.wait(10)

    



if __name__ == "__main__":
    main()