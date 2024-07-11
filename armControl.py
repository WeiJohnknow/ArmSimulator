
from Kinematics import Kinematics
from Matrix import Matrix4x4
from PathPlanning import PathPlanning
from dataBase_v1 import *
from Toolbox import TimeTool
from SimulatorV2 import Simulator
import numpy as np
import matplotlib.pyplot as plt
from MotomanUdpPacket import MotomanUDP

class Generator:
    # 類別變數
    Kin = Kinematics()
    Mat = Matrix4x4()
    TrjPlan = PathPlanning()
    Udp = MotomanUDP()


    @classmethod
    def generateTrajectory(cls, NowPoseMat, GoalPoseMat, sampleTime, **velocityInf):
        """矩陣軌跡法 | 速度版本
        - Args:
            1. NowPoseMat
            2. GoalPoseMat
            3. sampleTime(s)
            4. GoalSpeed : (unit: mm/s)
        - Return:
            1. HomogeneousMatData(3D array)
            2. PoseMatData
            3. VelocityData
            4. TimeData
        """
        # 取出速度的類別與值
        # GoalSpeedType = GoalSpeed.keys()
        for key in velocityInf:  # 直接迭代字典取得鍵
           GoalSpeedType = key
        GoalSpeed = velocityInf[f"{GoalSpeedType}"]


        d2r = np.deg2rad
        NowEnd = np.eye(4)
        GoalEnd = np.eye(4)
        
        NowEnd = NowEnd @ cls.Mat.TransXYZ(NowPoseMat[0], NowPoseMat[1], NowPoseMat[2]) @ cls.Mat.RotaXYZ(d2r(NowPoseMat[3]), d2r(NowPoseMat[4]), d2r(NowPoseMat[5])) 
        GoalEnd = GoalEnd @ cls.Mat.TransXYZ(GoalPoseMat[0], GoalPoseMat[1], GoalPoseMat[2]) @ cls.Mat.RotaXYZ(d2r(GoalPoseMat[3]), d2r(GoalPoseMat[4]), d2r(GoalPoseMat[5]))
        # 矩陣軌跡法(原本)
        # HomogeneousMatData, velocityData, timeData = cls.TrjPlan.MatrixPathPlanning(GoalEnd, NowEnd, alltime, sampleTime)
        
        # 矩陣軌跡法(速度版)
        HomogeneousMatData, VelocityData, TimeData = cls.TrjPlan.MatrixPathPlanSpeed(GoalEnd, NowEnd, GoalSpeedType, GoalSpeed, sampleTime)
        # HomogeneousMatData, VelocityData, TimeData = cls.TrjPlan.PathToHomogeneousMats_Speed(GoalEnd, NowEnd, GoalSpeed, sampleTime)
         
        # HomogeneousMat to PoseMat
        PoseMatData = database_PoseMat.HomogeneousMatToPoseMat(HomogeneousMatData)
        
        return HomogeneousMatData, PoseMatData, VelocityData, TimeData
    
    @classmethod
    def generateTrajectory_totalTime(cls, NowPoseMat, GoalPoseMat, sampleTime, totalTime):
        """矩陣軌跡法 | 時間版本
        - Args:
            1. NowPoseMat
            2. GoalPoseMat
            3. sampleTime(s)
            4. GoalSpeed : (unit: mm/s)
        - Return:
            1. HomogeneousMatData(3D array)
            2. PoseMatData
            3. VelocityData
            4. TimeData
        """
        d2r = np.deg2rad
        NowEnd = np.eye(4)
        GoalEnd = np.eye(4)
        
        NowEnd = NowEnd @ cls.Mat.TransXYZ(NowPoseMat[0], NowPoseMat[1], NowPoseMat[2]) @ cls.Mat.RotaXYZ(d2r(NowPoseMat[3]), d2r(NowPoseMat[4]), d2r(NowPoseMat[5])) 
        GoalEnd = GoalEnd @ cls.Mat.TransXYZ(GoalPoseMat[0], GoalPoseMat[1], GoalPoseMat[2]) @ cls.Mat.RotaXYZ(d2r(GoalPoseMat[3]), d2r(GoalPoseMat[4]), d2r(GoalPoseMat[5]))
        
        # 矩陣軌跡法(總時間版)
        HomogeneousMatData, SpeedData, TimeData = cls.TrjPlan.MatrixPathPlanning(GoalEnd, NowEnd, totalTime, sampleTime)
        
        # HomogeneousMat to PoseMat
        PoseMatData = database_PoseMat.HomogeneousMatToPoseMat(HomogeneousMatData)
        
        return HomogeneousMatData, PoseMatData, SpeedData, TimeData

    @classmethod
    def generateTrajectoryJointAngle(cls, nowJointAngle:np.ndarray, HomogeneousMatData:np.ndarray):
        """
        """
        θ_Buffer = (np.zeros((6,1)))
        d2r = np.deg2rad
        """
        機器手臂原點 各關節角度:
        θ_Buffer[0, 0] =  d2r(-0.006)
        θ_Buffer[1, 0] =  d2r(-38.8189)
        θ_Buffer[2, 0] =  d2r(-41.0857)
        θ_Buffer[3, 0] =  d2r(-0.0030)
        θ_Buffer[4, 0] =  d2r(-76.4394)
        θ_Buffer[5, 0] =  d2r(1.0687)
        """
        θ_Buffer[0, 0] =  d2r(nowJointAngle[0, 0])
        θ_Buffer[1, 0] =  d2r(nowJointAngle[1, 0])
        θ_Buffer[2, 0] =  d2r(nowJointAngle[2, 0])
        θ_Buffer[3, 0] =  d2r(nowJointAngle[3, 0])
        θ_Buffer[4, 0] =  d2r(nowJointAngle[4, 0])
        θ_Buffer[5, 0] =  d2r(nowJointAngle[5, 0])

        # 透過逆向運動學獲得關節角度
        JointAngleData = np.zeros((len(HomogeneousMatData), 6, 1))
        for i in range(HomogeneousMatData.shape[0]):
            JointAngleData[i] = cls.Kin.IK_4x4(HomogeneousMatData[i], θ_Buffer)

        return JointAngleData
    
    @classmethod
    def generateTrajectory_Spline(cls, NowPoseMat, GoalPoseMat, sampleTime, GoalSpeed):
        Time = TimeTool()
        Kin = Kinematics()
        
        d2r = np.deg2rad
        b = Time.ReadNowTime()
        
        startPoint = np.array([NowPoseMat[0], NowPoseMat[1], NowPoseMat[2]])
        endPoint   = np.array([GoalPoseMat[0], GoalPoseMat[1], GoalPoseMat[2]])
        samplePoint = 200
        x , y, z, controlPoint = PathPlanning.cubicSpline(startPoint, endPoint, samplePoint)
        print(controlPoint)

        # # 繪製曲線
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.plot(x, y, z)

        # # 將控制點繪製到曲線上
        # ax.scatter(controlPoint[0], controlPoint[1], controlPoint[2], color='red', label='Control Points')

        # # 設置圖形屬性
        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')
        # ax.set_title('Spline Curve Connecting Points A, B, and C')

        # # 顯示圖形
        # plt.show()

        Data = np.zeros((len(x), 4, 4))
        Angular = np.arange(NowPoseMat[-1], GoalPoseMat[-1]+(GoalPoseMat[-1]-NowPoseMat[-1])/len(x), (GoalPoseMat[-1]-NowPoseMat[-1])/len(x))
        for i in range(len(x)-1):
            NowEnd = np.eye(4)  
            GoalEnd = np.eye(4)
            NowEnd = NowEnd @ cls.Mat.TransXYZ(x[i],y[i],z[i]) @ cls.Mat.RotaXYZ(d2r(-165.2876), d2r(-7.1723), d2r(Angular[i]))
            GoalEnd = GoalEnd @ cls.Mat.TransXYZ(x[i+1],y[i+1],z[i+1]) @ cls.Mat.RotaXYZ(d2r(-165.2876), d2r(-7.1723), d2r(Angular[i+1])) 
            homogeneousMat = PathPlanning.PathToHomogeneousMat(GoalEnd, NowEnd)
            
            Data[i] = homogeneousMat

        Data = Data[:-1]
        a = Time.ReadNowTime()
        calerr = Time.TimeError(b, a)
        print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")
        # Joint Angle
        nowJointAngle = (np.zeros((6,1)))
        nowJointAngle[0, 0] =  d2r(-0.006)
        nowJointAngle[1, 0] =  d2r(-38.8189)
        nowJointAngle[2, 0] =  d2r(-41.0857)
        nowJointAngle[3, 0] =  d2r(-0.0030)
        nowJointAngle[4, 0] =  d2r(-76.4394)
        nowJointAngle[5, 0] =  d2r(1.0687)

        # 透過逆向運動學獲得關節角度
        JointAngleData = np.zeros((len(Data), 6, 1))
        for i in range(Data.shape[0]):
            JointAngleData[i] = Kin.IK_4x4(Data[i], nowJointAngle)
    
        Sim.paitGL(JointAngleData, Data)

    @staticmethod
    def mergeTrjs(axis=0, *arrays:np.ndarray):
        """連接多個軌跡資料數組。

        Args:
            axis (int): 沿哪個軸連接數組，默認為0。
            *arrays (ndarray): 任意數量的待連接數組。

        Return:
            np.ndarray: 連接後的數組。
        """
        if not arrays:
            raise ValueError("至少需要一個數組來連接")
        
        # 檢查所有數組是否為 numpy array
        for array in arrays:
            if not isinstance(array, np.ndarray):
                raise TypeError("所有輸入必須是 numpy array")

        # 使用 np.concatenate 連接數組
        result = np.concatenate((arrays), axis=axis)
        return result
    
    @staticmethod
    def GenerBoxPath(ReplanPathNumber:list, Velocity, AngularVelocity):
        """生成四邊形軌跡

        Arg:
            ReplanPathNumber: 需要重新規劃軌跡的路徑編號，ex:[1, 2, 3]
            Velocity: mm/s
            AngularVelocity: deg/s
        1. 生成軌跡
        2. 計算IK
        3. 模擬
        """
        

        # 歐式距離: 18mm
        # 第一段
        # NowEnd1 = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd1 = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
        # # 第一段 to 第二段 純姿態轉換
        # NowEnd2 = [958.521, -18.527, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd2 = [958.525, -18.527, -164.933, -165.2873, -7.1725, 107.5181]
        # # 第二段
        # NowEnd3 = [958.521, -18.527, -164.943, -165.2876, -7.1723, 97.5181]
        # GoalEnd3 = [940.525, -18.527, -164.933, -165.2873, -7.1725, 97.5181]


        # 歐式距離: 150mm
        # NowEnd = [958.521, -109.209, -158.398, -165.2876, -52.1723, 17.5191]
        # GoalEnd = [958.525, 41.670, -158.417, -165.2876, -52.1723, 17.5191]

        # NowEnd = [958.525, 41.670, -158.417, -165.2876, -52.1723, 97.5191]
        # GoalEnd = [808.525, 41.670, -158.417, -165.2876, -52.1723, 97.5191]
        # 曲線:150mm
        # NowEnd = [958.521, -109.209, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd = [858.525, 41.670, -164.943, -165.2876, -7.1723, 97.5191]
        """L型軌跡
        第一段:
            起點: [1031.987, -104.122, -139.911, -152.7425, 23.1266, 20.5289]
            姿態修改起點:[1032.008, 37.584, -139.896, -152.746, 23.1284, 20.5184]
            終點:[1033.112, 47.657, -140.156, -152.7421, 23.1349, 110.6475]
        第二段:
            起點:[1033.112, 47.657, -140.156, -152.7421, 23.1349, 110.6475]
            姿態修正起點:[893.962, 48.64, -139.7, -152.7357, 23.1516, 110.6175]
        """

        """矩形軌跡
        Org = [485.126, -1.295, 234.296, 179.9772, 20.2428, 1.6694]

        PreGo:[1028.838, -100.512, -60.384, 153.7943, -12.9858, -137.0558]

        第一段起點:[1028.892, -100.126, -133.43, 153.7838, -12.9644, -137.0478]
        第一段姿態變換起點:[1028.898, 39.173, -133.479, 153.7858, -12.965, -137.0483]

        第二段起點:[1031.113, 46.448, -133.548, 153.794, -12.9626, -67.5844]
        第二段姿態變換前:[889.137, 46.416, -133.527, 153.7951, -12.9672, -67.5838]

        第三段起點:[883.23, 46.267, -136.13, 152.7504, 9.8314, 46.9511]
        第三段姿態變換前:[883.227, -94.75, -133.892, 152.7565, 9.824, 46.9406]

        第四段起點:[883.285, -103.725, -135.859, 166.9137, 9.1798, 131.1553]
        第四段終點:[1034.248, -103.696, -135.859, 166.9115, 9.179, 131.1576]

        PreBack:[1034.267, -103.681, -45.869, 166.9084, 9.181, 131.1607]
        
        Org = [485.126, -1.295, 234.296, 179.9772, 20.2428, 1.6694]
        """
        PreGo             = [1028.838, -100.512, -60.384, 153.7943, -12.9858, -137.0558]

        line1stStart      = [1015.663, -97.245, -136.568, 156.9335, -25.4738, -153.5185]
        line1stFixPosture = [1014.641, 37.281, -136.031, 157.2382, -24.6544, -151.3165]
        line1stEnd        = [1015.64, 50.987, -136.698, 156.9356, -25.4816, -63.1536]

        line2ndStart      = [1015.64, 50.987, -136.698, 156.9356, -25.4816, -63.1536]
        line2ndFixPosture = [876.832, 50.348, -137.807, 156.9315, -25.4789, -63.1439]
        line2ndEnd        = [865.751, 48.678, -136.009, 156.8277, -25.0825, 32.9625]
        
        line3rdStart      = [865.751, 48.678, -136.009, 156.8277, -25.0825, 32.9625]
        line3rdFixPosture = [866.842, -87.175, -136.515, 156.8276, -25.0821, 32.9619]
        line3rdEnd        = [867.546, -99.766, -136.385, 164.302, 2.6641, 107.3331]
        
        line4thStart      = [867.546, -99.766, -136.385, 164.302, 2.6641, 107.3331]
        line4thEnd        = [1014.06, -98.571, -134.457, 164.2953, 2.668, 107.3375]

        PreBack           = [1034.267, -103.681, -45.869, 166.9084, 9.181, 131.1607]
        
        WeldSpeed = Velocity
        angularVelocity = np.deg2rad(AngularVelocity)
        sampleTime = 0.04
        
        b = Time.ReadNowTime()
        """
        Box Path
        """
        # TODO 利用ReplanPathNumber分類需要重新規畫的路徑編號
        # 第一直線段
        HomogeneousMatData1, PoseMatData1, VelocityData1, TimeData1 = Generator.generateTrajectory(line1stStart, line1stFixPosture, sampleTime, Velocity=WeldSpeed)
        # 第一段>>第二段 姿態規劃
        HomogeneousMatData2, PoseMatData2, VelocityData2, TimeData2 = Generator.generateTrajectory(line1stFixPosture, line1stEnd, sampleTime, Velocity=WeldSpeed)
        # 第二直線段
        HomogeneousMatData3, PoseMatData3, VelocityData3, TimeData3 = Generator.generateTrajectory(line2ndStart, line2ndFixPosture, sampleTime, Velocity=WeldSpeed)
        # 第二段>>第三段 姿態規劃
        HomogeneousMatData4, PoseMatData4, VelocityData4, TimeData4 = Generator.generateTrajectory(line2ndFixPosture, line2ndEnd, sampleTime, Velocity=WeldSpeed)
        # 第三直線段
        HomogeneousMatData5, PoseMatData5, VelocityData5, TimeData5 = Generator.generateTrajectory(line3rdStart, line3rdFixPosture, sampleTime, Velocity=WeldSpeed)
        # 第三段>>第四段 姿態規劃
        HomogeneousMatData6, PoseMatData6, VelocityData6, TimeData6 = Generator.generateTrajectory(line3rdFixPosture, line3rdEnd, sampleTime, Velocity=WeldSpeed)
        # 第四直線段
        HomogeneousMatData7, PoseMatData7, VelocityData7, TimeData7 = Generator.generateTrajectory(line4thStart, line4thEnd, sampleTime, Velocity=WeldSpeed)
        
        a = Time.ReadNowTime()
        calerr = Time.TimeError(b, a)
        print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")

        # 軌跡資料整併
        axis = 0
        HomogeneousMatData = Generator.mergeTrjs(axis, HomogeneousMatData1, HomogeneousMatData2, HomogeneousMatData3, HomogeneousMatData4, HomogeneousMatData5, HomogeneousMatData6, HomogeneousMatData7)
        PoseMatData = Generator.mergeTrjs(axis, PoseMatData1, PoseMatData2, PoseMatData3, PoseMatData4, PoseMatData5, PoseMatData6, PoseMatData7)
        VelocityData = Generator.mergeTrjs(axis, VelocityData1, VelocityData2, VelocityData3, VelocityData4, VelocityData5, VelocityData6, VelocityData7)
        TimeData = Generator.mergeTrjs(axis, TimeData1, TimeData2, TimeData3, TimeData4, TimeData5, TimeData6, TimeData7)
        
        mode = "w"
        filename_header = "database/dynamicllyPlanTEST/"
        # 標號為0表示其為軌跡原檔
        number = 0

        HomogeneousMat_file = filename_header + f"HomogeneousMat_{number}.csv"
        PoseMat_file = filename_header + f"PoseMat_{number}.csv"
        Speed_file = filename_header + f"Speed_{number}.csv"
        Time_file = filename_header + f"Time_{number}.csv"
        PoseMatAndTime_file = filename_header + f"PoseMatAndTime_{number}.csv"

        
        database_HomogeneousMat.Save(HomogeneousMatData, HomogeneousMat_file, mode)
        database_PoseMat.Save(PoseMatData, PoseMat_file, mode)
        database_Velocity.Save(VelocityData, Speed_file, mode)
        database_time.Save(TimeData, Time_file, mode)
        TimeData = TimeData.reshape(-1, 1, 1)
        PoseMatAndTime = np.concatenate((PoseMatData, TimeData), axis=2)
        database_time.Save_PoseMat_Time(PoseMatAndTime, PoseMatAndTime_file, mode)
        
        nowJointAngle = (np.zeros((6,1)))
        nowJointAngle[0, 0] =  d2r(-0.006)
        nowJointAngle[1, 0] =  d2r(-38.8189)
        nowJointAngle[2, 0] =  d2r(-41.0857)
        nowJointAngle[3, 0] =  d2r(-0.0030)
        nowJointAngle[4, 0] =  d2r(-76.4394)
        nowJointAngle[5, 0] =  d2r(1.0687)
        HomogeneousMat = database_HomogeneousMat.Load(filename_header+f"HomogeneousMat_{number}.csv")
        b = Time.ReadNowTime()
        JointAngle = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
        a = Time.ReadNowTime()
        calerr = Time.TimeError(b, a)
        print("計算新軌跡IK總共花費: ", calerr["millisecond"], "ms")
        database_JointAngle.Save(JointAngle, filename_header+f"JointAngle_{number}.csv", mode)

        Sim.paitGL(JointAngle, HomogeneousMat)

    
if __name__ == "__main__":
    d2r = np.deg2rad
    Time = TimeTool()
    Sim = Simulator()
    Udp = MotomanUDP()

    # 功能模式調整區
    """
    Planning or Simulator
    Planning: True
    Simulator: False
    """
    userMode = True

    """
    Online or Offline 測試
    Online: True
    Offline: False
    """
    Line = True

    # Generator.GenerBoxPath(0, 1.5, 10)

    if userMode is True:
        """
        1. 生成軌跡
        2. 計算IK
        3. 模擬
        """
        
        # 歐式距離: 18mm
        # 第一段
        # NowEnd1 = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd1 = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
        # # 第一段 to 第二段 純姿態轉換
        # NowEnd2 = [958.521, -18.527, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd2 = [958.525, -18.527, -164.933, -165.2873, -7.1725, 107.5181]
        # # 第二段
        # NowEnd3 = [958.521, -18.527, -164.943, -165.2876, -7.1723, 97.5181]
        # GoalEnd3 = [940.525, -18.527, -164.933, -165.2873, -7.1725, 97.5181]


        # 歐式距離: 150mm
        # NowEnd = [960.216, 41.426, -151.949, 175.7717, 17.9366, 59.3998]
        # GoalEnd = [960.216, -109.209, -151.949, 175.7717, 17.9366, 59.3998]

        """
        對接 無填料
        NowEnd = [959.911, 21.293, -164.953, 175.9975, 17.9492, 58.6475]
        GoalEnd = [960.84, -96.446, -164.83, 175.9973, 17.9444, 58.6498]

        對接 有填料
        a:
        NowEnd = [956.58, -101.585, -165.127, 160.4994, 7.8481, -157.0421]
        GoalEnd = [953.691, 35.608, -165.241, 160.4223, 7.7129, -157.0598]
        b:
        NowEnd = [956.736, -101.583, -165.144, 160.5061, 7.8549, -157.0437]
        GoalEnd = [953.798, 35.604, -165.26, 160.5005, 7.8458, -157.0483]
        c:
        NowEnd = [956.081, -101.598, -165.123, 160.5135, 7.8629, -157.0418]
        GoalEnd = [953.801, 35.611, -165.26, 160.506, 7.855, -157.0438]
        d:
        NowEnd = [956.306, -101.617, -165.151, 160.5194, 7.8727, -157.0404]
        GoalEnd = [953.804, 35.61, -165.263, 160.5135, 7.8616, -157.042]
        """

        

        """
        角接 無填料
        NowEnd = [966.726, -108.062, -138.663, 151.5946, -25.0176, -130.4836]
        GoalEnd = [965.324, 39.827, -138.689, 151.5878, -25.0162, -130.4795]

        角接 有填料
        變電流 a
        NowEnd = [969.599, -103.133, -138.516, 156.8904, -25.2523, -153.4883]
        GoalEnd = [968.44, 37.806, -138.469, 156.8825, -25.2732, -153.4673]
        變電流 b
        NowEnd = [969.048, -103.006, -138.104, 156.8821, -25.239, -153.4861]
        GoalEnd = [968.219, 37.8, -138.833, 156.8862, -25.2513, -153.4835]
        變速度 c
        NowEnd = [969.383, -103.003, -138.606, 156.8765, -25.2241, -153.4754]
        GoalEnd = [968.45, 37.781, -138.832, 156.8818, -25.2384, -153.4846]
        變速度 d'
        NowEnd = [969.507, -102.994, -139.141, 156.8727, -25.2113, -153.4683]
        GoalEnd = [968.864, 37.117, -138.451, 156.8598, -25.1973, -153.4546]
        變速度d
        NowEnd = [969.94, -102.936, -139.216, 156.8581, -25.1919, -153.4552]
        GoalEnd = [968.723, 37.107, -138.451, 156.8721, -25.2099, -153.4682]
        """
        # NowEnd     = [1028.892, -100.126, -133.43, 153.7838, -12.9644, -137.0478]
        # GoalEnd = [1028.898, 39.173, -133.479, 153.7858, -12.965, -137.0483]

        NowEnd = [969.94, -102.936, -139.216, 156.8581, -25.1919, -153.4552]
        GoalEnd = [968.723, 37.107, -138.451, 156.8721, -25.2099, -153.4682]
        
        if Line is True:
            NowEndData = [17, 4, 5, 0, NowEnd[0], NowEnd[1], NowEnd[2], NowEnd[3]*10, NowEnd[4]*10, NowEnd[5]*10]
            Udp.WriteRPVar(2, NowEndData)
            NowEndData = [17, 4, 5, 0, GoalEnd[0], GoalEnd[1], GoalEnd[2], GoalEnd[3]*10, GoalEnd[4]*10, GoalEnd[5]*10]
            Udp.WriteRPVar(3, NowEndData)


        # NowEnd = [958.525, 41.670, -158.417, -165.2876, -52.1723, 97.5191]
        # GoalEnd = [808.525, 41.670, -158.417, -165.2876, -52.1723, 97.5191]
        # 曲線:150mm
        # NowEnd = [958.521, -109.209, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd = [858.525, 41.670, -164.943, -165.2876, -7.1723, 97.5191]
        
        
        WeldSpeed = 1
        angularVelocity = np.deg2rad(10)
        sampleTime = 0.04
        
        b = Time.ReadNowTime()
        """
        Linear
        """
        # 直線段
        HomogeneousMatData, PoseMatData, VelocityData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, Velocity=WeldSpeed)
        
        # Generator.generateTrajectory_Spline(NowEnd, GoalEnd, sampleTime, Goalspeed)
        # HomogeneousMatData2, PoseMatData2, VelocityData2, TimeData2 = Generator.generateTrajectory_totalTime(NowEnd2, GoalEnd2, sampleTime, 1)
        a = Time.ReadNowTime()
        calerr = Time.TimeError(b, a)
        print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")

        mode = "w"
        filename_header = "database/dynamicllyPlanTEST/"
        # 標號為0表示其為軌跡原檔
        number = 0

        HomogeneousMat_file = filename_header + f"HomogeneousMat_{number}.csv"
        PoseMat_file = filename_header + f"PoseMat_{number}.csv"
        Speed_file = filename_header + f"Speed_{number}.csv"
        Time_file = filename_header + f"Time_{number}.csv"
        PoseMatAndTime_file = filename_header + f"PoseMatAndTime_{number}.csv"

        
        database_HomogeneousMat.Save(HomogeneousMatData, HomogeneousMat_file, mode)
        database_PoseMat.Save(PoseMatData, PoseMat_file, mode)
        database_Velocity.Save(VelocityData, Speed_file, mode)
        database_time.Save(TimeData, Time_file, mode)
        TimeData = TimeData.reshape(-1, 1, 1)
        PoseMatAndTime = np.concatenate((PoseMatData, TimeData), axis=2)
        database_time.Save_PoseMat_Time(PoseMatAndTime, PoseMatAndTime_file, mode)
        
        nowJointAngle = (np.zeros((6,1)))
        nowJointAngle[0, 0] =  d2r(-0.006)
        nowJointAngle[1, 0] =  d2r(-38.8189)
        nowJointAngle[2, 0] =  d2r(-41.0857)
        nowJointAngle[3, 0] =  d2r(-0.0030)
        nowJointAngle[4, 0] =  d2r(-76.4394)
        nowJointAngle[5, 0] =  d2r(1.0687)
        
        HomogeneousMat = database_HomogeneousMat.Load(filename_header+f"HomogeneousMat_{number}.csv")
        b = Time.ReadNowTime()
        JointAngle = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
        a = Time.ReadNowTime()
        calerr = Time.TimeError(b, a)
        print("計算新軌跡IK總共花費: ", calerr["millisecond"], "ms")
        database_JointAngle.Save(JointAngle, filename_header+f"JointAngle_{number}.csv", mode)

        Sim.paitGL(JointAngle, HomogeneousMat)


    if userMode is False:
        """
        模擬指定路徑檔案
        """
        nowJointAngle = (np.zeros((6,1)))
        nowJointAngle[0, 0] =  d2r(-0.006)
        nowJointAngle[1, 0] =  d2r(-38.8189)
        nowJointAngle[2, 0] =  d2r(-41.0857)
        nowJointAngle[3, 0] =  d2r(-0.0030)
        nowJointAngle[4, 0] =  d2r(-76.4394)
        nowJointAngle[5, 0] =  d2r(1.0687)
        
        # PoseMat >>> HomogeneousMat
        filename_header = "Experimental_data/20240527/a/"
        PoseMat = database_PoseMat.Load(filename_header+"PoseMat_0.csv")
        HomogeneousMat = database_HomogeneousMat.Load(filename_header+"HomogeneousMat_0.csv")
        JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
        database_JointAngle.Save(JointAngleData, filename_header+"JointAngle_0.csv", "w")
        
        Sim.paitGL(JointAngleData, HomogeneousMat)