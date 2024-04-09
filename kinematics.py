import numpy as np
from Matrix import *
import sys
from Toolbox import TimeTool
from dataBase_v0 import dataBase


class Kinematics:
    def __init__(self):
        self.Time = TimeTool() 
        self.dB = dataBase()

    def Normdeg(self,Mat):
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
    
    # 原始FK Parameter
    def YASKAWA_MA1440_ArmFK(self, Base, Saxisθ, Laxisθ, Uaxisθ, Raxisθ, Baxisθ, Taxisθ):
        '''
        輸入請注意角度單位: 度、mm
        OpenGL Unit = 0.01(10cm)
        注意各轉軸角度限制(單位:度):
        S軸 : ±170
        L軸 : -90 / +155
        U軸 : -175 / +240(待確認)
        R軸 : ±150
        B軸 : -135 / +90
        T軸 : ±210
        Payload : 6 kg
        ROBOT Base axis 距離工作臺 : 571.054(mm)
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

        RtoB = Mat.TransXYZ(0,0,385*Unit) @ Mat.RotaX(d2r(90)) @ Mat.RotaZ(Baxisθ)
        Baxis = Raxis @ RtoB

        BtoT = Mat.TransXYZ(0,100*Unit,0) @ Mat.RotaX(d2r(-90))  @ Mat.RotaZ(Taxisθ)
        Taxis = Baxis @ BtoT

        # 末端法蘭面 to 銲槍末端 (工具座標號:5)
        # TtoWeldingGun = Mat.TransXYZ(-15.461*Unit, 0.897*Unit, 323.762*Unit) @ Mat.RotaXYZ(d2r(0.3753), d2r(-31.4994), d2r(-0.7909))
        # EndEffector = Taxis @ TtoWeldingGun

        EndEffector = Taxis
        return Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector
    
    # 依編碼器方向設定的FK Parameter
    def YASKAWA_MA1440_ArmFK_Encoder(self, WorldCoord, Saxisθ, Laxisθ, Uaxisθ, Raxisθ, Baxisθ, Taxisθ):
        '''
        輸入請注意角度單位: 度、mm
        OpenGL Unit = 0.01(10cm)
        注意各轉軸角度限制(單位:度):
        S軸 : ±170
        L軸 : -90 / +155
        U軸 : -175 / +240(待確認)
        R軸 : ±150
        B軸 : -135 / +90
        T軸 : ±210
        Payload : 6 kg
        ROBOT Base axis 距離工作臺 : 571.054(mm)
        '''
        
        Unit = 0.01

        # 世界坐標系轉換成機器人基礎坐標系
        WtoB = Mat.TransXYZ(0, 0, -450*Unit)
        Base = WorldCoord @ WtoB
        
        BtoS = Mat.TransXYZ(0,0,299*Unit)  @ Mat.RotaZ(Saxisθ)
        Saxis = Base @ BtoS

        StoL = Mat.RotaX(d2r(-90)) @ Mat.TransXYZ(151*Unit,-155*Unit,0) @ Mat.RotaZ(Laxisθ)
        Laxis = Saxis @ StoL

        LtoU = Mat.RotaX(d2r(180)) @ Mat.TransXYZ(0,614*Unit,0) @ Mat.RotaZ(Uaxisθ)
        Uaxis = Laxis @ LtoU

        UtoR = Mat.RotaY(d2r(-90)) @ Mat.TransXYZ(0,200*Unit,z=-255*Unit) @ Mat.RotaZ(Raxisθ)
        Raxis = Uaxis @ UtoR

        RtoB = Mat.RotaY(d2r(90)) @ Mat.TransXYZ(385*Unit,0,0) @ Mat.RotaZ(Baxisθ)
        Baxis = Raxis @ RtoB

        BtoT = Mat.RotaY(d2r(-90)) @ Mat.TransXYZ(0,0,-100*Unit)  @ Mat.RotaZ(Taxisθ)
        # BtoT = Mat.RotaY(d2r(90)) @ Mat.TransXYZ(0,0,100*Unit)  @ Mat.RotaZ(Taxisθ)
        Taxis = Baxis @ BtoT

        # SimuToReal = np.array([[0, -1, 0, 0],
        #                               [1, 0, 0, -3.99933190e-02],
        #                                [0, 0,  1,  4.00047547e-02],
        #                                [0, 0, 0,  1]])
        
        NewTaxis = Taxis 

        # 末端法蘭面 to 銲槍末端 (工具座標號:5)
        TtoWeldingGun = Mat.RotaZ(d2r(90)) @ Mat.RotaX(d2r(180)) @  Mat.TransXYZ(-15.460*Unit, 0.896*Unit, 323.761*Unit) @ Mat.RotaXYZ(d2r(0.3753), d2r(-31.4994), d2r(-0.7909)) 
        EndEffector = NewTaxis @ TtoWeldingGun
        # TtoWeldingGun = Mat.RotaZ(d2r(90)) @ Mat.RotaX(d2r(180)) @  Mat.TransXYZ(-15.461*Unit, 0.897*Unit, 323.762*Unit) @ Mat.RotaXYZ(d2r(0.3753), d2r(-31.4994), d2r(-0.7909)) 
        # EndEffector = NewTaxis @ TtoWeldingGun
        # 模擬與現實誤差
        # SimuToReal = np.array([[ 1.00000000e+00, -1.30913500e-16, -1.18135399e-13,  4.40041929e-02],
        #                                 [-2.02024244e-16,  1.00000000e+00, -1.80438607e-15, -8.69497133e-08],
        #                                 [-7.37827662e-14, -4.59887844e-15,  1.00000000e+00, -3.89952691e-02],
        #                                 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
        # SimuToReal = np.array([[   9.99999994e-01,-2.93870019e-06, 1.07516960e-04, 7.39025440e-03],
        #                                 [ 2.93858342e-06, 1.00000000e+00, 1.08621619e-06, 1.18572239e-03],
        #                                 [-1.07516963e-04,-1.08590023e-06, 9.99999994e-01, 6.24277543e-02],
        #                                 [ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        # SimuToReal = np.array([[   9.99999994e-01,-2.93870019e-06, 1.07516960e-04, 5.13944473e-02],
        #                                 [ 2.93858342e-06, 1.00000000e+00, 1.08621619e-06, 1.18563544e-03],
        #                                 [-1.07516963e-04,-1.08590023e-06, 9.99999994e-01, 2.34324852e-02],
        #                                 [ 0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
        # CorrEndEffector = EndEffector @ SimuToReal
        CorrEndEffector = EndEffector
        

        # TtoWeldingGun = Mat.RotaZ(d2r(90)) @ Mat.RotaX(d2r(180)) @ Mat.RotaX(d2r(0.3753)) @ Mat.RotaY(d2r(-31.4994)) @ Mat.RotaZ(d2r(-0.7909))  @  Mat.TransXYZ(-15.461*Unit, 0.897*Unit, 323.762*Unit) 
        # EndEffector = Taxis @ TtoWeldingGun

        CorrEndEffector = NewTaxis
        return Base, Saxis, Laxis, Uaxis, Raxis, Baxis, NewTaxis, CorrEndEffector
    
    def Mh12_FK(self, WorldCoordinate, Saxisθ, Laxisθ, Uaxisθ, Raxisθ, Baxisθ, Taxisθ, Unit):
        """Motoman MH12 Forward kinematics
        - Ref. Yaskawa_mh12.xacro
        - Arg: 
            - Unit: 
                - Real: 1
                - Simulator: 0.01 (default)
        """
        WorldCoordinate = np.eye(4)

        # 模擬器倍率
        # Unit = 0.01

        # 真實倍率
        # Unit = 1

        # urdf解釋器scale
        # Unit = 0.00078
        
        WtoB = Mat.TransXYZ(0, 0, -450*Unit)
        Base = WorldCoordinate @ WtoB
        
        BtoS = Mat.TransXYZ(0,0,450*Unit)  @ Mat.RotaZ(Saxisθ)
        Saxis = Base @ BtoS

        StoL = Mat.RotaX(d2r(-90)) @ Mat.TransXYZ(155*Unit,0,0) @ Mat.RotaZ(Laxisθ)
        Laxis = Saxis @ StoL

        LtoU = Mat.RotaX(d2r(180)) @ Mat.TransXYZ(0,614*Unit,0) @ Mat.RotaZ(Uaxisθ)
        Uaxis = Laxis @ LtoU

        UtoR = Mat.RotaY(d2r(-90)) @ Mat.TransXYZ(0,200*Unit,z=-640*Unit) @ Mat.RotaZ(Raxisθ)
        Raxis = Uaxis @ UtoR

        RtoB = Mat.RotaY(d2r(90))  @ Mat.RotaZ(Baxisθ)
        Baxis = Raxis @ RtoB

        BtoT = Mat.RotaY(d2r(-90))   @ Mat.RotaZ(Taxisθ)
        Taxis = Baxis @ BtoT

        TtoTool =  Mat.TransXYZ(0,0,-100*Unit)
        Tool = Taxis @ TtoTool

        
        TtoWeldingGun = Mat.RotaZ(d2r(90)) @ Mat.RotaX(d2r(180)) @  Mat.TransXYZ(-15.460*Unit, 0.896*Unit, 323.761*Unit) @ Mat.RotaXYZ(d2r(0.3753), d2r(-31.4994), d2r(-0.7909)) 
        EndEffector = Tool @ TtoWeldingGun

        
        return Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector
    
    def PUMA_Arm_FK(self, Base,θ1,θ2,θ3,θ4,θ5,θ6):
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
    
    def Jacobian(self, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6):
        JacMat = np.eye(6)

        # 線速度
        v1 = np.cross(Joint1[:3,2],Joint6[:3,3]-Joint1[:3,3])
        v2 = np.cross(Joint2[:3,2],Joint6[:3,3]-Joint2[:3,3])
        v3 = np.cross(Joint3[:3,2],Joint6[:3,3]-Joint3[:3,3])
        v4 = np.cross(Joint4[:3,2],Joint6[:3,3]-Joint4[:3,3])
        v5 = np.cross(Joint5[:3,2],Joint6[:3,3]-Joint5[:3,3])
        v6 = np.cross(Joint6[:3,2],Joint6[:3,3]-Joint6[:3,3])

        # 角速度(轉軸多為Z軸，故取Z軸的x、y、z分量)
        # w1 = Joint1[:3,2] @ Joint6[:3,:3]
        # w2 = Joint2[:3,2] @ Joint6[:3,:3]
        # w3 = Joint3[:3,2] @ Joint6[:3,:3]
        # w4 = Joint4[:3,2] @ Joint6[:3,:3]
        # w5 = Joint5[:3,2] @ Joint6[:3,:3]
        # w6 = Joint6[:3,2] @ Joint6[:3,:3]
        w1 = Joint1[:3,2]
        w2 = Joint2[:3,2]
        w3 = Joint3[:3,2]
        w4 = Joint4[:3,2]
        w5 = Joint5[:3,2]
        w6 = Joint6[:3,2]

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
    
    def IK(self, GoalEnd, θ_Buffer):

        World_Point = np.eye(4)
        θ_Buffer = θ_Buffer.reshape(6,1)

        # Base_GoalEnd = [x,y,z,rx,ry,rz] 
        # Base_NowEnd = [x,y,z,rx,ry,rz]
        # V=Jw
        # V = GoalEnd - NowEnd

        # 跌代次數
        iter = 10

        # 學習率
        alpha = 0.98
        beta = 0.01 
        test = 0.008

        while iter > 0 :
            iter -= 1

            # PumaFK
            # Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, End_Effector = \
            #     PUMA_Arm_FK(World_Point,θ[0,0],θ[1,0],θ[2,0],θ[3,0],θ[4,0],θ[5,0])
            
            # Yaskawa MA1440 FK
            Base, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = \
                self.YASKAWA_MA1440_ArmFK(World_Point,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])
            
            # 現在q 回傳的是角度 須改 可參考家欣的IKHead
            q = Mat.MatToAngle(EndEffector)
            # q = Mat.MatToAngle(End_Effector)
            # q[3:6] = d2r(q[3:6])

            # 取現在位置
            NowEnd = np.array([q]).reshape(6,1)
            
            # 末端姿態
            V = GoalEnd - NowEnd

            # 誤差
            error = np.sqrt(np.sum(V** 2))
            # print("error " , error) 

            # 收斂條件
            if error  < 0.001:
                break
            # error = np.mean((Goal_4x4 - EndEffector)**2)
            # print("error " , error)

            # if error  < 0.001:
            #     break
            
            # 計算角速度
            JacMat = self.Jacobian(Joint1, Joint2, Joint3, Joint4, Joint5, Joint6)

            # detJ = np.linalg.det(JacMat)
            # if detJ == 0:
            #     print("奇異點")
            #     return None
            
            # Inv
            J_1 = np.linalg.pinv(JacMat)
            w = J_1 @ V

            # 更新角度
            θ_Buffer += w * test
            # θ_Buffer = Normdeg(θ_Buffer)
            print(θ_Buffer)

        print("iter :", iter)
        # normθ = norm_deg(θ)
        # print(θ)
        normθ = self.Normdeg(θ_Buffer)

        print("error " , error)

        return normθ

    # def Jacbaian4X4(self, θ_Buffer):
    #     World_Point = np.eye(4)
    #     J = np.zeros((12,6))
    #     dt = d2r(0.01)

    #     Base, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = \
    #                     self.YASKAWA_MA1440_ArmFK(World_Point,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])

    #     for i in range(len(θ_Buffer)):
    #         # 變化量
    #         θ_copyMat = np.copy(θ_Buffer)
    #         θ_copyMat[i,0] += dt

    #         # 下一刻EndEffector 6*1
    #         Goal = self.YASKAWA_MA1440_ArmFK(World_Point,θ_copyMat[0,0],θ_copyMat[1,0],θ_copyMat[2,0],θ_copyMat[3,0],θ_copyMat[4,0],θ_copyMat[5,0])[-1]
            
    #         dmat = (Goal-EndEffector)/dt
            
    #         J[:,i] = dmat[:3,:].T.reshape(-1)
    #         print(J)

    #     return J

    # def IK_4x4(self, GoalEnd, θ_Buffer):
    #     World_Point = np.eye(4)

    #     # 學習率
    #     learnRate = 0.05

    #     # 疊代次數
    #     iter = 10

    #     while iter > 0:
    #         iter -= 1

    #         # 現在位置姿態矩陣
    #         Base, Joint1, Joint2, Joint3, Joint4, Joint5, Joint6, EndEffector = \
    #                 self.YASKAWA_MA1440_ArmFK(World_Point,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0])
            
    #         # V is 6*1
    #         V = GoalEnd - EndEffector

    #         # 最小二乘法判斷誤差
    #         error = np.sqrt(np.sum(V** 2 ))
    #         if error < 0.001:
    #             break

    #         # print(error)
    #         # J shape is 12*6
    #         J = self.Jacbaian4X4(θ_Buffer)

    #         # J shape is 6*12
    #         J_1 = np.linalg.pinv(J)

    #         # V shape is 12*1
    #         V = V[:3,:].T.reshape(-1)

    #         w = np.reshape(J_1 @ V,(6,1))
    #         # print(w)
    #         θ_Buffer += w * learnRate
    #     normθ = self.Normdeg(θ_Buffer)

    #     return normθ

    def Jacobian4x4(self, θ_Buffer):
        '''
        使用前請注意此時Jacobian內的FK Model
        '''
        J = np.zeros((12,6))
        dt = d2r(0.01)
        World_Point = np.eye(4)

        Unit = 1

        for i in range(len(θ_Buffer)):
            # 查看當前FK末端(Endeffector)位置向量
            Now_End = self.Mh12_FK(World_Point,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0], Unit)[-1]

            # 將θ_Buffer資料與格式複製
            θ_cpy = np.copy(θ_Buffer)
            θ_cpy[i,0] += dt

            # 取經過一次dt的角度變化量，放入FK中查看末端的變化
            dEnd = self.Mh12_FK(World_Point,θ_cpy[0,0],θ_cpy[1,0],θ_cpy[2,0],θ_cpy[3,0],θ_cpy[4,0],θ_cpy[5,0], Unit)[-1]

            # 微分概念公式，目的為求變化量
            Dmat = (dEnd - Now_End) / dt

            # 把Dmat的raw:1~3,與其col取出來，並轉置，再進行攤平，最後放入J矩陣中每一個raw的第一個col中
            J[:,i] = Dmat[:3,:].T.reshape(-1)
            # print("test")

            # # 算Jacbian matrix det(用SVD)
            # _, s, _ = np.linalg.svd(J)
            # # 計算行列式
            # determinant = np.prod(s)
            # print("det(J)", determinant)
            # if determinant == 0:
            #     print("奇異點")

            # 計算rank
            # rank = np.linalg.matrix_rank(J)
            # # print("rank(J)", rank)
            # if rank < 6:
            #     print("rank<6")

        return J

    def IK_4x4(self, Goal_4x4, θ_Buffer):
        """使用4x4齊次變換矩陣來迭代Jacobian matrix
        - Args:
            - Goal_4x4: 目標點之齊次變換矩陣
            - θ_Buffer: 此時此刻之關節角度
        """
        # b = self.Time.ReadNowTime()
        World_Point = np.eye(4)
        
        Jbuffer = 0

        iter = 15
        # 學習率
        # test = 0.05
        test = 0.85
        while iter > 0:
            iter -= 1

            unit = 1
            Now_End = self.Mh12_FK(World_Point,θ_Buffer[0,0],θ_Buffer[1,0],θ_Buffer[2,0],θ_Buffer[3,0],θ_Buffer[4,0],θ_Buffer[5,0], unit)[-1]

            V_4x4 = Goal_4x4 - Now_End
            error = np.sqrt(np.sum(V_4x4** 2))
            # print("error " , error) 

            # 收斂條件
            if error  < 0.001:
                J = self.Jacobian4x4(θ_Buffer)
                Jbuffer = J
                break

            J = self.Jacobian4x4(θ_Buffer)
            Jbuffer = J
            # Pseudo Inverse
            J_1 = np.linalg.pinv(J)

            # 利用Jacboian Inverse計算各軸角度，計算需要將V 4*4矩陣維度調整，並將計算後的答案矩陣調整為6*1的維度
            w = np.reshape(J_1 @ V_4x4[:3,:].T.reshape(-1),(6,1))

            # 更新角度
            θ_Buffer += w * test
            # θ_Buffer = Normdeg(θ_Buffer)
            # print(θ_Buffer)

        """
        奇異點判定:
        1. rank小於matrix本身之row或column
        2.非對稱矩陣使用SVD(奇異值分解)，若奇異值等於0，則為奇異點
        """  

        # 算Jacbian matrix det(用SVD)
        _, s, _ = np.linalg.svd(Jbuffer)

        # 計算行列式
        determinant = np.prod(s)

        # if determinant == 0:
        #     print("SVD =  0, 是奇異點")

        rankJ = np.linalg.matrix_rank(Jbuffer)
        
        if rankJ < 6 or determinant == 0:
            print("SVD =  0, 是奇異點")


        # print("iter :", 10-iter)
        normθ = self.Normdeg(θ_Buffer)
        # print(normθ)
        # print("error " , error)

        if error > 0.001:
            sys.exit("IK迭代誤差過大")
        if normθ[0,0] > d2r(170) or normθ[0,0] < d2r(-170):
            sys.exit("S軸超過角度限制")
        elif normθ[1,0] >= d2r(155) or normθ[1,0] < d2r(-90):
            sys.exit("L軸超過角度限制")
        elif normθ[2,0] > d2r(240) or normθ[2,0] < d2r(-84.995):
            sys.exit("U軸超過角度限制")
        elif normθ[3,0] > d2r(150) or normθ[3,0] < d2r(-150):
            sys.exit("R軸超過角度限制")
        elif normθ[4,0] > d2r(90) or normθ[4,0] < d2r(-135):
            sys.exit("B軸超過角度限制")
        elif normθ[5,0] > d2r(210) or normθ[5,0] < d2r(-210):
            sys.exit("T軸超過角度限制")

        # a = self.Time.ReadNowTime()
        # err = self.Time.TimeError(b, a)

        return normθ

    