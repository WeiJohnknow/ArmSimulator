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

        θ_Buffer = (np.zeros((6,1)))
        θ_Buffer[0, 0] =  d2r(-0.006)
        θ_Buffer[1, 0] =  d2r(-38.8189)
        θ_Buffer[2, 0] =  d2r(-41.0857)
        θ_Buffer[3, 0] =  d2r(-0.0030)
        θ_Buffer[4, 0] =  d2r(-76.4394)
        θ_Buffer[5, 0] =  d2r(1.0687)

   
        NowEnd = np.eye(4)
        GoalEnd = np.eye(4)
        NowEnd = NowEnd @ self.Mat.TransXYZ(485.364*self.Unit,-1.213*self.Unit,234.338*self.Unit) @ self.Mat.RotaXYZ(d2r(179.984), d2r(20.2111), d2r(1.6879)) 
        GoalEnd = GoalEnd @ self.Mat.TransXYZ(955.386*self.Unit,-19.8*self.Unit,z=-75.117*self.Unit) @ self.Mat.RotaXYZ(d2r(-165.2853), d2r(-7.1884), d2r(17.5443))

        alltime = 80
        sampleTime = 0.05

        # 軌跡規劃演算法
        # pathData, timeData = self.Plan.MatrixPathPlanning(GoalEnd, NowEnd, alltime, sampleTime)
        pathData, velData, timeData = self.Plan.MatrixPath434(GoalEnd, NowEnd, alltime, sampleTime)
        # pathData, timeData = self.Plan.MatrixPath_Scurve(GoalEnd, NowEnd, sampleTime)

        # 存入軌跡資料
        filePath = "dataBase/MarPlan.csv"
        self.dB.saveMatrix4x4(pathData, timeData, "w", filePath)

        # 存入速度資料
        filePath = "dataBase/MarPlan_velocity.csv"
        self.dB.saveVelocity(velData, "w", filePath)

        # 載入軌跡資料
        _, pathData_df, pathData_np4x4, pathData_np6x1 = self.dB.LoadMatrix4x4("dataBase/MarPlan.csv")

        # 計算逆向運動學
        path_JointAngle = np.zeros((len(pathData_np4x4), 6, 1))
        for i in range(len(path_JointAngle)):
            path_JointAngle[i] = self.Kin.IK_4x4(pathData_np4x4[i], θ_Buffer)
            

        # 儲存關節角度
        filePath = "dataBase/MarPlan_JointAngle.csv"
        self.dB.saveJointAngle(path_JointAngle, "w", filePath)

        # 儲存姿態矩陣
        filePath = "dataBase/MarPlan_PoseMatrix.csv"
        self.dB.savePoseMatrix(pathData_np6x1, "w", filePath)

        return path_JointAngle, pathData_np4x4

    def main(self):
        path_JointAngle, pathData_np4x4 = self.generateTrajectory()
        self.paitGL(path_JointAngle, pathData_np4x4)

if __name__ == "__main__":
    ctrl = armControl()
    ctrl.main()