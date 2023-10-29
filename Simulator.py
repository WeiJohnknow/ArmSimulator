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
from PathPlanning import *
from Kinematics import *



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

def draw_chessboard(size):
    
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

def MOVJ():
    '''
    PTP Motion Planning
    ➜軌跡不拘，通常為弧形軌跡
    '''
    pass

def MOVL():
    '''
    PTP Motion Planning
    軌跡為直線
    '''
    pass

def WeldingLine(StartPoint, EndPoint):
    '''
    軌跡:
    1.手臂起點➜焊接起弧點
    2.起弧點➜收弧點(等速度)
    3.收弧點➜手臂起點
    '''
    pass


def main():
    init()
    Mat = Matrix4x4()
    Plan = PathPlanning()
    K = Kinematics()

    # 世界坐標系原點
    World_coordinate = np.eye(4)

    # 設定camera
    '''
    forward -> 相機Z軸，看向物體的方向。
    Right -> 相機x軸
    Top -> 相機上方，與右手坐標系Y軸反向
    ''' 
    camera =  Mat.TransXYZ(20,0,20) @ Mat.RotaY(d2r(-135)) @ Mat.RotaZ(d2r(90))

    # Jointθ Buffer
    θ_Buffer = d2r(np.zeros((6,1)))
    
    # 示教模式 Jointθ Buffer
    teachθ = [0, 0, 0, 0, 0, 0]

    # 軌跡規劃
    rate = 0.25
    xθfinal = 6
    yθfinal = 2
    zθfinal = 4
    xTP = [6,0,0,xθfinal*rate,xθfinal*(1-rate),xθfinal,0,0,1,1,1]
    yTP = [0,0,0,yθfinal*rate,yθfinal*(1-rate),yθfinal,0,0, 0.5, 0.5, 0.5]
    zTP = [4,0,0,zθfinal*rate,zθfinal*(1-rate),zθfinal,0,0,1,1,1]
    # Time, xPos, xVel, xAcc, _ = Plan.TrajectoryPlanning_434(xTP[0],xTP[1],xTP[2],xTP[3],xTP[4],xTP[5],xTP[6],xTP[7],xTP[8],xTP[9],xTP[10])
    Time, yPos, yVel, yAcc, _ = Plan.TrajectoryPlanning_434(yTP[0],yTP[1],yTP[2],yTP[3],yTP[4],yTP[5],yTP[6],yTP[7],yTP[8],yTP[9],yTP[10])
    # Time, zPos, zVel, zAcc, _ = Plan.TrajectoryPlanning_434(zTP[0],zTP[1],zTP[2],zTP[3],zTP[4],zTP[5],zTP[6],zTP[7],zTP[8],zTP[9],zTP[10])
    
    GoalEnd = np.zeros((len(Time), 6))
    TrajectoryBuffer = np.zeros((len(Time),3))

    for i in range(len(Time)):
        GoalEnd[i,:] = [6, yPos[i], 4,d2r(-180), d2r(0), d2r(0)]
        print(GoalEnd)
    # plt.plot(Time,yPos, label='Pos')
    # plt.xlabel('Time')
    # plt.ylabel('Position')
    # plt.show()
    iter = 0

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
        
        gluLookAt(camera[0,3], camera[1,3], camera[2,3],
                World_coordinate[0,3], World_coordinate[1,3], World_coordinate[2,3], 
                -camera[0,1], -camera[1,1], -camera[2,1])
        

        # 對視景模型操作
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # 繪製地板
        draw_chessboard(40)
        
        # 繪製工作臺
        draw_WorkPlatform()
        
        if iter < len(Time):
            # GoalEnd =np.array([[6, -2, 4, d2r(-180), d2r(0), d2r(0)]]).reshape(6,1)
            GoalEnd4X4 = Mat.AngletoMat(GoalEnd[iter,:].reshape(6,1))
            # draw_axis(GoalEnd4X4, 1)
            θ_Buffer = K.IK_4x4(GoalEnd4X4, θ_Buffer)
            print('θ', θ_Buffer)
            if θ_Buffer is not None:
                Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = K.YASKAWA_MA1440_ArmFK(World_coordinate,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])
                print("End: ", EndEffector)
                for i in range(3):
                    TrajectoryBuffer[iter,i] = EndEffector[i,3]
                    print(TrajectoryBuffer[0])
                for i in range(iter):
                    draw_Point(TrajectoryBuffer[i])
            iter += 1
        # for i in range(iter):
        #     draw_Point(TrajectoryBuffer[iter])
        draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)

        pygame.display.flip()
        pygame.time.wait(10)

    



if __name__ == "__main__":
    main()