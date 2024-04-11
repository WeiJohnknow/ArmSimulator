# from SimulatorV2 import Simulator
# from dataBase_v0 import dataBase
# from Matrix import Matrix4x4
# from PathPlanning import PathPlanning
# import numpy as np
# from dataBase_v1 import *


# class armControl(Simulator):
#     def __init__(self):
#         pass

#     def generateTrajectory(self):
#         d2r = np.deg2rad

#         # Arm org point Joint angle
#         θ_Buffer = (np.zeros((6,1)))
#         θ_Buffer[0, 0] =  d2r(-0.006)
#         θ_Buffer[1, 0] =  d2r(-38.8189)
#         θ_Buffer[2, 0] =  d2r(-41.0857)
#         θ_Buffer[3, 0] =  d2r(-0.0030)
#         θ_Buffer[4, 0] =  d2r(-76.4394)
#         θ_Buffer[5, 0] =  d2r(1.0687)

#         ################################################################################################
#         """
#         Parameter set:
#         * NowEnd
#         * GoalEnd
#         * alltime
#         * sampleTime
#         * header_filePath
#         """

#         """
#         * Point Name: [px, py, pz, rx, ry, rz] 

#         * ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
#         * testPoint = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]

#         * weldingStart = [956.316, -109.275, -159.859, -165.2936, -7.1766, 17.5381]
#         * weldingEnd   = [956.3, -9.275, -159.871, -165.291, -7.1738, 17.5332]
#         """

#         # File Path parameter
#         # header_filePath = "Experimental_data/20240312/"
#         header_filePath = "dataBase/"
        
#         # Set Now and Goal Point
#         # NowData: {'dataType': 16, 'Form': 4, 'Toolnumber': 0, 'UserCoordinate': 0}
#         Now = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
        
#         # GoalData:{'dataType': 16, 'Form': 4, 'Toolnumber': 0, 'UserCoordinate': 0}
#         Goal = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]

#         # Trajectory total time(second)
#         alltime = 8

#         # Sample time(second)
#         sampleTime = 0.04
#         ################################################################################################
#         NowEnd = np.eye(4)
#         GoalEnd = np.eye(4)
        
#         NowEnd = NowEnd @ self.Mat.TransXYZ(Now[0]*self.Unit, Now[1]*self.Unit, Now[2]*self.Unit) @ self.Mat.RotaXYZ(d2r(Now[3]), d2r(Now[4]), d2r(Now[5])) 
#         GoalEnd = GoalEnd @ self.Mat.TransXYZ(Goal[0]*self.Unit, Goal[1]*self.Unit, Goal[2]*self.Unit) @ self.Mat.RotaXYZ(d2r(Goal[3]), d2r(Goal[4]), d2r(Goal[5]))

#         # 軌跡規劃演算法
#         pathData, velData, timeData = self.Plan.MatrixPathPlanning(GoalEnd, NowEnd, alltime, sampleTime)
#         print("最大速度: ", np.max(velData))
#         # pathData, velData, timeData = self.Plan.MatrixPath434(GoalEnd, NowEnd, alltime, sampleTime)
#         # pathData, timeData = self.Plan.MatrixPath_Scurve(GoalEnd, NowEnd, sampleTime)

#         # 存入軌跡資料
#         # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434.csv"
#         # filePath = header_filePath + "MatrixPlan_linear.csv"
#         filePath = header_filePath + "test0326_mat4x4.csv"
#         # self.dB.saveMatrix4x4(pathData, timeData, "w", filePath)
#         database_HomogeneousMat.Save(pathData, timeData, filePath, "w")
#         HomogeneousMat = database_HomogeneousMat.Load(filePath)
#         PoseMat = database_PoseMat.HomogeneousMatToPoseMat(HomogeneousMat)
#         database_PoseMat.Save(PoseMat, header_filePath + "test0326_Posemat.csv", "w")
#         PoseMatData = database_PoseMat.Load(header_filePath + "test0326_Posemat.csv")

#         # 存入速度資料
#         # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_velocity.csv"
#         # filePath = header_filePath + "MatrixPlan_linear_velocity.csv"
#         # self.dB.saveVelocity(velData, "w", filePath)
#         database_Velocity.Save(velData, header_filePath + "test0.26_velocity.csv", "w")
#         VelocityData = database_Velocity.Load(header_filePath + "test0.26_velocity.csv")

#         # 載入軌跡資料
#         # filePath = header_filePath + "MatrixPlan_linear.csv"
#         # _, pathData_df, pathData_np4x4, pathData_np6x1 = self.dB.LoadMatrix4x4(filePath)
#         HomogeneousMatData = database_HomogeneousMat.Load(header_filePath + "test0326_mat4x4.csv")

#         # 計算逆向運動學
#         path_JointAngle = np.zeros((len(HomogeneousMatData), 6, 1))
#         for i in range(len(path_JointAngle)):
#             path_JointAngle[i] = self.Kin.IK_4x4(HomogeneousMatData[i], θ_Buffer)
            

#         # 儲存關節角度
#         # filePath = header_filePath + "MatrixPlan_linear_JointAngle.csv"
#         # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_JointAngle.csv"
#         # self.dB.saveJointAngle(path_JointAngle, "w", filePath)
#         database_JointAngle.Save(path_JointAngle, header_filePath + "test0326_JointAngle.csv", "w")
#         JointAngle = database_JointAngle.Load(header_filePath + "test0326_JointAngle.csv")

#         # 儲存姿態矩陣
#         # filePath = header_filePath + "MatrixPlan_linear_PoseMatrix.csv"
#         # # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_PoseMatrix.csv"
#         # self.dB.savePoseMatrix(pathData_np6x1, "w", filePath)

#         # return path_JointAngle, pathData_np4x4
#         return path_JointAngle, HomogeneousMat
#         """
#         現有路徑檔案模擬
#         """
#         # filePath = "Experimental_data/20240306/Revise/Teach_mode_Multi_Trajectory_welding.csv"
#         # rowData = self.dB.Load(filePath)
#         # path_Pose = np.zeros((len(rowData), 6))
#         # path_4x4 = np.zeros((len(rowData), 4, 4))
        
#         # for i in range(len(path_Pose)):
#         #     buffer_np = np.zeros((6,1))
#         #     buffer_np[0, 0] = rowData['X'][i]
#         #     buffer_np[1, 0] = rowData['Y'][i]
#         #     buffer_np[2, 0] = rowData['Z'][i]
#         #     buffer_np[3, 0] = d2r(rowData['Rx'][i])
#         #     buffer_np[4, 0] = d2r(rowData['Ry'][i])
#         #     buffer_np[5, 0] = d2r(rowData['Rz'][i])

#         #     path_4x4[i] = self.Mat.AngletoMat(buffer_np)
        
#         # path_JointAngle = np.zeros((len(rowData), 6, 1))

#         # # 計算逆向運動學
#         # for i in range(len(rowData)):
#         #     path_JointAngle[i] = self.Kin.IK_4x4(path_4x4[i], θ_Buffer)

#         # return path_JointAngle, path_4x4

#     def main(self):
#         path_JointAngle, pathData_np4x4 = self.generateTrajectory()
#         self.paitGL(path_JointAngle, pathData_np4x4)

# if __name__ == "__main__":
#     ctrl = armControl()
#     ctrl.main()

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
        """
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

    NowEnd = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
    # NowEnd = [958.521, -23.142, -164.943, -165.2876, -7.1723, 17.5191]
    GoalEnd = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
    Goalspeed = 2
    sampleTime = 0.04
    filename_header = "database/dynamicllyPlanTEST/"
    b = Time.ReadNowTime()
    HomogeneousMatData, PoseMatData, VelocityData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, Goalspeed)
    a = Time.ReadNowTime()
    calerr = Time.TimeError(b, a)
    print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")

    mode = "w"
    database_HomogeneousMat.Save(HomogeneousMatData, filename_header+"HomogeneousMat.csv", mode)
    database_PoseMat.Save(PoseMatData, filename_header+"PoseMat.csv", mode)
    database_Velocity.Save(VelocityData, filename_header+"Velocity.csv", mode)
    database_time.Save(TimeData, filename_header+"Time.csv", mode)
    
    nowJointAngle = (np.zeros((6,1)))
    nowJointAngle[0, 0] =  d2r(-0.006)
    nowJointAngle[1, 0] =  d2r(-38.8189)
    nowJointAngle[2, 0] =  d2r(-41.0857)
    nowJointAngle[3, 0] =  d2r(-0.0030)
    nowJointAngle[4, 0] =  d2r(-76.4394)
    nowJointAngle[5, 0] =  d2r(1.0687)
    HomogeneousMat = database_HomogeneousMat.Load(filename_header+"HomogeneousMat.csv")
    JointAngle = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
    database_JointAngle.Save(JointAngle, filename_header+"JointAngle.csv", mode)

    Sim.paitGL(JointAngle, HomogeneousMat)
    
    # PoseMat >>> HomogeneousMat
    # PoseMat = database_PoseMat.Load("database/test0330/new/Remix_PoseMat.csv")
    # HomogeneousMat = database_HomogeneousMat.Load("database/test0330/new/Remix_HomogeneousMat.csv")
    # JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, HomogeneousMat)
    # database_JointAngle.Save(JointAngleData, "database/test0330/new/Remix_JointAngle.csv", "w")
    
    # Sim.paitGL(JointAngleData, HomogeneousMat)