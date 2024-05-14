
from Kinematics import Kinematics
from Matrix import Matrix4x4
from PathPlanning import PathPlanning
from dataBase_v1 import *
from Toolbox import TimeTool
from SimulatorV2 import Simulator
import numpy as np

class Generator:
    # 類別變數
    Kin = Kinematics()
    Mat = Matrix4x4()
    TrjPlan = PathPlanning()


    @classmethod
    def generateTrajectory(cls, NowPoseMat, GoalPoseMat, sampleTime, GoalSpeed):
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
        d2r = np.deg2rad
        NowEnd = np.eye(4)
        GoalEnd = np.eye(4)
        
        NowEnd = NowEnd @ cls.Mat.TransXYZ(NowPoseMat[0], NowPoseMat[1], NowPoseMat[2]) @ cls.Mat.RotaXYZ(d2r(NowPoseMat[3]), d2r(NowPoseMat[4]), d2r(NowPoseMat[5])) 
        GoalEnd = GoalEnd @ cls.Mat.TransXYZ(GoalPoseMat[0], GoalPoseMat[1], GoalPoseMat[2]) @ cls.Mat.RotaXYZ(d2r(GoalPoseMat[3]), d2r(GoalPoseMat[4]), d2r(GoalPoseMat[5]))
        # 矩陣軌跡法(原本)
        # HomogeneousMatData, velocityData, timeData = cls.TrjPlan.MatrixPathPlanning(GoalEnd, NowEnd, alltime, sampleTime)
        
        # 矩陣軌跡法(速度版)
        HomogeneousMatData, VelocityData, TimeData = cls.TrjPlan.MatrixPathPlanSpeed(GoalEnd, NowEnd, GoalSpeed, sampleTime)
         
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
        NowEnd = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
        GoalEnd = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
        # 歐式距離: 150mm
        # NowEnd = [958.521, -109.209, -158.398, -164.6564, -7.5189, 18.1239]
        # GoalEnd = [958.525, 41.670, -158.417, -164.6548, -7.5165, 18.1217]
        
        Goalspeed = 2
        sampleTime = 0.04
        
        b = Time.ReadNowTime()
        # HomogeneousMatData, PoseMatData, VelocityData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, Goalspeed)
        HomogeneousMatData, PoseMatData, VelocityData, TimeData = Generator.generateTrajectory_totalTime(NowEnd, GoalEnd, sampleTime, 8.8)
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
        filename_header = "database/dynamicllyPlanTEST/"
        PoseMat = database_PoseMat.Load(filename_header+"Remix_PoseMat.csv")
        HomogeneousMat = database_HomogeneousMat.Load(filename_header+"Remix_HomogeneousMat.csv")
        JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
        database_JointAngle.Save(JointAngleData, filename_header+"Remix_JointAngle.csv", "w")
        
        Sim.paitGL(JointAngleData, HomogeneousMat)