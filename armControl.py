from SimulatorV2 import Simulator
from dataBase import dataBase
from Matrix import Matrix4x4
from PathPlanning import PathPlanning
import numpy as np


class armControl(Simulator):
    def __init__(self):
        super().__init__()
        pass
    
    def generateTrajectory(self):
        d2r = np.deg2rad

        # Arm org point Joint angle
        θ_Buffer = (np.zeros((6,1)))
        θ_Buffer[0, 0] =  d2r(-0.006)
        θ_Buffer[1, 0] =  d2r(-38.8189)
        θ_Buffer[2, 0] =  d2r(-41.0857)
        θ_Buffer[3, 0] =  d2r(-0.0030)
        θ_Buffer[4, 0] =  d2r(-76.4394)
        θ_Buffer[5, 0] =  d2r(1.0687)

        ################################################################################################
        """
        Parameter set:
        * NowEnd
        * GoalEnd
        * alltime
        * sampleTime
        * header_filePath
        """

        """
        * Point Name: [px, py, pz, rx, ry, rz] 

        * ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
        * testPoint = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]

        * weldingStart = [956.316, -109.275, -159.859, -165.2936, -7.1766, 17.5381]
        * weldingEnd   = [956.3, -9.275, -159.871, -165.291, -7.1738, 17.5332]
        """

        # File Path parameter
        header_filePath = "Experimental_data/20240312/"
        
        # Set Now and Goal Point
        # NowData: {'dataType': 16, 'Form': 4, 'Toolnumber': 0, 'UserCoordinate': 0}
        Now = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
        
        # GoalData:{'dataType': 16, 'Form': 4, 'Toolnumber': 0, 'UserCoordinate': 0}
        Goal = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]

        # Trajectory total time(second)
        alltime = 80

        # Sample time(second)
        sampleTime = 0.04
        ################################################################################################
        NowEnd = np.eye(4)
        GoalEnd = np.eye(4)
        
        NowEnd = NowEnd @ self.Mat.TransXYZ(Now[0]*self.Unit, Now[1]*self.Unit, Now[2]*self.Unit) @ self.Mat.RotaXYZ(d2r(Now[3]), d2r(Now[4]), d2r(Now[5])) 
        GoalEnd = GoalEnd @ self.Mat.TransXYZ(Goal[0]*self.Unit, Goal[1]*self.Unit, Goal[2]*self.Unit) @ self.Mat.RotaXYZ(d2r(Goal[3]), d2r(Goal[4]), d2r(Goal[5]))

        # 軌跡規劃演算法
        pathData, velData, timeData = self.Plan.MatrixPathPlanning(GoalEnd, NowEnd, alltime, sampleTime)
        # pathData, velData, timeData = self.Plan.MatrixPath434(GoalEnd, NowEnd, alltime, sampleTime)
        # pathData, timeData = self.Plan.MatrixPath_Scurve(GoalEnd, NowEnd, sampleTime)

        # 存入軌跡資料
        # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434.csv"
        filePath = header_filePath + "MatrixPlan_liner.csv"
        self.dB.saveMatrix4x4(pathData, timeData, "w", filePath)

        # 存入速度資料
        # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_velocity.csv"
        filePath = header_filePath + "MatrixPlan_liner_velocity.csv"
        self.dB.saveVelocity(velData, "w", filePath)

        # 載入軌跡資料
        filePath = header_filePath + "MatrixPlan_liner.csv"
        _, pathData_df, pathData_np4x4, pathData_np6x1 = self.dB.LoadMatrix4x4(filePath)

        # 計算逆向運動學
        path_JointAngle = np.zeros((len(pathData_np4x4), 6, 1))
        for i in range(len(path_JointAngle)):
            path_JointAngle[i] = self.Kin.IK_4x4(pathData_np4x4[i], θ_Buffer)
            

        # 儲存關節角度
        filePath = header_filePath + "MatrixPlan_liner_JointAngle.csv"
        # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_JointAngle.csv"
        self.dB.saveJointAngle(path_JointAngle, "w", filePath)

        # 儲存姿態矩陣
        filePath = header_filePath + "MatrixPlan_liner_PoseMatrix.csv"
        # filePath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_PoseMatrix.csv"
        self.dB.savePoseMatrix(pathData_np6x1, "w", filePath)

        return path_JointAngle, pathData_np4x4
        
        """
        現有路徑檔案模擬
        """
        # filePath = "Experimental_data/20240306/Revise/Teach_mode_Multi_Trajectory_welding.csv"
        # rowData = self.dB.Load(filePath)
        # path_Pose = np.zeros((len(rowData), 6))
        # path_4x4 = np.zeros((len(rowData), 4, 4))
        
        # for i in range(len(path_Pose)):
        #     buffer_np = np.zeros((6,1))
        #     buffer_np[0, 0] = rowData['X'][i]
        #     buffer_np[1, 0] = rowData['Y'][i]
        #     buffer_np[2, 0] = rowData['Z'][i]
        #     buffer_np[3, 0] = d2r(rowData['Rx'][i])
        #     buffer_np[4, 0] = d2r(rowData['Ry'][i])
        #     buffer_np[5, 0] = d2r(rowData['Rz'][i])

        #     path_4x4[i] = self.Mat.AngletoMat(buffer_np)
        
        # path_JointAngle = np.zeros((len(rowData), 6, 1))

        # # 計算逆向運動學
        # for i in range(len(rowData)):
        #     path_JointAngle[i] = self.Kin.IK_4x4(path_4x4[i], θ_Buffer)

        # return path_JointAngle, path_4x4

    def main(self):
        path_JointAngle, pathData_np4x4 = self.generateTrajectory()
        self.paitGL(path_JointAngle, pathData_np4x4)

if __name__ == "__main__":
    ctrl = armControl()
    ctrl.main()