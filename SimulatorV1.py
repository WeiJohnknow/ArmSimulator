import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Matrix import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PathPlanning import *
from Kinematics import *
from MotomanEthernet import *
from Toolbox import TimeTool, CsvTool

class Simulator:
    def __init__(self):
        # 視窗大小
        self.display = (1000, 800)


        # 現實長度與OpenGL長度為1:0.01
        self.Unit = 1

        # 銲接工作台尺寸參數(mm)
        '''
        工作臺檯面:60*80(cm) = 600*800 (mm)
        ROBOT Base axis 距離工作臺 : 571.054 (mm)
        機器人Base離工作台高度差 : 208.097 (mm) ; 新數據(捲尺量) : 23.76(cm) = 237.6 (mm)
        黑色洞洞板高12.5 (mm)
        '''
        self.WorkTable_lenght = 800 * self.Unit
        self.WorkTable_Weight = 600 * self.Unit

        self.BaseToWorkTable_Height = 238.438 * self.Unit
        self.BaseToWorkTable_lenght = 571.054 * self.Unit
        self.BlackBoard_Height = 14.1 * self.Unit 

        
        self.Mat = Matrix4x4() 
        self.Plan = PathPlanning()
        self.Kin = Kinematics()
        self.mh = MotomanConnector()
        self.Time = TimeTool()
        self.Csv = CsvTool()
        self.dB = dataBase()

    def Pygameinit(self):
        
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        
        glEnable(GL_DEPTH_TEST)  # 启用深度测试
        glDepthFunc(GL_LESS)  # 设置深度测试函数


    def draw_axis(self, Mats, Axislength):
        '''Axislenth 單位: OpenGL Unit
        - Args:
            - Mats : homogeneous transformation matrix(4x4)
            - Axislength: line lengh, Unit is OpenGL unit.
        - Axis color:
            - Red :X axis
            - green : Y axis
            - Blue : Z axis
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

    def draw_chessboard(self, Worldcoordinate,TatamiNumber=2000, TatamiSize=100):
        '''
        TatamiNumber 地板組成(塌塌米數量)
        TatamiSize 單格塌塌米大小(n*n)
        '''
        
        is_gray = True 
        z = Worldcoordinate @ Mat.TransXYZ(0,0,-450*self.Unit)
        Height = z[2,3]
        glPushMatrix()
        glBegin(GL_QUADS)
        for i in range(-TatamiNumber, TatamiNumber, TatamiSize):
            is_gray = not is_gray
            for j in range(-TatamiNumber, TatamiNumber, TatamiSize):
                if is_gray:
                    glColor3f(0.4, 0.4, 0.4)  # 灰色
                else:
                    glColor3f(0.7, 0.7, 0.7)  # 白色
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

    def draw_Arm(self, BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector, length):
        # length = 1
        self.draw_axis(BasePoint, length)
        self.draw_axis(Joint1, length)
        self.draw_axis(Joint2, length)
        self.draw_axis(Joint3, length)
        self.draw_axis(Joint4, length)
        self.draw_axis(Joint5, length)
        self.draw_axis(Joint6, length)
        self.draw_axis(EndEffector, length)

        self.draw_Link(BasePoint, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector)

    def draw_Point(self, coordinateMat):
        '''繪製座標點
        - Args: Matrix 4x4
        '''
        # 設定點的大小，單位(Pixel)
        glPointSize(3.0) 

        glBegin(GL_POINTS)
        glColor3f(1.0, 1.0, 1.0)  
        glVertex3f(coordinateMat[0, 3], coordinateMat[1, 3], coordinateMat[2, 3])  # 在(0,0,0)处绘制点
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
        
        # 此Base是為配合世界坐標系與地板的顯示
        Base = WorldCoordinate @ Mat.TransXYZ(0, 0, -450*self.Unit)
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
        (0,3,7,4),
        (3,2,6,7),
        (1,2,6,5),
        (0,1,5,4),
        (4,5,6,7)
        )


        colors = (
            (0,0,0),
            (0,0,0),
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

        glLineWidth(5.0)  # 設置線條寬度為2個單位

        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    def BlackBoard(self, WorldCoordinate):
        
        height = self.BaseToWorkTable_Height 
        Base = WorldCoordinate @ Mat.TransXYZ(0, 0, -450*self.Unit)
        BaseHeight = Base[2,3]
        vertices = (
        (744.006*self.Unit, -362.450*self.Unit, height+BaseHeight),
        (1173.834*self.Unit, -358.294*self.Unit, height+BaseHeight),
        (1168.142*self.Unit, 292.4*self.Unit, height+BaseHeight),
        (740.125*self.Unit, 288.409*self.Unit, height+BaseHeight),
        (744.006*self.Unit, -362.450*self.Unit, -450*self.Unit-(-196.757*self.Unit)),
        (1173.834*self.Unit, -358.294*self.Unit, -450*self.Unit-(-193.579*self.Unit)),
        (1168.142*self.Unit, 292.4*self.Unit, -450*self.Unit-(-195.658*self.Unit)),
        (740.125*self.Unit, 288.409*self.Unit, -450*self.Unit-(-197.426*self.Unit)),
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
        """於畫面中繪製矩陣
        """
        mat = np.round(mat,3)

        font = pygame.font.SysFont('Time New Roman', 24)
        
        for i in range(len(mat)-1):
            text =  f"{mat[i,:]}"
            textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
            textData = pygame.image.tostring(textSurface, "RGBA", True)
            glWindowPos2d(x, y-i*scale)
            glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

        # 讓輸出矩陣不會使用科學記號顯示
        np.set_printoptions(suppress=True)

    def draw_Var(self, dis, x, y):
        """於畫面中繪製變數
        """
        font = pygame.font.SysFont('Time New Roman', 24)
        text =  f"{dis}"
        textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def drawText(self, x, y, text:str): 
        """於畫面中繪製文字
        """
        font = pygame.font.SysFont('Time New Roman', 24)
        textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def draw_Matrix4X4(self, coord, dis,x=750, y= 140):
        '''
        X, Y座標原點為螢幕左上角
        '''

        text = "Endeffector : "
        self.drawText(x, y+40, "Gun to Obj(mm) :")
        self.draw_Var(dis, x, y+20)
        self.drawText(x, y, text)
        self.drawMatrixText(x,y-20,coord,20)

    def draw_Trajectory(self, Path, iter):
        '''
        - Args:
            - Path : Matrix 4*4
            - iter : 迴圈疊代次數計數器
        '''

        if iter>len(Path):
                iter = len(Path)-1

        for Index in range(0, iter, 5):
            self.draw_Point(Path[Index])
            self.draw_axis(Path[Index],70)

    def init_dynamicCurve(self, y_axisData):
        
        # 曲線名稱
        name = ['S', 'L', 'U', 'R', 'B', 'T']

        # 繪圖設定
        fig, axs = plt.subplots(3, 2, figsize=(6, 10))  # 2行3列的子图布局
        fig.suptitle('Dynamic Curves')

        # 初始化六条曲线
        lines = [axs[i // 2, i % 2].plot([], [], label=f'{name[i]} Axis Angle')[0] for i in range(6)]

        # Set legend for the first time
        for ax in axs.flat:
            ax.legend()

        # 初始y轴范围
        y_axis_ranges = [(min(y_axisData[i]), max(y_axisData[i])) for i in range(y_axisData.shape[0])]
        
        poltData = [fig, axs, lines, y_axis_ranges]

        return poltData
    
    def updata_dynamicCurve(self, x_axisData, y_axisData, loopIter, poltdata):

        fig = poltdata[0]
        axs = poltdata[1]
        lines = poltdata[2]
        y_axis_ranges = poltdata[3]
        
        name = ["S", "L", "U", "R", "B", "T"]

        # 初始化y軸級距
        # y_axis_ranges = [(min(y_axisData[i]), max(y_axisData[i])) for i in range(6)]

        for i, ax in enumerate(axs.flat):
            line = lines[i]
            line.set_data(x_axisData[:loopIter], y_axisData[i, :loopIter])
            ax.set_xlim(0, max(x_axisData))
            ax.set_ylim(y_axis_ranges[i])
            ax.set_title(f'{name[i]} Axis Angle')

        fig.subplots_adjust(hspace=0.4, wspace=0.3)
        plt.draw()
        plt.pause(0.03)

        # return lines
    

        
    def main(self):
        self.Pygameinit()
        
        # 世界坐標系原點
        World_coordinate = np.eye(4)

        # 設定camera
        '''
        forward -> 相機Z軸，看向物體的方向。
        Right -> 相機x軸
        Top -> 相機上方，與右手坐標系Y軸反向
        ''' 
        # camera =  Mat.TransXYZ(20,0,5) @ Mat.RotaY(d2r(-135)) @ Mat.RotaZ(d2r(90))

        # Jointθ Buffer
        θ_Buffer = d2r(np.zeros((6,1)))



        # Yaskawa Ma1440 Work Org Point
        # θ_Buffer[0, 0] =  d2r(-1.6671311132785285)
        # θ_Buffer[1, 0] =  d2r(-38.81651799446324)
        # θ_Buffer[2, 0] =  d2r(-41.087751371115175)
        # θ_Buffer[3, 0] =  d2r(-0.0020620682544592226)
        # θ_Buffer[4, 0] =  d2r(-76.44358294225668)
        # θ_Buffer[5, 0] =  d2r(1.071035847811744)

        θ_Buffer[0, 0] =  d2r(-0.006)
        θ_Buffer[1, 0] =  d2r(-38.8189)
        θ_Buffer[2, 0] =  d2r(-41.0857)
        θ_Buffer[3, 0] =  d2r(-0.0030)
        θ_Buffer[4, 0] =  d2r(-76.4394)
        θ_Buffer[5, 0] =  d2r(1.0687)

        # 示教模式 Jointθ Buffer
        teachθ = [θ_Buffer[0, 0], θ_Buffer[1, 0], θ_Buffer[2, 0], θ_Buffer[3, 0], θ_Buffer[4, 0], θ_Buffer[5, 0]]

        """
        矩陣軌跡法參數設置區:
        """
        NowEnd = np.eye(4)
        GoalEnd = np.eye(4)
        """
        ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
        weldstart = [955.398, -87.132, -166.811, -165.2914, -7.1824, 17.5358]
        weldend = [955.421, -8.941, -166.768, -165.288, -7.1896, 17.5397]
        """

        # NowEnd = NowEnd @ Mat.TransXYZ(4.85,0,2.34) @ Mat.RotaXYZ(d2r(180), d2r(20.2111), d2r(21.6879)) 
        # GoalEnd = GoalEnd @ Mat.TransXYZ(9,-4,z=-2) @ Mat.RotaXYZ(d2r(-165.2922), d2r(-7.1994), d2r(17.5635))
        NowEnd = NowEnd @ Mat.TransXYZ(485.364*self.Unit,-1.213*self.Unit,234.338*self.Unit) @ Mat.RotaXYZ(d2r(179.984), d2r(20.2111), d2r(1.6879)) 
        GoalEnd = GoalEnd @ Mat.TransXYZ(955.386*self.Unit,-19.8*self.Unit,z=-75.117*self.Unit) @ Mat.RotaXYZ(d2r(-165.2853), d2r(-7.1884), d2r(17.5443))

        alltime = 12
        sampleTime = 0.04
        startTime = 0

        # 線性插值版本
        pathData, timeData = self.Plan.MatrixPathPlanning( GoalEnd, NowEnd, alltime, sampleTime)
        self.dB.saveMatrix4x4(pathData, timeData, "w", "dataBase\MatrixPathPlanning.csv")
        # self.dB.Save(pathData, timeData,"dataBase\MatrixPathPlanning.csv")
        # self.Plan.QuaternionsInterpolation(GoalEnd, NowEnd, 5)
        
        # 434差值版本
        # self.Plan.MatrixPath434( "dataBase/MatrixPath434.csv", GoalEnd, NowEnd, alltime, startTime, sampleTime)

        # Scurve版本
        # self.Plan.MatrixPath_Scurve("dataBase/MatrixPath_Scurve.csv", GoalEnd, NowEnd, sampleTime)

        # 由資料庫取得路徑資訊
        path_dict_4X4, path_df_4X4, path_np_4X4, path_np_6X1 = self.dB.LoadMatrix4x4("dataBase\MatrixPathPlanning.csv")
        # path_dict_4X4, path_df_4X4, path_np_4X4, path_np_6X1 = self.dB.LoadMatrix4x4("dataBase/MatrixPath434.csv")
        # path_dict_4X4, path_df_4X4, path_np_4X4, path_np_6X1 = self.dB.LoadMatrix4x4("dataBase/MatrixPath_Scurve.csv")

        # 建立path buffer
        θ = np.zeros((len(path_np_4X4),6,1))


        # 取出資料後放入IK，將coordinate data ➔ Joint Angle data
        for i in range(len(path_np_4X4)):
            θ[i] = self.Kin.IK_4x4(path_np_4X4[i], θ_Buffer)

        """
        存取JointAngle data
        """    
        self.dB.saveJointAngle(θ, "w", "dataBase/MatrixPathPlanning_JointAngle.csv")
        # self.dB.Save(θ, 0, "dataBase/MatrixPathPlanning_JointAngle.csv")
        # self.dB.Save(θ, 0, "dataBase/MatrixPath434_JointAngle.csv")
        # self.dB.Save(θ, 0, "dataBase/MatrixPath_Scurve_JointAngle.csv")

        """
        存取Pose Matrix data
        """
        self.dB.savePoseMatrix(path_np_6X1, "w", "dataBase/MatrixPathPlanning_PoseMatrix.csv")
        # self.dB.Save(path_np_6X1, 0, "dataBase/MatrixPathPlanning_PoseMatrix.csv")
        # self.dB.Save(path_np_6X1, 0, "dataBase/MatrixPath434_PoseMatrix.csv")
        # self.dB.Save(path_np_6X1, 0, "dataBase/MatrixPath_Scurve_PoseMatrix.csv")

        """
        載入Joint Angle data
        """
        JointAngle_df, JointAngle_np = self.dB.LoadJointAngle("dataBase/MatrixPathPlanning_JointAngle.csv")

        # 迴圈疊代次數
        Mainloopiter = 0
        
        # 視角移動參數
        # cameraDir = 20
        cameraDir = 2500
        cameraθ = 45
        cameraφ = 0

        # 動態曲線圖初始化
        # poltData = self.init_dynamicCurve(JointAngle_np)
        # t = np.linspace(0, alltime, int(alltime/sampleTime))

        while True:
            tb = self.Time.ReadNowTime()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        # cameraDir -= 1
                        cameraDir -= 20
                    elif event.button == 5:
                        # cameraDir += 1
                        cameraDir += 20
           
            keys = pygame.key.get_pressed()

            # 觀察者視角移動
            if keys[pygame.K_a]:
                cameraφ -= 0.05
            if keys[pygame.K_d]:
                cameraφ += 0.05
            
            if keys[pygame.K_w]:
                cameraθ -= 0.05
            if keys[pygame.K_s]:
                cameraθ += 0.05

            # 手臂關節移動
            if keys[pygame.K_3]:
                teachθ[0] += d2r(1)
            elif keys[pygame.K_e]:
                teachθ[0] -= d2r(1)
            elif keys[pygame.K_4]:
                teachθ[1] += d2r(1)
            elif keys[pygame.K_r]:
                teachθ[1] -= d2r(1)
            elif keys[pygame.K_5]:
                teachθ[2] += d2r(1)
            elif keys[pygame.K_t]:
                teachθ[2] -= d2r(1)
            elif keys[pygame.K_6]:
                teachθ[3] += d2r(1)
            elif keys[pygame.K_y]:
                teachθ[3] -= d2r(1)
            elif keys[pygame.K_7]:
                teachθ[4] += d2r(1)
            elif keys[pygame.K_u]:
                teachθ[4] -= d2r(1)
            elif keys[pygame.K_8]:
                teachθ[5] += d2r(1)
            elif keys[pygame.K_i]:
                teachθ[5] -= d2r(1)


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
            gluPerspective(45, aspect, 0.1, 6000.0)
            

            # 極座標系統
            cameraX = cameraDir * np.sin(cameraθ) * np.cos(cameraφ)
            cameraY = cameraDir * np.sin(cameraθ) * np.sin(cameraφ)
            cameraZ = cameraDir * np.cos(cameraθ)

            # 設定OpenGL Lookat(觀察者視角)
            gluLookAt(cameraX, cameraY, cameraZ,
                      World_coordinate[0,3], World_coordinate[1,3], World_coordinate[2,3]
                      ,0,0,1)
            
            # 對視景模型操作
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # 繪製世界坐標系
            self.draw_axis(World_coordinate, 100)
            
            # 繪製地板
            self.draw_chessboard(World_coordinate)
            
            # 繪製工作臺
            self.draw_WorkTable(World_coordinate)
            # self.BlackBoard( World_coordinate)

            """
            teach mode
            """
            Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.Mh12_FK\
                    (World_coordinate,
                     teachθ[0],
                     teachθ[1],
                     teachθ[2],
                     teachθ[3],
                     teachθ[4],
                     teachθ[5],
                    1)
            self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector, 100)
            self.draw_Matrix4X4(EndEffector, 550)

            """
            矩陣軌跡法
            """
            # # if Mainloopiter < len(θ):
            # if Mainloopiter < JointAngle_np.shape[1]:
            #     # Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.Mh12_FK\
            #         # (World_coordinate,θ[Mainloopiter,0,0],θ[Mainloopiter,1,0],θ[Mainloopiter,2,0],θ[Mainloopiter,3,0],θ[Mainloopiter,4,0],θ[Mainloopiter,5,0], 0.01)
            #     Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = self.Kin.Mh12_FK\
            #         (World_coordinate,
            #          JointAngle_np[0, Mainloopiter],
            #          JointAngle_np[1, Mainloopiter],
            #          JointAngle_np[2, Mainloopiter],
            #          JointAngle_np[3, Mainloopiter],
            #          JointAngle_np[4, Mainloopiter],
            #          JointAngle_np[5, Mainloopiter],
            #         1)
                
            # self.draw_axis(NowEnd,100)    
            # self.draw_axis(GoalEnd,100)    
            # self.draw_Matrix4X4(EndEffector, 550)
            # self.draw_Arm(World_coordinate, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis,EndEffector, 100)
            # self.draw_Trajectory(path_np_4X4, Mainloopiter)


            """
            Dynamic draw Joint Angle data Curve
            """
            # self.updata_dynamicCurve(t, JointAngle_np, Mainloopiter, poltData)
            

            Mainloopiter += 1
            pygame.display.flip()
            pygame.time.wait(10)

            """
            Loop delay time 
            """
            ta = self.Time.ReadNowTime()
            time_err = self.Time.TimeError(tb, ta)

            # print(time_err["totalus"])

        # 用於繪製動態曲線
        # plt.show()

    
if __name__ == "__main__":
    Sim = Simulator()
    Sim.main()