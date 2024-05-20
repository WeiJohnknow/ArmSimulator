
from Kinematics import Kinematics
from Matrix import Matrix4x4
from PathPlanning import PathPlanning
from dataBase_v1 import *
from Toolbox import TimeTool
from SimulatorV2 import Simulator
import numpy as np
import matplotlib.pyplot as plt

class Generator:
    # 類別變數
    Kin = Kinematics()
    Mat = Matrix4x4()
    TrjPlan = PathPlanning()


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
    def generateTrajectoryJointAngle(cls, nowJointAngle, HomogeneousMatData):
        θ_Buffer = (np.zeros((6,1)))
        d2r = np.deg2rad
        # θ_Buffer[0, 0] =  d2r(-0.006)
        # θ_Buffer[1, 0] =  d2r(-38.8189)
        # θ_Buffer[2, 0] =  d2r(-41.0857)
        # θ_Buffer[3, 0] =  d2r(-0.0030)
        # θ_Buffer[4, 0] =  d2r(-76.4394)
        # θ_Buffer[5, 0] =  d2r(1.0687)
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


    
if __name__ == "__main__":
    d2r = np.deg2rad
    Time = TimeTool()
    Sim = Simulator()

    # 功能模式調整區
    userMode = True

    if userMode is True:
        """
        1. 生成軌跡
        2. 計算IK
        3. 模擬
        """
        # 歐式距離: 18mm
        # 第一段
        NowEnd1 = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
        GoalEnd1 = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
        # 第一段 to 第二段 純姿態轉換
        NowEnd2 = [958.521, -18.527, -164.943, -165.2876, -7.1723, 17.5191]
        GoalEnd2 = [958.525, -18.527, -164.933, -165.2873, -7.1725, 107.5181]
        # 第二段
        NowEnd3 = [958.521, -18.527, -164.943, -165.2876, -7.1723, 97.5181]
        GoalEnd3 = [940.525, -18.527, -164.933, -165.2873, -7.1725, 97.5181]


        # 歐式距離: 150mm
        # NowEnd = [958.521, -109.209, -158.398, -165.2876, -52.1723, 17.5191]
        # GoalEnd = [958.525, 41.670, -158.417, -165.2876, -52.1723, 17.5191]

        # NowEnd = [958.525, 41.670, -158.417, -165.2876, -52.1723, 97.5191]
        # GoalEnd = [808.525, 41.670, -158.417, -165.2876, -52.1723, 97.5191]
        # 曲線:150mm
        # NowEnd = [958.521, -109.209, -164.943, -165.2876, -7.1723, 17.5191]
        # GoalEnd = [858.525, 41.670, -164.943, -165.2876, -7.1723, 97.5191]
        
        Goalspeed = 2
        angularVelocity = np.deg2rad(100)
        sampleTime = 0.04
        
        b = Time.ReadNowTime()

        # 第一直線段
        HomogeneousMatData1, PoseMatData1, VelocityData1, TimeData1 = Generator.generateTrajectory(NowEnd1, GoalEnd1, sampleTime, Velocity=Goalspeed)
        # 第一段>>第二段 姿態規劃
        HomogeneousMatData2, PoseMatData2, VelocityData2, TimeData2 = Generator.generateTrajectory(NowEnd2, GoalEnd2, sampleTime, angularVelocity=angularVelocity)
        # HomogeneousMatData2, PoseMatData2, VelocityData2, TimeData2 = Generator.generateTrajectory_totalTime(NowEnd2, GoalEnd2, sampleTime, 1)
        # 第二直線段
        HomogeneousMatData3, PoseMatData3, VelocityData3, TimeData3 = Generator.generateTrajectory(NowEnd3, GoalEnd3, sampleTime, Velocity=Goalspeed)
        
        # Generator.generateTrajectory_Spline(NowEnd, GoalEnd, sampleTime, Goalspeed)
        
        a = Time.ReadNowTime()
        calerr = Time.TimeError(b, a)
        print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")

        # 軌跡資料整併
        axis = 0
        HomogeneousMatData = Generator.mergeTrjs(axis, HomogeneousMatData1, HomogeneousMatData2, HomogeneousMatData3)
        PoseMatData = Generator.mergeTrjs(axis, PoseMatData1, PoseMatData2, PoseMatData3)
        VelocityData = Generator.mergeTrjs(axis, VelocityData1, VelocityData2, VelocityData3)
        TimeData = Generator.mergeTrjs(axis, TimeData1, TimeData2, TimeData3)
        
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
        filename_header = "database/dynamicllyPlanTEST/"
        PoseMat = database_PoseMat.Load(filename_header+"Remix_PoseMat.csv")
        HomogeneousMat = database_HomogeneousMat.Load(filename_header+"Remix_HomogeneousMat.csv")
        JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
        database_JointAngle.Save(JointAngleData, filename_header+"Remix_JointAngle.csv", "w")
        
        Sim.paitGL(JointAngleData, HomogeneousMat)