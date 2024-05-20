"""
- 版本: 1.0
- 名稱: 速度補償系統(模擬實驗架構)
- 最後使用日期: 20240512
- 問題: 送軌跡之通訊會導致軌跡延遲問題，平均通訊一組，延遲60ms。
- 解決方案:
    1.減少送出的軌跡點數量
    2.配合DX200之系統時間進行補償
"""

# import pygame
# import threading
# import numpy as np
# from MotomanUdpPacket import MotomanUDP
# from Toolbox import TimeTool
# from dataBase_v1 import *
# from Kinematics import Kinematics
# from armControl import Generator
# from SimulatorV2 import Simulator



# class GetNewTrj(threading.Thread):
#     def __init__(self, target, args=()):
#         super().__init__(target=target, args=args)
#         self._result = None

#     def run(self):
#         self._result = self._target(*self._args)

#     def get_result(self):
#         return self._result

# class Motomancontrol():
#     def __init__(self, TrjdatafilePath, VeldatafilePath):
#         """
#         Online(含通訊之測試) >> True  要記得解開self.Udp的相關註解
#         Offline(純邏輯測試) >> False
#         """
#         self.Line = True
#         self.Udp = MotomanUDP()
#         self.Kin = Kinematics()
#         self.Time = TimeTool()
#         self.Sim = Simulator()

        
#         # INFORM 迴圈變數
#         """
#         資料單位:
#         9筆=1批, 2批=1組

#         I0:  資料筆數index
#         I1:  資料組數index
#         I28: 資料組數計數器
#         """
#         self.I0 = 2
#         self.I1 = 0
#         self.I28 = 19

#         if self.Line is True:
#             status = self.Udp.multipleWriteVar(0, 2, [self.I0, self.I1])
#             status = self.Udp.WriteVar("Integer", 28, 0)

#         # 載入軌跡檔案
#         self.Trj = database_PoseMat.Load(TrjdatafilePath)
#         self.Speed = database_Velocity.Load(VeldatafilePath)
        
#         # 載入軌跡時間紀錄檔
#         self.SysTime = database_time.Load("dataBase/dynamicllyPlanTEST/Time_0.csv")
        
#         # 刪除軌跡資料第一筆資料
#         self.Trj = Motomancontrol.deleteFirstData(self.Trj)
#         self.Speed = Motomancontrol.deleteFirstData(self.Speed)
#         self.SysTime = Motomancontrol.deleteFirstData(self.SysTime)

#         # PC >> DX200 通訊紀錄
#         self.communicationRecords_Trj = np.zeros((50000, 9, 6))
#         self.communicationRecords_Speed = np.zeros((50000, 9))
#         self.communicationRecords_Counter = 0

#         # DX200 feedback的手臂資料紀錄
#         self.feedbackRecords_Trj = np.zeros((50000, 1, 6)) 
#         self.feedbackRecords_sysTime = np.zeros((50000, 1))
#         self.feedbackRecords_Trj_ArmSysTime = np.zeros((50000, 1, 7))
#         self.feedbackRecords_Counter = 0

#     @staticmethod
#     def deleteFirstData(Data):
#         """Delete the first data.
#         - Arg: Data(Type: ndarray)
#         - Return : afterProcessData(Type: ndarray)
#         """
#         afterProcessData = Data[1:]
    
#         return afterProcessData
    
#     @staticmethod
#     def CutTrj(copies, Trj, Speed):
#         """由軌跡檔案中取出相應等份的資料點數
#         - Args:
#             copies: 等份數(ex: copies=18，將軌跡資料分成18等份。)
#         """
#         # 將資料分成指定等份
#         indices = np.linspace(0, len(Trj)-1, copies, dtype=int)
#         Trj = Trj[indices]
#         Speed = Speed[indices]

#         return Trj, Speed
    
#     @staticmethod
#     def dataProcessBeforeSent(Trj, Speed):
#         """將資料處理成DX200需要的格式
#         - 處理過程如下: 
#         1. 改變資料形式
#             Pose Matrix: [x, y, z, Rx*10, Ry*10, Rz*10]
#             Speed: [int(2.1254*10)]
#         2. 將資料容器調整為n*9*6的shape
#         """
#         # 處理軌跡資料
#         Trj_copy = np.copy(Trj)
#         Trj_copy[:, :, 3:6]*= 10

#         # 處理速度資料
#         Speed_copy = np.copy(Speed)
#         Speed_copy *= 10
#         Speed_copy = Speed_copy.astype(int)

#         # 一批次>>9筆資料
#         RPdata = Trj_copy.reshape(-1, 9, 6)
#         Veldata = Speed_copy.reshape(-1, 9)

#         return RPdata, Veldata
    
#     @staticmethod
#     def packetRPdataVeldata(RPdata, Veldata, dataCount):
#         """將一批軌跡與速度資料包裝成可發送的形式
#         - Args: RPdata、Veldata、datacount
#             - datacount: 已送出多少批資料的計數器值
#         """
#         RPpacket = {'0':[17, 4, 5, 0, RPdata[dataCount][0][0], RPdata[dataCount][0][1], RPdata[dataCount][0][2], RPdata[dataCount][0][3], RPdata[dataCount][0][4], RPdata[dataCount][0][5]],
#                     '1':[17, 4, 5, 0, RPdata[dataCount][1][0], RPdata[dataCount][1][1], RPdata[dataCount][1][2], RPdata[dataCount][1][3], RPdata[dataCount][1][4], RPdata[dataCount][1][5]],
#                     '2':[17, 4, 5, 0, RPdata[dataCount][2][0], RPdata[dataCount][2][1], RPdata[dataCount][2][2], RPdata[dataCount][2][3], RPdata[dataCount][2][4], RPdata[dataCount][2][5]],
#                     '3':[17, 4, 5, 0, RPdata[dataCount][3][0], RPdata[dataCount][3][1], RPdata[dataCount][3][2], RPdata[dataCount][3][3], RPdata[dataCount][3][4], RPdata[dataCount][3][5]],
#                     '4':[17, 4, 5, 0, RPdata[dataCount][4][0], RPdata[dataCount][4][1], RPdata[dataCount][4][2], RPdata[dataCount][4][3], RPdata[dataCount][4][4], RPdata[dataCount][4][5]],
#                     '5':[17, 4, 5, 0, RPdata[dataCount][5][0], RPdata[dataCount][5][1], RPdata[dataCount][5][2], RPdata[dataCount][5][3], RPdata[dataCount][5][4], RPdata[dataCount][5][5]],
#                     '6':[17, 4, 5, 0, RPdata[dataCount][6][0], RPdata[dataCount][6][1], RPdata[dataCount][6][2], RPdata[dataCount][6][3], RPdata[dataCount][6][4], RPdata[dataCount][6][5]],
#                     '7':[17, 4, 5, 0, RPdata[dataCount][7][0], RPdata[dataCount][7][1], RPdata[dataCount][7][2], RPdata[dataCount][7][3], RPdata[dataCount][7][4], RPdata[dataCount][7][5]],
#                     '8':[17, 4, 5, 0, RPdata[dataCount][8][0], RPdata[dataCount][8][1], RPdata[dataCount][8][2], RPdata[dataCount][8][3], RPdata[dataCount][8][4], RPdata[dataCount][8][5]]}
        
#         Velpacket =[Veldata[dataCount, 0], 
#                     Veldata[dataCount, 1], 
#                     Veldata[dataCount, 2], 
#                     Veldata[dataCount, 3], 
#                     Veldata[dataCount, 4], 
#                     Veldata[dataCount, 5], 
#                     Veldata[dataCount, 6], 
#                     Veldata[dataCount, 7], 
#                     Veldata[dataCount, 8]]
        

#         return RPpacket, Velpacket
    
    
#     def writeRPvarINTvar(self, firstAddress, number, RPpacket, Velpacket):
#         """Write multiple variable data
#         - Args: RPdata, Veldata
#         """
#         Is_success = False
        
#         if self.Line is True:
#             RPstatus = self.Udp.multipleWriteRPVar(firstAddress, number, RPpacket)       
#             Istatus = self.Udp.multipleWriteVar(firstAddress, number, Velpacket)
                
            
#         else:
#             # 靜態測試的模擬訊號
#             RPstatus = []
#             Istatus =[]

#         if RPstatus == [] and Istatus == []:
#             Is_success = True
#         else:
#             Is_success = False
        
#         return Is_success
    
#     def feedbackRecords(self, ArmEndEffector, ArmSysTime):
#         """由機器手臂反饋回PC的數據紀錄
#         """
#         # 儲存實際軌跡資料
#         self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([ArmEndEffector])
#         self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = ArmSysTime
#         ArmEndEffectorAndSysTime = [ArmEndEffector[0], ArmEndEffector[1], ArmEndEffector[2], ArmEndEffector[3], ArmEndEffector[4], ArmEndEffector[5], ArmSysTime]
#         self.feedbackRecords_Trj_ArmSysTime[self.feedbackRecords_Counter] = np.array([ArmEndEffectorAndSysTime])
#         self.feedbackRecords_Counter += 1

#     def communicationRecords(self, RPdata, Veldata, alreadySent_DataBatchNBR):
#         """通訊時用於紀錄通訊內容
#         """
#         # 紀錄通訊所傳輸的資料
#         self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySent_DataBatchNBR]
#         self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySent_DataBatchNBR]
#         self.communicationRecords_Counter += 1

    
#     def readSysTime(self, ArmSysStartTime_second):
#         """讀取DX200系統時間
#         """
#         beforeReadSysTime = self.Time.ReadNowTime()
#         # 讀取系統時間
#         hours, minutes, seconds, totalSecond = self.Udp.getSysTime()

#         afterReadSysTime = self.Time.ReadNowTime()
#         communicationCostTime = self.Time.TimeError(beforeReadSysTime, afterReadSysTime)
#         # TODO 扣除讀取系統時間所花費的通訊時間
#         # communicationCostTime_ms = ArmSysTime["millisecond"]
#         # communicationCostTime_ms -= communicationCostTime

#         # 計算從開始到現在經過的時間
#         elapsedTime = totalSecond - ArmSysStartTime_second

#         return elapsedTime

#     def judgmentTrj(self, eucDisThreshold):
#         """判斷軌跡情況 | 超前 or 落後
#         - Arg:
#             eucDisThreshold: 軌跡超前與落後之判斷閥值(歐式距離)
#         - Return:
#             compenseFlag: 軌跡狀態旗標
#                 True : 需補償
#                 False: 無須補償
#         """
#         feedbackTrjAndTime = self.feedbackRecords_Trj_ArmSysTime[self.feedbackRecords_Counter-1]
#         # 現在位置(不含姿態)
#         feedbackNowPos = feedbackTrjAndTime[0, :3]
#         feedbackTime = feedbackTrjAndTime[-1, -1]
#         print(f"最新DX200系統時間{feedbackTime}s")

#         # 期望系統時間與回饋系統時間比較
#         SysTime = pd.read_csv("dataBase/dynamicllyPlanTEST/Time_0.csv")
#         closestData, closestIndex = dataOperating.searchSimilar(SysTime, feedbackTime)
#         # 此時期望軌跡需到達的位置
#         if closestIndex == 0:
#             closestIndex = 1
#         expectNowPos = self.Trj[closestIndex-1][:3]
#         # 利用理想軌跡的已移動距離 與 現實軌跡的已移動距離 進行比較
#         expectMoveDis = np.linalg.norm(expectNowPos - self.Trj[0][:3])
#         realMoveDis = np.linalg.norm(feedbackNowPos - self.feedbackRecords_Trj_ArmSysTime[0, 0, :3])

#         # 剩餘的軌跡時間 = 理想的軌跡總時間 - 現在實際經過的系統時間
#         timeLeft = self.SysTime[-1] - feedbackTime

#         compenseFlag = False
        
#         if expectMoveDis-realMoveDis > eucDisThreshold:
#             print(f"軌跡落後:{realMoveDis}mm, 需提升軌跡速度")
#             compenseFlag = True

#         elif expectMoveDis-realMoveDis < -eucDisThreshold:
#             print(f"軌跡超前:{realMoveDis}mm, 需降低軌跡速度")
#             compenseFlag = True
            
#         else:
#             print(f"補償系統不做動")
            
#         return compenseFlag, timeLeft
    
#     def PlanCompenseTrj(self, NowEnd, GoalEnd, sampleTime, totalTime):
#         beforePlan = self.Time.ReadNowTime()

#         # 創造新軌跡
#         HomogeneousMatData, PoseMatData, SpeedData, TimeData = Generator.generateTrajectory_totalTime(NowEnd, GoalEnd, sampleTime, totalTime)
        
#         afterPlan = self.Time.ReadNowTime()
#         err = self.Time.TimeError(beforePlan, afterPlan)
#         print("計算新軌跡所花費的總時間: ", err["millisecond"], "ms")
#         costTime_PlanTrj = err["millisecond"]

#         return HomogeneousMatData, PoseMatData, SpeedData, TimeData, costTime_PlanTrj
    
#     def main(self):

#         # 紀錄UDP目前已送出的資料批次數(1批 = 9筆)
#         alreadySent_DataBatchNBR = 0

#         # 軌跡補償次數
#         compenseTrjNBR = 0

#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0
#         startTime = 0
#         startNode = 0
#         ArmSysStartTime = 0
#         # 取樣時間
#         sampleTime = 0.04
#         # 系統時間初始化flag
#         sysflag = True

#         # 要傳送給DX200的軌跡點數量(目前有18個Robot Position variable可以使用)
#         copies = 18
#         # 切割軌跡為18個點
#         Trj, Speed = Motomancontrol.CutTrj(copies, self.Trj, self.Speed)
#         # 資料處理
#         RPdata, Veldata = Motomancontrol.dataProcessBeforeSent(Trj, Speed)

#         # 包裝、傳送所有軌跡點
#         firstAddress = 2
#         number = 9
#         for i in range(copies//9):
#             # 包裝n筆資料  
#             RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
#             # 傳送n筆資料
#             Is_success = self.writeRPvarINTvar(firstAddress, number, RPpacket, Velpacket)
#             # 紀錄通訊所送出的軌跡資料 | 用於驗證
#             self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR)
#             # 資料(批次)計數器更新
#             alreadySent_DataBatchNBR += 1

#             firstAddress+=number


#         # 主迴圈旗標 | 開關
#         mainLoop = False
#         while True:
#             if self.Line is True:
#                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                 if np.linalg.norm(np.array(coordinate) - self.Trj[0, 0]) <= 0.05:
#                     print("------------------------------實測實驗開始------------------------------")
#                     print(f"軌跡開始位置: {coordinate}")
#                     mainLoop = True
#                     break
#             else:
#                 print("------------------------------模擬實驗開始------------------------------")
#                 mainLoop = True
#                 break

#         while mainLoop:
#             # -----------------------此區在本迴圈只會在剛進迴圈時執行一次-------------------
#             if sysflag is True:
#                 # 儲存系統開始時間
#                 startTime = self.Time.ReadNowTime()

#                 if self.Line is True:
#                     # 紀錄feedback數據 | 紀錄初始位置與系統時間
#                     pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                     # 取得DX200初始系統時間
#                     hours, minutes, seconds, totalSecond = self.Udp.getSysTime()
#                     ArmSysStartTime = totalSecond
#                     self.feedbackRecords(coordinate, 0)
#                 else:
#                     I0 = [3]
#                 sysflag = False

#             # ---------------------------------------------------------------------------
#             else:
#                 # 更新每禎時間
#                 nowTime = self.Time.ReadNowTime()
#                 # 更新系統時間
#                 sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                 sysTime = round(sysTime/1000, 1)
#                 """
#                 1.讀取位置、系統時間
#                 2.比對期望的位置時間表
#                 3.判斷 有落後>>補償 | 沒落後>>繼續執行
#                 4.判斷是否結束執行
#                 """
                
#                 # 讀取實際手臂位置
#                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                 # 讀取DX200系統時間
#                 # TODO 需回扣讀取系統時間所消耗的通訊時間
#                 ArmSysTime = self.readSysTime(ArmSysStartTime)
#                 self.feedbackRecords(coordinate, sysTime)

#                 # 判斷是否需要速度補償
#                 eucDisThreshold = 0.2
#                 compenseFlag, timeLeft = self.judgmentTrj(eucDisThreshold)

#                 # if compenseFlag is True:
#                 #     # 取得剩餘時間 | 剩餘多少時間需要將此軌跡跑完
#                 #     # 利用矩陣軌跡法(時間版本)規劃新軌跡
#                 #     # 進行通訊前的資料處理
#                 #     # 以I000判斷實際軌跡走到哪一部分
#                 #     # 更新尚未走到的軌跡點
                
#                 #     totalTime = timeLeft
#                 #     sampleTime = 0.04
#                 #     I0 = self.Udp.ReadVar("Integer", 0)
#                 #     NowEnd = self.Trj[I0+1]
#                 #     GoalEnd = self.Trj[-1]

#                 #     # 執行緒
#                 #     compenseThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, totalTime))
#                 #     compenseThread.start()

#                 # if compenseThread.is_alive() is False:
#                 #     # 軌跡已變化一次，需更新計數器值
#                 #     compenseTrjNBR += 1
#                 #     result = compenseThread.get_result()
                    
#                 #     NewHomogeneousMat = result[0]
#                 #     NewPoseMatData = result[1]
#                 #     NewSpeedData = result[2]
#                 #     NewTimeData = result[3]
#                 #     costTime_PlanTrj = result[4]

#                 #     # 存檔(新軌跡資料) 
#                 #     mode = "w"
#                 #     database_HomogeneousMat.Save(NewHomogeneousMat, f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{compenseTrjNBR}.csv", mode)
#                 #     database_PoseMat.Save(NewPoseMatData, f"dataBase/dynamicllyPlanTEST/PoseMat_{compenseTrjNBR}.csv", mode)
#                 #     database_Velocity.Save(NewSpeedData, f"dataBase/dynamicllyPlanTEST/Speed_{compenseTrjNBR}.csv", mode)
#                 #     database_time.Save(NewTimeData,f"dataBase/dynamicllyPlanTEST/Time_{compenseTrjNBR}.csv", mode)

#                 #     # 要傳送給DX200的軌跡點數量
#                 #     I0 = self.Udp.ReadVar("Integer", 0)
#                 #     copies = 18-I0
#                 #     # 切割軌跡為copies個點
#                 #     self.Trj, self.Speed = Motomancontrol.CutTrj(copies, NewPoseMatData, NewSpeedData)
#                 #     # 資料處理
#                 #     RPdata, Veldata = Motomancontrol.dataProcessBeforeSent(self.Trj, self.Speed)

#                 #     # TODO 此區尚未完成
#                 #     # 包裝、傳送所有軌跡點
#                 #     firstAddress = 2
#                 #     number = 9
#                 #     for i in range(copies//9):
#                 #         # 包裝n筆資料  
#                 #         RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
#                 #         # 傳送n筆資料
#                 #         Is_success = self.writeRPvarINTvar(firstAddress, number, RPpacket, Velpacket)
#                 #         # 紀錄通訊所送出的軌跡資料 | 用於驗證
#                 #         self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR)
#                 #         # 資料(批次)計數器更新
#                 #         alreadySent_DataBatchNBR += 1

#                 #         firstAddress+=number
                
#                 # 結束
#                 if np.linalg.norm(self.Trj[-1, 0, :3]- np.array(coordinate)[:3]) < 0.1:
#                     mode = "w"
#                     # feedback的軌跡資料
#                     # 濾除整個row為0的部分
#                     non_zero_rows_Trajectory = np.any(self.feedbackRecords_Trj != 0, axis=(1, 2))
#                     non_zero_rows_Time = np.any(self.feedbackRecords_sysTime != 0, axis=1)
#                     non_zero_rows_PoseMat_Time = np.any(self.feedbackRecords_Trj_ArmSysTime != 0, axis=(1, 2))
#                     # 系統時間需保留初值0
#                     non_zero_rows_Time[:200] = True

#                     self.feedbackRecords_Trj = self.feedbackRecords_Trj[non_zero_rows_Trajectory]
#                     self.feedbackRecords_sysTime = self.feedbackRecords_sysTime[non_zero_rows_Time]
#                     self.feedbackRecords_Trj_ArmSysTime = self.feedbackRecords_Trj_ArmSysTime[non_zero_rows_PoseMat_Time]

#                     database_PoseMat.Save(self.feedbackRecords_Trj, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj.csv", mode)
#                     database_time.Save(self.feedbackRecords_sysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_sysTime.csv", mode)
#                     database_time.Save_PoseMat_Time(self.feedbackRecords_Trj_ArmSysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj_ArmSysTime.csv",mode)
                    
#                     # 儲存通訊所送出的軌跡資料
#                     self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
#                     self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
#                     # 濾除整個row為0的部分
#                     non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
#                     non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
                    

#                     self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
#                     self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
                    
                    
#                     database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
#                     database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
#                     print("------------------------------結束-----------------------------------")
#                     print(f"軌跡總花費時間: {sysTime}")
#                     break
                
# if __name__ == "__main__":
#     trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
#     speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
#     Motomancontrol(trjdataPath, speeddataPath).main()


"""
- 版本: 0.0
- 名稱: 動態軌跡規劃與通訊架構(模擬實驗架構)
- 最後使用日期: 20240512
- 問題: 送軌跡之通訊會導致軌跡延遲問題，平均通訊一組，延遲60ms。
- 解決方案:
    1.減少送出的軌跡點數量
    2.配合DX200之系統時間進行補償
"""
import pygame
import math
import threading
import numpy as np
from MotomanUdpPacket import MotomanUDP
from Toolbox import TimeTool
from dataBase_v1 import *
from Kinematics import Kinematics
from armControl import Generator
from SimulatorV2 import Simulator
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, QThread
from communctionThread import *


class GetNewTrj(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = None

    def run(self):
        self._result = self._target(*self._args)

    def get_result(self):
        return self._result

class Motomancontrol():
    def __init__(self, TrjdatafilePath, VeldatafilePath):
        """
        Online(含通訊之測試) >> True  要記得解開self.Udp的相關註解
        Offline(純邏輯測試) >> False
        """
        self.Line = False
        self.Udp = MotomanUDP()
        
        self.Kin = Kinematics()
        self.Time = TimeTool()
        self.Sim = Simulator()

        
        # INFORM 迴圈變數
        """
        資料單位:
        9筆=1批, 2批=1組

        I0:  資料筆數index
        I1:  資料組數index
        I28: 資料組數計數器
        """
        self.I0 = 2
        self.I1 = 0
        self.I28 = 0

        if self.Line is True:
            status = self.Udp.multipleWriteVar(0, 2, [self.I0, self.I1])
            status = self.Udp.WriteVar("Integer", 28, 0)


        # 動態變更銲接參數預設值
        """
        AC:   I21
        AVP : I22
        """
        self.AC = 40
        self.AVP = 50
        if self.Line is True:
            status = self.Udp.multipleWriteVar(21, 2, [self.AC, self.AVP])

        # 載入軌跡檔案
        self.trjData = database_PoseMat.Load(TrjdatafilePath)
        self.velData = database_Velocity.Load(VeldatafilePath)
        # 刪除軌跡資料第一筆資料
        self.trjData, self.velData = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)

        # PC >> DX200 通訊紀錄
        self.communicationRecords_Trj = np.zeros((50000, 9, 6))
        self.communicationRecords_Speed = np.zeros((50000, 9))
        self.communicationRecords_Counter = 0

        # DX200 feedback的手臂資料紀錄
        self.feedbackRecords_Trj = np.zeros((50000, 1, 6)) 
        self.feedbackRecords_sysTime = np.zeros((50000, 1))
        self.feedbackRecords_Counter = 0

        # 規劃新軌跡 各工作階段所花費的時間
        """
        Cost Time = ["Trj_Algorithm", "Data_merge", "IK_Iterate"]
        """
        self.costTime = np.zeros((100, 3))
        self.costTimeDataCounter = 0

        # I0驗證系統
        """
        I0、PrvUpdataTime、SysTime :[I0, PrvUpdataTime, SysTime]
        """
        self.I0AndPrvUpdataTimeAndSysTime = np.zeros((50000, 6))
        self.I0AndPrvUpdataTimeAndSysTimeCounter = 0
        
        self.WriteSpeedBypass = 0

        
    @staticmethod
    def deleteFirstTrajectoryData(TrajectoryData, VelocityData):
        """Delete the first data.
        """
        TrajectoryData = TrajectoryData[1:]
        VelocityData = VelocityData[1:]
        
        return TrajectoryData, VelocityData
    
    def changeWeldingPartmeter(self, AC, AVP):
        """Dynamically change welding parameters.
        - Args: AC、AVP
        - Return: cmd_Status
        """
        
        # DX200 variable(Integer) settings
        # AC:   I21
        # AVP : I22

        firstAddress = 21
        number = 2
        IData =[AC, AVP]

        if self.Line is True:
            Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
        
    def calculateDataGroupBatch(self, TrajectoryData):
        """Calculate data segmentation groups and batches.
        Group: 組數 (About: I001)
        Batch: 批次 (About: I000)
        
        - Args: Trajectory data
        - Return: Number of data groups , Number of data batches
        """
        # Calculate batch(About: I000)
        quotient_batch, remainder_batch = divmod(TrajectoryData.shape[0], 9)
        if remainder_batch != 0:
            # 餘數不等於0，表示原始資料分批(9筆為1批)時，最後一批不足9筆，故要+1批並做填充
            batch = quotient_batch + 1
        else:
            batch = quotient_batch

        # 修改DX200變數暫存器值
        if self.Line is True:
            print("INFORM程式 I001: ", batch)
            status = self.Udp.WriteVar("Integer", 1, batch)
        
        return batch
    
    def dataSegmentation(self, trajectoryData, velocityData, batch):
        """
        資料分批處理
        單位: 9筆/批
        """
        
        """資料分割演算法
        1.判斷原資料(m*1*6)是否可完整切個為shape(n*9*6), m=該資料原本的筆數; n= m/9.
        2.若第一步中發現有不足9筆需要補齊資料，使用最後一筆資料補齊剩下的缺口.
        3.補齊後，將資料切割為(n*9*6).
        """

        # 軌跡資料處理與分割
        # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
        quotient_trj, remainder_trj = divmod(trajectoryData.shape[0], 9)
        if remainder_trj != 0:
            # 讀取最後一個Row的數據
            last_row = trajectoryData[-1]

            # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
            padding = np.tile(last_row, (9 - remainder_trj, 1, 1))

            # 將需要填充的Row與原資料進行(Row堆疊)
            padded_array = np.vstack((trajectoryData, padding))

            # 將資料分割成以批次(一批次有9筆資料)為單位
            reshaped_trajectoryData = padded_array.reshape(batch, 9, 6)
        else:
            # 將資料分割成以批次(一批次有9筆資料)為單位
            reshaped_trajectoryData = trajectoryData.reshape(batch, 9, 6)

        # 将第4、5、6列的值都乘以10
        reshaped_trajectoryData[:, :, 3:6]*= 10
        # 完成初步分割與封裝後的軌跡資料
        RPdata = reshaped_trajectoryData



        # 軌跡資料處理與分割(速度)
        # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
        quotient_vel, remainder_vel = divmod(velocityData.shape[0], 9)
        if remainder_vel != 0:
            # 讀取最後一個Row的數據
            last_row = velocityData[-1]

            # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
            padding = np.tile(last_row, (9 - remainder_vel, 1))

            # 將需要填充的Row與原資料進行(Row堆疊)
            padded_array = np.vstack((velocityData, padding))

            # 將資料分割成以批次(一批次有9筆資料)為單位
            reshaped_velocityData = padded_array.reshape(batch, 9)
        else:
            # 將資料分割成以批次(一批次有9筆資料)為單位
            reshaped_velocityData = velocityData.reshape(batch, 9)

        # 將所有值都乘以10(DX200的速度指令只接受整數，送入後會將數值自動*0.1，故發送前須將數值都乘以10)
        reshaped_velocityData *= 10
        Veldata = reshaped_velocityData

        # 完成初步分割與封裝後的軌跡(速度)資料
        Veldata = Veldata.astype(int)
    
        return RPdata, Veldata
    
    @staticmethod
    def packetRPdataVeldata(RPdata, Veldata, dataCount):
        """將一批軌跡與速度資料包裝成可發送的形式
        - Args: RPdata、Veldata、datacount
            - datacount: 已送出多少批資料的計數器值
        """
        RPpacket = {'0':[17, 4, 5, 0, RPdata[dataCount][0][0], RPdata[dataCount][0][1], RPdata[dataCount][0][2], RPdata[dataCount][0][3], RPdata[dataCount][0][4], RPdata[dataCount][0][5]],
                    '1':[17, 4, 5, 0, RPdata[dataCount][1][0], RPdata[dataCount][1][1], RPdata[dataCount][1][2], RPdata[dataCount][1][3], RPdata[dataCount][1][4], RPdata[dataCount][1][5]],
                    '2':[17, 4, 5, 0, RPdata[dataCount][2][0], RPdata[dataCount][2][1], RPdata[dataCount][2][2], RPdata[dataCount][2][3], RPdata[dataCount][2][4], RPdata[dataCount][2][5]],
                    '3':[17, 4, 5, 0, RPdata[dataCount][3][0], RPdata[dataCount][3][1], RPdata[dataCount][3][2], RPdata[dataCount][3][3], RPdata[dataCount][3][4], RPdata[dataCount][3][5]],
                    '4':[17, 4, 5, 0, RPdata[dataCount][4][0], RPdata[dataCount][4][1], RPdata[dataCount][4][2], RPdata[dataCount][4][3], RPdata[dataCount][4][4], RPdata[dataCount][4][5]],
                    '5':[17, 4, 5, 0, RPdata[dataCount][5][0], RPdata[dataCount][5][1], RPdata[dataCount][5][2], RPdata[dataCount][5][3], RPdata[dataCount][5][4], RPdata[dataCount][5][5]],
                    '6':[17, 4, 5, 0, RPdata[dataCount][6][0], RPdata[dataCount][6][1], RPdata[dataCount][6][2], RPdata[dataCount][6][3], RPdata[dataCount][6][4], RPdata[dataCount][6][5]],
                    '7':[17, 4, 5, 0, RPdata[dataCount][7][0], RPdata[dataCount][7][1], RPdata[dataCount][7][2], RPdata[dataCount][7][3], RPdata[dataCount][7][4], RPdata[dataCount][7][5]],
                    '8':[17, 4, 5, 0, RPdata[dataCount][8][0], RPdata[dataCount][8][1], RPdata[dataCount][8][2], RPdata[dataCount][8][3], RPdata[dataCount][8][4], RPdata[dataCount][8][5]]}
        
        Velpacket =[Veldata[dataCount, 0], 
                    Veldata[dataCount, 1], 
                    Veldata[dataCount, 2], 
                    Veldata[dataCount, 3], 
                    Veldata[dataCount, 4], 
                    Veldata[dataCount, 5], 
                    Veldata[dataCount, 6], 
                    Veldata[dataCount, 7], 
                    Veldata[dataCount, 8]]
        

        return RPpacket, Velpacket
    
    
    def writeRPvarINTvar(self, firstAddress, RPpacket, Velpacket):
        """Write multiple variable data
        - Args: RPdata, Veldata
        """
        Is_success = False
        
        if self.Line is True:
            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
            if self.WriteSpeedBypass >= 2:
                Istatus = []
                pass
            else:
                Istatus = self.Udp.multipleWriteVar(firstAddress, 9, Velpacket)
                self.WriteSpeedBypass += 1
            
        else:
            # 靜態測試的模擬訊號
            RPstatus = []
            Istatus =[]

        if RPstatus == [] and Istatus == []:
            Is_success = True
        else:
            Is_success = False
        
        return Is_success
    
    
    def PlanNewTrj(self, NowEnd, GoalEnd, sampleTime, GoalSpeed):
        """規劃新軌跡，時間線沿用舊軌跡
        目的: 產生新軌跡, 並即時傳輸。
        """
        b = self.Time.ReadNowTime()

        # 創造新軌跡
        HomogeneousMatData, PoseMatData, SpeedData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, GoalSpeed)
        
        a = self.Time.ReadNowTime()
        err = self.Time.TimeError(b, a)
        print("計算新軌跡所花費的總時間: ", err["millisecond"], "ms")
        costTime_PlanTrj = err["millisecond"]

        return HomogeneousMatData, PoseMatData, SpeedData, TimeData, costTime_PlanTrj
    
    def simulation(self, trjUpdataNBR):
        d2r = np.deg2rad
        b = self.Time.ReadNowTime()
        newHomogeneousMat = database_HomogeneousMat.Load(f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{trjUpdataNBR}.csv")
        nowJointAngle = (np.zeros((6,1)))
        nowJointAngle[0, 0] =  d2r(-0.006)
        nowJointAngle[1, 0] =  d2r(-38.8189)
        nowJointAngle[2, 0] =  d2r(-41.0857)
        nowJointAngle[3, 0] =  d2r(-0.0030)
        nowJointAngle[4, 0] =  d2r(-76.4394)
        nowJointAngle[5, 0] =  d2r(1.0687)
        JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, newHomogeneousMat)
        a = self.Time.ReadNowTime()
        err = self.Time.TimeError(b, a)
        print("關節角度計算所消耗的總時間: ", err["millisecond"], "ms")
        database_JointAngle.Save(JointAngleData, f"dataBase/dynamicllyPlanTEST/JointAngle_{trjUpdataNBR}.csv", "w")
        # self.Sim.paitGL(JointAngleData, newHomogeneousMat)


    def feedbackRecords(self, sysTime):
        """由機器手臂反饋回PC的數據紀錄
        """
        # 讀取實際手臂位置
        pos_result, coordinate = self.Udp.getcoordinateMH(101)
        # 儲存實際軌跡資料
        self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([coordinate])
        self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = sysTime
        self.feedbackRecords_Counter += 1
        
    
    def communicationRecords(self, RPdata, Veldata, alreadySent_DataBatchNBR, batch):
        """通訊時用於紀錄通訊內容
        """
        # 紀錄通訊所傳輸的資料
        if alreadySent_DataBatchNBR > batch-1:
            pass
        else:    
            self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySent_DataBatchNBR]
            self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySent_DataBatchNBR]
        self.communicationRecords_Counter += 1

    def main(self):
        #---------------------------------------------Inital-----------------------------------------------
        # 初始化Pygame
        pygame.init()

        # 設置畫面寬高
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        # 紀錄UDP目前已送出的資料批次數(1批 = 9筆)
        alreadySent_DataBatchNBR = 0
        # 系統時間與軌跡節點
        sysTime, Node = 0, 0
        startNode = 0
        # 取樣時間
        sampleTime = 0.04
        # 系統時間初始化flag
        sysflag = True
        # 變軌跡次數
        trjUpdataNBR = 0
        Prv_trjUpdataNBR = 0
        
        # 計算資料分割的組數與批數
        batch = self.calculateDataGroupBatch(self.trjData)
        
        # 資料分割
        RPdata, Veldata = self.dataSegmentation(self.trjData, self.velData, batch)
        
        # 包裝並寫入首9筆資料   
        RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
        Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
        # 紀錄通訊所送出的軌跡資料 | 用於驗證
        self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR, batch)
        # 資料(批次)計數器更新
        alreadySent_DataBatchNBR += 1
        
        
        
        # 軌跡規劃執行緒
        Thread_started = False
        planThread = GetNewTrj(target=self.PlanNewTrj)

        # 軌跡資料儲存容器(驗證資料)
        
        #-------------------------------------------------------------------------------------------------
        
        # 測試通訊資料批次數
        I3count = 0
        I11count = 0
        feedback_count = 0

        # 更新位置變數時的時間點
        updataTrjTime = self.Time.ReadNowTime()

        # 時間限制
        timeLimit = 100

        # 互鎖
        I2Lock = False
        I11Lock = False

        # 主迴圈旗標 | 開關
        mainLoop = False
        while True:
            if self.Line is True:
                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                if np.linalg.norm(np.array(coordinate) - self.trjData[0, 0]) <= 0.05:
                    print("------------------------------實測實驗開始------------------------------")
                    print(f"軌跡開始位置: {coordinate}")
                    mainLoop = True
                    break
            else:
                print("------------------------------模擬實驗開始------------------------------")
                mainLoop = True
                break
        
        while mainLoop:
            singlelooptime1 = self.Time.ReadNowTime()
            # 更新每禎時間
            nowTime = self.Time.ReadNowTime()
            
            if sysflag is True:
                """
                此區在本迴圈只會在剛進迴圈時執行一次
                """
                # 儲存系統開始時間
                startTime = self.Time.ReadNowTime()

                
                if self.Line is True:
                    # 取得I0初值
                    # I0 = self.Udp.ReadVar("Integer", 0)
                    I0 = [2]
                    # 起始變數位置
                    firstAddress = 11
                    # 打包需要傳送的變數資料
                    RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
                    # 將打包完的資料寫入DX200
                    Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR, batch)
                    # 資料(批次)計數器更新
                    alreadySent_DataBatchNBR += 1

                    I11count+=1
                    
                    # 紀錄feedback數據 | 紀錄初始位置與系統時間
                    self.feedbackRecords(0)
                else:
                    I0 = [3]

                sysflag = False
            
            else:
                # 更新系統時間
                
                sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
                sysTime = round(sysTime/1000, 1)
                
                #----------------------------------------------命令執行區-----------------------------------------            
                if self.Line is True:
                    # 更新距離上次更新軌跡時，又經過多久的時間
                    b = self.Time.ReadNowTime()
                    timeLeft = self.Time.TimeError(updataTrjTime, b)
                    timeLeft_ms = timeLeft["millisecond"]
                    print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取I0處")

                    
                    I2Lock = True
                    I11Lock = True

                    Prv_I0 = I0
                    I0 = self.Udp.ReadVar("Integer", 0)
                    # 將I0、PrvUpdataTime、SysTimer記錄下來
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 0] = I0[0]
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 1] = timeLeft_ms
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 2] = sysTime
                    
                    print(f"I000 : {I0}")
                    """
                    防止重複
                    """
                    if Prv_I0 != I0 and I0 >= [2] and I0 <= [10]:
                        I2Lock = True
                        # print(f"I0: {I0}，允許寫入I11-I19")
                    elif Prv_I0 != I0 and I0 >= [11] and I0 <= [19]:
                        I11Lock = True
                        # print(f"I0: {I0}，允許寫入I02-I10")
                    else:
                        pass
                    print(f"上次的I0與本次I0相同，不允許寫入。")

                    """
                    計算更新時間
                    """
                    # if timeLeft_ms <= timeLimit:
                    #     I0 = self.Udp.ReadVar("Integer", 0)
                    #     print(f"I000 : {I0}")

                    # elif timeLeft_ms > timeLimit :
                        
                    #     if I0 >= [2] and I0 <= [10]:
                    #         I0 = [11]
                    #         print("已鄰近下次需要更新軌跡的時間，強制將I000變更為11。")
                    #     elif I0 >= [11] and I0 <= [19]:
                    #         I0 = [2]
                    #         print("已鄰近下次需要更新軌跡的時間，強制將I000變更為2。")

                    # else:
                    #     pass

                    

                else:
                    # 模擬I0變換
                    if I0 == [11]:
                        I0 = [3]
                    elif I0 == [3]:
                        I0 = [11]

                    
                #----------------------------------------------資料通訊區-----------------------------------------
                """
                通訊
                * 變數區間:
                1. I02 - I10
                2. I11 - I19
                """
                
                if I0 == [2] and I2Lock is True:
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 3] = sysTime
                    
                    I2_b = self.Time.ReadNowTime()

                    # 起始變數位置
                    firstAddress = 11
                    # 打包需要傳送的變數資料
                    RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
                    # 將打包完的資料寫入DX200
                    Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR, batch)
                    # 資料(批次)計數器更新
                    alreadySent_DataBatchNBR += 1

                    if self.Line is False:
                        # 模擬軌跡時間
                        self.Time.time_sleep(0.36)

                    I2_a = self.Time.ReadNowTime()
                    I2err = self.Time.TimeError(I2_b, I2_a)
                    I2err_ms = I2err["millisecond"]
                    print(f"更新I11-I20的軌跡資料花費時間: {I2err_ms}ms")

                    # 紀錄送軌跡所花費的時間與變數區間
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 4] = I2err_ms
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 5] = 2
                    self.I0AndPrvUpdataTimeAndSysTimeCounter += 1

                    # 紀錄軌跡更新時間
                    updataTrjTime = self.Time.ReadNowTime()

                    I11count+=1
                    I2Lock = False
                    

                elif I0 == [11] and I11Lock is True:
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 3] = sysTime
                    I11_b = self.Time.ReadNowTime()

                    # 起始變數位置
                    firstAddress = 2
                    # 打包需要傳送的變數資料
                    RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
                    # 將打包完的資料寫入DX200
                    Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR, batch)
                    # 資料(批次)計數器更新
                    alreadySent_DataBatchNBR += 1

                    if self.Line is False:
                        # 模擬軌跡時間
                        self.Time.time_sleep(0.36)
                        
                    I11_a = self.Time.ReadNowTime()
                    I11_err = self.Time.TimeError(I11_b, I11_a)
                    I11_err_ms = I11_err["millisecond"]
                    print(f"更新I02-I10的軌跡資料花費時間: {I11_err_ms}ms")

                    # 紀錄送軌跡所花費的時間與變數區間
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 4] = I11_err_ms
                    self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 5] = 1
                    self.I0AndPrvUpdataTimeAndSysTimeCounter += 1

                    # 紀錄軌跡更新時間
                    updataTrjTime = self.Time.ReadNowTime()

                    I3count+=1
                    I11Lock = False

                else:
                    self.I0AndPrvUpdataTimeAndSysTimeCounter += 1
                    # if self.Line is True:
                    #     # 更新距離上次更新軌跡時，又經過多久的時間
                    #     b = self.Time.ReadNowTime()
                    #     timeLeft = self.Time.TimeError(updataTrjTime, b)
                    #     timeLeft_ms = timeLeft["millisecond"]
                    #     print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取feedback資料處")
                    #     # 紀錄feedback數據
                    #     self.feedbackRecords(sysTime)
                    #     feedback_count+=1

                    #     if timeLeft_ms <= timeLimit:
                    #         # 紀錄feedback數據
                    #         self.feedbackRecords(sysTime)
                    #         feedback_count+=1
                    #         print(f"feedback寫入次數: {feedback_count}次")
                    #     elif timeLeft_ms > timeLimit :
                    #         print("已鄰近下次需要更新軌跡的時間，略過讀取feedback數據動作。")
                    #         pass
                        
                    #     else:
                    #         pass
                   
                
                if alreadySent_DataBatchNBR == batch:
                    """結束條件
                    外迴圈數 = 批次數
                    """
                
                    # -------------------------------------通訊資紀錄與feedback紀錄 | 處理與存檔-----------------------------------
                    # 讀取最後一刻軌跡資料       
                    if self.Line is True:
                        can_End = False
                        while True:
                            # 讀取I000變數
                            I0 = self.Udp.ReadVar("Integer", 0)

                            # 更新系統時間
                            nowTime = self.Time.ReadNowTime()
                            # 取得系統時間
                            sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
                            sysTime = round(sysTime/1000, 1)

                            # 紀錄feedback數據
                            self.feedbackRecords(sysTime)
                            feedback_count+=1
                            print(f"feedback寫入次數: {feedback_count}次")

                            # 判斷此筆軌跡資料的I0會停留在I0=11還是I0=2
                            quotient, remainder = divmod(RPdata.shape[0]*RPdata.shape[1], 18)
                            
                            if remainder == 9 and I0 == [11]:
                                can_End = True
                            elif remainder == 0 and I0 == [2]:
                                can_End = True
                            else: 
                                can_End = False
                                
                            if can_End is True:
                                # feedback的軌跡資料
                                # 濾除整個row為0的部分
                                non_zero_rows_Trajectory = np.any(self.feedbackRecords_Trj != 0, axis=(1, 2))
                                non_zero_rows_Time = np.any(self.feedbackRecords_sysTime != 0, axis=1)
                                # 系統時間需保留初值0
                                non_zero_rows_Time[:2] = True

                                self.feedbackRecords_Trj = self.feedbackRecords_Trj[non_zero_rows_Trajectory]
                                self.feedbackRecords_sysTime = self.feedbackRecords_sysTime[non_zero_rows_Time]
                                
                                database_PoseMat.Save(self.feedbackRecords_Trj, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj.csv", "w")
                                database_time.Save(self.feedbackRecords_sysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_sysTime.csv", "w")
                                
                                # 儲存通訊所送出的軌跡資料
                                self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
                                self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
                                # 濾除整個row為0的部分
                                non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
                                non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
                                non_zero_rows_costTime = np.any(self.costTime != 0, axis=1)

                                self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
                                self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
                                self.costTime = self.costTime[non_zero_rows_costTime]
                                mode = "w"
                                database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
                                database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
                                database_time.Save_costTime(self.costTime, "dataBase/dynamicllyPlanTEST/costTime.csv", mode)
                                
                                # 儲存 I0、PrvUdpataTime、SysTime紀錄(Debug)
                                non_zero_rows_I0AndPrvUpdataTimeAndSysTime = np.any(self.I0AndPrvUpdataTimeAndSysTime != 0, axis=1)
                                self.I0AndPrvUpdataTimeAndSysTime = self.I0AndPrvUpdataTimeAndSysTime[non_zero_rows_I0AndPrvUpdataTimeAndSysTime]
                                database_time.Save_I0AndPrvUpdataTimeAndSysTime(self.I0AndPrvUpdataTimeAndSysTime, "dataBase/dynamicllyPlanTEST/I0AndPrvUpdataTimeAndSysTime.csv", mode)
                                break
                    else:
                        self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
                        self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
                        # 濾除整個row為0的部分
                        non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
                        non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
                        non_zero_rows_costTime = np.any(self.costTime != 0, axis=1)

                        self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
                        self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
                        self.costTime = self.costTime[non_zero_rows_costTime]
                        mode = "w"
                        database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
                        database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
                        database_time.Save_costTime(self.costTime, "dataBase/dynamicllyPlanTEST/costTime.csv", mode)
                    
                    print(f"I2批次有{I3count+1}批，I11批次有{I11count}批")
                    print(f"軌跡實驗結束，共花費 {sysTime} ms")
                    break
                #----------------------------------------------鍵盤事件區-----------------------------------------
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_u:
                            """動態修改銲接參數
                            AC:   I21
                            AVP : I22
                            """
                            AC = 50
                            AVP = 50
                            status = self.changeWeldingPartmeter(AC, AVP)

                        elif event.key == pygame.K_p:
                            """
                            獲得新速度軌跡
                            """
                            # 創建線程
                            # 開始重新規劃新軌跡時，紀錄舊軌跡已經寫入的資料筆數       
                            startPlan_alreadySent_DataBatchNBR = alreadySent_DataBatchNBR
                            
                            if self.Line is True:
                                # 讀取當下位置
                                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                                # 設定新軌跡起點
                                NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]
                            else:
                                # 模擬讀取當下位置
                                coordinate = RPdata[startPlan_alreadySent_DataBatchNBR, 0]
                                # 設定新軌跡起點
                                NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3]/10, coordinate[4]/10, coordinate[5]/10]

                            # 終點與原軌跡保持一致
                            GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                            
                           
                            GoalSpeed = float(input("請輸入走速："))
                            # ---------------------------防呆------------------------------------
                            fractional_part, integer_part = math.modf(GoalSpeed)
                            # 转换为字符串并分割
                            fractional_str = str(fractional_part).split(".")[1]
                            # 去除可能存在的尾随零和负号
                            fractional_str = fractional_str.rstrip('0').rstrip('-')
                            
                            if integer_part >= 10:
                                print("要更改的速度過快!!!")
                                GoalSpeed = float(input("請重新輸入走速："))
                            if len(fractional_str) > 1:
                                print("輸入值超過小數後一位!!!")
                                GoalSpeed = float(input("請重新輸入走速："))
                            # -------------------------------------------------------------------
                            
                            print(f"理想速度: {GoalSpeed} mm/s")
                            
                            # 執行緒
                            planThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, GoalSpeed))
                            planThread.start()

                            # 改變狀態旗標>>> 執行續已被啟動過
                            Thread_started = True
                            
                if planThread.is_alive() is False and Thread_started is True:
                    # 軌跡已變化一次，需更新計數器值
                    trjUpdataNBR += 1

                    # 取出執行緒計算結果
                    b = self.Time.ReadNowTime()
                    result = planThread.get_result()
                    
                    NewHomogeneousMat = result[0]
                    NewPoseMatData = result[1]
                    NewSpeedData = result[2]
                    NewTimeData = result[3]
                    costTime_PlanTrj = result[4]

                    print(f"新軌跡資料長度:{NewHomogeneousMat.shape}")
                    # 存檔(新軌跡資料) 
                    mode = "w"
                    database_HomogeneousMat.Save(NewHomogeneousMat, f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{trjUpdataNBR}.csv", mode)
                    database_PoseMat.Save(NewPoseMatData, f"dataBase/dynamicllyPlanTEST/PoseMat_{trjUpdataNBR}.csv", mode)
                    database_Velocity.Save(NewSpeedData, f"dataBase/dynamicllyPlanTEST/Speed_{trjUpdataNBR}.csv", mode)
                    database_time.Save(NewTimeData,f"dataBase/dynamicllyPlanTEST/Time_{trjUpdataNBR}.csv", mode)
                    
                    # 規劃完時，紀錄舊軌跡已經寫入的資料批數
                    endPlan_alreadySent_DataBatchNBR = alreadySent_DataBatchNBR
                    # 計算規劃時，時間差所產生的資料落後批數
                    dataErr = endPlan_alreadySent_DataBatchNBR-startPlan_alreadySent_DataBatchNBR
                    print("系統反應時間所消耗的資料(批次)數: ", dataErr)

                    
                    
                    # -----------------------------------資料整併(軌跡)--------------------------------------------------------------
                    oldFile_PoseMat = f"dataBase/dynamicllyPlanTEST/PoseMat_{Prv_trjUpdataNBR}.csv"
                    newFile_PoseMat = f"dataBase/dynamicllyPlanTEST/PoseMat_{trjUpdataNBR}.csv"
                    RemixFile_PoseMat = f"dataBase/dynamicllyPlanTEST/Remix_PoseMat_{Prv_trjUpdataNBR}_{trjUpdataNBR}.csv"
                    data_frame1 = pd.read_csv(oldFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
                    data_frame2 = pd.read_csv(newFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
                    # 取得舊資料切換新資料時的最後一筆資料
                    # 提取舊資料
                    oldFileIndex = endPlan_alreadySent_DataBatchNBR*9
                    dfBuffer1 = data_frame1.iloc[:oldFileIndex]
                    # 找相似的資料
                    targetData = data_frame1.iloc[oldFileIndex]
                    closestData, closestIndex = dataOperating.searchSimilar(data_frame2, targetData)
                    # 要合併的新資料
                    dfBuffer2 = data_frame2.iloc[closestIndex+1:]
                    Remix_PoseMat_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
                    Remix_PoseMat_df.to_csv(RemixFile_PoseMat, index=False,  header=True)
                    Remix_PoseMat = np.array(Remix_PoseMat_df).reshape(-1, 1, 6)
                    # --------------------------------------------------------------------------------------------------------------

                    # -----------------------------------資料整併(速度)--------------------------------------------------------------
                    oldFile_Speed = f"dataBase/dynamicllyPlanTEST/Speed_{Prv_trjUpdataNBR}.csv"
                    newFile_Speed = f"dataBase/dynamicllyPlanTEST/Speed_{trjUpdataNBR}.csv"
                    RemixFile_Speed = f"dataBase/dynamicllyPlanTEST/Remix_Speed_{Prv_trjUpdataNBR}_{trjUpdataNBR}.csv"
                    data_frame1 = pd.read_csv(oldFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
                    data_frame2 = pd.read_csv(newFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')

                    # 軌跡已變化一次，將上一個軌跡檔編號也須更新
                    Prv_trjUpdataNBR += 1

                    # 取得舊資料切換新資料時的最後一筆資料
                    # 提取舊資料
                    oldFileIndex = endPlan_alreadySent_DataBatchNBR*9
                    dfBuffer1 = data_frame1.iloc[:oldFileIndex]
                    # 找相似的資料
                    targetData = data_frame1.iloc[oldFileIndex]
                    # 要合併的新資料
                    dfBuffer2 = data_frame2.iloc[closestIndex+1:]
                    Remix_Speed_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
                    Remix_Speed_df.to_csv(RemixFile_Speed, index=False,  header=True)
                    Remix_Speed = np.array(Remix_Speed_df)
                    # --------------------------------------------------------------------------------------------------------------
                    # 將物件變數中的軌跡資料替換為新的軌跡資料
                    self.trjData = Remix_PoseMat
                    self.velData = Remix_Speed
                    

                    # 固定流程(資料分割與初步封裝)
                    Remix_PoseMat, Remix_Speed = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)
                    NewRemixBatch = self.calculateDataGroupBatch(Remix_PoseMat)
                    NewRemixRPdata, NewRemixSpeeddata = self.dataSegmentation(Remix_PoseMat, Remix_Speed, NewRemixBatch)
                    # --------------------------------------------------------------------------------------------------------------
                    
                    # 使用合併後的軌跡檔案(已分割與封裝)，覆蓋原始的軌跡資料
                    RPdata = NewRemixRPdata
                    Veldata = NewRemixSpeeddata
                    
                    # 更新資料計數器，因使用合併後的軌跡檔案，故將計數器的值加上[計算新軌跡所花費的總時間(以批次計算)]
                    # alreadySent_DataBatchNBR -= dataErr
                    """
                    經實驗證實，若系統反應時間不超過1批資料時間，即可不用特別更新[資料批次計數]之批次數
                    """
                    # 更新Batch，將總批次數更新成與合併後的軌跡檔案相符的
                    batch = NewRemixBatch
                    
                    Thread_started = False
                    print("--------------新軌跡資料已覆寫---------------")

                    a = self.Time.ReadNowTime()
                    err = self.Time.TimeError(b,a)
                    costTime_dataMerge = err["millisecond"]
                    print(f"新軌跡規劃後處理所花時長: {costTime_dataMerge} ms")

                    self.costTime[self.costTimeDataCounter, 0] = costTime_PlanTrj
                    self.costTime[self.costTimeDataCounter, 1] = costTime_dataMerge

                    # 計算IK
                    SimThread = threading.Thread(target=self.simulation, args=(trjUpdataNBR,))
                    SimThread.start()
                #-----------------------------------------------------------------------------------------------
                singlelooptime2 = self.Time.ReadNowTime()
                singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
                # singleloopCosttime_ms = singleloopCosttime["millisecond"]
                # print(f"單個迴圈花費 {singleloopCosttime_ms} ms")

                # 剩餘時間
                laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
                # self.Time.time_sleep(laveTime*0.001)
            
if __name__ == "__main__":


    trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
    speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
    Motomancontrol(trjdataPath, speeddataPath).main()