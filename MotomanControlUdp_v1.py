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

#     def communicationRecords(self, RPdata, Veldata, alreadySentDataBatch):
#         """通訊時用於紀錄通訊內容
#         """
#         # 紀錄通訊所傳輸的資料
#         self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySentDataBatch]
#         self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySentDataBatch]
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
#         alreadySentDataBatch = 0

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
#             RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#             # 傳送n筆資料
#             Is_success = self.writeRPvarINTvar(firstAddress, number, RPpacket, Velpacket)
#             # 紀錄通訊所送出的軌跡資料 | 用於驗證
#             self.communicationRecords(RPdata, Veldata, alreadySentDataBatch)
#             # 資料(批次)計數器更新
#             alreadySentDataBatch += 1

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
#                 #         RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                 #         # 傳送n筆資料
#                 #         Is_success = self.writeRPvarINTvar(firstAddress, number, RPpacket, Velpacket)
#                 #         # 紀錄通訊所送出的軌跡資料 | 用於驗證
#                 #         self.communicationRecords(RPdata, Veldata, alreadySentDataBatch)
#                 #         # 資料(批次)計數器更新
#                 #         alreadySentDataBatch += 1

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


# """
# - 版本: 0.0
# - 名稱: 動態軌跡規劃與通訊架構(模擬實驗架構)
# - 最後使用日期: 20240512
# - 問題: 送軌跡之通訊會導致軌跡延遲問題，平均通訊一組，延遲60ms。
# - 解決方案:
#     1.減少送出的軌跡點數量
#     2.配合DX200之系統時間進行補償
# """
# import pygame
# import math
# import threading
# import numpy as np
# from MotomanUdpPacket import MotomanUDP
# from Toolbox import TimeTool
# from dataBase_v1 import *
# from Kinematics import Kinematics
# from armControl import Generator
# from SimulatorV2 import Simulator
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTimer, QThread
# from communctionThread import *


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
#         self.I28 = 0

#         if self.Line is True:
#             status = self.Udp.multipleWriteVar(0, 2, [self.I0, self.I1])
#             status = self.Udp.WriteVar("Integer", 28, 0)


#         # 動態變更銲接參數預設值
#         """
#         AC:   I21
#         AVP : I22
#         """
#         self.AC = 40
#         self.AVP = 50
#         if self.Line is True:
#             status = self.Udp.multipleWriteVar(21, 2, [self.AC, self.AVP])

#         # 載入軌跡檔案
#         self.trjData = database_PoseMat.Load(TrjdatafilePath)
#         self.velData = database_Velocity.Load(VeldatafilePath)
#         # 刪除軌跡資料第一筆資料
#         self.trjData, self.velData = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)

#         # PC >> DX200 通訊紀錄
#         self.communicationRecords_Trj = np.zeros((50000, 9, 6))
#         self.communicationRecords_Speed = np.zeros((50000, 9))
#         self.communicationRecords_Counter = 0

#         # DX200 feedback的手臂資料紀錄
#         self.feedbackRecords_Trj = np.zeros((50000, 1, 6)) 
#         self.feedbackRecords_sysTime = np.zeros((50000, 1))
#         self.feedbackRecords_Counter = 0

#         # 規劃新軌跡 各工作階段所花費的時間
#         """
#         Cost Time = ["Trj_Algorithm", "Data_merge", "IK_Iterate"]
#         """
#         self.costTime = np.zeros((100, 3))
#         self.costTimeDataCounter = 0

#         # I0驗證系統
#         """
#         I0、PrvUpdataTime、SysTime :[I0, PrvUpdataTime, SysTime]
#         """
#         self.I0AndPrvUpdataTimeAndSysTime = np.zeros((50000, 6))
#         self.I0AndPrvUpdataTimeAndSysTimeCounter = 0
        
#         self.WriteSpeedBypass = 0

        
#     @staticmethod
#     def deleteFirstTrajectoryData(TrajectoryData, VelocityData):
#         """Delete the first data.
#         """
#         TrajectoryData = TrajectoryData[1:]
#         VelocityData = VelocityData[1:]
        
#         return TrajectoryData, VelocityData
    
#     def changeWeldingPartmeter(self, AC, AVP):
#         """Dynamically change welding parameters.
#         - Args: AC、AVP
#         - Return: cmd_Status
#         """
        
#         # DX200 variable(Integer) settings
#         # AC:   I21
#         # AVP : I22

#         firstAddress = 21
#         number = 2
#         IData =[AC, AVP]

#         if self.Line is True:
#             Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
        
#     def calculateDataGroupBatch(self, TrajectoryData):
#         """Calculate data segmentation groups and batches.
#         Group: 組數 (About: I001)
#         Batch: 批次 (About: I000)
        
#         - Args: Trajectory data
#         - Return: Number of data groups , Number of data batches
#         """
#         # Calculate batch(About: I000)
#         quotient_batch, remainder_batch = divmod(TrajectoryData.shape[0], 9)
#         if remainder_batch != 0:
#             # 餘數不等於0，表示原始資料分批(9筆為1批)時，最後一批不足9筆，故要+1批並做填充
#             batch = quotient_batch + 1
#         else:
#             batch = quotient_batch

#         # 修改DX200變數暫存器值
#         if self.Line is True:
#             print("INFORM程式 I001: ", batch)
#             status = self.Udp.WriteVar("Integer", 1, batch)
        
#         return batch
    
#     def dataSegmentation(self, trajectoryData, velocityData, batch):
#         """
#         資料分批處理
#         單位: 9筆/批
#         """
        
#         """資料分割演算法
#         1.判斷原資料(m*1*6)是否可完整切個為shape(n*9*6), m=該資料原本的筆數; n= m/9.
#         2.若第一步中發現有不足9筆需要補齊資料，使用最後一筆資料補齊剩下的缺口.
#         3.補齊後，將資料切割為(n*9*6).
#         """

#         # 軌跡資料處理與分割
#         # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
#         quotient_trj, remainder_trj = divmod(trajectoryData.shape[0], 9)
#         if remainder_trj != 0:
#             # 讀取最後一個Row的數據
#             last_row = trajectoryData[-1]

#             # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
#             padding = np.tile(last_row, (9 - remainder_trj, 1, 1))

#             # 將需要填充的Row與原資料進行(Row堆疊)
#             padded_array = np.vstack((trajectoryData, padding))

#             # 將資料分割成以批次(一批次有9筆資料)為單位
#             reshaped_trajectoryData = padded_array.reshape(batch, 9, 6)
#         else:
#             # 將資料分割成以批次(一批次有9筆資料)為單位
#             reshaped_trajectoryData = trajectoryData.reshape(batch, 9, 6)

#         # 将第4、5、6列的值都乘以10
#         reshaped_trajectoryData[:, :, 3:6]*= 10
#         # 完成初步分割與封裝後的軌跡資料
#         RPdata = reshaped_trajectoryData



#         # 軌跡資料處理與分割(速度)
#         # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
#         quotient_vel, remainder_vel = divmod(velocityData.shape[0], 9)
#         if remainder_vel != 0:
#             # 讀取最後一個Row的數據
#             last_row = velocityData[-1]

#             # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
#             padding = np.tile(last_row, (9 - remainder_vel, 1))

#             # 將需要填充的Row與原資料進行(Row堆疊)
#             padded_array = np.vstack((velocityData, padding))

#             # 將資料分割成以批次(一批次有9筆資料)為單位
#             reshaped_velocityData = padded_array.reshape(batch, 9)
#         else:
#             # 將資料分割成以批次(一批次有9筆資料)為單位
#             reshaped_velocityData = velocityData.reshape(batch, 9)

#         # 將所有值都乘以10(DX200的速度指令只接受整數，送入後會將數值自動*0.1，故發送前須將數值都乘以10)
#         reshaped_velocityData *= 10
#         Veldata = reshaped_velocityData

#         # 完成初步分割與封裝後的軌跡(速度)資料
#         Veldata = Veldata.astype(int)
    
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
    
    
#     def writeRPvarINTvar(self, firstAddress, RPpacket, Velpacket):
#         """Write multiple variable data
#         - Args: RPdata, Veldata
#         """
#         Is_success = False
        
#         if self.Line is True:
#             RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
#             if self.WriteSpeedBypass >= 2:
#                 Istatus = []
#                 pass
#             else:
#                 Istatus = self.Udp.multipleWriteVar(firstAddress, 9, Velpacket)
#                 self.WriteSpeedBypass += 1
            
#         else:
#             # 靜態測試的模擬訊號
#             RPstatus = []
#             Istatus =[]

#         if RPstatus == [] and Istatus == []:
#             Is_success = True
#         else:
#             Is_success = False
        
#         return Is_success
    
    
#     def PlanNewTrj(self, NowEnd, GoalEnd, sampleTime, GoalSpeed):
#         """規劃新軌跡，時間線沿用舊軌跡
#         目的: 產生新軌跡, 並即時傳輸。
#         """
#         b = self.Time.ReadNowTime()

#         # 創造新軌跡
#         HomogeneousMatData, PoseMatData, SpeedData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, GoalSpeed)
        
#         a = self.Time.ReadNowTime()
#         err = self.Time.TimeError(b, a)
#         print("計算新軌跡所花費的總時間: ", err["millisecond"], "ms")
#         costTime_PlanTrj = err["millisecond"]

#         return HomogeneousMatData, PoseMatData, SpeedData, TimeData, costTime_PlanTrj
    
#     def simulation(self, trjUpdataNBR):
#         d2r = np.deg2rad
#         b = self.Time.ReadNowTime()
#         newHomogeneousMat = database_HomogeneousMat.Load(f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{trjUpdataNBR}.csv")
#         nowJointAngle = (np.zeros((6,1)))
#         nowJointAngle[0, 0] =  d2r(-0.006)
#         nowJointAngle[1, 0] =  d2r(-38.8189)
#         nowJointAngle[2, 0] =  d2r(-41.0857)
#         nowJointAngle[3, 0] =  d2r(-0.0030)
#         nowJointAngle[4, 0] =  d2r(-76.4394)
#         nowJointAngle[5, 0] =  d2r(1.0687)
#         JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, newHomogeneousMat)
#         a = self.Time.ReadNowTime()
#         err = self.Time.TimeError(b, a)
#         print("關節角度計算所消耗的總時間: ", err["millisecond"], "ms")
#         database_JointAngle.Save(JointAngleData, f"dataBase/dynamicllyPlanTEST/JointAngle_{trjUpdataNBR}.csv", "w")
#         # self.Sim.paitGL(JointAngleData, newHomogeneousMat)


#     def feedbackRecords(self, sysTime):
#         """由機器手臂反饋回PC的數據紀錄
#         """
#         # 讀取實際手臂位置
#         pos_result, coordinate = self.Udp.getcoordinateMH(101)
#         # 儲存實際軌跡資料
#         self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([coordinate])
#         self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = sysTime
#         self.feedbackRecords_Counter += 1
        
    
#     def communicationRecords(self, RPdata, Veldata, alreadySentDataBatch, batch):
#         """通訊時用於紀錄通訊內容
#         """
#         # 紀錄通訊所傳輸的資料
#         if alreadySentDataBatch > batch-1:
#             pass
#         else:    
#             self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySentDataBatch]
#             self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySentDataBatch]
#         self.communicationRecords_Counter += 1

#     def main(self):
#         #---------------------------------------------Inital-----------------------------------------------
#         # 初始化Pygame
#         pygame.init()

#         # 設置畫面寬高
#         screen_width = 800
#         screen_height = 600
#         screen = pygame.display.set_mode((screen_width, screen_height))
        
#         # 紀錄UDP目前已送出的資料批次數(1批 = 9筆)
#         alreadySentDataBatch = 0
#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0
#         startNode = 0
#         # 取樣時間
#         sampleTime = 0.04
#         # 系統時間初始化flag
#         sysflag = True
#         # 變軌跡次數
#         trjUpdataNBR = 0
#         Prv_trjUpdataNBR = 0
        
#         # 計算資料分割的組數與批數
#         batch = self.calculateDataGroupBatch(self.trjData)
        
#         # 資料分割
#         RPdata, Veldata = self.dataSegmentation(self.trjData, self.velData, batch)
        
#         # 包裝並寫入首9筆資料   
#         RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#         Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
#         # 紀錄通訊所送出的軌跡資料 | 用於驗證
#         self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#         # 資料(批次)計數器更新
#         alreadySentDataBatch += 1
        
        
        
#         # 軌跡規劃執行緒
#         Thread_started = False
#         planThread = GetNewTrj(target=self.PlanNewTrj)

#         # 軌跡資料儲存容器(驗證資料)
        
#         #-------------------------------------------------------------------------------------------------
        
#         # 測試通訊資料批次數
#         I3count = 0
#         I11count = 0
#         feedback_count = 0

#         # 更新位置變數時的時間點
#         updataTrjTime = self.Time.ReadNowTime()

#         # 時間限制
#         timeLimit = 100

#         # 互鎖
#         I2Lock = False
#         I11Lock = False

#         # 主迴圈旗標 | 開關
#         mainLoop = False
#         while True:
#             if self.Line is True:
#                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                 if np.linalg.norm(np.array(coordinate) - self.trjData[0, 0]) <= 0.05:
#                     print("------------------------------實測實驗開始------------------------------")
#                     print(f"軌跡開始位置: {coordinate}")
#                     mainLoop = True
#                     break
#             else:
#                 print("------------------------------模擬實驗開始------------------------------")
#                 mainLoop = True
#                 break
        
#         while mainLoop:
#             singlelooptime1 = self.Time.ReadNowTime()
#             # 更新每禎時間
#             nowTime = self.Time.ReadNowTime()
            
#             if sysflag is True:
#                 """
#                 此區在本迴圈只會在剛進迴圈時執行一次
#                 """
#                 # 儲存系統開始時間
#                 startTime = self.Time.ReadNowTime()

                
#                 if self.Line is True:
#                     # 取得I0初值
#                     # I0 = self.Udp.ReadVar("Integer", 0)
#                     I0 = [2]
#                     # 起始變數位置
#                     firstAddress = 11
#                     # 打包需要傳送的變數資料
#                     RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                     # 將打包完的資料寫入DX200
#                     Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
#                     # 通訊紀錄
#                     self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#                     # 資料(批次)計數器更新
#                     alreadySentDataBatch += 1

#                     I11count+=1
                    
#                     # 紀錄feedback數據 | 紀錄初始位置與系統時間
#                     self.feedbackRecords(0)
#                 else:
#                     I0 = [3]

#                 sysflag = False
            
#             else:
#                 # 更新系統時間
                
#                 sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                 sysTime = round(sysTime/1000, 1)
                
#                 #----------------------------------------------命令執行區-----------------------------------------            
#                 if self.Line is True:
#                     # 更新距離上次更新軌跡時，又經過多久的時間
#                     b = self.Time.ReadNowTime()
#                     timeLeft = self.Time.TimeError(updataTrjTime, b)
#                     timeLeft_ms = timeLeft["millisecond"]
#                     print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取I0處")

                    
#                     I2Lock = True
#                     I11Lock = True

#                     Prv_I0 = I0
#                     I0 = self.Udp.ReadVar("Integer", 0)
#                     # 將I0、PrvUpdataTime、SysTimer記錄下來
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 0] = I0[0]
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 1] = timeLeft_ms
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 2] = sysTime
                    
#                     print(f"I000 : {I0}")
#                     """
#                     防止重複
#                     """
#                     if Prv_I0 != I0 and I0 >= [2] and I0 <= [10]:
#                         I2Lock = True
#                         # print(f"I0: {I0}，允許寫入I11-I19")
#                     elif Prv_I0 != I0 and I0 >= [11] and I0 <= [19]:
#                         I11Lock = True
#                         # print(f"I0: {I0}，允許寫入I02-I10")
#                     else:
#                         pass
#                     print(f"上次的I0與本次I0相同，不允許寫入。")

#                     """
#                     計算更新時間
#                     """
#                     # if timeLeft_ms <= timeLimit:
#                     #     I0 = self.Udp.ReadVar("Integer", 0)
#                     #     print(f"I000 : {I0}")

#                     # elif timeLeft_ms > timeLimit :
                        
#                     #     if I0 >= [2] and I0 <= [10]:
#                     #         I0 = [11]
#                     #         print("已鄰近下次需要更新軌跡的時間，強制將I000變更為11。")
#                     #     elif I0 >= [11] and I0 <= [19]:
#                     #         I0 = [2]
#                     #         print("已鄰近下次需要更新軌跡的時間，強制將I000變更為2。")

#                     # else:
#                     #     pass

                    

#                 else:
#                     # 模擬I0變換
#                     if I0 == [11]:
#                         I0 = [3]
#                     elif I0 == [3]:
#                         I0 = [11]

                    
#                 #----------------------------------------------資料通訊區-----------------------------------------
#                 """
#                 通訊
#                 * 變數區間:
#                 1. I02 - I10
#                 2. I11 - I19
#                 """
                
#                 if I0 == [2] and I2Lock is True:
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 3] = sysTime
                    
#                     I2_b = self.Time.ReadNowTime()

#                     # 起始變數位置
#                     firstAddress = 11
#                     # 打包需要傳送的變數資料
#                     RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                     # 將打包完的資料寫入DX200
#                     Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
#                     # 通訊紀錄
#                     self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#                     # 資料(批次)計數器更新
#                     alreadySentDataBatch += 1

#                     if self.Line is False:
#                         # 模擬軌跡時間
#                         self.Time.time_sleep(0.36)

#                     I2_a = self.Time.ReadNowTime()
#                     I2err = self.Time.TimeError(I2_b, I2_a)
#                     I2err_ms = I2err["millisecond"]
#                     print(f"更新I11-I20的軌跡資料花費時間: {I2err_ms}ms")

#                     # 紀錄送軌跡所花費的時間與變數區間
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 4] = I2err_ms
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 5] = 2
#                     self.I0AndPrvUpdataTimeAndSysTimeCounter += 1

#                     # 紀錄軌跡更新時間
#                     updataTrjTime = self.Time.ReadNowTime()

#                     I11count+=1
#                     I2Lock = False
                    

#                 elif I0 == [11] and I11Lock is True:
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 3] = sysTime
#                     I11_b = self.Time.ReadNowTime()

#                     # 起始變數位置
#                     firstAddress = 2
#                     # 打包需要傳送的變數資料
#                     RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                     # 將打包完的資料寫入DX200
#                     Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
#                     # 通訊紀錄
#                     self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#                     # 資料(批次)計數器更新
#                     alreadySentDataBatch += 1

#                     if self.Line is False:
#                         # 模擬軌跡時間
#                         self.Time.time_sleep(0.36)
                        
#                     I11_a = self.Time.ReadNowTime()
#                     I11_err = self.Time.TimeError(I11_b, I11_a)
#                     I11_err_ms = I11_err["millisecond"]
#                     print(f"更新I02-I10的軌跡資料花費時間: {I11_err_ms}ms")

#                     # 紀錄送軌跡所花費的時間與變數區間
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 4] = I11_err_ms
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 5] = 1
#                     self.I0AndPrvUpdataTimeAndSysTimeCounter += 1

#                     # 紀錄軌跡更新時間
#                     updataTrjTime = self.Time.ReadNowTime()

#                     I3count+=1
#                     I11Lock = False

#                 else:
#                     self.I0AndPrvUpdataTimeAndSysTimeCounter += 1
#                     # if self.Line is True:
#                     #     # 更新距離上次更新軌跡時，又經過多久的時間
#                     #     b = self.Time.ReadNowTime()
#                     #     timeLeft = self.Time.TimeError(updataTrjTime, b)
#                     #     timeLeft_ms = timeLeft["millisecond"]
#                     #     print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取feedback資料處")
#                     #     # 紀錄feedback數據
#                     #     self.feedbackRecords(sysTime)
#                     #     feedback_count+=1

#                     #     if timeLeft_ms <= timeLimit:
#                     #         # 紀錄feedback數據
#                     #         self.feedbackRecords(sysTime)
#                     #         feedback_count+=1
#                     #         print(f"feedback寫入次數: {feedback_count}次")
#                     #     elif timeLeft_ms > timeLimit :
#                     #         print("已鄰近下次需要更新軌跡的時間，略過讀取feedback數據動作。")
#                     #         pass
                        
#                     #     else:
#                     #         pass
                   
                
#                 if alreadySentDataBatch == batch:
#                     """結束條件
#                     外迴圈數 = 批次數
#                     """
                
#                     # -------------------------------------通訊資紀錄與feedback紀錄 | 處理與存檔-----------------------------------
#                     # 讀取最後一刻軌跡資料       
#                     if self.Line is True:
#                         can_End = False
#                         while True:
#                             # 讀取I000變數
#                             I0 = self.Udp.ReadVar("Integer", 0)

#                             # 更新系統時間
#                             nowTime = self.Time.ReadNowTime()
#                             # 取得系統時間
#                             sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                             sysTime = round(sysTime/1000, 1)

#                             # 紀錄feedback數據
#                             self.feedbackRecords(sysTime)
#                             feedback_count+=1
#                             print(f"feedback寫入次數: {feedback_count}次")

#                             # 判斷此筆軌跡資料的I0會停留在I0=11還是I0=2
#                             quotient, remainder = divmod(RPdata.shape[0]*RPdata.shape[1], 18)
                            
#                             if remainder == 9 and I0 == [11]:
#                                 can_End = True
#                             elif remainder == 0 and I0 == [2]:
#                                 can_End = True
#                             else: 
#                                 can_End = False
                                
#                             if can_End is True:
#                                 # feedback的軌跡資料
#                                 # 濾除整個row為0的部分
#                                 non_zero_rows_Trajectory = np.any(self.feedbackRecords_Trj != 0, axis=(1, 2))
#                                 non_zero_rows_Time = np.any(self.feedbackRecords_sysTime != 0, axis=1)
#                                 # 系統時間需保留初值0
#                                 non_zero_rows_Time[:2] = True

#                                 self.feedbackRecords_Trj = self.feedbackRecords_Trj[non_zero_rows_Trajectory]
#                                 self.feedbackRecords_sysTime = self.feedbackRecords_sysTime[non_zero_rows_Time]
                                
#                                 database_PoseMat.Save(self.feedbackRecords_Trj, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj.csv", "w")
#                                 database_time.Save(self.feedbackRecords_sysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_sysTime.csv", "w")
                                
#                                 # 儲存通訊所送出的軌跡資料
#                                 self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
#                                 self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
#                                 # 濾除整個row為0的部分
#                                 non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
#                                 non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
#                                 non_zero_rows_costTime = np.any(self.costTime != 0, axis=1)

#                                 self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
#                                 self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
#                                 self.costTime = self.costTime[non_zero_rows_costTime]
#                                 mode = "w"
#                                 database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
#                                 database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
#                                 database_time.Save_costTime(self.costTime, "dataBase/dynamicllyPlanTEST/costTime.csv", mode)
                                
#                                 # 儲存 I0、PrvUdpataTime、SysTime紀錄(Debug)
#                                 non_zero_rows_I0AndPrvUpdataTimeAndSysTime = np.any(self.I0AndPrvUpdataTimeAndSysTime != 0, axis=1)
#                                 self.I0AndPrvUpdataTimeAndSysTime = self.I0AndPrvUpdataTimeAndSysTime[non_zero_rows_I0AndPrvUpdataTimeAndSysTime]
#                                 database_time.Save_I0AndPrvUpdataTimeAndSysTime(self.I0AndPrvUpdataTimeAndSysTime, "dataBase/dynamicllyPlanTEST/I0AndPrvUpdataTimeAndSysTime.csv", mode)
#                                 break
#                     else:
#                         self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
#                         self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
#                         # 濾除整個row為0的部分
#                         non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
#                         non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
#                         non_zero_rows_costTime = np.any(self.costTime != 0, axis=1)

#                         self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
#                         self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
#                         self.costTime = self.costTime[non_zero_rows_costTime]
#                         mode = "w"
#                         database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
#                         database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
#                         database_time.Save_costTime(self.costTime, "dataBase/dynamicllyPlanTEST/costTime.csv", mode)
                    
#                     print(f"I2批次有{I3count+1}批，I11批次有{I11count}批")
#                     print(f"軌跡實驗結束，共花費 {sysTime} ms")
#                     break
#                 #----------------------------------------------鍵盤事件區-----------------------------------------
#                 for event in pygame.event.get():
#                     if event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_u:
#                             """動態修改銲接參數
#                             AC:   I21
#                             AVP : I22
#                             """
#                             AC = 50
#                             AVP = 50
#                             status = self.changeWeldingPartmeter(AC, AVP)

#                         elif event.key == pygame.K_p:
#                             """
#                             獲得新速度軌跡
#                             """
#                             # 創建線程
#                             # 開始重新規劃新軌跡時，紀錄舊軌跡已經寫入的資料筆數       
#                             startPlan_alreadySentDataBatch = alreadySentDataBatch
                            
#                             if self.Line is True:
#                                 # 讀取當下位置
#                                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                                 # 設定新軌跡起點
#                                 NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]
#                             else:
#                                 # 模擬讀取當下位置
#                                 coordinate = RPdata[startPlan_alreadySentDataBatch, 0]
#                                 # 設定新軌跡起點
#                                 NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3]/10, coordinate[4]/10, coordinate[5]/10]

#                             # 終點與原軌跡保持一致
#                             GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                            
                           
#                             GoalSpeed = float(input("請輸入走速："))
#                             # ---------------------------防呆------------------------------------
#                             fractional_part, integer_part = math.modf(GoalSpeed)
#                             # 转换为字符串并分割
#                             fractional_str = str(fractional_part).split(".")[1]
#                             # 去除可能存在的尾随零和负号
#                             fractional_str = fractional_str.rstrip('0').rstrip('-')
                            
#                             if integer_part >= 10:
#                                 print("要更改的速度過快!!!")
#                                 GoalSpeed = float(input("請重新輸入走速："))
#                             if len(fractional_str) > 1:
#                                 print("輸入值超過小數後一位!!!")
#                                 GoalSpeed = float(input("請重新輸入走速："))
#                             # -------------------------------------------------------------------
                            
#                             print(f"理想速度: {GoalSpeed} mm/s")
                            
#                             # 執行緒
#                             planThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, GoalSpeed))
#                             planThread.start()

#                             # 改變狀態旗標>>> 執行續已被啟動過
#                             Thread_started = True
                            
#                 if planThread.is_alive() is False and Thread_started is True:
#                     # 軌跡已變化一次，需更新計數器值
#                     trjUpdataNBR += 1

#                     # 取出執行緒計算結果
#                     b = self.Time.ReadNowTime()
#                     result = planThread.get_result()
                    
#                     NewHomogeneousMat = result[0]
#                     NewPoseMatData = result[1]
#                     NewSpeedData = result[2]
#                     NewTimeData = result[3]
#                     costTime_PlanTrj = result[4]

#                     print(f"新軌跡資料長度:{NewHomogeneousMat.shape}")
#                     # 存檔(新軌跡資料) 
#                     mode = "w"
#                     database_HomogeneousMat.Save(NewHomogeneousMat, f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{trjUpdataNBR}.csv", mode)
#                     database_PoseMat.Save(NewPoseMatData, f"dataBase/dynamicllyPlanTEST/PoseMat_{trjUpdataNBR}.csv", mode)
#                     database_Velocity.Save(NewSpeedData, f"dataBase/dynamicllyPlanTEST/Speed_{trjUpdataNBR}.csv", mode)
#                     database_time.Save(NewTimeData,f"dataBase/dynamicllyPlanTEST/Time_{trjUpdataNBR}.csv", mode)
                    
#                     # 規劃完時，紀錄舊軌跡已經寫入的資料批數
#                     endPlan_alreadySentDataBatch = alreadySentDataBatch
#                     # 計算規劃時，時間差所產生的資料落後批數
#                     dataErr = endPlan_alreadySentDataBatch-startPlan_alreadySentDataBatch
#                     print("系統反應時間所消耗的資料(批次)數: ", dataErr)

                    
                    
#                     # -----------------------------------資料整併(軌跡)--------------------------------------------------------------
#                     oldFile_PoseMat = f"dataBase/dynamicllyPlanTEST/PoseMat_{Prv_trjUpdataNBR}.csv"
#                     newFile_PoseMat = f"dataBase/dynamicllyPlanTEST/PoseMat_{trjUpdataNBR}.csv"
#                     RemixFile_PoseMat = f"dataBase/dynamicllyPlanTEST/Remix_PoseMat_{Prv_trjUpdataNBR}_{trjUpdataNBR}.csv"
#                     data_frame1 = pd.read_csv(oldFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
#                     data_frame2 = pd.read_csv(newFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
#                     # 取得舊資料切換新資料時的最後一筆資料
#                     # 提取舊資料
#                     oldFileIndex = endPlan_alreadySentDataBatch*9
#                     dfBuffer1 = data_frame1.iloc[:oldFileIndex]
#                     # 找相似的資料
#                     targetData = data_frame1.iloc[oldFileIndex]
#                     closestData, closestIndex = dataOperating.searchSimilar(data_frame2, targetData)
#                     # 要合併的新資料
#                     dfBuffer2 = data_frame2.iloc[closestIndex+1:]
#                     Remix_PoseMat_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
#                     Remix_PoseMat_df.to_csv(RemixFile_PoseMat, index=False,  header=True)
#                     Remix_PoseMat = np.array(Remix_PoseMat_df).reshape(-1, 1, 6)
#                     # --------------------------------------------------------------------------------------------------------------

#                     # -----------------------------------資料整併(速度)--------------------------------------------------------------
#                     oldFile_Speed = f"dataBase/dynamicllyPlanTEST/Speed_{Prv_trjUpdataNBR}.csv"
#                     newFile_Speed = f"dataBase/dynamicllyPlanTEST/Speed_{trjUpdataNBR}.csv"
#                     RemixFile_Speed = f"dataBase/dynamicllyPlanTEST/Remix_Speed_{Prv_trjUpdataNBR}_{trjUpdataNBR}.csv"
#                     data_frame1 = pd.read_csv(oldFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
#                     data_frame2 = pd.read_csv(newFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')

#                     # 軌跡已變化一次，將上一個軌跡檔編號也須更新
#                     Prv_trjUpdataNBR += 1

#                     # 取得舊資料切換新資料時的最後一筆資料
#                     # 提取舊資料
#                     oldFileIndex = endPlan_alreadySentDataBatch*9
#                     dfBuffer1 = data_frame1.iloc[:oldFileIndex]
#                     # 找相似的資料
#                     targetData = data_frame1.iloc[oldFileIndex]
#                     # 要合併的新資料
#                     dfBuffer2 = data_frame2.iloc[closestIndex+1:]
#                     Remix_Speed_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
#                     Remix_Speed_df.to_csv(RemixFile_Speed, index=False,  header=True)
#                     Remix_Speed = np.array(Remix_Speed_df)
#                     # --------------------------------------------------------------------------------------------------------------
#                     # 將物件變數中的軌跡資料替換為新的軌跡資料
#                     self.trjData = Remix_PoseMat
#                     self.velData = Remix_Speed
                    

#                     # 固定流程(資料分割與初步封裝)
#                     Remix_PoseMat, Remix_Speed = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)
#                     NewRemixBatch = self.calculateDataGroupBatch(Remix_PoseMat)
#                     NewRemixRPdata, NewRemixSpeeddata = self.dataSegmentation(Remix_PoseMat, Remix_Speed, NewRemixBatch)
#                     # --------------------------------------------------------------------------------------------------------------
                    
#                     # 使用合併後的軌跡檔案(已分割與封裝)，覆蓋原始的軌跡資料
#                     RPdata = NewRemixRPdata
#                     Veldata = NewRemixSpeeddata
                    
#                     # 更新資料計數器，因使用合併後的軌跡檔案，故將計數器的值加上[計算新軌跡所花費的總時間(以批次計算)]
#                     # alreadySentDataBatch -= dataErr
#                     """
#                     經實驗證實，若系統反應時間不超過1批資料時間，即可不用特別更新[資料批次計數]之批次數
#                     """
#                     # 更新Batch，將總批次數更新成與合併後的軌跡檔案相符的
#                     batch = NewRemixBatch
                    
#                     Thread_started = False
#                     print("--------------新軌跡資料已覆寫---------------")

#                     a = self.Time.ReadNowTime()
#                     err = self.Time.TimeError(b,a)
#                     costTime_dataMerge = err["millisecond"]
#                     print(f"新軌跡規劃後處理所花時長: {costTime_dataMerge} ms")

#                     self.costTime[self.costTimeDataCounter, 0] = costTime_PlanTrj
#                     self.costTime[self.costTimeDataCounter, 1] = costTime_dataMerge

#                     # 計算IK
#                     SimThread = threading.Thread(target=self.simulation, args=(trjUpdataNBR,))
#                     SimThread.start()
#                 #-----------------------------------------------------------------------------------------------
#                 singlelooptime2 = self.Time.ReadNowTime()
#                 singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#                 # singleloopCosttime_ms = singleloopCosttime["millisecond"]
#                 # print(f"單個迴圈花費 {singleloopCosttime_ms} ms")

#                 # 剩餘時間
#                 laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
#                 # self.Time.time_sleep(laveTime*0.001)
            
# if __name__ == "__main__":


#     trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
#     speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
#     Motomancontrol(trjdataPath, speeddataPath).main()
"""
- 版本: 1.0
- 名稱: 動態軌跡規劃與通訊架構(模擬實驗架構)
- 更新日期: 20240521
- 搭配的INFORM檔名: RUN_TRJ_0421

"""
# import pygame
# import math
# import threading
# import numpy as np
# from MotomanUdpPacket import MotomanUDP
# from Toolbox import TimeTool
# from dataBase_v1 import *
# from Kinematics import Kinematics
# from armControl import Generator
# from SimulatorV2 import Simulator
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTimer, QThread
# from communctionThread import *


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
#         self.Line = False
#         self.Udp = MotomanUDP()
        
#         self.Kin = Kinematics()
#         self.Time = TimeTool()
#         self.Sim = Simulator()

        
#         # INFORM 迴圈變數
#         """
#         資料單位:
#         9筆=1批, 2批=1組

#         I0:  資料筆數index
#         I1:  資料總批數(資料總筆數/9)(batch)
#         I28: 迴圈跌代次數計數器
#         """
#         self.I0 = 2
#         self.I1 = 0
#         self.I28 = 0

#         if self.Line is True:
#             status = self.Udp.multipleWriteVar(0, 2, [self.I0, self.I1])
#             status = self.Udp.WriteVar("Integer", 28, 0)


#         # 動態變更銲接參數預設值
#         """
#         AC:   I21
#         AVP : I22
#         """
#         self.AC = 40
#         self.AVP = 50
#         if self.Line is True:
#             status = self.Udp.multipleWriteVar(21, 2, [self.AC, self.AVP])

#         # 載入軌跡檔案
#         self.trjData = database_PoseMat.Load(TrjdatafilePath)
#         self.velData = database_Velocity.Load(VeldatafilePath)
#         # 刪除軌跡資料第一筆資料
#         self.trjData, self.velData = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)

#         # PC >> DX200 通訊紀錄
#         self.communicationRecords_Trj = np.zeros((50000, 9, 6))
#         self.communicationRecords_Speed = np.zeros((50000, 9))
#         self.communicationRecords_Counter = 0

#         # DX200 feedback的手臂資料紀錄
#         self.feedbackRecords_Trj = np.zeros((50000, 1, 6)) 
#         self.feedbackRecords_sysTime = np.zeros((50000, 1))
#         self.feedbackRecords_Counter = 0

#         # 規劃新軌跡 各工作階段所花費的時間
#         """
#         Cost Time = ["Trj_Algorithm", "Data_merge", "IK_Iterate"]
#         """
#         self.costTime = np.zeros((100, 3))
#         self.costTimeDataCounter = 0

#         # I0驗證系統
#         """
#         I0、PrvUpdataTime、SysTime :[I0, PrvUpdataTime, SysTime]
#         """
#         self.I0AndPrvUpdataTimeAndSysTime = np.zeros((50000, 8))
#         self.I0AndPrvUpdataTimeAndSysTimeCounter = 0
        
    
#         self.WriteSpeedBypass = 0

#         # 新軌跡資料合併節點紀錄
#         self.mergeNode = np.zeros(1000)


        
#     @staticmethod
#     def deleteFirstTrajectoryData(TrajectoryData, VelocityData):
#         """Delete the first data.
#         """
#         TrajectoryData = TrajectoryData[1:]
#         VelocityData = VelocityData[1:]
        
#         return TrajectoryData, VelocityData
    
#     def changeWeldingPartmeter(self, AC, AVP):
#         """Dynamically change welding parameters.
#         - Args: AC、AVP
#         - Return: cmd_Status
#         """
        
#         # DX200 variable(Integer) settings
#         # AC:   I21
#         # AVP : I22

#         firstAddress = 21
#         number = 2
#         IData =[AC, AVP]

#         if self.Line is True:
#             Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
        
#     def calculateDataGroupBatch(self, TrajectoryData):
#         """Calculate data segmentation groups and batches.
#         Group: 組數 (About: I001)
#         Batch: 批次 (About: I000)
        
#         - Args: Trajectory data
#         - Return: Number of data groups , Number of data batches
#         """
#         # Calculate batch(About: I000)
#         quotient_batch, remainder_batch = divmod(TrajectoryData.shape[0], 9)
#         if remainder_batch != 0:
#             # 餘數不等於0，表示原始資料分批(9筆為1批)時，最後一批不足9筆，故要+1批並做填充
#             batch = quotient_batch + 1
#         else:
#             batch = quotient_batch

#         # 修改DX200變數暫存器值
#         if self.Line is True:
#             print("INFORM程式 I001: ", batch)
#             status = self.Udp.WriteVar("Integer", 1, batch)
        
#         return batch
    
#     def dataSegmentation(self, trajectoryData, velocityData, batch, SpeedIndex=0):
#         """
#         資料分批處理
#         單位: 9筆/批
#         """
        
#         """資料分割演算法
#         1.判斷原資料(m*1*6)是否可完整切個為shape(n*9*6), m=該資料原本的筆數; n= m/9.
#         2.若第一步中發現有不足9筆需要補齊資料，使用最後一筆資料補齊剩下的缺口.
#         3.補齊後，將資料切割為(n*9*6).
#         """

#         # 軌跡資料處理與分割
#         # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
#         quotient_trj, remainder_trj = divmod(trajectoryData.shape[0], 9)
#         if remainder_trj != 0:
#             # 讀取最後一個Row的數據
#             last_row = trajectoryData[-1]

#             # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
#             padding = np.tile(last_row, (9 - remainder_trj, 1, 1))

#             # 將需要填充的Row與原資料進行(Row堆疊)
#             padded_array = np.vstack((trajectoryData, padding))

#             # 將資料分割成以批次(一批次有9筆資料)為單位
#             reshaped_trajectoryData = padded_array.reshape(batch, 9, 6)
#         else:
#             # 將資料分割成以批次(一批次有9筆資料)為單位
#             reshaped_trajectoryData = trajectoryData.reshape(batch, 9, 6)

#         # 将第4、5、6列的值都乘以10
#         reshaped_trajectoryData[:, :, 3:6]*= 10
#         # 完成初步分割與封裝後的軌跡資料
#         RPdata = reshaped_trajectoryData

#         # # 軌跡資料處理與分割(速度)
#         # # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
#         # quotient_vel, remainder_vel = divmod(velocityData.shape[0], 9)
#         # if remainder_vel != 0:
#         #     # 讀取最後一個Row的數據
#         #     last_row = velocityData[-1]

#         #     # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
#         #     padding = np.tile(last_row, (9 - remainder_vel, 1))

#         #     # 將需要填充的Row與原資料進行(Row堆疊)
#         #     padded_array = np.vstack((velocityData, padding))

#         #     # 將資料分割成以批次(一批次有9筆資料)為單位
#         #     reshaped_velocityData = padded_array.reshape(batch, 9)
#         # else:
#         #     # 將資料分割成以批次(一批次有9筆資料)為單位
#         #     reshaped_velocityData = velocityData.reshape(batch, 9)

#         # # 將所有值都乘以10(DX200的速度指令只接受整數，送入後會將數值自動*0.1，故發送前須將數值都乘以10)
#         # reshaped_velocityData *= 10
#         # Veldata = reshaped_velocityData

#         # # 完成初步分割與封裝後的軌跡(速度)資料
#         # Veldata = Veldata.astype(int)

#         Veldata =  velocityData[SpeedIndex]*10
#         Veldata = Veldata.astype(int)
    
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
        
#         # Velpacket =[Veldata[dataCount, 0], 
#         #             Veldata[dataCount, 1], 
#         #             Veldata[dataCount, 2], 
#         #             Veldata[dataCount, 3], 
#         #             Veldata[dataCount, 4], 
#         #             Veldata[dataCount, 5], 
#         #             Veldata[dataCount, 6], 
#         #             Veldata[dataCount, 7], 
#         #             Veldata[dataCount, 8]]
#         # Bypass
#         Velpacket = Veldata

#         return RPpacket, Velpacket
    
    
#     def writeRPvarINTvar(self, firstAddress, RPpacket, Velpacket):
#         """Write multiple variable data
#         - Args: RPdata, Veldata
#         """
#         Is_success = False
        
#         if self.Line is True:
#             RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
#             if self.WriteSpeedBypass >= 2:
#                 Istatus = []
#                 pass
#             else:
#                 # Istatus = self.Udp.multipleWriteVar(firstAddress, 9, Velpacket)
#                 # self.WriteSpeedBypass += 1
#                 pass
            
#         else:
#             # 靜態測試的模擬訊號
#             RPstatus = []
#             Istatus =[]

#         if RPstatus == [] and Istatus == []:
#             Is_success = True
#         else:
#             Is_success = False
        
#         return Is_success
    
    
#     def PlanNewTrj(self, NowEnd, GoalEnd, sampleTime, GoalSpeed):
#         """規劃新軌跡，時間線沿用舊軌跡
#         目的: 產生新軌跡, 並即時傳輸。
#         """
#         b = self.Time.ReadNowTime()

#         # 創造新軌跡
#         HomogeneousMatData, PoseMatData, SpeedData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, Velocity=GoalSpeed)
        
#         a = self.Time.ReadNowTime()
#         err = self.Time.TimeError(b, a)
#         print("計算新軌跡所花費的總時間: ", err["millisecond"], "ms")
#         costTime_PlanTrj = err["millisecond"]

#         return HomogeneousMatData, PoseMatData, SpeedData, TimeData, costTime_PlanTrj
    
#     def simulation(self, trjUpdataNBR):
#         d2r = np.deg2rad
#         b = self.Time.ReadNowTime()
#         newHomogeneousMat = database_HomogeneousMat.Load(f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{trjUpdataNBR}.csv")
#         nowJointAngle = (np.zeros((6,1)))
#         nowJointAngle[0, 0] =  d2r(-0.006)
#         nowJointAngle[1, 0] =  d2r(-38.8189)
#         nowJointAngle[2, 0] =  d2r(-41.0857)
#         nowJointAngle[3, 0] =  d2r(-0.0030)
#         nowJointAngle[4, 0] =  d2r(-76.4394)
#         nowJointAngle[5, 0] =  d2r(1.0687)
#         JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, newHomogeneousMat)
#         a = self.Time.ReadNowTime()
#         err = self.Time.TimeError(b, a)
#         print("關節角度計算所消耗的總時間: ", err["millisecond"], "ms")
#         database_JointAngle.Save(JointAngleData, f"dataBase/dynamicllyPlanTEST/JointAngle_{trjUpdataNBR}.csv", "w")
#         # self.Sim.paitGL(JointAngleData, newHomogeneousMat)


#     def feedbackRecords(self, sysTime):
#         """由機器手臂反饋回PC的數據紀錄
#         """
#         # 讀取實際手臂位置
#         pos_result, coordinate = self.Udp.getcoordinateMH(101)
#         # 儲存實際軌跡資料
#         self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([coordinate])
#         self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = sysTime
#         self.feedbackRecords_Counter += 1
        
    
#     def communicationRecords(self, RPdata, Veldata, alreadySentDataBatch, batch):
#         """通訊時用於紀錄通訊內容
#         """
#         # 紀錄通訊所傳輸的資料
#         if alreadySentDataBatch > batch-1:
#             pass
#         else:    
#             self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySentDataBatch]
#             # self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySentDataBatch]
#             # Bypass
#             self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata
            
#         self.communicationRecords_Counter += 1

#     def MergeTrj(self, oldTrjData:np.ndarray, oldSpeedData:np.ndarray, newData:list, alreadySentDataBatch:int):
#         """Trajectory data merge.

#         args: 
#             - oldTrjData(ndarray): 舊軌跡資料
#             - oldSpeedData(ndarray): 新軌跡資料
#             - newData: 新規劃好的結果
#             - alreadySentDataBatch: 已送出的軌跡點(批次)
        
#         return:
#             - mergeTrj(ndarray): 舊+新軌跡資料
#             - mergeSpeed(ndarray): 舊+新速度資料
#             - updataNode: 更新節點
            
#         """
#         # 新的軌跡與速度資料
#         newTrjData = newData[1]
#         newSpeedData = newData[2].reshape(-1, 1)
        

#         # 追蹤目前軌跡已送出的資料進度
#         alreadySentDataCount = alreadySentDataBatch*9

#         # 取出已送出的最後一筆當作目標樣本>>用於在新軌跡資料中找到最相近的資料
#         targetOldTrjData =  oldTrjData[alreadySentDataCount]
        
#         # 在新資料中找與目標資料最相近的資料與其索引值
#         mostSimilarTrjData, mostSimilarIndex = dataOperating.searchSimilarTrj(newTrjData, targetOldTrjData)

#         # 將舊資料已送出部分保留(軌跡)
#         oldTrj =  oldTrjData[:alreadySentDataCount]
#         # 將新資料最新一筆保持與舊資料最後一筆相似(軌跡)
#         newTrj = newTrjData[mostSimilarIndex:]
#         # 舊+新(軌跡)
#         mergeTrj = np.concatenate((oldTrj, newTrj), axis=0)

#         # 將舊資料已送出部分保留(速度)
#         oldSpeed =  oldSpeedData[:alreadySentDataCount]
#         # 將新資料最新一筆保持與舊資料最後一筆相似(速度)
#         newSpeed = newSpeedData[mostSimilarIndex:]
#         # 舊+新(速度)
#         mergeSpeed = np.concatenate((oldSpeed, newSpeed), axis=0)

#         return mergeTrj, mergeSpeed, mostSimilarIndex


#     def main(self):
#         #---------------------------------------------Inital-----------------------------------------------
#         # 初始化Pygame
#         pygame.init()

#         # 設置畫面寬高
#         screen_width = 800
#         screen_height = 600
#         screen = pygame.display.set_mode((screen_width, screen_height))
        
#         # 紀錄UDP目前已送出的資料批次數(1批 = 9筆)
#         alreadySentDataBatch = 0
#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0
#         startNode = 0
#         # 取樣時間
#         sampleTime = 0.1
#         # 系統時間初始化flag
#         sysflag = True
#         # 變軌跡次數
#         trjUpdataNBR = 0
#         Prv_trjUpdataNBR = 0
        
#         # 計算資料分割的組數與批數
#         batch = self.calculateDataGroupBatch(self.trjData)
        
#         # 資料分割
#         RPdata, Veldata = self.dataSegmentation(self.trjData, self.velData, batch)
        
#         # 包裝並寫入首9筆資料   
#         RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#         # Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
#         if self.Line is True:
#             RPstatus = self.Udp.multipleWriteRPVar(2, 9, RPpacket)
#             Istatus = self.Udp.WriteVar("Integer", 3, Velpacket[0])

#         # 紀錄通訊所送出的軌跡資料 | 用於驗證
#         self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#         # 資料(批次)計數器更新
#         alreadySentDataBatch += 1
        
        
#         # 軌跡規劃執行緒
#         Thread_started = False
#         planThread = GetNewTrj(target=self.PlanNewTrj)

#         # 軌跡資料儲存容器(驗證資料)
        
#         #-------------------------------------------------------------------------------------------------
        
#         # 測試通訊資料批次數
#         I3count = 0
#         I11count = 0
#         feedback_count = 0

#         # 更新位置變數時的時間點
#         updataTrjTime = self.Time.ReadNowTime()

#         # 時間限制
#         timeLimit = 100

#         # 互鎖
#         I2Lock = False
#         I11Lock = False

#         # 主迴圈旗標 | 開關
#         mainLoop = False
#         while True:
#             if self.Line is True:
#                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                 if np.linalg.norm(np.array(coordinate) - self.trjData[0, 0]) <= 0.05:
#                     print("------------------------------實測實驗開始------------------------------")
#                     print(f"軌跡開始位置: {coordinate}")
#                     mainLoop = True
#                     break
#             else:
#                 print("------------------------------模擬實驗開始------------------------------")
#                 mainLoop = True
#                 break
        
        
#         while mainLoop:
#             singlelooptime1 = self.Time.ReadNowTime()
#             # 更新每禎時間
#             nowTime = self.Time.ReadNowTime()
            
#             if sysflag is True:
#                 """
#                 此區在本迴圈只會在剛進迴圈時執行一次
#                 """
#                 # 儲存系統開始時間
#                 startTime = self.Time.ReadNowTime()

                
#                 if self.Line is True:
#                     # 取得I0初值
#                     # I0 = self.Udp.ReadVar("Integer", 0)
#                     I0 = [2]
#                     # 起始變數位置
#                     firstAddress = 11
#                     # 打包需要傳送的變數資料
#                     RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                     # 將打包完的資料寫入DX200
#                     # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
#                     RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)

#                     # 通訊紀錄
#                     self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#                     # 資料(批次)計數器更新
#                     alreadySentDataBatch += 1

#                     I11count+=1
                    
#                     # 紀錄feedback數據 | 紀錄初始位置與系統時間
#                     self.feedbackRecords(0)
#                 else:
#                     I0 = [2]

#                 sysflag = False
            
#             else:
#                 # 更新系統時間
                
#                 sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                 sysTime = round(sysTime/1000, 1)
                
#                 #----------------------------------------------命令執行區-----------------------------------------            
#                 if self.Line is True:
#                     # 更新距離上次更新軌跡時，又經過多久的時間
#                     b = self.Time.ReadNowTime()
#                     timeLeft = self.Time.TimeError(updataTrjTime, b)
#                     timeLeft_ms = timeLeft["millisecond"]
#                     print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取I0處")

#                     # I2Lock = True
#                     # I11Lock = True

#                     Prv_I0 = I0
#                     I0 = self.Udp.ReadVar("Integer", 0)
#                     # 將I0、PrvUpdataTime、SysTimer記錄下來
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 0] = I0[0]
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 1] = Prv_I0[0]
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 3] = timeLeft_ms
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 4] = sysTime
                    
#                     print(f"I000 : {I0}")
#                     """
#                     防止重複
#                     """
#                     if Prv_I0[0] != I0[0] and I0[0] == 2:
#                         I2Lock = True
#                         self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 2] = 1
#                         # print(f"I0: {I0}，允許寫入I11-I19")
#                     elif Prv_I0[0] != I0[0] and I0[0] == 11:
#                         I11Lock = True
#                         self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 2] = 1
#                         # print(f"I0: {I0}，允許寫入I02-I10")
#                     else:
#                         self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 2] = 0
#                         pass
#                         # print(f"上次的I0與本次I0相同，不允許寫入。")

#                 else:
#                     # 模擬I0變換
#                     if I0[0] == 11:
#                         I0 = [2]
#                         I2Lock = True
#                     elif I0[0] == 2:
#                         I0 = [11]
#                         I11Lock = True
#                 #----------------------------------------------資料通訊區-----------------------------------------
#                 """
#                 通訊
#                 * 變數區間:
#                 1. I02 - I10
#                 2. I11 - I19
#                 """
                
#                 if I2Lock is True:
#                 # if I0 == [2] :
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 5] = sysTime
                    
#                     I2_b = self.Time.ReadNowTime()

#                     # 起始變數位置
#                     firstAddress = 11
#                     # 打包需要傳送的變數資料
#                     RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                     # 將打包完的資料寫入DX200
#                     # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
#                     if self.Line is True:
#                         RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                    
#                     # 通訊紀錄
#                     self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#                     # 資料(批次)計數器更新
#                     alreadySentDataBatch += 1

#                     if self.Line is False:
#                         # 模擬軌跡時間
#                         self.Time.time_sleep(0.36)

#                     I2_a = self.Time.ReadNowTime()
#                     I2err = self.Time.TimeError(I2_b, I2_a)
#                     I2err_ms = I2err["millisecond"]
#                     # print(f"更新I11-I20的軌跡資料花費時間: {I2err_ms}ms")

#                     # 紀錄送軌跡所花費的時間與變數區間
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 6] = I2err_ms
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 7] = 2
#                     self.I0AndPrvUpdataTimeAndSysTimeCounter += 1

#                     # 紀錄軌跡更新時間
#                     updataTrjTime = self.Time.ReadNowTime()

#                     I11count+=1
#                     I2Lock = False
                    

#                 elif I11Lock is True:
#                 # elif I0 == [11] :
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 5] = sysTime
#                     I11_b = self.Time.ReadNowTime()

#                     # 起始變數位置
#                     firstAddress = 2
#                     # 打包需要傳送的變數資料
#                     RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
#                     # 將打包完的資料寫入DX200
#                     # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
#                     if self.Line is True:
#                         RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)

#                     # 通訊紀錄
#                     self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
#                     # 資料(批次)計數器更新
#                     alreadySentDataBatch += 1

#                     if self.Line is False:
#                         # 模擬軌跡時間
#                         self.Time.time_sleep(0.36)
                        
#                     I11_a = self.Time.ReadNowTime()
#                     I11_err = self.Time.TimeError(I11_b, I11_a)
#                     I11_err_ms = I11_err["millisecond"]
#                     # print(f"更新I02-I10的軌跡資料花費時間: {I11_err_ms}ms")

#                     # 紀錄送軌跡所花費的時間與變數區間
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 6] = I11_err_ms
#                     self.I0AndPrvUpdataTimeAndSysTime[self.I0AndPrvUpdataTimeAndSysTimeCounter, 7] = 1
#                     self.I0AndPrvUpdataTimeAndSysTimeCounter += 1

#                     # 紀錄軌跡更新時間
#                     updataTrjTime = self.Time.ReadNowTime()

#                     I3count+=1
#                     I11Lock = False

#                 else:
#                     self.I0AndPrvUpdataTimeAndSysTimeCounter += 1
#                     if self.Line is True:
#                         # 更新距離上次更新軌跡時，又經過多久的時間
#                         b = self.Time.ReadNowTime()
#                         timeLeft = self.Time.TimeError(updataTrjTime, b)
#                         timeLeft_ms = timeLeft["millisecond"]
#                         # print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取feedback資料處")
#                         # 紀錄feedback數據
#                         self.feedbackRecords(sysTime)
#                         feedback_count+=1

#                         # if timeLeft_ms <= timeLimit:
#                         #     # 紀錄feedback數據
#                         #     self.feedbackRecords(sysTime)
#                         #     feedback_count+=1
#                         #     print(f"feedback寫入次數: {feedback_count}次")
#                         # elif timeLeft_ms > timeLimit :
#                         #     print("已鄰近下次需要更新軌跡的時間，略過讀取feedback數據動作。")
#                         #     pass
                        
#                         # else:
#                         #     pass
                   
                
#                 if alreadySentDataBatch == batch:
#                     """結束條件
#                     外迴圈數 = 批次數
#                     """
                
#                     # -------------------------------------通訊資紀錄與feedback紀錄 | 處理與存檔-----------------------------------
#                     # 讀取最後一刻軌跡資料       
#                     if self.Line is True:
#                         can_End = False
#                         while True:
#                             # 讀取I000變數
#                             I0 = self.Udp.ReadVar("Integer", 0)

#                             # 更新系統時間
#                             nowTime = self.Time.ReadNowTime()
#                             # 取得系統時間
#                             sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                             sysTime = round(sysTime/1000, 1)

#                             # 紀錄feedback數據
#                             self.feedbackRecords(sysTime)
#                             feedback_count+=1
#                             print(f"feedback寫入次數: {feedback_count}次")

#                             # 判斷此筆軌跡資料的I0會停留在I0=11還是I0=2
#                             quotient, remainder = divmod(RPdata.shape[0]*RPdata.shape[1], 18)
                            
#                             if remainder == 9 and I0 == [11]:
#                                 can_End = True
#                             elif remainder == 0 and I0 == [2]:
#                                 can_End = True
#                             else: 
#                                 can_End = False
                                
#                             if can_End is True:
#                                 # feedback的軌跡資料
#                                 # 濾除整個row為0的部分
#                                 non_zero_rows_Trajectory = np.any(self.feedbackRecords_Trj != 0, axis=(1, 2))
#                                 non_zero_rows_Time = np.any(self.feedbackRecords_sysTime != 0, axis=1)
#                                 # 系統時間需保留初值0
#                                 non_zero_rows_Time[:2] = True

#                                 self.feedbackRecords_Trj = self.feedbackRecords_Trj[non_zero_rows_Trajectory]
#                                 self.feedbackRecords_sysTime = self.feedbackRecords_sysTime[non_zero_rows_Time]
                                
#                                 database_PoseMat.Save(self.feedbackRecords_Trj, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj.csv", "w")
#                                 database_time.Save(self.feedbackRecords_sysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_sysTime.csv", "w")
                                
#                                 # 儲存通訊所送出的軌跡資料
#                                 self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
#                                 self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
#                                 # 濾除整個row為0的部分
#                                 non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
#                                 non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
#                                 non_zero_rows_costTime = np.any(self.costTime != 0, axis=1)

#                                 self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
#                                 self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
#                                 self.costTime = self.costTime[non_zero_rows_costTime]
#                                 mode = "w"
#                                 database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
#                                 database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
#                                 database_time.Save_costTime(self.costTime, "dataBase/dynamicllyPlanTEST/costTime.csv", mode)
                                
#                                 # 儲存 I0、PrvUdpataTime、SysTime紀錄(Debug)
#                                 non_zero_rows_I0AndPrvUpdataTimeAndSysTime = np.any(self.I0AndPrvUpdataTimeAndSysTime != 0, axis=1)
#                                 self.I0AndPrvUpdataTimeAndSysTime = self.I0AndPrvUpdataTimeAndSysTime[non_zero_rows_I0AndPrvUpdataTimeAndSysTime]
#                                 database_time.Save_I0AndPrvUpdataTimeAndSysTime(self.I0AndPrvUpdataTimeAndSysTime, "dataBase/dynamicllyPlanTEST/I0AndPrvUpdataTimeAndSysTime.csv", mode)
#                                 break
#                     else:
#                         self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
#                         self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
#                         # 濾除整個row為0的部分
#                         non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
#                         non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
#                         non_zero_rows_costTime = np.any(self.costTime != 0, axis=1)

#                         self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
#                         self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
#                         self.costTime = self.costTime[non_zero_rows_costTime]
#                         mode = "w"
#                         database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
#                         database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
#                         database_time.Save_costTime(self.costTime, "dataBase/dynamicllyPlanTEST/costTime.csv", mode)
                    
#                     print(f"I2批次有{I3count+1}批，I11批次有{I11count}批")
#                     print(f"軌跡實驗結束，共花費 {sysTime} ms")
#                     break
#                 #----------------------------------------------鍵盤事件區-----------------------------------------
#                 for event in pygame.event.get():
#                     if event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_u:
#                             """動態修改銲接參數
#                             AC:   I21
#                             AVP : I22
#                             """
#                             AC = 50
#                             AVP = 50
#                             status = self.changeWeldingPartmeter(AC, AVP)

#                         elif event.key == pygame.K_p:
#                             """
#                             獲得新速度軌跡
#                             """
#                             # 創建線程
#                             # 開始重新規劃新軌跡時，紀錄舊軌跡已經寫入的資料筆數       
#                             startPlan_alreadySentDataBatch = alreadySentDataBatch
                            
#                             if self.Line is True:
#                                 # 讀取當下位置
#                                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                                 # 設定新軌跡起點
#                                 NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]
#                             else:
#                                 # 模擬讀取當下位置
#                                 coordinate = RPdata[startPlan_alreadySentDataBatch, 0]
#                                 # 設定新軌跡起點
#                                 NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3]/10, coordinate[4]/10, coordinate[5]/10]

#                             # 終點與原軌跡保持一致
#                             GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                            
#                             # GoalSpeed = float(input("請輸入走速："))
#                             # print(f"理想速度: {GoalSpeed} mm/s")

#                             GoalSpeed = 5
                            
#                             # 執行緒
#                             planThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, GoalSpeed))
#                             planThread.start()

#                             # 改變狀態旗標>>> 執行續已被啟動過
#                             Thread_started = True
                        
#                         elif event.key == pygame.K_o:
#                             """
#                             獲得新速度軌跡
#                             """
#                             # 創建線程
#                             # 開始重新規劃新軌跡時，紀錄舊軌跡已經寫入的資料筆數       
#                             startPlan_alreadySentDataBatch = alreadySentDataBatch
                            
#                             if self.Line is True:
#                                 # 讀取當下位置
#                                 pos_result, coordinate = self.Udp.getcoordinateMH(101)
#                                 # 設定新軌跡起點
#                                 NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]
#                             else:
#                                 # 模擬讀取當下位置
#                                 coordinate = RPdata[startPlan_alreadySentDataBatch, 0]
#                                 # 設定新軌跡起點
#                                 NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3]/10, coordinate[4]/10, coordinate[5]/10]

#                             # 終點與原軌跡保持一致
#                             GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                        
#                             GoalSpeed = 2
                            
#                             # 執行緒
#                             planThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, GoalSpeed))
#                             planThread.start()

#                             # 改變狀態旗標>>> 執行續已被啟動過
#                             Thread_started = True
                            
#                 if planThread.is_alive() is False and Thread_started is True:
#                     # 軌跡已變化一次，需更新計數器值
#                     trjUpdataNBR += 1

#                     # 取出執行緒計算結果
#                     b = self.Time.ReadNowTime()
#                     result = planThread.get_result()
                    
#                     NewHomogeneousMat = result[0]
#                     NewPoseMatData = result[1]
#                     NewSpeedData = result[2]
#                     NewTimeData = result[3]
#                     costTime_PlanTrj = result[4]

#                     print(f"新軌跡資料長度:{NewHomogeneousMat.shape}")
#                     # 存檔(新軌跡資料) 
#                     mode = "w"
#                     database_HomogeneousMat.Save(NewHomogeneousMat, f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{trjUpdataNBR}.csv", mode)
#                     database_PoseMat.Save(NewPoseMatData, f"dataBase/dynamicllyPlanTEST/PoseMat_{trjUpdataNBR}.csv", mode)
#                     database_Velocity.Save(NewSpeedData, f"dataBase/dynamicllyPlanTEST/Speed_{trjUpdataNBR}.csv", mode)
#                     database_time.Save(NewTimeData,f"dataBase/dynamicllyPlanTEST/Time_{trjUpdataNBR}.csv", mode)
                    
#                     # 規劃完時，紀錄舊軌跡已經寫入的資料批數
#                     endPlan_alreadySentDataBatch = alreadySentDataBatch
#                     # 計算規劃時，時間差所產生的資料落後批數
#                     dataErr = endPlan_alreadySentDataBatch-startPlan_alreadySentDataBatch
#                     print("系統反應時間所消耗的資料(批次)數: ", dataErr)

#                     # mergeTrj, mergeSpeed, mostSimilarIndex = self.MergeTrj(self.trjData, self.velData, result, endPlan_alreadySentDataBatch)
#                     # -----------------------------------資料整併(軌跡)--------------------------------------------------------------
#                     allFile_PoseMat = "dataBase/dynamicllyPlanTEST/Remix_PoseMat_all.csv"
#                     oldFile_PoseMat = f"dataBase/dynamicllyPlanTEST/PoseMat_{Prv_trjUpdataNBR}.csv"
#                     newFile_PoseMat = f"dataBase/dynamicllyPlanTEST/PoseMat_{trjUpdataNBR}.csv"
#                     RemixFile_PoseMat = f"dataBase/dynamicllyPlanTEST/Remix_PoseMat_{Prv_trjUpdataNBR}_{trjUpdataNBR}.csv"
#                     data_frame1 = pd.read_csv(oldFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
#                     data_frame2 = pd.read_csv(newFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
#                     # 取得舊資料切換新資料時的最後一筆資料
#                     # 提取舊資料
#                     oldFileIndex = endPlan_alreadySentDataBatch*9
#                     dfBuffer1 = data_frame1.iloc[:oldFileIndex]
#                     # 找出目前舊資料已送出的最後一筆資料 與 新資料中哪一筆資料 最相似
#                     targetData = data_frame1.iloc[oldFileIndex]
#                     closestData, closestIndex = dataOperating.searchSimilar(data_frame2, targetData)
#                     # 要合併的新資料
#                     dfBuffer2 = data_frame2.iloc[closestIndex+1:]
#                     # 紀錄本次新軌跡的合併資料節點
#                     self.mergeNode[trjUpdataNBR] = oldFileIndex
#                     # 新舊合併
#                     Remix_PoseMat_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
#                     # 存檔
#                     Remix_PoseMat_df.to_csv(RemixFile_PoseMat, index=False,  header=True)
#                     if trjUpdataNBR == 1:
#                         Remix_PoseMat_df.to_csv(allFile_PoseMat, index=False,  header=True)
#                     elif trjUpdataNBR > 1:
#                         all_PathData_frame = pd.read_csv(allFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
#                         # 本次要合併的新資料
#                         allPathDf = all_PathData_frame.iloc[:oldFileIndex]
#                         dfBuffer2 = data_frame2.iloc[closestIndex+1:]
#                         # 新舊合併
#                         RemixAll_PoseMat_df = pd.concat([allPathDf, dfBuffer2], axis=0)
#                         RemixAll_PoseMat_df.to_csv(allFile_PoseMat, index=False,  header=True)
                        
#                     # 轉為可用型別
#                     Remix_PoseMat = np.array(Remix_PoseMat_df).reshape(-1, 1, 6)
#                     # --------------------------------------------------------------------------------------------------------------

#                     # -----------------------------------資料整併(速度)--------------------------------------------------------------
#                     allFile_Speed = "dataBase/dynamicllyPlanTEST/Remix_Speed_all.csv"
#                     oldFile_Speed = f"dataBase/dynamicllyPlanTEST/Speed_{Prv_trjUpdataNBR}.csv"
#                     newFile_Speed = f"dataBase/dynamicllyPlanTEST/Speed_{trjUpdataNBR}.csv"
#                     RemixFile_Speed = f"dataBase/dynamicllyPlanTEST/Remix_Speed_{Prv_trjUpdataNBR}_{trjUpdataNBR}.csv"
#                     data_frame1 = pd.read_csv(oldFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
#                     data_frame2 = pd.read_csv(newFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
                    
#                     # 軌跡已變化一次，將上一個軌跡檔編號也須更新
#                     Prv_trjUpdataNBR += 1

#                     # 取得舊資料切換新資料時的最後一筆資料
#                     # 提取舊資料
#                     oldFileIndex = endPlan_alreadySentDataBatch*9
#                     dfBuffer1 = data_frame1.iloc[:oldFileIndex]
#                     # 找相似的資料
#                     # targetData = data_frame1.iloc[oldFileIndex]
#                     # 要合併的新資料
#                     dfBuffer2 = data_frame2.iloc[closestIndex+1:]
#                     Remix_Speed_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
#                     Remix_Speed_df.to_csv(RemixFile_Speed, index=False,  header=True)
#                     Remix_Speed = np.array(Remix_Speed_df)
#                     if trjUpdataNBR == 1:
#                         Remix_PoseMat_df.to_csv(allFile_Speed, index=False,  header=True)
#                     elif trjUpdataNBR > 1:
#                         all_SpeedData_frame = pd.read_csv(allFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
#                         # 本次要合併的新資料
#                         allSpeedDf = all_SpeedData_frame.iloc[:oldFileIndex]
#                         dfBuffer2 = data_frame2.iloc[closestIndex+1:]
#                         # 新舊合併
#                         RemixAll_Speed_df = pd.concat([allSpeedDf, dfBuffer2], axis=0)
#                         RemixAll_Speed_df.to_csv(allFile_Speed, index=False,  header=True)
#                     # --------------------------------------------------------------------------------------------------------------

#                     # 將物件變數中的軌跡資料替換為新的軌跡資料
#                     self.trjData = Remix_PoseMat
#                     self.velData = mergeSpeed
                    
#                     # 固定流程(資料分割與初步封裝)
#                     Remix_PoseMat, Remix_Speed = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)
#                     NewRemixBatch = self.calculateDataGroupBatch(Remix_PoseMat)
#                     NewRemixRPdata, NewRemixSpeeddata = self.dataSegmentation(Remix_PoseMat, Remix_Speed, NewRemixBatch, oldFileIndex+1)
#                     # 更新速度
#                     if self.Line is True:
#                         """
#                         I002 : VJ
#                         I003 : V
#                         I004 : VR
#                         """
#                         self.Udp.WriteVar("Integer", 3, NewRemixSpeeddata[0])
#                         NewSpeed = NewRemixSpeeddata[0]*0.1
#                         print(f"速度已更新為:{NewSpeed}")
#                     else:
#                         NewSpeed = NewRemixSpeeddata[0]*0.1
#                         print(f"速度已更新為:{NewSpeed}mm/s")
#                     # --------------------------------------------------------------------------------------------------------------
                    
#                     # 使用合併後的軌跡檔案(已分割與封裝)，覆蓋原始的軌跡資料
#                     RPdata = NewRemixRPdata
#                     Veldata = NewRemixSpeeddata
                    
#                     # 更新資料計數器，因使用合併後的軌跡檔案，故將計數器的值加上[計算新軌跡所花費的總時間(以批次計算)]
#                     # alreadySentDataBatch -= dataErr
#                     """
#                     經實驗證實，若系統反應時間不超過1批資料時間，即可不用特別更新[資料批次計數]之批次數
#                     """
#                     # 更新Batch，將總批次數更新成與合併後的軌跡檔案相符的
#                     batch = NewRemixBatch
                    
#                     Thread_started = False
#                     print("--------------新軌跡資料已覆寫---------------")

#                     a = self.Time.ReadNowTime()
#                     err = self.Time.TimeError(b,a)
#                     costTime_dataMerge = err["millisecond"]
#                     print(f"新軌跡規劃後處理所花時長: {costTime_dataMerge} ms")

#                     self.costTime[self.costTimeDataCounter, 0] = costTime_PlanTrj
#                     self.costTime[self.costTimeDataCounter, 1] = costTime_dataMerge

#                     # 計算IK
#                     SimThread = threading.Thread(target=self.simulation, args=(trjUpdataNBR,))
#                     SimThread.start()
#                 #-----------------------------------------------------------------------------------------------
#                 singlelooptime2 = self.Time.ReadNowTime()
#                 singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#                 # singleloopCosttime_ms = singleloopCosttime["millisecond"]
#                 # print(f"單個迴圈花費 {singleloopCosttime_ms} ms")

#                 # 剩餘時間
#                 laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
#                 # self.Time.time_sleep(laveTime*0.001)
            
# if __name__ == "__main__":


#     trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
#     speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
#     Motomancontrol(trjdataPath, speeddataPath).main()
"""
- 版本: 2.0
- 名稱: 動態軌跡規劃與通訊架構(模擬實驗架構)
- 更新日期: 20240523
- 搭配的INFORM檔名: RUN_TRJ_MAINCODE

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
from WeldingModel import *


class GetTreadResult(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._result = None

    def run(self):
        self._result = self._target(*self._args)

    def get_result(self):
        return self._result

class Motomancontrol():
    def __init__(self, TrjdatafilePath, VeldatafilePath):
        self.Kin = Kinematics()
        self.Time = TimeTool()
        self.Sim = Simulator()
        self.Udp = MotomanUDP()

        # 載入軌跡檔案
        self.trjData = database_PoseMat.Load(TrjdatafilePath)
        self.velData = database_Velocity.Load(VeldatafilePath)
        # 刪除軌跡資料第一筆資料
        self.trjData, self.velData = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)

        # ----------------------------------------------------------------狀態與初始參數設定區----------------------------------------------------------------
        # --------------------狀態預設區--------------------
        """
        Online(含通訊之測試) >> True  
        Offline(純邏輯測試) >> False
        """
        self.Line = True
        """
        軌跡速度補償系統:
        開啟 >> True  
        關閉 >> False
        """
        # 速度補償值(要X10，需要補償0.3mm/s，要輸入0.3X10 = 3)
        self.compensationSpeed = 0
        # 動態速度補償功能
        self.compensationSpeedFUN = False
        """
        軌跡資料傳送Bypass
        Online 且 傳送軌跡資料 >> True
        Online 但不 傳送軌跡資料 >> False
        """
        self.sentTrjData = True

        """
        資料儲存路徑
        """
        # 資料夾名稱
        # self.FolderPath = "dataBase/dynamicllyPlanTEST/"
        self.FolderPath = "dataBase/BoxWelding/"
        # 第幾個軌跡檔案(取軌跡檔名的編號)
        self.dataNumber = int(TrjdatafilePath[-5])

        """
        多段銲接任務 軌跡過渡起點
        """
        if self.dataNumber == 0:
            # 第一段軌跡 過渡至 第二段軌跡起點
            self.transitionTrjStart = [1014.632, 38.764, -136.986, 151.068, -25.1213, -138.0066]
            # 第二段軌跡起點
            self.transitionTrjEnd = [1013.994, 49.756, -136.167, 151.5514, -25.0542, -63.4091]
        
        else:
            # 第三段軌跡 過渡至 第四段軌跡起點
            self.transitionTrjStart = [866.791, -90.01, -137.035, 151.5799, -25.2112, 30.1944]
            # 第四段軌跡起點
            self.transitionTrjEnd = [868.589, -102.76, -136.791, 162.5575, 7.1226, 105.8818]
        # 是否已停止送絲一次:  從未停只過>>False;有停過一次>>True
        self.stopSentWire = False
        self.allTrjEnd = False
        

            
        """
        軌跡資料單位:
        9筆=1批, 2批=1組

        # 軌跡資料發送(機器人程式相關)
        I0:  資料筆數index(機器人程式迴圈index)
        I1:  資料總批數(資料總筆數/9)(batch)
        I28: 已執行或正在執行的軌跡資料批次數
        I29: 機器人程式迴圈控制旗標(控制結束)

        # 變速度
        I3: 運動速度1
        I4: 控制位元
        I5: 運動速度2

        # 變電流、填料速度
        I21 : 銲接電流 AC
        I22 : 填料速度 AVP
        """
        # --------------------預設參數區--------------------
        # 機器人程式運行相關變數
        self.I0 = 2
        self.I1 = 0
        self.I28 = 0

        # 變電流參數
        self.AC = 50
        self.AVP = 50

        # 預設銲接速度
        self.GoalSpeed = 1.5
        # 軌跡速度切換旗標
        self.variableSpeedFlag = 0

        # 預設銲道寬度
        self.weldBeadWidth = 4.7


        if self.Line is True:
            mWTrjData_Status = self.Udp.multipleWriteVar(0, 2, [self.I0, self.I1])
            wI28_Status = self.Udp.WriteVar("Integer", 28, 0)
            mWParam_Status = self.Udp.multipleWriteVar(21, 2, [self.AC, self.AVP])
            wI29_Status = self.Udp.WriteVar("Integer", 29, 0)
            wI4_Statu = self.Udp.WriteVar("Integer", 4, 0)
            if mWTrjData_Status==[] and wI28_Status==[] and mWParam_Status==[] and wI29_Status==[] and wI4_Statu==[]:
                print("初始參數已成功寫入DX200")
            else:
                print("初始參數位寫入失敗!!!")
        else:
            print("初始參數已寫入DX200")

        # ----------------------------------------------------------------各種紀錄變數初始化區----------------------------------------------------------------

        # 銲接電流紀錄
        self.arcCurrentRecards = np.zeros((1000, 1))
        self.arcCurrentRecards[0, 0] = self.AC
        self.arcCurrentRecards_counter = 1

        # 銲道寬度變更紀錄
        self.weldBeadWidthRecards = np.zeros((1000, 5))
        self.weldBeadWidthRecards[0, 0] = self.weldBeadWidth
        self.weldBeadWidthRecards[0, 1] = self.GoalSpeed
        self.weldBeadWidthRecards[0, 2] = self.AC
        self.weldBeadWidthRecards[0, 3] = self.AVP
        self.weldBeadWidthRecards[0, 4] = 0
        self.weldBeadWidthRecards_counter = 1

        # PC >> DX200 通訊紀錄
        self.communicationRecords_Trj = np.zeros((50000, 9, 6))
        self.communicationRecords_Speed = np.zeros((50000, 9))
        self.communicationRecords_Counter = 0

        # DX200 feedback的手臂資料紀錄-位姿矩陣
        self.feedbackRecords_Trj = np.zeros((50000, 1, 6)) 
        self.feedbackRecords_sysTime = np.zeros((50000, 1))
        # DX200 feedback的手臂資料紀錄-關節角度
        self.feedbackRecords_MotorPulse = np.zeros((50000, 1, 6)) 
        self.feedbackRecords_JointAngle = np.zeros((50000, 1, 6)) 
        self.feedbackRecords_Counter = 0

        # 紀錄軌跡終點、feedback最後一筆位姿做為程式結束條件
        self.NowEndEffector = np.zeros(6)
        self.Goal = np.array([self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2]])

        # 規劃新軌跡 各工作階段所花費的時間
        """
        Cost Time = ["Trj_Algorithm", "Data_merge", "IK_Iterate"]
        """
        self.costTime = np.zeros((100, 3))
        self.costTimeDataCounter = 0

        # I0驗證系統
        """
        迴圈事件紀錄
        I0、PrvUpdataTime、SysTime :[I0, PrvUpdataTime, SysTime]
        """
        self.EventRecord = np.zeros((50000, 8))
        self.EventRecordCounter = 0
        
        self.WriteSpeedBypass = 0

        # 封包發送問題紀錄
        """
        紀錄格式:[發送軌跡的區間編號(2 or 11), 發送狀態(成功(0) or 失敗(1), 系統時間(ms))]
        """
        self.packetSent_isSuccessRecord = np.zeros((5000, 3))
        self.packetSent_isSuccessRecord_counter = 0

        # 關節角度紀錄
        self.JointAngleRecords = np.zeros((50000, 1, 6))

        # IK迭代執行續旗標(用於中斷)
        self.IKisRunning = False


        # 速度監測
        # 期望速度
        self.exceptSpeed = 0
        # 需補償的速度 = 期望速度-實際速度
        self.speedCompensate = 0
        # 紀錄上次補償的速度
        self.PrvSpeed = 0
        self.speedBuffer = np.zeros((100))
        self.SpeedDatacounter = 0


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
    
    def dataSegmentation(self, trajectoryData, velocityData, batch, SpeedIndex=0):
        """
        資料分批處理
        單位: 9筆/批
        """
        
        """資料分割演算法
        1.判斷原資料(m*1*6)是否可完整切個為shape(n*9*6), m=該資料原本的筆數; n= m/9.
        2.若第一步中發現有不足9筆需要補齊資料，使用最後一筆資料補齊剩下的缺口.
        3.補齊後，將資料切割為(n*9*6).
        """
        # 防止竄改到來源
        trajectory = np.copy(trajectoryData)
        # 軌跡資料處理與分割
        # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
        quotient_trj, remainder_trj = divmod(trajectory.shape[0], 9)
        if remainder_trj != 0:
            # 讀取最後一個Row的數據
            last_row = trajectory[-1]

            # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
            padding = np.tile(last_row, (9 - remainder_trj, 1, 1))

            # 將需要填充的Row與原資料進行(Row堆疊)
            padded_array = np.vstack((trajectory, padding))

            # 將資料分割成以批次(一批次有9筆資料)為單位
            reshaped_trajectory = padded_array.reshape(batch, 9, 6)
        else:
            # 將資料分割成以批次(一批次有9筆資料)為單位
            reshaped_trajectory = trajectory.reshape(batch, 9, 6)

        # 将第4、5、6列的值都乘以10
        reshaped_trajectory[:, :, 3:6]*= 10
        # 完成初步分割與封裝後的軌跡資料
        RPdata = reshaped_trajectory

        # # 軌跡資料處理與分割(速度)
        # # 計算是否需要補齊資料與資料分割批次數(9筆為1批)
        # quotient_vel, remainder_vel = divmod(velocityData.shape[0], 9)
        # if remainder_vel != 0:
        #     # 讀取最後一個Row的數據
        #     last_row = velocityData[-1]

        #     # 產生用於填滿最後一個Row(筆)的數據(當該layer不滿9個row時)
        #     padding = np.tile(last_row, (9 - remainder_vel, 1))

        #     # 將需要填充的Row與原資料進行(Row堆疊)
        #     padded_array = np.vstack((velocityData, padding))

        #     # 將資料分割成以批次(一批次有9筆資料)為單位
        #     reshaped_velocityData = padded_array.reshape(batch, 9)
        # else:
        #     # 將資料分割成以批次(一批次有9筆資料)為單位
        #     reshaped_velocityData = velocityData.reshape(batch, 9)

        # # 將所有值都乘以10(DX200的速度指令只接受整數，送入後會將數值自動*0.1，故發送前須將數值都乘以10)
        # reshaped_velocityData *= 10
        # Veldata = reshaped_velocityData

        # # 完成初步分割與封裝後的軌跡(速度)資料
        # Veldata = Veldata.astype(int)
       
        # 防止竄改到來源
        velocity = np.copy(velocityData)
        # 最後一項是速度補償值
        # 依期望速度判斷 補償值
        if velocity[SpeedIndex]*10 <=13:
            self.compensationSpeed = 2
        elif velocity[SpeedIndex]*10 >13 and velocity[SpeedIndex]*10 <=22:
            self.compensationSpeed = 3
        else:
            self.compensationSpeed = 0
            print("速度補償值未確定，先歸0")
        Veldata =  velocity[SpeedIndex]*10+self.compensationSpeed
        Veldata = Veldata.astype(int)
    
        return RPdata, Veldata
    
    @staticmethod
    def packetRPdataVeldata(RPdata, Veldata, dataCount):
        """將一批軌跡與速度資料包裝成可發送的形式
        - Args: RPdata、Veldata、datacount
            - datacount: 已送出多少批資料的計數器值
        """

        RPpacket = {'0':[17, 0, 5, 0, RPdata[dataCount][0][0], RPdata[dataCount][0][1], RPdata[dataCount][0][2], RPdata[dataCount][0][3], RPdata[dataCount][0][4], RPdata[dataCount][0][5]],
                    '1':[17, 0, 5, 0, RPdata[dataCount][1][0], RPdata[dataCount][1][1], RPdata[dataCount][1][2], RPdata[dataCount][1][3], RPdata[dataCount][1][4], RPdata[dataCount][1][5]],
                    '2':[17, 0, 5, 0, RPdata[dataCount][2][0], RPdata[dataCount][2][1], RPdata[dataCount][2][2], RPdata[dataCount][2][3], RPdata[dataCount][2][4], RPdata[dataCount][2][5]],
                    '3':[17, 0, 5, 0, RPdata[dataCount][3][0], RPdata[dataCount][3][1], RPdata[dataCount][3][2], RPdata[dataCount][3][3], RPdata[dataCount][3][4], RPdata[dataCount][3][5]],
                    '4':[17, 0, 5, 0, RPdata[dataCount][4][0], RPdata[dataCount][4][1], RPdata[dataCount][4][2], RPdata[dataCount][4][3], RPdata[dataCount][4][4], RPdata[dataCount][4][5]],
                    '5':[17, 0, 5, 0, RPdata[dataCount][5][0], RPdata[dataCount][5][1], RPdata[dataCount][5][2], RPdata[dataCount][5][3], RPdata[dataCount][5][4], RPdata[dataCount][5][5]],
                    '6':[17, 0, 5, 0, RPdata[dataCount][6][0], RPdata[dataCount][6][1], RPdata[dataCount][6][2], RPdata[dataCount][6][3], RPdata[dataCount][6][4], RPdata[dataCount][6][5]],
                    '7':[17, 0, 5, 0, RPdata[dataCount][7][0], RPdata[dataCount][7][1], RPdata[dataCount][7][2], RPdata[dataCount][7][3], RPdata[dataCount][7][4], RPdata[dataCount][7][5]],
                    '8':[17, 0, 5, 0, RPdata[dataCount][8][0], RPdata[dataCount][8][1], RPdata[dataCount][8][2], RPdata[dataCount][8][3], RPdata[dataCount][8][4], RPdata[dataCount][8][5]]}
        
        # Velpacket =[Veldata[dataCount, 0], 
        #             Veldata[dataCount, 1], 
        #             Veldata[dataCount, 2], 
        #             Veldata[dataCount, 3], 
        #             Veldata[dataCount, 4], 
        #             Veldata[dataCount, 5], 
        #             Veldata[dataCount, 6], 
        #             Veldata[dataCount, 7], 
        #             Veldata[dataCount, 8]]
        # Bypass
        Velpacket = Veldata

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
                # Istatus = self.Udp.multipleWriteVar(firstAddress, 9, Velpacket)
                # self.WriteSpeedBypass += 1
                pass
            
        else:
            # 靜態測試的模擬訊號
            RPstatus = []
            Istatus =[]

        if RPstatus == [] and Istatus == []:
            Is_success = True
        else:
            Is_success = False
        
        return Is_success
    
    def updataTrjSpeed(self, needUpdataSpeed):
        """軌跡速度變更

        """
        if self.variableSpeedFlag == 0:
            """
            目前機器人程式的速度取自I3:
            - 須將速度旗標I4切換至1
            - 把新速度軌跡送至I5
            """
            if self.Line:
                self.variableSpeedFlag = 1
                firstAddress  = 4
                Number = 2
                data = [self.variableSpeedFlag, needUpdataSpeed]
                status = self.Udp.multipleWriteVar(firstAddress, Number, data)
            else:
                self.variableSpeedFlag = 1
                status = []
        else:
            """
            目前機器人程式的速度取自I5:
            - 須將速度旗標I4切換至0
            - 把新速度軌跡送至I3
            """
            self.variableSpeedFlag = 0
            if self.Line:
                firstAddress  = 3
                Number = 2
                data = [needUpdataSpeed, self.variableSpeedFlag]
                status = self.Udp.multipleWriteVar(firstAddress, Number, data)
            else:
                self.variableSpeedFlag = 0
                status = []
                

        return status
    
    
    def PlanNewTrj(self, NowEnd, GoalEnd, sampleTime, GoalSpeed):
        """規劃新軌跡，時間線沿用舊軌跡
        目的: 產生新軌跡, 並即時傳輸。
        """
        b = self.Time.ReadNowTime()

        # 創造新軌跡
        HomogeneousMatData, PoseMatData, SpeedData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, Velocity=GoalSpeed)
        
        a = self.Time.ReadNowTime()
        err = self.Time.TimeError(b, a)
        print("計算新軌跡所花費的總時間: ", err["millisecond"], "ms")
        costTime_PlanTrj = err["millisecond"]

        return HomogeneousMatData, PoseMatData, SpeedData, TimeData, costTime_PlanTrj
    
    def simulation(self, trjUpdataNBR, newHomogeneousMat):
        d2r = np.deg2rad
        b = self.Time.ReadNowTime()
        
        # nowJointAngle = (np.zeros((6,1)))
        # nowJointAngle[0, 0] =  d2r(-0.006)
        # nowJointAngle[1, 0] =  d2r(-38.8189)
        # nowJointAngle[2, 0] =  d2r(-41.0857)
        # nowJointAngle[3, 0] =  d2r(-0.0030)
        # nowJointAngle[4, 0] =  d2r(-76.4394)
        # nowJointAngle[5, 0] =  d2r(1.0687)
        # JointAngleData = Generator.generateTrajectoryJointAngle(nowJointAngle, newHomogeneousMat, IKisRunning)
        # a = self.Time.ReadNowTime()
        # err = self.Time.TimeError(b, a)
        # print("關節角度計算所消耗的總時間: ", err["millisecond"], "ms")
        # database_JointAngle.Save(JointAngleData, f"dataBase/dynamicllyPlanTEST/JointAngle_{trjUpdataNBR}.csv", "w")
        # self.Sim.paitGL(JointAngleData, newHomogeneousMat)

        
        θ_Buffer = (np.zeros((6,1)))
        θ_Buffer[0, 0] =  d2r(-0.006)
        θ_Buffer[1, 0] =  d2r(-38.8189)
        θ_Buffer[2, 0] =  d2r(-41.0857)
        θ_Buffer[3, 0] =  d2r(-0.0030)
        θ_Buffer[4, 0] =  d2r(-76.4394)
        θ_Buffer[5, 0] =  d2r(1.0687)

        counter = 0
        totalNumner = newHomogeneousMat.shape[0]
        JointAngleData = np.zeros((len(newHomogeneousMat), 6, 1))
        while self.IKisRunning:
            if counter == totalNumner:
                break
            # 透過逆向運動學獲得關節角度
            JointAngleData[counter] = self.Kin.IK_4x4(newHomogeneousMat[counter], θ_Buffer)
            counter+=1
        
        if self.IKisRunning:
            print("IK運算結束")
        else:
            print("IK運算中斷")

        a = self.Time.ReadNowTime()
        err = self.Time.TimeError(b, a)
        print("關節角度計算所消耗的總時間: ", err["millisecond"], "ms")

        return JointAngleData
    
    
        
    def feedbackRecords(self, sysTime):
        """由機器手臂反饋回PC的數據紀錄
        """
        
        # 讀取實際手臂位姿
        pos_result, coordinate = self.Udp.getcoordinateMH(101)
        # 讀取實際手臂關節角度
        result, JointAngle, pulse = self.Udp.getcoordinateMH(1)
        
        # 軌跡速度補償
        if self.compensationSpeedFUN:
            if self.feedbackRecords_Counter >= 3:
                if self.SpeedDatacounter>=99 and np.isinf(self.speedBuffer).any() == False:
                    speedMean = np.mean(self.speedBuffer)
                    
                    self.speedCompensate = self.exceptSpeed - speedMean
                    needUpdataSpeed = int(((self.exceptSpeed+self.speedCompensate)*10))
                    print(f"軌跡平均速度: {speedMean}ms, 需補償: {self.speedCompensate}ms, 需更新的速度: {needUpdataSpeed}")

                    if needUpdataSpeed > 25:
                        print("要更新的速度值有問題，值過大!!!")
                        needUpdataSpeed = 22
                    elif needUpdataSpeed < 7:
                        print("要更新的速度值有問題，值過小!!!")
                        needUpdataSpeed = 9

                    
                    # 更新速度
                    if needUpdataSpeed < self.PrvSpeed-1 or needUpdataSpeed > self.PrvSpeed+1:
                        print(f"速度命令更新: {needUpdataSpeed}")
                        # Istatus = self.Udp.WriteVar("Integer", 3, needUpdataSpeed)
                        Istatus = self.updataTrjSpeed(needUpdataSpeed)
                        if Istatus == []:
                            print("成功更新速度值")
                            self.PrvSpeed = needUpdataSpeed
                        else:
                            print("速度更新封包有問題!!!更新失敗")
                        
                    else:
                        print("不用更新速度")

                    # 清空緩存區
                    self.speedBuffer.fill(0)
                    # 計數器重製
                    self.SpeedDatacounter = 0

                elif self.SpeedDatacounter >= 100:
                    print(self.feedbackRecords_Counter)
                    # 清空緩存區
                    self.speedBuffer.fill(0)
                    # 計數器重製
                    self.SpeedDatacounter = 0
            

            # 取一百筆
            dis = np.linalg.norm(self.feedbackRecords_Trj[self.feedbackRecords_Counter-1][0][:3]-self.feedbackRecords_Trj[self.feedbackRecords_Counter-2][0][:3])
            time = (self.feedbackRecords_sysTime[self.feedbackRecords_Counter-1]-self.feedbackRecords_sysTime[self.feedbackRecords_Counter-2])/1000
            Speed = dis/time
            self.speedBuffer[self.SpeedDatacounter] = Speed
            self.SpeedDatacounter+=1
            
        # 儲存實際軌跡位姿
        self.NowEndEffector = np.array([coordinate])
        self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([coordinate])
        # 儲存實際軌跡關節角度
        self.feedbackRecords_JointAngle[self.feedbackRecords_Counter] = np.array([JointAngle])
        self.feedbackRecords_MotorPulse[self.feedbackRecords_Counter] = np.array([pulse])
        # 儲存對應的系統時間
        self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = sysTime
        # 資料計數器更新
        self.feedbackRecords_Counter += 1

        # 多段軌跡過渡區間需要停止送銲絲
        if np.linalg.norm(self.NowEndEffector[0][0:3]-self.transitionTrjStart[0:3]) < 6 and self.stopSentWire is False:
            # AVP = 50
            firstAddress  = 21
            Number = 2
            self.AC = self.AC-10
            self.AVP = 50
            data = [self.AC, self.AVP]
            Istatus = self.Udp.multipleWriteVar(firstAddress, Number, data)
            
            
            if Istatus == []:
                print(f"已停止銲絲，AC下降至:{self.AC} A,AVP: {self.AVP}%, sysTime:{sysTime}ms")
                # 紀錄更新的銲接電流
                self.recordArcCurrent()
                # 紀錄新寫入的銲道寬度與經模型估測後的銲接製成參數(電流、速度)
                self.recordWeldBeadWidth(sysTime)
                self.stopSentWire = True
            else:
                print("填料速度更改失敗!!!")
                Istatus = self.Udp.WriteVar("Integer", 22, 50)
                
                print("已補發送封包")
        
        elif np.linalg.norm(self.NowEndEffector[0][0:3]-self.transitionTrjEnd[0:3]) < 1 and self.stopSentWire is True:
            # 第二段軌跡 開始更新銲接電流與填料速度
            firstAddress  = 21
            Number = 2
            self.AC = 50
            self.AVP = 50
            data = [self.AC, self.AVP]
            Istatus = self.Udp.multipleWriteVar(firstAddress, Number, data)
           
            if Istatus == []:
                print(f"已開始送銲絲，AC:{self.AC} A,AVP: {self.AVP}%, sysTime:{sysTime}ms")
                # 紀錄更新的銲接電流
                self.recordArcCurrent()
                # 紀錄新寫入的銲道寬度與經模型估測後的銲接製成參數(電流、速度)
                self.recordWeldBeadWidth(sysTime)
                self.stopSentWire = False
            else:
                print("填料速度更改失敗!!!")
                Istatus = self.Udp.WriteVar("Integer", 22, self.AVP)
                print("已補發送封包")

        elif np.linalg.norm(self.NowEndEffector[0][0:3]-self.trjData[-1][0][0:3]) <= 3 and self.allTrjEnd is False:
            # 快到終點時提前停止送料
            # 更新銲接電流與填料速度
            self.AVP = 50
            Istatus = self.Udp.WriteVar("Integer", 22, self.AVP)

            if Istatus == []:
                # print(f"已停止送銲絲，AVP: 50 %, sysTime:{sysTime}ms, 軌跡速度增加至: {UpdataSpeed} mm/s")
                print(f"軌跡快結束，已停止送銲絲，AVP: 50 %, sysTime:{sysTime}ms")
                # 紀錄更新的銲接電流
                self.recordArcCurrent()
                # 紀錄新寫入的銲道寬度與經模型估測後的銲接製成參數(電流、速度)
                self.recordWeldBeadWidth(sysTime)
                self.allTrjEnd = True
            else:
                print("填料速度更改失敗!!!")
                Istatus = self.Udp.WriteVar("Integer", 22, 50)
                
                print("已補發送封包")

    def SentSuccessRecords(self, interval, status, sysTime):
        """紀錄軌跡封包發送狀況
        - arg:
            interval:
                I2~I10: 2
                I11~I19: 11
            status:
                Sent success: 0
                Sent No success: 1

        """
        self.packetSent_isSuccessRecord[self.packetSent_isSuccessRecord_counter, 0] = interval
        self.packetSent_isSuccessRecord[self.packetSent_isSuccessRecord_counter, 1] = status
        self.packetSent_isSuccessRecord[self.packetSent_isSuccessRecord_counter, 2] = sysTime
        self.packetSent_isSuccessRecord_counter+=1
    
    def communicationRecords(self, RPdata, Veldata, alreadySentDataBatch, batch):
        """通訊時用於紀錄通訊內容
        """
        # 紀錄通訊所傳輸的資料
        if alreadySentDataBatch > batch-1:
            pass
        else:    
            self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySentDataBatch]
            # self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySentDataBatch]
            # Bypass
            self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata
            
        self.communicationRecords_Counter += 1

    def recordArcCurrent(self):
        """紀錄銲接電流參數
        """
        self.arcCurrentRecards[self.arcCurrentRecards_counter, 0] = self.AC
        self.arcCurrentRecards_counter += 1

    def recordWeldBeadWidth(self, sysTime):
        """紀錄指定的銲道寬度與經模型估測後的銲接製成參數(電流、速度)
        
        arg:
            estimatedGoalspeed: 模型估測後的銲接速度值。
        """
        self.weldBeadWidthRecards[self.weldBeadWidthRecards_counter, 0] = self.weldBeadWidth
        self.weldBeadWidthRecards[self.weldBeadWidthRecards_counter, 1] = self.GoalSpeed
        self.weldBeadWidthRecards[self.weldBeadWidthRecards_counter, 2] = self.AC
        self.weldBeadWidthRecards[self.weldBeadWidthRecards_counter, 3] = self.AVP
        self.weldBeadWidthRecards[self.weldBeadWidthRecards_counter, 4] = sysTime
        self.weldBeadWidthRecards_counter += 1


    def MergeTrj(self, oldTrjData:np.ndarray, oldSpeedData:np.ndarray, newData:list, alreadySentDataBatch:int):
        """Trajectory data merge.

        args: 
            - oldTrjData(ndarray): 舊軌跡資料
            - oldSpeedData(ndarray): 新軌跡資料
            - newData: 新規劃好的結果
            - alreadySentDataBatch: 已送出的軌跡點(批次)
        
        return:
            - mergeTrj(ndarray): 舊+新軌跡資料
            - mergeSpeed(ndarray): 舊+新速度資料
            - updataNode: 更新節點
            
        """
        # 新的軌跡與速度資料
        newTrjData = newData[1]
        newSpeedData = newData[2].reshape(-1, 1)
        
        # 追蹤目前軌跡已送出的資料進度
        alreadySentDataCount = alreadySentDataBatch*9

        # 取出已送出的最後一筆當作目標樣本>>用於在新軌跡資料中找到最相近的資料
        targetOldTrjData =  oldTrjData[alreadySentDataCount]
        
        # 在新資料中找與目標資料最相近的資料與其索引值
        mostSimilarTrjData, mostSimilarIndex = dataOperating.searchSimilarTrj(newTrjData, targetOldTrjData)

        # 將舊資料已送出部分保留(軌跡)
        oldTrj =  oldTrjData[:alreadySentDataCount]
        # 將新資料最新一筆保持與舊資料最後一筆相似(軌跡)
        newTrj = newTrjData[mostSimilarIndex:]
        # 舊+新(軌跡)
        mergeTrj = np.concatenate((oldTrj, newTrj), axis=0)

        # 將舊資料已送出部分保留(速度)
        oldSpeed =  oldSpeedData[:alreadySentDataCount]
        # 將新資料最新一筆保持與舊資料最後一筆相似(速度)
        newSpeed = newSpeedData[mostSimilarIndex:]
        # 舊+新(速度)
        mergeSpeed = np.concatenate((oldSpeed, newSpeed), axis=0)

        return mergeTrj, mergeSpeed, mostSimilarIndex
    
    def removeUnnecessaryData(self, data:np.ndarray):
        """最後儲存資料前，將資料容器內的冗餘資料去除
        
        args: Data(ndarray) comes in three shapes.
            - 3D array
            - 2D array
            - 1D array
        
        return: 
            filterData: After filtering the data, the data shape remains unchanged.
        """
        dataShape = data.shape
        # 依資料形狀判別運算軸參數
        if len(dataShape) == 3 :
            axisType = (1, 2) 
        elif len(dataShape) == 2:
            axisType = 1
        else:
            axisType = 0

        # 找出非零的 row 的索引
        nonzero_rows = np.any(data != 0, axis=axisType)

        # 從原始陣列中取出非零的 row 及其之前的部分
        filtered_data = data[nonzero_rows]

        # 找出第一個非零 row 的索引
        first_nonzero_row_index = np.argmax(nonzero_rows)

        # 取出第一個非零 row 之前的部分
        filtered_data_with_previous = data[:first_nonzero_row_index + len(filtered_data)]

        return filtered_data_with_previous
    
    def finalSaveData(self):
        """
        主迴圈結束時，儲存所有資料，包含以下:
        - 回饋資料: feedbackRecords_Trj、feedbackRecords_sysTime
        - 通訊紀錄: communicationRecords_Trj、communicationRecords_Speed、costTime
        - 主迴圈事件紀錄: EventRecord
        - 軌跡總資料(合併後): trjData、velData

        args: 
            FolderPath: 要儲存的資料夾路徑名稱，ex: dataBase/dynamicllyPlanTEST/，務必要加最後的斜線!!!
        """
        # 檔案寫入模式
        mode = "w"

        if self.Line:
            self.feedbackRecords_Trj = self.removeUnnecessaryData(self.feedbackRecords_Trj)
            self.feedbackRecords_JointAngle = self.removeUnnecessaryData(self.feedbackRecords_JointAngle)
            self.feedbackRecords_MotorPulse = self.removeUnnecessaryData(self.feedbackRecords_MotorPulse)
            self.feedbackRecords_sysTime = self.removeUnnecessaryData(self.feedbackRecords_sysTime)
            self.EventRecord = self.removeUnnecessaryData(self.EventRecord)
            self.packetSent_isSuccessRecord = self.removeUnnecessaryData(self.packetSent_isSuccessRecord)

            database_PoseMat.Save(self.feedbackRecords_Trj, self.FolderPath+"feedbackRecords_Trj"+f"_{self.dataNumber}"+".csv", mode)
            database_JointAngle.Save(self.feedbackRecords_JointAngle, self.FolderPath+"feedbackRecords_JointAngle"+f"_{self.dataNumber}"+".csv", mode)
            database_JointAngle.Save(self.feedbackRecords_JointAngle, self.FolderPath+"feedbackRecords_MotorPulse"+f"_{self.dataNumber}"+".csv", mode)
            database_time.Save(self.feedbackRecords_sysTime, self.FolderPath+"feedbackRecords_sysTime"+f"_{self.dataNumber}"+".csv", mode)
            database_time.Save_EventRecords(self.EventRecord, self.FolderPath+"EventRecords"+f"_{self.dataNumber}"+".csv", mode)
            database_time.Save_packetSent_isSuccessRecord(self.packetSent_isSuccessRecord, self.FolderPath+"packetSent_isSuccessRecord"+f"_{self.dataNumber}"+".csv", mode)
            
        # 更改數據形狀以便儲存
        self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
        self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
        # 濾除多餘部分(0)
        self.communicationRecords_Trj = self.removeUnnecessaryData(self.communicationRecords_Trj)
        self.communicationRecords_Speed = self.removeUnnecessaryData(self.communicationRecords_Speed)
        self.costTime = self.removeUnnecessaryData(self.costTime)
        self.arcCurrentRecards = self.removeUnnecessaryData(self.arcCurrentRecards)
        self.weldBeadWidthRecards = self.removeUnnecessaryData(self.weldBeadWidthRecards)
        
        # 存入CSV
        database_PoseMat.Save(self.communicationRecords_Trj, self.FolderPath+"communicationRecords_Trj"+f"_{self.dataNumber}"+".csv", mode)
        database_Velocity.Save(self.communicationRecords_Speed, self.FolderPath+"communicationRecords_Speed"+f"_{self.dataNumber}"+".csv", mode)
        database_time.Save_costTime(self.costTime, self.FolderPath+"costTime"+f"_{self.dataNumber}"+".csv", mode)
        database_PoseMat.Save(self.trjData, self.FolderPath+"mergeTrj"+f"_{self.dataNumber}"+".csv", mode)
        database_Velocity.Save(self.velData, self.FolderPath+"mergeSpeed"+f"_{self.dataNumber}"+".csv", mode)
        database_time.Save_arcCurrent(self.arcCurrentRecards, self.FolderPath+"ArcCurrentRecords"+f"_{self.dataNumber}"+".csv", mode)
        database_time.Save_weldBeadWidth(self.weldBeadWidthRecards, self.FolderPath+"weldBeadWidthRecords"+f"_{self.dataNumber}"+".csv", mode)
        

    def main(self):
        #---------------------------------------------Inital-----------------------------------------------
        # 初始化Pygame
        pygame.init()

        # 設置畫面寬高
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        # 紀錄UDP目前已送出的資料批次數(1批 = 9筆)
        alreadySentDataBatch = 0
        # 系統時間與軌跡節點
        sysTime, Node = 0, 0
        startNode = 0
        # 取樣時間
        sampleTime = 0.04
        # 系統時間初始化flag
        sysflag = True
        # 變軌跡次數
        trjUpdataNBR = 0

        # 測試通訊資料批次數
        I3count = 0
        I11count = 0
        feedback_count = 0
        
        
        # 計算資料分割的組數與批數
        batch = self.calculateDataGroupBatch(self.trjData)
        # 資料分割
        RPdata, Veldata = self.dataSegmentation(self.trjData, self.velData, batch)
        
        # 包裝並寫入首9筆資料   
        RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
        # 期望速度(速度補償用)
        self.exceptSpeed = int(Velpacket[0]*0.1)
        # Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
        if self.Line is True:
            RPstatus = self.Udp.multipleWriteRPVar(2, 9, RPpacket)
            Istatus = self.Udp.WriteVar("Integer", 3, Velpacket[0])
            if RPstatus==[]:
                status = 0
                self.SentSuccessRecords( 2, status, sysTime)
            else:
                status = 1
                self.SentSuccessRecords( 2, status, sysTime)
        # 紀錄通訊所送出的軌跡資料 | 用於驗證
        self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
        I3count+=1
        # 已送出之軌跡資料(批次數)+1
        alreadySentDataBatch += 1

        # 軌跡規劃執行緒
        Thread_started = False
        planThread = GetTreadResult(target=self.PlanNewTrj)

        # IK迭代執行緒
        IKThread = GetTreadResult(target=self.simulation)
        
        # 更新位置變數時的時間點
        updataTrjTime = self.Time.ReadNowTime()

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
                    RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
                    # 將打包完的資料寫入DX200
                    # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                    if RPstatus==[]:
                            status = 0
                            self.SentSuccessRecords( 11, status, sysTime)
                    else:
                        status = 1
                        self.SentSuccessRecords( 11, status, sysTime)

                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
                    # 資料(批次)計數器更新
                    alreadySentDataBatch += 1

                    I11count+=1
                    
                    # 紀錄feedback數據 | 紀錄初始位置與系統時間
                    self.feedbackRecords(0)
                else:
                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)

                    # 資料(批次)計數器更新
                    alreadySentDataBatch += 1

                    # 模擬送出第二批資料
                    I11count+=1

                    I0 = [2]
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
                    # print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取I0處")
                    
                    # 上一次偵測到的I000值
                    Prv_I0 = I0
                    I0 = self.Udp.ReadVar("Integer", 0)
                    # 將I0、PrvUpdataTime、SysTimer記錄下來
                    self.EventRecord[self.EventRecordCounter, 0] = I0[0]
                    self.EventRecord[self.EventRecordCounter, 1] = Prv_I0[0]
                    # 距離上次更新軌跡數據經過多久ms
                    self.EventRecord[self.EventRecordCounter, 3] = timeLeft_ms
                    self.EventRecord[self.EventRecordCounter, 4] = sysTime
                    
                    # print(f"I000 : {I0}")
                    """
                    防止重複
                    """
                    # TODO 此判斷機制會使得I0讀取時機若剛好錯過2或11時，少更新一次軌跡資料，造成軌跡回朔，需設計新的方法判斷!!!!!
                    # if Prv_I0[0] != I0[0] and I0[0] == 2:
                    if Prv_I0[0] != I0[0] and (I0[0] >=2 and I0[0] <=4) and timeLeft_ms > 180:
                        I2Lock = True
                        self.EventRecord[self.EventRecordCounter, 2] = 1
                        # print(f"I0: {I0}，允許寫入I11-I19")
                    # elif Prv_I0[0] != I0[0] and I0[0] == 11:
                    if Prv_I0[0] != I0[0] and (I0[0] >=11 and I0[0] <=13) and timeLeft_ms > 180:
                        I11Lock = True
                        self.EventRecord[self.EventRecordCounter, 2] = 1
                        # print(f"I0: {I0}，允許寫入I02-I10")
                    else:
                        self.EventRecord[self.EventRecordCounter, 2] = 0
                        # print(f"上次的I0與本次I0相同，不允許寫入。")

                else:
                    # 模擬I0變換
                    if I0[0] == 11:
                        I0 = [2]
                        I2Lock = True
                    elif I0[0] == 2:
                        I0 = [11]
                        I11Lock = True
                #----------------------------------------------資料通訊區-----------------------------------------
                """
                通訊
                * 變數區間:
                1. I02 - I10
                2. I11 - I19
                """
                
                if I2Lock is True and self.sentTrjData is True:
                    self.EventRecord[self.EventRecordCounter, 5] = sysTime
                    
                    I2_b = self.Time.ReadNowTime()

                    # 起始變數位置
                    firstAddress = 11
                    # 打包需要傳送的變數資料
                    RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
                    # 將打包完的資料寫入DX200
                    # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    if self.Line is True:
                        RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                        if RPstatus==[]:
                            status = 0
                            self.SentSuccessRecords( 11, status, sysTime)
                            
                        else:
                            # 封包有漏
                            status = 1
                            self.SentSuccessRecords( 11, status, sysTime)
                            # 補發送軌跡資料
                            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                    else:
                        if np.linalg.norm(RPdata[alreadySentDataBatch,-1][0:3]-self.transitionTrjStart[0:3]) < 2 and self.stopSentWire is False:
 
                            print(f"已停止送銲絲，AVP: 50 %, sysTime:{sysTime}ms")
                            self.stopSentWire = True

                        elif np.linalg.norm(RPdata[alreadySentDataBatch,-1][0:3]-self.transitionTrjEnd[0:3]) < 1 and self.stopSentWire is True:

                            print(f"已開始送銲絲，AVP: {self.AVP}%, sysTime:{sysTime}ms")
                            self.stopSentWire = False
                        # 模擬軌跡時間
                        self.Time.time_sleep(0.36)
                    
                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
                    # 資料(批次)計數器更新
                    alreadySentDataBatch += 1

                    I2_a = self.Time.ReadNowTime()
                    I2err = self.Time.TimeError(I2_b, I2_a)
                    I2err_ms = I2err["millisecond"]
                    # print(f"更新I11-I20的軌跡資料花費時間: {I2err_ms}ms")

                    # 紀錄送軌跡所花費的時間與變數區間
                    self.EventRecord[self.EventRecordCounter, 6] = I2err_ms
                    self.EventRecord[self.EventRecordCounter, 7] = 2
                    self.EventRecordCounter += 1

                    # 紀錄軌跡更新時間
                    updataTrjTime = self.Time.ReadNowTime()

                    I11count+=1
                    I2Lock = False
                    
                elif I11Lock is True and self.sentTrjData is True:
                    self.EventRecord[self.EventRecordCounter, 5] = sysTime
                    I11_b = self.Time.ReadNowTime()

                    # 起始變數位置
                    firstAddress = 2
                    # 打包需要傳送的變數資料
                    RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
                    # 將打包完的資料寫入DX200
                    # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    if self.Line is True:
                        RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                        if RPstatus==[]:
                            status = 0
                            self.SentSuccessRecords( 2, status, sysTime)
                        else:
                            # 封包有漏
                            status = 1
                            self.SentSuccessRecords( 2, status, sysTime)
                            # 補發送軌跡資料
                            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                    else:   
                        if np.linalg.norm(RPdata[alreadySentDataBatch,-1][0:3]-self.transitionTrjStart[0:3]) < 2 and self.stopSentWire is False:
 
                            print(f"已停止送銲絲，AVP: 50 %, sysTime:{sysTime}ms")
                            self.stopSentWire = True

                        elif np.linalg.norm(RPdata[alreadySentDataBatch,-1][0:3]-self.transitionTrjEnd[0:3]) < 1 and self.stopSentWire is True:

                            print(f"已開始送銲絲，AVP: {self.AVP}%, sysTime:{sysTime}ms")
                            self.stopSentWire = False
                            

                        # 模擬軌跡時間
                        self.Time.time_sleep(0.36)
                    # 通訊紀錄
                    self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
                    # 資料(批次)計數器更新
                    alreadySentDataBatch += 1

                    I11_a = self.Time.ReadNowTime()
                    I11_err = self.Time.TimeError(I11_b, I11_a)
                    I11_err_ms = I11_err["millisecond"]
                    # print(f"更新I02-I10的軌跡資料花費時間: {I11_err_ms}ms")

                    # 紀錄送軌跡所花費的時間與變數區間
                    self.EventRecord[self.EventRecordCounter, 6] = I11_err_ms
                    self.EventRecord[self.EventRecordCounter, 7] = 1
                    self.EventRecordCounter += 1

                    # 紀錄軌跡更新時間
                    updataTrjTime = self.Time.ReadNowTime()

                    I3count+=1
                    I11Lock = False

                else:
                    self.EventRecordCounter += 1
                    if self.Line is True:
                        # 更新距離上次更新軌跡時，又經過多久的時間
                        b = self.Time.ReadNowTime()
                        timeLeft = self.Time.TimeError(updataTrjTime, b)
                        timeLeft_ms = timeLeft["millisecond"]
                        # print(f"距離上次更新軌跡時間經過: {timeLeft_ms} ms | 讀取feedback資料處")
                        # 紀錄feedback數據
                        self.feedbackRecords(sysTime)
                        feedback_count+=1

                        
                    

                
                # if alreadySentDataBatch == batch or np.linalg.norm(self.NowEndEffector[0][0:3]-self.Goal)< 0.1:
                # if np.linalg.norm(self.NowEndEffector[0][0:3]-self.Goal)< 0.1
                if alreadySentDataBatch == batch :
                    """結束條件
                    外迴圈數 = 批次數 or 手臂末段點到終點
                    """
                    
                    # -------------------------------------通訊資紀錄與feedback紀錄 | 處理與存檔-----------------------------------
                    # 讀取最後一刻軌跡資料       
                    if self.Line is True:
                        can_End = False
                        print("--------------------等待軌跡結束-----------------------")
                        while True:
                            
                            # 讀取I000變數
                            I0 = self.Udp.ReadVar("Integer", 0)

                            # 更新系統時間
                            nowTime = self.Time.ReadNowTime()
                            # 取得系統時間
                            sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
                            sysTime = round(sysTime/1000, 1)

                            # 紀錄feedback數據
                            for i in range(5):
                                self.feedbackRecords(sysTime)
                                feedback_count+=1
                            # print(f"feedback寫入次數: {feedback_count}次")

                            # 判斷此筆軌跡資料的I0會停留在I0=11還是I0=2
                            quotient, remainder = divmod(RPdata.shape[0]*RPdata.shape[1], 18)
                            
                            if remainder == 9 and I0 == [11]:
                                can_End = True              
                            elif remainder == 0 and I0 == [2]:
                                can_End = True
                            else: 
                                can_End = False
                                
                            if can_End is True:
                                #讓機器人程式的迴圈結束
                                Istatus = self.Udp.WriteVar("Integer", 29, batch+100)

                                self.finalSaveData()
                                break
                    else:
                        self.finalSaveData()
                    
                    print(f"I2批次有{I3count}批，I11批次有{I11count}批")
                    print(f"軌跡實驗結束，共花費 {sysTime} ms")
                    break
                #----------------------------------------------鍵盤事件區-----------------------------------------
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        #----------------------------------------------銲接電流調變區-----------------------------------------
                        if event.key == pygame.K_i:
                            """動態修改銲電流
                            AC:   I21
                            AVP : I22
                            """
                            if self.Line:
                                Istatus = self.Udp.WriteVar("Integer", 21, self.AC)

                                if Istatus == []:
                                    print(f"已將銲接電流更改至 {self.AC}A")
                                    self.recordArcCurrent()
                                else:
                                    print("銲接電流更改失敗!!!")

                            else:
                                print(f"已將銲接電流更改至 {self.AC}A")
                                self.recordArcCurrent()
                        
                        elif event.key == pygame.K_y:
                            """
                            銲接電流-5
                            """
                            self.AC -= 5
                            print(f"已減少銲接電流至: {self.AC}A")

                        elif event.key == pygame.K_u:
                            """
                            銲接電流+5
                            """
                            self.AC += 5
                            print(f"已增加銲接電流至: {self.AC}A")

                        #----------------------------------------------銲接速度調變區-----------------------------------------
                        elif event.key == pygame.K_m:
                            """增加目標走速 | +0.1/次
                            """
                            self.GoalSpeed+=0.1
                            print(f"已增加目標走速至: {self.GoalSpeed}mm/s")
                        
                        elif event.key == pygame.K_n:
                            """增加目標走速 | -0.1/次
                            """
                            self.GoalSpeed-=0.1
                            print(f"已減少目標走速至: {self.GoalSpeed}mm/s")

                        elif event.key == pygame.K_p:
                            """
                            指定銲接速度 重新規劃新速度軌跡
                            """
                            # 如果IK正在跌代中，須終止
                            self.IKisRunning = False
                            
                            # 創建線程
                            # 開始重新規劃新軌跡時，紀錄舊軌跡已經寫入的資料筆數       
                            startPlan_alreadySentDataBatch = alreadySentDataBatch
                            
                            if self.Line is True:
                                # 讀取當下位置
                                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                                # 設定新軌跡起點
                                NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]
                            else:
                                # 模擬讀取當下位置
                                coordinate = self.trjData[startPlan_alreadySentDataBatch*9, 0]
                                # 設定新軌跡起點
                                NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]


                            # Debug用(姿態會被乘以10倍)
                            condition = (self.trjData[:, 0, 3] > 180) | (self.trjData[:, 0, 3] < -180)
                            result = np.any(condition)
                            if result is True:
                                sys.exit("姿態被乘以10倍!!!!")

                            # 終點與原軌跡保持一致
                            GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                            print(f"起點:{NowEnd} | 終點:{GoalEnd}")
                            
                            print(f"理想速度: {self.GoalSpeed} mm/s")
                            
                            # 執行緒
                            planThread = GetTreadResult(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, self.GoalSpeed))
                            planThread.start()

                            # 改變狀態旗標>>> 執行續已被啟動過
                            Thread_started = True
                        
                        #----------------------------------------------指定銲道寬度 調變 銲接參數(電流、速度)區-----------------------------------------
                        elif event.key == pygame.K_j:
                            """增加目標銲道寬度 | +0.1/次
                            """
                            self.weldBeadWidth+=0.1
                            self.weldBeadWidth = int(self.weldBeadWidth*10)*0.1
                            print(f"已增加銲道寬度至: {self.weldBeadWidth}mm")
                        
                        elif event.key == pygame.K_h:
                            self.weldBeadWidth-=0.1
                            self.weldBeadWidth = int(self.weldBeadWidth*10)*0.1
                            print(f"已減少銲道寬度至: {self.weldBeadWidth}mm")

                        elif event.key == pygame.K_k:
                            """
                            指定銲道寬度 調變銲接電流
                            """
                            # 銲接速度與銲接電流之轉換關係
                            estimatedWeldingCurrent =  Feed_filletWeld.weldCurrentTOweldBeadWidth(self.weldBeadWidth)
                            
                            self.AC = int(round(estimatedWeldingCurrent, 0))
                            
                            if self.AC > 35 and self.AC <= 45:
                                self.AVP = 90
                            elif self.AC >45 and self.AC <= 55:
                                self.AVP = 85
                            elif self.AC > 55 and self.AC <= 65:
                                self.AVP = 80
                            print(f"經數學模型換算後的理想銲接電流: {self.AC} A ; 填料速度{self.AVP}%")
                            if self.Line:
                                # 更新銲接電流與填料速度
                                firstAddress  = 21
                                Number = 2
                                data = [self.AC, self.AVP]
                                status = self.Udp.multipleWriteVar(firstAddress, Number, data)
                                # Istatus = self.Udp.WriteVar("Integer", 21, self.AC)
                                # Istatus = self.Udp.WriteVar("Integer", 22, self.AVP)
                                
                                # 紀錄更新的銲接電流
                                self.recordArcCurrent()

                                # 紀錄新寫入的銲道寬度
                                self.recordWeldBeadWidth(sysTime)
                                
                            else:
                                if self.AC >= 35 and self.AC <= 45:
                                    self.AVP = 90
                                elif self.AC > 45 and self.AC <= 55:
                                    self.AVP = 85
                                elif self.AC > 55 and self.AC <= 65:
                                    self.AVP = 80
                                print(f"已將銲接電流更改至 {self.AC}A ; 填料速度更改至{self.AVP}%")
                                # 紀錄更新的銲接電流
                                self.recordArcCurrent()
                                # 紀錄新寫入的銲道寬度與經模型估測後的銲接製成參數(電流、速度)
                                self.recordWeldBeadWidth(sysTime)

                        elif event.key == pygame.K_o:
                            """
                            指定銲道寬度 重新規劃  銲接速度軌跡
                            """
                            # 如果IK正在跌代中，須終止
                            self.IKisRunning = False
                            
                            # 創建線程
                            # 開始重新規劃新軌跡時，紀錄舊軌跡已經寫入的資料筆數       
                            startPlan_alreadySentDataBatch = alreadySentDataBatch
                            
                            if self.Line is True:
                                # 讀取當下位置
                                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                                # 設定新軌跡起點
                                NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]

                            else:
                                # 模擬讀取當下位置
                                coordinate = self.trjData[startPlan_alreadySentDataBatch*9, 0]
                                # 設定新軌跡起點
                                NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]


                            # Debug用(姿態會被乘以10倍)
                            condition = (self.trjData[:, 0, 3] > 180) | (self.trjData[:, 0, 3] < -180)
                            result = np.any(condition)
                            if result is True:
                                sys.exit("姿態被乘以10倍!!!!")

                            # 終點與原軌跡保持一致
                            GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                            print(f"起點:{NowEnd} | 終點:{GoalEnd}")

                            """
                            模型更改區
                            """
                            estimatedGoalSpeed = Feed_filletWeld.weldingSpeedTOweldBeadWidth(self.weldBeadWidth)
                            
                            estimatedGoalSpeed = int(estimatedGoalSpeed*10)*0.1
                            self.GoalSpeed = estimatedGoalSpeed

                            if self.GoalSpeed >= 0.8 and self.GoalSpeed <= 1.2:
                                self.AVP = 83
                            elif self.GoalSpeed > 1.2 and self.GoalSpeed <= 1.7:
                                self.AVP = 85
                            elif self.GoalSpeed > 1.7 and self.GoalSpeed <= 2.2:
                                self.AVP = 87

                            # 將填料速度調變至該銲接速度對應之數值
                            Istatus = self.Udp.WriteVar("Integer", 22, self.AVP)

                            print(f"經數學模型換算後的理想銲接速度: {estimatedGoalSpeed} mm/s")

                            # 紀錄新寫入的銲道寬度與經模型估測後的銲接製成參數(電流、速度)
                            self.recordWeldBeadWidth(sysTime)

                            # 執行緒
                            planThread = GetTreadResult(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, estimatedGoalSpeed))
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
                    endPlan_alreadySentDataBatch = alreadySentDataBatch
                    # 計算規劃時，時間差所產生的資料落後批數
                    dataErr = endPlan_alreadySentDataBatch-startPlan_alreadySentDataBatch
                    print("系統反應時間所消耗的資料(批次)數: ", dataErr)

                    # 軌跡與速度資料整併
                    mergeTrj, mergeSpeed, mostSimilarIndex = self.MergeTrj(self.trjData, self.velData, result, endPlan_alreadySentDataBatch)
                   
                    # 將物件變數中的軌跡資料替換為新的軌跡資料
                    self.trjData = mergeTrj
                    self.velData = mergeSpeed

                    # Debug用(姿態會被乘以10倍)
                    condition = (self.trjData[:, 0, 3] > 180) | (self.trjData[:, 0, 3] < -180)
                    result = np.any(condition)
                    if result is True:
                        sys.exit("姿態被乘以10倍!!!!")
                
                    # 固定流程(資料分割與初步封裝)
                    Remix_PoseMat, Remix_Speed = Motomancontrol.deleteFirstTrajectoryData(self.trjData, self.velData)
                    NewRemixBatch = self.calculateDataGroupBatch(self.trjData)
                    NewRemixRPdata, NewRemixSpeeddata = self.dataSegmentation(self.trjData, self.velData, NewRemixBatch, alreadySentDataBatch*9+1)
                   
                    # 更新速度
                    # Istatus = self.Udp.WriteVar("Integer", 3, NewRemixSpeeddata[0])
                    Istatus = self.updataTrjSpeed(NewRemixSpeeddata[0])
                    if Istatus==[]:
                        print(f"------------------速度旗標更新至: {self.variableSpeedFlag}; 速度{NewRemixSpeeddata[0]*0.1}ms ------------------")
                    else:
                        print(f"------------------新速度旗標更新失敗!!!------------------")
                    # 使用合併後的軌跡檔案(已分割與封裝)，覆蓋原始的軌跡資料
                    RPdata = NewRemixRPdata
                    Veldata = NewRemixSpeeddata
                    # 更新Batch，將總批次數更新成與合併後的軌跡檔案相符的
                    batch = NewRemixBatch
                    
                    # 更新資料計數器，因使用合併後的軌跡檔案，故將計數器的值加上[計算新軌跡所花費的總時間(以批次計算)]
                    # alreadySentDataBatch -= dataErr
                    """
                    經實驗證實，若系統反應時間不超過1批資料時間，即可不用特別更新[資料批次計數]之批次數
                    """
        
                    Thread_started = False
                    print("--------------新軌跡資料已覆寫---------------")

                    a = self.Time.ReadNowTime()
                    err = self.Time.TimeError(b,a)
                    costTime_dataMerge = err["millisecond"]
                    print(f"新軌跡規劃後處理所花時長: {costTime_dataMerge} ms")

                    self.costTime[self.costTimeDataCounter, 0] = costTime_PlanTrj
                    self.costTime[self.costTimeDataCounter, 1] = costTime_dataMerge
                    self.costTimeDataCounter += 1

                    # 計算IK
                    # 讓IK可以跌代
                    self.IKisRunning = True
                    IKThread = GetTreadResult(target=self.simulation, args=(trjUpdataNBR, NewHomogeneousMat,))
                    IKThread.start()
                
                
                    
                #-----------------------------------------------------------------------------------------------
                singlelooptime2 = self.Time.ReadNowTime()
                singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
                # singleloopCosttime_ms = singleloopCosttime["millisecond"]
                # print(f"單個迴圈花費 {singleloopCosttime_ms} ms")

                # 剩餘時間
                laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
                # self.Time.time_sleep(laveTime*0.001)
            
if __name__ == "__main__":


    # trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
    # speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
    trjdataPath = "dataBase/BoxWelding/PoseMat_1.csv"
    speeddataPath = "dataBase/BoxWelding/Speed_1.csv"
    Motomancontrol(trjdataPath, speeddataPath).main()