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
from MotomanEthernet import *

class Simulator:
    def __init__(self):
        self.display = (800, 600)
        # 紀錄軌跡點(x,y,z)所用 
        self.PosBuffer = np.zeros((100000,3))

        # 現實長度與OpenGL長度為1:0.01
        self.Unit = 0.01

        # 銲接工作台尺寸參數(mm)
        '''
        工作臺檯面:60*80(cm) = 600*800 (mm)
        ROBOT Base axis 距離工作臺 : 571.054 (mm)
        機器人Base離工作台高度差 : 208.097 (mm) ; 新數據(捲尺量) : 23.76(cm) = 237.6 (mm)
        黑色洞洞板高12.5 (mm)
        '''
        self.WorkTable_lenght = 800 * self.Unit
        self.WorkTable_Weight = 600 * self.Unit
        # self.BaseToWorkTable_Height = 237.6 * self.Unit
        # self.BaseToWorkTable_Height = 208.097 * self.Unit
        self.BaseToWorkTable_Height = 241.7 * self.Unit
        self.BaseToWorkTable_lenght = 571.054 * self.Unit
        self.BlackBoard_Height = 14.1 * self.Unit 

        self.pi = np.pi
        self.Mat = Matrix4x4() 
        self.Plan = PathPlanning()
        self.Kin = Kinematics()
        self.Con = MotomanConnector()

    def Pygameinit(self):
        # glutInit(sys.argv)
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        # # 設定攝影機視角
        # gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    def draw_cube(self):
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
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    def draw_axis(self, Mats, Axislength):
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

    def draw_chessboard(self, Worldcoordinate,TatamiNumber=40, TatamiSize=2):
        '''
        TatamiNumber 地板組成(塌塌米數量)
        TatamiSize 單格塌塌米大小(n*n)
        '''
        Unit = 0.01
        is_gray = True 
        z = Worldcoordinate @ Mat.TransXYZ(0,0,-450*Unit)
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

    def draw_Link(self, BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector):

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
            # (0,1),
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

    def draw_Arm(self, BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector):
        length = 1
        self.draw_axis(BasePoint, length)
        self.draw_axis(Joint1, length)
        self.draw_axis(Joint2, length)
        self.draw_axis(Joint3, length)
        self.draw_axis(Joint4, length)
        self.draw_axis(Joint5, length)
        self.draw_axis(Joint6, length)
        self.draw_axis(EndEffector, length)

        self.draw_Link(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector)
        
    def GetTime(self):
        current_datetime = datetime.datetime.now()
        seconds_str = int(current_datetime.strftime("%S"))

        return seconds_str

    def draw_Point(self, coordinateMat):
        '''
        Please Ipnut 4*4 Array
        '''
        # 設定點的大小，單位(Pixel)
        glPointSize(3.0) 

        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)  
        glVertex3f(coordinateMat[0], coordinateMat[1], coordinateMat[2])  # 在(0,0,0)处绘制点
        glEnd()

    def draw_WorkTable(self, WorldCoordinate):
        '''
        工作臺檯面:60*80(cm) = 600*800 (mm)
        檯面具地面:89.45(cm) = 894.5 (mm)
        ROBOT Base axis 距離工作臺 : 571.054 (mm)
        工作臺高於ROBOT Base axis : 260 (mm)
        機器人Base離工作台高 : 208.097 (mm) ; 新數據(捲尺量) : 23.76(cm) = 237.6 (mm)
        黑色洞洞板高12.5 (mm)

        self.WorkTable_lenght = 800 * self.Unit
        self.WorkTable_Weight = 600 * self.Unit
        self.BaseToWorkTable_Height = 237.6 * self.Unit
        self.BaseToWorkTable_lenght = 571.054 * self.Unit
        self.BlackBoard_Height = 12.5 * self.Unit 
        '''
        Unit = 0.01
        # 此Base是為配合世界坐標系與地板的顯示
        Base = WorldCoordinate @ Mat.TransXYZ(0, 0, -450*Unit)
        BaseHeight = Base[2,3]

        StartX = self.BaseToWorkTable_lenght 
        StartY = 0
        self.WorkTable_lenght = 800 * self.Unit
        self.WorkTable_Weight = 600 * self.Unit
        # height = self.BaseToWorkTable_Height + self.BlackBoard_Height
        height = self.BaseToWorkTable_Height 
        vertices = (
        (StartX, StartY-self.WorkTable_lenght/2, BaseHeight),
        (StartX, StartY+self.WorkTable_lenght/2, BaseHeight),
        (StartX+self.WorkTable_Weight, StartY+self.WorkTable_lenght/2, BaseHeight),
        (StartX+self.WorkTable_Weight, StartY-self.WorkTable_lenght/2, BaseHeight),
        (StartX, StartY-self.WorkTable_lenght/2, height+BaseHeight),
        (StartX, StartY+self.WorkTable_lenght/2, height+BaseHeight),
        (StartX+self.WorkTable_Weight, StartY+self.WorkTable_lenght/2, height+BaseHeight),
        (StartX+self.WorkTable_Weight, StartY-self.WorkTable_lenght/2, height+BaseHeight),
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

        surfaces = (
        (0,1,2,3),
        (0,3,4,7),
        (3,2,6,7),
        (1,2,6,5),
        (0,1,4,5),
        (4,5,6,7)
        )


        colors = (
            (0,0,0),
            (0,1,0),
            (0,0,1),
            (0,1,0),
            (1,1,1),
            (0,1,1),
            (1,0,0),
            (0,1,0),
            (0,0,1),
            (1,0,0),
            (1,1,1),
            (0,1,1),
            )

        glBegin(GL_QUADS)
        for surface in surfaces:
            x = 0

            glColor3fv(colors[x])
            for vertex in surface:
                # x+=1
                glVertex3fv(vertices[vertex])
                
        glEnd()

        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    def MOVJ(self, GoalEnd4X4, θ_Buffer, WorldPoint, OrgJointAngle):
        '''
        PTP Motion Planning
        ➜軌跡不拘，通常為弧形軌跡
        '''
        # 先用IK算出關節角度，再利用軌跡規劃。
        # IK
        θ = self.Kin.IK_4x4( GoalEnd4X4, θ_Buffer)
        if θ is not None:
            rate = 0.25
            t1, t2, t3 = 0.5, 0.5, 0.5
            # Joint Parameter = [θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t1, t2, t3]
            Pmr_J1 = [OrgJointAngle[0,0], 0, 0, θ[0,0]*rate, θ[0,0]*(1-rate), θ[0,0], 0, 0, t1, t2, t3]
            Pmr_J2 = [OrgJointAngle[1,0], 0, 0, θ[1,0]*rate, θ[1,0]*(1-rate), θ[1,0], 0, 0, t1, t2, t3]
            Pmr_J3 = [OrgJointAngle[2,0], 0, 0, θ[2,0]*rate, θ[2,0]*(1-rate), θ[2,0], 0, 0, t1, t2, t3]
            Pmr_J4 = [OrgJointAngle[3,0], 0, 0, θ[3,0]*rate, θ[3,0]*(1-rate), θ[3,0], 0, 0, t1, t2, t3]
            Pmr_J5 = [OrgJointAngle[4,0], 0, 0, θ[4,0]*rate, θ[4,0]*(1-rate), θ[4,0], 0, 0, t1, t2, t3]
            Pmr_J6 = [OrgJointAngle[5,0], 0, 0, θ[5,0]*rate, θ[5,0]*(1-rate), θ[5,0], 0, 0, t1, t2, t3]
            TimeList, PosList1, VelList1, AccList1, samplePoint1 = self.Plan.TrajectoryPlanning_434(Pmr_J1[0],Pmr_J1[1], Pmr_J1[2], Pmr_J1[3], Pmr_J1[4], Pmr_J1[5], Pmr_J1[6], Pmr_J1[7], Pmr_J1[8], Pmr_J1[9],Pmr_J1[10])
            TimeList, PosList2, VelList2, AccList2, samplePoint2 = self.Plan.TrajectoryPlanning_434(Pmr_J2[0],Pmr_J2[1], Pmr_J2[2], Pmr_J2[3], Pmr_J2[4], Pmr_J2[5], Pmr_J2[6], Pmr_J2[7], Pmr_J2[8], Pmr_J2[9],Pmr_J2[10])
            TimeList, PosList3, VelList3, AccList3, samplePoint3 = self.Plan.TrajectoryPlanning_434(Pmr_J3[0],Pmr_J3[1], Pmr_J3[2], Pmr_J3[3], Pmr_J3[4], Pmr_J3[5], Pmr_J3[6], Pmr_J3[7], Pmr_J3[8], Pmr_J3[9],Pmr_J3[10])
            TimeList, PosList4, VelList4, AccList4, samplePoint4 = self.Plan.TrajectoryPlanning_434(Pmr_J4[0],Pmr_J4[1], Pmr_J4[2], Pmr_J4[3], Pmr_J4[4], Pmr_J4[5], Pmr_J4[6], Pmr_J4[7], Pmr_J4[8], Pmr_J4[9],Pmr_J4[10])
            TimeList, PosList5, VelList5, AccList5, samplePoint5 = self.Plan.TrajectoryPlanning_434(Pmr_J5[0],Pmr_J5[1], Pmr_J5[2], Pmr_J5[3], Pmr_J5[4], Pmr_J5[5], Pmr_J5[6], Pmr_J5[7], Pmr_J5[8], Pmr_J5[9],Pmr_J5[10])
            TimeList, PosList6, VelList6, AccList6, samplePoint6 = self.Plan.TrajectoryPlanning_434(Pmr_J6[0],Pmr_J6[1], Pmr_J6[2], Pmr_J6[3], Pmr_J6[4], Pmr_J6[5], Pmr_J6[6], Pmr_J6[7], Pmr_J6[8], Pmr_J6[9],Pmr_J6[10])
            # plt.plot(TimeList, PosList1, label='Pos')
            # plt.plot(TimeList, PosList2, label='Pos')
            # plt.plot(TimeList, PosList3, label='Pos')
            # plt.plot(TimeList, PosList4, label='Pos')
            # plt.plot(TimeList, PosList5, label='Pos')
            # plt.plot(TimeList, PosList6, label='Pos')
            # plt.xlabel('Time')
            # plt.ylabel('Position')
            # plt.show()
            # 線性映射
            '''
            Joint Angle 應把比初始角扣除
            '''
            # PosList1 =  PosList1 + OrgJointAngle[0] 
            # PosList2 =  PosList2 + OrgJointAngle[1]
            # PosList3 =  PosList3 + OrgJointAngle[2]
            # PosList4 =  PosList4 + OrgJointAngle[3]
            # PosList5 =  PosList5 + OrgJointAngle[4]
            # PosList6 =  PosList6 + OrgJointAngle[5]

        return TimeList, PosList1, PosList2, PosList3, PosList4, PosList5, PosList6

    def MOVL(self, GoalEnd4X4, θ_Buffer, NowPos):
        '''
        PTP Motion Planning
        軌跡為直線
        先規劃，後IK

        return TrajectoryBuffer(N,6,1) ,N為軌跡點數目
        '''

        rate = 0.25
        t1, t2, t3 = 1, 1, 1
        # New_x, New_y, New_z = NewEnd[0,3], NewEnd[1,3], NewEnd[2,3] 
        Goalx, Goaly, Goalz = GoalEnd4X4[0,3], GoalEnd4X4[1,3], GoalEnd4X4[2,3]
        # Joint Parameter = [θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t1, t2, t3]
        Pmr_x = [NowPos[0,0], 0, 0, Goalx*rate, Goalx*(1-rate), Goalx, 0, 0, t1, t2, t3]
        Pmr_y = [NowPos[1,0], 0, 0, Goaly*rate, Goaly*(1-rate), Goaly, 0, 0, t1, t2, t3]
        Pmr_z = [NowPos[2,0], 0, 0, Goalz*rate, Goalz*(1-rate), Goalz, 0, 0, t1, t2, t3]
        # TimeList, PosListx, VelListx, AccListx, samplePointx = self.Plan.TrajectoryPlanning_434(Pmr_x[0],Pmr_x[1], Pmr_x[2], Pmr_x[3], Pmr_x[4], Pmr_x[5], Pmr_x[6], Pmr_x[7], Pmr_x[8], Pmr_x[9],Pmr_x[10])
        TimeList, PosListy, VelListy, AccListy, samplePointy = self.Plan.TrajectoryPlanning_434(Pmr_y[0],Pmr_y[1], Pmr_y[2], Pmr_y[3], Pmr_y[4], Pmr_y[5], Pmr_y[6], Pmr_y[7], Pmr_y[8], Pmr_y[9],Pmr_y[10])
        # TimeList, PosListz, VelListz, AccListz, samplePointz = self.Plan.TrajectoryPlanning_434(Pmr_z[0],Pmr_z[1], Pmr_z[2], Pmr_z[3], Pmr_z[4], Pmr_z[5], Pmr_z[6], Pmr_z[7], Pmr_z[8], Pmr_z[9],Pmr_z[10])
        plt.plot(TimeList, PosListy, label='Pos')
        plt.xlabel('Time')
        plt.ylabel('Position')
        plt.show()
        Trajectory_Buffer = np.zeros((len(TimeList),6,1))
        
        for page in range(len(TimeList)):
            # GoalEnd4X4[0,3] = PosListx[page] 
            GoalEnd4X4[1,3] = PosListy[page] 
            # GoalEnd4X4[2,3] = PosListz[page] 
            for row in range(6):
                θ = self.Kin.IK_4x4( GoalEnd4X4, θ_Buffer)
                Trajectory_Buffer[page, row, 0] = θ[row, 0]
            
        return Trajectory_Buffer
    
    def WeldingLine(self, StartPoint, EndPoint):
        '''
        軌跡:
        1.手臂起點➜焊接起弧點
        2.起弧點➜收弧點(等速度)
        3.收弧點➜手臂起點
        '''

        pass
    
    def TeachMode(self, Base, teachθ):
        '''
        大鍵盤數字1 : Joint1正轉
        小鍵盤數字1 : Joint1逆轉
        .
        .依此類推
        .
        大鍵盤數字6 : Joint6正轉
        小鍵盤數字6 : Joint6逆轉
        '''
        Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK(Base, teachθ[0],teachθ[1],teachθ[2],teachθ[3],teachθ[4],teachθ[5])
        self.draw_Arm(Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
        
        return EndEffector
    
    def drawMatrixText(self,x,y,mat:np.array,scale = 15):
        mat = np.round(mat,3)

        font = pygame.font.SysFont('Time New Roman', 24)
        
        for i in range(len(mat)-1):
            text =  f"{mat[i,:]}"
            textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
            textData = pygame.image.tostring(textSurface, "RGBA", True)
            glWindowPos2d(x, y-i*scale)
            glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
    
    def draw_Var(self, dis, x, y):
        font = pygame.font.SysFont('Time New Roman', 24)
        text =  f"{dis}"
        textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    
    def drawText(self, x, y, text:str): 

        font = pygame.font.SysFont('Time New Roman', 24)
        textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def draw_Matrix4X4(self, coord, dis,x=550, y= 140):
        '''
        X, Y座標原點為螢幕左上角
        '''

        text = "Endeffector : "
        self.drawText(x, y+40, "Gun to Obj(mm) :")
        self.draw_Var(dis, x, y+20)
        self.drawText(x, y, text)
        self.drawMatrixText(x,y-20,coord,20)

    def draw_Trajectory(self, EndEffector, iter):
        '''
        此函式需搭配PosBuffer(全域變數)使用
        EndEffector : 4*4大小
        iter : 迴圈疊代次數計數器
        '''
        self.PosBuffer[iter,0] = EndEffector[0,3]
        self.PosBuffer[iter,1] = EndEffector[1,3]
        self.PosBuffer[iter,2] = EndEffector[2,3]
        for i in range(iter):
            self.draw_Point(self.PosBuffer[i])
        
    def ReadPos(self):
        '''
        原點:
        編碼器(Pluser):0,0,0,0,0,0

        平常手臂原點:
        編碼器:-2389,-50477,-58433,0,-74923,481
        馬達角度(U軸888):[-1.6643989318307064, -38.81881655557888, -65.73689492086777, 0.0, -76.4330105565553, 1.0577077428164932]
        馬達角度(U軸690):[-1.6643989318307064, -38.81881655557888, -84.58816955561282, 0.0, -76.4330105565553, 1.0577077428164932]


        校正後(準)
        原點:
        編碼器:0,0,0,0,0,0
        馬達絕對角度:[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        馬達對地角度:[0,90,0,0,0,0]

        手臂平常原點:
        編碼器:-2389,-50477,-58433,0,-74923,481
        馬達角度:[-1.6643444336073567, -38.81651799446324, -41.08634509914217, 0.0, -76.43644154254234, 1.0578403342863427]
        
        '''
        NowJointθ = []
        mh = MotomanConnector() #Create Connector
        mh.connectMH() #Connect
        NowJointθ = mh.getJointAnglesMH()
        print(NowJointθ) #Get the Joint angles and print them
        mh.disconnectMH()
        # NowJointθ = [-x for x in NowJointθ]

        return NowJointθ
    
    def XYCorrection_FK(self, x, y, EndEffector):
        """
        Args:
            x➜預測量點到工作台"下"邊緣之實際距離(mm)
            y➜為預測量點到工作台"左"邊緣之實際距離(mm)
            EndEffector➜模擬器中手臂在該預測點的4X4Matrix

        return:
            ErrX➜ Robot末端X方向上的誤差(mm)
            ErrY➜ Robot末端Y方向上的誤差(mm)
        """
        x = x * self.Unit
        y = y * self.Unit
        ErrX = abs(EndEffector[0,3]-(self.BaseToWorkTable_lenght+(self.WorkTable_Weight-x))) * (1/self.Unit)
        ErrY = abs(abs(EndEffector[1,3])-((self.WorkTable_lenght/2-y))) * (1/self.Unit)

        return ErrX, ErrY

    def main(self):
        self.Pygameinit()
        glEnable(GL_DEPTH_TEST)  # 启用深度测试
        glDepthFunc(GL_LESS)  # 设置深度测试函数
        # 世界坐標系原點
        World_coordinate = np.eye(4)

        # 設定camera
        '''
        forward -> 相機Z軸，看向物體的方向。
        Right -> 相機x軸
        Top -> 相機上方，與右手坐標系Y軸反向
        ''' 
        camera =  Mat.TransXYZ(20,0,5) @ Mat.RotaY(d2r(-135)) @ Mat.RotaZ(d2r(90))
        # camera =  Mat.TransXYZ(0,-20,5) @ Mat.RotaY(d2r(-135)) @ Mat.RotaZ(d2r(90))
        # Jointθ Buffer
        θ_Buffer = d2r(np.zeros((6,1)))
        # 示教模式 Jointθ Buffer
        teachθ = [0, 0, 0, 0, 0, 0]
        # 鎢棒至工件表面距離 Buffer
        DisBuffer = []
        # 針對FK模型與實際模型的X、Y軸誤差 Buffer
        ErrXBuffer = []
        ErrYBuffer = []
        '''
        YASKAWA MA1440 起始位置與姿態
        [-1.6671311132785285, -38.81651799446324, -41.087751371115175, -0.0020620682544592226, -76.44358294225668, 1.071035847811744]
        '''
        OrgJointAngle = np.array([[d2r(-1.6671311132785285)],
                                  [d2r(-38.81651799446324)],
                                  [d2r(-41.087751371115175)],
                                  [d2r(-0.0020620682544592226)],
                                  [d2r(-76.44358294225668)],
                                  [d2r(1.071035847811744)]])
        θ_Buffer[0, 0] =  d2r(-1.6671311132785285)
        θ_Buffer[1, 0] =  d2r(-38.81651799446324)
        θ_Buffer[2, 0] =  d2r(-41.087751371115175)
        θ_Buffer[3, 0] =  d2r(-0.0020620682544592226)
        θ_Buffer[4, 0] =  d2r(-76.44358294225668)
        θ_Buffer[5, 0] =  d2r(1.071035847811744)




        # # 4-3-4軌跡規劃
        # rate = 0.25
        # xθfinal = self.BaseToWorkTable_lenght + self.WorkTable_Weight/2
        # yθfinal = 2
        # zθfinal = self.BaseToWorkTable_Height+self.BlackBoard_Height+4*self.Unit
        # # PosTP = [θinit, Vinit, Ainit, θlift-off, θset-down, θfinal, Vfinal, Afinal, t1, t2, t3]
        # # xTP = [0,0,0, 6, 6, xθfinal, 0, 0, 0.5, 0.5, 0.5]
        # yTP = [0,0,0, yθfinal*rate, yθfinal*(1-rate), yθfinal, 0, 0, 0.5, 0.5, 0.5]
        # # zTP = [0,0,0, 4, 4, zθfinal, 0, 0, 0.5, 0.5, 0.5]
        # # Time, xPos, xVel, xAcc, _ = self.Plan.TrajectoryPlanning_434(xTP[0],xTP[1],xTP[2],xTP[3],xTP[4],xTP[5],xTP[6],xTP[7],xTP[8],xTP[9],xTP[10])
        # Time, yPos, yVel, yAcc, _ = self.Plan.TrajectoryPlanning_434(yTP[0],yTP[1],yTP[2],yTP[3],yTP[4],yTP[5],yTP[6],yTP[7],yTP[8],yTP[9],yTP[10])
        # # Time, zPos, zVel, zAcc, _ = self.Plan.TrajectoryPlanning_434(zTP[0],zTP[1],zTP[2],zTP[3],zTP[4],zTP[5],zTP[6],zTP[7],zTP[8],zTP[9],zTP[10])
        
        # # 位置資訊反轉
        # # yPos[:] = yPos[::-1]
        # yPos = yPos-3.5
        
        # GoalEnd = np.zeros((len(Time), 6))
        # TrajectoryBuffer = np.zeros((len(Time),3))

        # # 將規劃完的資料放進軌跡暫存器裡
        # for i in range(len(Time)):
        #     GoalEnd[i,:] = [xθfinal, yPos[i], zθfinal+5*self.Unit, d2r(-180), d2r(0), d2r(0)]
        #     # print(GoalEnd)

        # plt.plot(Time, yPos, label='Pos')
        # plt.xlabel('Time')
        # plt.ylabel('Position')
        # plt.show()

        # MOVJ(4-3-4)
        GoalEnd =np.array([[6, 4, -2, d2r(-180), d2r(0), d2r(0)]]).reshape(6,1)
        GoalEnd4X4 = self.Mat.AngletoMat(GoalEnd.reshape(6,1))
        TimeList, PosList1, PosList2, PosList3, PosList4, PosList5, PosList6 = self.MOVJ(GoalEnd4X4, θ_Buffer, World_coordinate, OrgJointAngle)
        
        # MOVL(4-3-4)
        OrgJointAngle_2nd = np.array([[d2r(0.80859733)],
                                  [d2r(-0.16683994)],
                                  [d2r(-1.18046817)],
                                  [d2r(1.20091336)],
                                  [d2r(-0.42177255)],
                                  [d2r(-1.90982586)]])
        GoalEnd_2nd =np.array([[6, -4, -2, d2r(-180), d2r(0), d2r(0)]]).reshape(6,1)
        GoalEnd4X4_2nd = self.Mat.AngletoMat(GoalEnd_2nd.reshape(6,1))
        TrajectoryBuffer = self.MOVL( GoalEnd4X4_2nd, OrgJointAngle_2nd, GoalEnd)
        # 兩段軌跡資料結合
        for i in range(len(TimeList)):
            PosList1[len(TimeList)+i] = TrajectoryBuffer[i,0,0]
            PosList2[len(TimeList)+i] = TrajectoryBuffer[i,1,0]
            PosList3[len(TimeList)+i] = TrajectoryBuffer[i,2,0]
            PosList4[len(TimeList)+i] = TrajectoryBuffer[i,3,0]
            PosList5[len(TimeList)+i] = TrajectoryBuffer[i,4,0]
            PosList6[len(TimeList)+i] = TrajectoryBuffer[i,5,0]


        '''
        Smax : 最大移動距離
        Vmax : 最大允許速度
        Amax : 最大允許加速度
        Aavg : 平均加速度
        定律:
        1. 平均加速度必須小於Amax ; 平均加速度必須大於最大加速度的一半
        2. 恆加速段時間不可小於0 ; 最大速度平方的兩倍/最大加速度 要大於最大移動距離
        先決定Smax, Vmax, Amax
        '''
        # Scurve
        # GoalEnd =np.array([[6, -4, -2, d2r(-180), d2r(0), d2r(0)]]).reshape(6,1)
        # GoalEnd4X4 = self.Mat.AngletoMat(GoalEnd.reshape(6,1))
        # self.draw_axis(GoalEnd4X4, 1)
        # θ_Buffer = self.Kin.IK_4x4(GoalEnd4X4, θ_Buffer)
        # print('θ', θ_Buffer)
        # # Smax1 ,Vmax1, Amax1, Aavg1 = θ_Buffer[0,0], -0.5, -1, -0.6
        # Smax1 ,Vmax1, Amax1, Aavg1 = θ_Buffer[0,0], -2.8, -20, -15
        # Smax2 ,Vmax2, Amax2, Aavg2 = θ_Buffer[1,0], -1.3243, -20, -15
        # Smax3 ,Vmax3, Amax3, Aavg3 = θ_Buffer[2,0], -3.4456, -20, -15
        # Smax4 ,Vmax4, Amax4, Aavg4 = θ_Buffer[3,0], -3.4775, -20, -15
        # Smax5 ,Vmax5, Amax5, Aavg5 = θ_Buffer[4,0], -2.02, -20, -15
        # Smax6 ,Vmax6, Amax6, Aavg6 = θ_Buffer[5,0], 4.3469, 20, 15
        # AccList1, VelList1, SList1, TimeList1 = self.Plan.S_curve(Smax1, Vmax1, Amax1, Amax1*0.75)
        # AccList2, VelList2, SList2, TimeList2 = self.Plan.S_curve(Smax2, Vmax2, Amax2, Amax2*0.75)
        # AccList3, VelList3, SList3, TimeList3 = self.Plan.S_curve(Smax3, Vmax3, Amax3, Amax3*0.75)
        # AccList4, VelList4, SList4, TimeList4 = self.Plan.S_curve(Smax4, Vmax4, Amax4, Amax4*0.75)
        # AccList5, VelList5, SList5, TimeList5 = self.Plan.S_curve(Smax5, Vmax5, Amax5, Amax5*0.75)
        # AccList6, VelList6, SList6, TimeList6 = self.Plan.S_curve(Smax6, Vmax6, Amax6, Amax6*0.75)
        # plt.plot(TimeList1, SList1, label='Pos')
        # plt.plot(TimeList2, SList2, label='Pos')
        # plt.plot(TimeList3, SList3, label='Pos')
        # plt.plot(TimeList4, SList4, label='Pos')
        # plt.plot(TimeList5, SList5, label='Pos')
        # plt.plot(TimeList6, SList6, label='Pos')
        # plt.xlabel('Time')
        # plt.ylabel('Position')
        # plt.show()

        # 迴圈疊代次數
        Mainloopiter = 0
        # iter1 = 0
        # iter2 = 0
        # iter3 = 0
        # iter4 = 0
        # iter5 = 0
        # iter6 = 0
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

            aspect = self.display[0] / float(self.display[1])
            gluPerspective(45, aspect, 0.1, 50.0)
            
            gluLookAt(camera[0,3], camera[1,3], camera[2,3],
                    World_coordinate[0,3], World_coordinate[1,3], World_coordinate[2,3], 
                    -camera[0,1], -camera[1,1], -camera[2,1])
            

            # 對視景模型操作
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            # 繪製世界坐標系
            self.draw_axis(World_coordinate, 1)
            
            # 繪製地板
            self.draw_chessboard(World_coordinate)
            
            # 繪製工作臺
            self.draw_WorkTable(World_coordinate)
            
            # 讀取機台個軸馬達角度
            # NowJointθ = self.ReadPos()
            # NowJointθ = d2r(NowJointθ)

            #%% 現場實驗專區
            # test Jointθ Buffer
            # 原點joint1, Joint2, Joint5 反向
            # 起弧點 J1, J5反向
            θ_test = d2r(np.array([[-25.75797687055873],
                                [14.289449400184557],
                                [-42.64871326114471],
                                [75.30570161872357],
                                [24.274637829014484],
                                [-94.99670112161866]]))
            
            # 手臂原點
            '''
            編碼器:-2393,-50477,-58435,-2,-74930,487
            馬達角度:[-1.6671311132785285, -38.81651799446324, -41.087751371115175, -0.0020620682544592226, -76.44358294225668, 1.071035847811744]
           
            '''
            # 起弧點
            '''
            註:焊接方向由右至左(與手臂方向同側看向工作台)

            此起弧點距離工作台邊緣(長) : 114 (mm) 
            此起弧點距離工作台邊緣(寬) : 219.5 (mm) 
            工作台上黑色洞洞板為 :12.5 (mm)
            此時工件疊加兩片厚度約為: 4 (mm)
            鎢棒伸出量約 : 5 (mm)
            鎢棒距離被銲物距離約 : 1 (mm)

            示教器資訊:
                編碼器:-36973,18582,-60655,-73039,-23794,43195
                絕對角度:[-25.75797687055873, -14.289449400184557, -42.64871326114471, 75.30570161872357, -24.274637829014484, -94.99670112161866]
            通訊取得:
                編碼器:-36973,18582,-60655,-73039,-23794,43195
                馬達角度:[-25.75797687055873, 14.289449400184557, -42.64871326114471, -75.30570161872357, -24.274637829014484, 94.99670112161866]
            FK角度:

            鎢棒與工件表面距離 = EndEffector_Pz(mm) - 機器人Base與工作台的距離237.6(mm) - 黑色固定板(洞洞板)12.5(mm) - 兩片工件約(4mm)
            => 2.615* (1/Unit) - 237.6 - 12.5 - 4 = 4.1 mm 
            '''
            # 角度測試專用
            # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,θ_test[0],θ_test[1],θ_test[2],θ_test[3],θ_test[4],θ_test[5])
            # self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector)

            # # 手臂原點 deg.0
            # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,θ_Buffer[0],θ_Buffer[1],θ_Buffer[2],θ_Buffer[3],θ_Buffer[4],θ_Buffer[5])
            # self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector)

            # # 機台數據測試(通訊專用)
            # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,NowJointθ[0],NowJointθ[1],NowJointθ[2],NowJointθ[3],NowJointθ[4],NowJointθ[5])
            # self.draw_Arm(Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector)
           
            # 繪製軌跡
            # self.draw_Trajectory(EndEffector, Mainloopiter)


            # 計算鎢棒到工件之距離
            # BasetoObj = 450 - (self.BaseToWorkTable_Height * (1/self.Unit) + self.BlackBoard_Height* (1/self.Unit) +4)
            # BasetoObj = 450 - (self.BaseToWorkTable_Height * (1/self.Unit) + self.BlackBoard_Height* (1/self.Unit) )
            # dis = BasetoObj -  abs(EndEffector[2,3] * (1/self.Unit))
            # print('鎢棒到工件的垂直距離 : ', dis, "mm")
            # DisBuffer.append(dis)

            # # 繪製Matrix4*3
            # self.draw_Matrix4X4(EndEffector, dis,450, 140)

            # 計算校正點實際與模擬的誤差
            # '''
            # x➜預測量點到工作台"下"邊緣之實際距離(mm)
            # y➜為預測量點到工作台"左"邊緣之實際距離(mm)
            # '''
            # x = 430.5 
            # y = 36
            # errX, errY = self.XYCorrection_FK(x, y, EndEffector)
            # ErrXBuffer.append(errX)
            # ErrYBuffer.append(errY)



#%%
            # IK
            # GoalEnd =np.array([[6, -4, -2, d2r(-180), d2r(0), d2r(0)]]).reshape(6,1)
            # GoalEnd4X4 = self.Mat.AngletoMat(GoalEnd.reshape(6,1))
            # self.draw_axis(GoalEnd4X4, 1)
            # θ_Buffer = self.Kin.IK_4x4(GoalEnd4X4, θ_Buffer)
            # print('θ', θ_Buffer)
            # if θ_Buffer is not None:
            #     Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])
            #     self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
                

            # # IK and TrajectoryPlan
            # if Mainloopiter < len(Time):
            #     # GoalEnd =np.array([[6, -2, 4, d2r(-180), d2r(0), d2r(0)]]).reshape(6,1)
            #     GoalEnd4X4 = self.Mat.AngletoMat(GoalEnd[Mainloopiter,:].reshape(6,1))
            #     # GoalEnd4X4 = self.Mat.AngletoMat(GoalEnd.reshape(6,1))
            #     # self.draw_axis(GoalEnd4X4, 1)
            #     θ_Buffer = self.Kin.IK_4x4(GoalEnd4X4, θ_Buffer)
            #     print('θ', θ_Buffer)
            #     if θ_Buffer is not None:
            #         Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])
            #         self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
            #         print("End: ", EndEffector)
            #         self.draw_Trajectory(EndEffector, Mainloopiter)
                
            # else:
            #     Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])
            #     self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
            #     self.draw_Trajectory(EndEffector, Mainloopiter)
            # # 繪製Matrix4*4
            # self.draw_Matrix4X4(EndEffector, 550, 140)

            # MOVJ
            if Mainloopiter < len(TimeList): 
                # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,PosList1[Mainloopiter],PosList2[Mainloopiter],PosList3[Mainloopiter],PosList4[Mainloopiter],PosList5[Mainloopiter],PosList6[Mainloopiter])
                 Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,TrajectoryBuffer[Mainloopiter,0],TrajectoryBuffer[Mainloopiter,1],TrajectoryBuffer[Mainloopiter,2],TrajectoryBuffer[Mainloopiter,3],TrajectoryBuffer[Mainloopiter,4],TrajectoryBuffer[Mainloopiter,5])
            # elif (Mainloopiter >= len(TimeList)):
                
                # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,TrajectoryBuffer[Mainloopiter,0],PosList2[Mainloopiter,1],PosList3[Mainloopiter,2],PosList4[Mainloopiter,3],PosList5[Mainloopiter,4],PosList6[Mainloopiter,5])
            self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)
            self.draw_Trajectory(EndEffector, Mainloopiter)
            self.draw_Matrix4X4(EndEffector, 550)

            
            
            
            # S-curve
            # if iter1 < len(TimeList1) or iter2 < len(TimeList2) or iter3 < len(TimeList3) or iter4 < len(TimeList4) or iter5 < len(TimeList5) or iter6 < len(TimeList6):
            #     if iter1 >= len(TimeList1)-1:
            #         iter1 = len(TimeList1)-1
            #     else:
            #         iter1 += 1
            #     if iter2 >= len(TimeList2)-1:
            #         iter2 = len(TimeList2)-1
            #     else:
            #         iter2 += 1
            #     if iter3 >= len(TimeList3)-1:
            #         iter3 = len(TimeList3)-1
            #     else:
            #         iter3 += 1
            #     if iter4 >= len(TimeList4)-1:
            #         iter4 = len(TimeList4)-1
            #     else:
            #         iter4 += 1
            #     if iter5 >= len(TimeList5)-1:
            #         iter5 = len(TimeList5)-1
            #     else:
            #         iter5 += 1
            #     if iter6 >= len(TimeList6)-1:
            #         iter6 = len(TimeList6)-1
            #     else:
            #         iter6 += 1

            #     Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.YASKAWA_MA1440_ArmFK_Encoder(World_coordinate,SList1[iter1],SList2[iter2],SList3[iter3],SList4[iter4],SList5[iter5],SList6[iter6])
            #     self.draw_Trajectory(EndEffector, Mainloopiter)
            #     self.draw_Matrix4X4(EndEffector, 550)
            #     self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector)


            Mainloopiter += 1
            pygame.display.flip()
            pygame.time.wait(10)

    
if __name__ == "__main__":
    Sim = Simulator()
    Sim.main()