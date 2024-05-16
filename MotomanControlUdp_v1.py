import pygame
import threading
import numpy as np
from MotomanUdpPacket import MotomanUDP
from Toolbox import TimeTool
from dataBase_v1 import *
from Kinematics import Kinematics
from armControl import Generator
from SimulatorV2 import Simulator



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
        self.Line = True
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
        self.I28 = 19

        if self.Line is True:
            status = self.Udp.multipleWriteVar(0, 2, [self.I0, self.I1])
            status = self.Udp.WriteVar("Integer", 28, 0)

        # 載入軌跡檔案
        self.Trj = database_PoseMat.Load(TrjdatafilePath)
        self.Speed = database_Velocity.Load(VeldatafilePath)
        
        # 載入軌跡時間紀錄檔
        self.SysTime = database_time.Load("dataBase/dynamicllyPlanTEST/Time_0.csv")
        
        # 刪除軌跡資料第一筆資料
        self.Trj = Motomancontrol.deleteFirstData(self.Trj)
        self.Speed = Motomancontrol.deleteFirstData(self.Speed)
        self.SysTime = Motomancontrol.deleteFirstData(self.SysTime)

        # PC >> DX200 通訊紀錄
        self.communicationRecords_Trj = np.zeros((50000, 9, 6))
        self.communicationRecords_Speed = np.zeros((50000, 9))
        self.communicationRecords_Counter = 0

        # DX200 feedback的手臂資料紀錄
        self.feedbackRecords_Trj = np.zeros((50000, 1, 6)) 
        self.feedbackRecords_sysTime = np.zeros((50000, 1))
        self.feedbackRecords_Trj_ArmSysTime = np.zeros((50000, 1, 7))
        self.feedbackRecords_Counter = 0

    @staticmethod
    def deleteFirstData(Data):
        """Delete the first data.
        - Arg: Data(Type: ndarray)
        - Return : afterProcessData(Type: ndarray)
        """
        afterProcessData = Data[1:]
    
        return afterProcessData
    
    @staticmethod
    def CutTrj(copies, Trj, Speed):
        """由軌跡檔案中取出相應等份的資料點數
        - Args:
            copies: 等份數(ex: copies=18，將軌跡資料分成18等份。)
        """
        # 將資料分成指定等份
        indices = np.linspace(0, len(Trj)-1, copies, dtype=int)
        Trj = Trj[indices]
        Speed = Speed[indices]

        return Trj, Speed
    
    @staticmethod
    def dataProcessBeforeSent(Trj, Speed):
        """將資料處理成DX200需要的格式
        - 處理過程如下: 
        1. 改變資料形式
            Pose Matrix: [x, y, z, Rx*10, Ry*10, Rz*10]
            Speed: [int(2.1254*10)]
        2. 將資料容器調整為n*9*6的shape
        """
        # 處理軌跡資料
        Trj_copy = np.copy(Trj)
        Trj_copy[:, :, 3:6]*= 10

        # 處理速度資料
        Speed_copy = np.copy(Speed)
        Speed_copy *= 10
        Speed_copy = Speed_copy.astype(int)

        # 一批次>>9筆資料
        RPdata = Trj_copy.reshape(-1, 9, 6)
        Veldata = Speed_copy.reshape(-1, 9)

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
    
    
    def writeRPvarINTvar(self, firstAddress, number, RPpacket, Velpacket):
        """Write multiple variable data
        - Args: RPdata, Veldata
        """
        Is_success = False
        
        if self.Line is True:
            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, number, RPpacket)       
            Istatus = self.Udp.multipleWriteVar(firstAddress, number, Velpacket)
                
            
        else:
            # 靜態測試的模擬訊號
            RPstatus = []
            Istatus =[]

        if RPstatus == [] and Istatus == []:
            Is_success = True
        else:
            Is_success = False
        
        return Is_success
    
    def feedbackRecords(self, ArmEndEffector, ArmSysTime):
        """由機器手臂反饋回PC的數據紀錄
        """
        # 儲存實際軌跡資料
        self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([ArmEndEffector])
        self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = ArmSysTime
        ArmEndEffectorAndSysTime = [ArmEndEffector[0], ArmEndEffector[1], ArmEndEffector[2], ArmEndEffector[3], ArmEndEffector[4], ArmEndEffector[5], ArmSysTime]
        self.feedbackRecords_Trj_ArmSysTime[self.feedbackRecords_Counter] = np.array([ArmEndEffectorAndSysTime])
        self.feedbackRecords_Counter += 1

    def communicationRecords(self, RPdata, Veldata, alreadySent_DataBatchNBR):
        """通訊時用於紀錄通訊內容
        """
        # 紀錄通訊所傳輸的資料
        self.communicationRecords_Trj[self.communicationRecords_Counter] = RPdata[alreadySent_DataBatchNBR]
        self.communicationRecords_Speed[self.communicationRecords_Counter] = Veldata[alreadySent_DataBatchNBR]
        self.communicationRecords_Counter += 1

    
    def readSysTime(self, ArmSysStartTime_second):
        """讀取DX200系統時間
        """
        beforeReadSysTime = self.Time.ReadNowTime()
        # 讀取系統時間
        hours, minutes, seconds, totalSecond = self.Udp.getSysTime()

        afterReadSysTime = self.Time.ReadNowTime()
        communicationCostTime = self.Time.TimeError(beforeReadSysTime, afterReadSysTime)
        # TODO 扣除讀取系統時間所花費的通訊時間
        # communicationCostTime_ms = ArmSysTime["millisecond"]
        # communicationCostTime_ms -= communicationCostTime

        # 計算從開始到現在經過的時間
        elapsedTime = totalSecond - ArmSysStartTime_second

        return elapsedTime

    def judgmentTrj(self, eucDisThreshold):
        """判斷軌跡情況 | 超前 or 落後
        - Arg:
            eucDisThreshold: 軌跡超前與落後之判斷閥值(歐式距離)
        - Return:
            compenseFlag: 軌跡狀態旗標
                True : 需補償
                False: 無須補償
        """
        feedbackTrjAndTime = self.feedbackRecords_Trj_ArmSysTime[self.feedbackRecords_Counter-1]
        # 現在位置(不含姿態)
        feedbackNowPos = feedbackTrjAndTime[0, :3]
        feedbackTime = feedbackTrjAndTime[-1, -1]
        print(f"最新DX200系統時間{feedbackTime}s")

        # 期望系統時間與回饋系統時間比較
        SysTime = pd.read_csv("dataBase/dynamicllyPlanTEST/Time_0.csv")
        closestData, closestIndex = dataOperating.searchSimilar(SysTime, feedbackTime)
        # 此時期望軌跡需到達的位置
        if closestIndex == 0:
            closestIndex = 1
        expectNowPos = self.Trj[closestIndex-1][:3]
        # 利用理想軌跡的已移動距離 與 現實軌跡的已移動距離 進行比較
        expectMoveDis = np.linalg.norm(expectNowPos - self.Trj[0][:3])
        realMoveDis = np.linalg.norm(feedbackNowPos - self.feedbackRecords_Trj_ArmSysTime[0, 0, :3])

        # 剩餘的軌跡時間 = 理想的軌跡總時間 - 現在實際經過的系統時間
        timeLeft = self.SysTime[-1] - feedbackTime

        compenseFlag = False
        
        if expectMoveDis-realMoveDis > eucDisThreshold:
            print(f"軌跡落後:{realMoveDis}mm, 需提升軌跡速度")
            compenseFlag = True

        elif expectMoveDis-realMoveDis < -eucDisThreshold:
            print(f"軌跡超前:{realMoveDis}mm, 需降低軌跡速度")
            compenseFlag = True
            
        else:
            print(f"補償系統不做動")
            
        return compenseFlag, timeLeft
    
    def PlanCompenseTrj(self, NowEnd, GoalEnd, sampleTime, totalTime):
        beforePlan = self.Time.ReadNowTime()

        # 創造新軌跡
        HomogeneousMatData, PoseMatData, SpeedData, TimeData = Generator.generateTrajectory_totalTime(NowEnd, GoalEnd, sampleTime, totalTime)
        
        afterPlan = self.Time.ReadNowTime()
        err = self.Time.TimeError(beforePlan, afterPlan)
        print("計算新軌跡所花費的總時間: ", err["millisecond"], "ms")
        costTime_PlanTrj = err["millisecond"]

        return HomogeneousMatData, PoseMatData, SpeedData, TimeData, costTime_PlanTrj
    
    def main(self):

        # 紀錄UDP目前已送出的資料批次數(1批 = 9筆)
        alreadySent_DataBatchNBR = 0

        # 軌跡補償次數
        compenseTrjNBR = 0

        # 系統時間與軌跡節點
        sysTime, Node = 0, 0
        startTime = 0
        startNode = 0
        ArmSysStartTime = 0
        # 取樣時間
        sampleTime = 0.04
        # 系統時間初始化flag
        sysflag = True

        # 要傳送給DX200的軌跡點數量(目前有18個Robot Position variable可以使用)
        copies = 18
        # 切割軌跡為18個點
        Trj, Speed = Motomancontrol.CutTrj(copies, self.Trj, self.Speed)
        # 資料處理
        RPdata, Veldata = Motomancontrol.dataProcessBeforeSent(Trj, Speed)

        # 包裝、傳送所有軌跡點
        firstAddress = 2
        number = 9
        for i in range(copies//9):
            # 包裝n筆資料  
            RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
            # 傳送n筆資料
            Is_success = self.writeRPvarINTvar(firstAddress, number, RPpacket, Velpacket)
            # 紀錄通訊所送出的軌跡資料 | 用於驗證
            self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR)
            # 資料(批次)計數器更新
            alreadySent_DataBatchNBR += 1

            firstAddress+=number


        # 主迴圈旗標 | 開關
        mainLoop = False
        while True:
            if self.Line is True:
                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                if np.linalg.norm(np.array(coordinate) - self.Trj[0, 0]) <= 0.05:
                    print("------------------------------實測實驗開始------------------------------")
                    print(f"軌跡開始位置: {coordinate}")
                    mainLoop = True
                    break
            else:
                print("------------------------------模擬實驗開始------------------------------")
                mainLoop = True
                break

        while mainLoop:
            # -----------------------此區在本迴圈只會在剛進迴圈時執行一次-------------------
            if sysflag is True:
                # 儲存系統開始時間
                startTime = self.Time.ReadNowTime()

                if self.Line is True:
                    # 紀錄feedback數據 | 紀錄初始位置與系統時間
                    pos_result, coordinate = self.Udp.getcoordinateMH(101)
                    # 取得DX200初始系統時間
                    hours, minutes, seconds, totalSecond = self.Udp.getSysTime()
                    ArmSysStartTime = totalSecond
                    self.feedbackRecords(coordinate, 0)
                else:
                    I0 = [3]
                sysflag = False

            # ---------------------------------------------------------------------------
            else:
                # 更新每禎時間
                nowTime = self.Time.ReadNowTime()
                # 更新系統時間
                sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
                sysTime = round(sysTime/1000, 1)
                """
                1.讀取位置、系統時間
                2.比對期望的位置時間表
                3.判斷 有落後>>補償 | 沒落後>>繼續執行
                4.判斷是否結束執行
                """
                
                # 讀取實際手臂位置
                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                # 讀取DX200系統時間
                # TODO 需回扣讀取系統時間所消耗的通訊時間
                ArmSysTime = self.readSysTime(ArmSysStartTime)
                self.feedbackRecords(coordinate, sysTime)

                # 判斷是否需要速度補償
                eucDisThreshold = 0.2
                compenseFlag, timeLeft = self.judgmentTrj(eucDisThreshold)

                # if compenseFlag is True:
                #     # 取得剩餘時間 | 剩餘多少時間需要將此軌跡跑完
                #     # 利用矩陣軌跡法(時間版本)規劃新軌跡
                #     # 進行通訊前的資料處理
                #     # 以I000判斷實際軌跡走到哪一部分
                #     # 更新尚未走到的軌跡點
                
                #     totalTime = timeLeft
                #     sampleTime = 0.04
                #     I0 = self.Udp.ReadVar("Integer", 0)
                #     NowEnd = self.Trj[I0+1]
                #     GoalEnd = self.Trj[-1]

                #     # 執行緒
                #     compenseThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, totalTime))
                #     compenseThread.start()

                # if compenseThread.is_alive() is False:
                #     # 軌跡已變化一次，需更新計數器值
                #     compenseTrjNBR += 1
                #     result = compenseThread.get_result()
                    
                #     NewHomogeneousMat = result[0]
                #     NewPoseMatData = result[1]
                #     NewSpeedData = result[2]
                #     NewTimeData = result[3]
                #     costTime_PlanTrj = result[4]

                #     # 存檔(新軌跡資料) 
                #     mode = "w"
                #     database_HomogeneousMat.Save(NewHomogeneousMat, f"dataBase/dynamicllyPlanTEST/HomogeneousMat_{compenseTrjNBR}.csv", mode)
                #     database_PoseMat.Save(NewPoseMatData, f"dataBase/dynamicllyPlanTEST/PoseMat_{compenseTrjNBR}.csv", mode)
                #     database_Velocity.Save(NewSpeedData, f"dataBase/dynamicllyPlanTEST/Speed_{compenseTrjNBR}.csv", mode)
                #     database_time.Save(NewTimeData,f"dataBase/dynamicllyPlanTEST/Time_{compenseTrjNBR}.csv", mode)

                #     # 要傳送給DX200的軌跡點數量
                #     I0 = self.Udp.ReadVar("Integer", 0)
                #     copies = 18-I0
                #     # 切割軌跡為copies個點
                #     self.Trj, self.Speed = Motomancontrol.CutTrj(copies, NewPoseMatData, NewSpeedData)
                #     # 資料處理
                #     RPdata, Veldata = Motomancontrol.dataProcessBeforeSent(self.Trj, self.Speed)

                #     # TODO 此區尚未完成
                #     # 包裝、傳送所有軌跡點
                #     firstAddress = 2
                #     number = 9
                #     for i in range(copies//9):
                #         # 包裝n筆資料  
                #         RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySent_DataBatchNBR)
                #         # 傳送n筆資料
                #         Is_success = self.writeRPvarINTvar(firstAddress, number, RPpacket, Velpacket)
                #         # 紀錄通訊所送出的軌跡資料 | 用於驗證
                #         self.communicationRecords(RPdata, Veldata, alreadySent_DataBatchNBR)
                #         # 資料(批次)計數器更新
                #         alreadySent_DataBatchNBR += 1

                #         firstAddress+=number
                
                # 結束
                if np.linalg.norm(self.Trj[-1, 0, :3]- np.array(coordinate)[:3]) < 0.1:
                    mode = "w"
                    # feedback的軌跡資料
                    # 濾除整個row為0的部分
                    non_zero_rows_Trajectory = np.any(self.feedbackRecords_Trj != 0, axis=(1, 2))
                    non_zero_rows_Time = np.any(self.feedbackRecords_sysTime != 0, axis=1)
                    non_zero_rows_PoseMat_Time = np.any(self.feedbackRecords_Trj_ArmSysTime != 0, axis=(1, 2))
                    # 系統時間需保留初值0
                    non_zero_rows_Time[:200] = True

                    self.feedbackRecords_Trj = self.feedbackRecords_Trj[non_zero_rows_Trajectory]
                    self.feedbackRecords_sysTime = self.feedbackRecords_sysTime[non_zero_rows_Time]
                    self.feedbackRecords_Trj_ArmSysTime = self.feedbackRecords_Trj_ArmSysTime[non_zero_rows_PoseMat_Time]

                    database_PoseMat.Save(self.feedbackRecords_Trj, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj.csv", mode)
                    database_time.Save(self.feedbackRecords_sysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_sysTime.csv", mode)
                    database_time.Save_PoseMat_Time(self.feedbackRecords_Trj_ArmSysTime, "dataBase/dynamicllyPlanTEST/feedbackRecords_Trj_ArmSysTime.csv",mode)
                    
                    # 儲存通訊所送出的軌跡資料
                    self.communicationRecords_Trj = self.communicationRecords_Trj.reshape(-1, 1, 6)
                    self.communicationRecords_Speed = self.communicationRecords_Speed.reshape(-1, 1)
                    # 濾除整個row為0的部分
                    non_zero_rows_Trajectory = np.any(self.communicationRecords_Trj != 0, axis=(1, 2))
                    non_zero_rows_Speed = np.any(self.communicationRecords_Speed != 0, axis=1)
                    

                    self.communicationRecords_Trj = self.communicationRecords_Trj[non_zero_rows_Trajectory]
                    self.communicationRecords_Speed = self.communicationRecords_Speed[non_zero_rows_Speed]
                    
                    
                    database_PoseMat.Save(self.communicationRecords_Trj, "dataBase/dynamicllyPlanTEST/communicationRecords_Trj.csv", mode)
                    database_Velocity.Save(self.communicationRecords_Speed, "dataBase/dynamicllyPlanTEST/communicationRecords_Speed.csv", mode)
                    print("------------------------------結束-----------------------------------")
                    print(f"軌跡總花費時間: {sysTime}")
                    break
                
if __name__ == "__main__":
    trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
    speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
    Motomancontrol(trjdataPath, speeddataPath).main()