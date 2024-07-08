"""
- 版本: 3.0
- 名稱: 動態軌跡規劃與通訊架構
- 更新日期: 20240707
- 搭配的INFORM檔名: RUN_TRJ_MAINCODE

"""
import pygame
import queue
import threading
import numpy as np
from MotomanUdpPacket import MotomanUDP
from Toolbox import TimeTool
from dataBase_v1 import *
from Kinematics import Kinematics
from armControl import Generator
from SimulatorV2 import Simulator
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
        """
        Online(含通訊之測試) >> True  要記得解開self.Udp的相關註解
        Offline(純邏輯測試) >> False
        """
        self.Line = True
        
        self.Kin = Kinematics()
        self.Time = TimeTool()
        self.Sim = Simulator()
        self.Udp = MotomanUDP()
        
        # INFORM 迴圈變數
        """
        資料單位:
        9筆=1批, 2批=1組

        I0:  資料筆數index
        I1:  資料總批數(資料總筆數/9)(batch)
        I28: 迴圈跌代次數計數器
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
        機器人程式迴圈控制旗標:I29
        """
        self.AC = 60
        self.AVP = 100
        if self.Line is True:
            status = self.Udp.multipleWriteVar(21, 2, [self.AC, self.AVP])
            Istatus = self.Udp.WriteVar("Integer", 29, 0)
        # 銲接電流紀錄
        self.arcCurrentRecards = np.zeros((1000, 1))
        self.arcCurrentRecards[0, 0] = self.AC
        self.arcCurrentRecards_counter = 1

        # 預設銲接速度
        self.GoalSpeed = 1

        # 預設銲道寬度
        self.weldBeadWidth = 6.7

        # 銲道寬度變更紀錄
        self.weldBeadWidthRecards = np.zeros((1000, 5))
        self.weldBeadWidthRecards[0, 0] = self.weldBeadWidth
        self.weldBeadWidthRecards[0, 1] = self.GoalSpeed
        self.weldBeadWidthRecards[0, 2] = self.AC
        self.weldBeadWidthRecards[0, 3] = self.AVP
        self.weldBeadWidthRecards[0, 4] = 0
        self.weldBeadWidthRecards_counter = 1


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

        self.EndEffector = np.zeros(6)
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

        # 關節角度紀錄
        self.JointAngleRecords = np.zeros((50000, 1, 6))

        # IK迭代執行續旗標(用於中斷)
        self.IKisRunning = False

        # 發送軌跡資料通訊執行續接收資料
        self.costTime_queue = queue.Queue()

        # 已發送的軌跡資料計數器(批次)
        self.alreadySentDataBatch_queue = queue.Queue()

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
        Veldata =  velocity[SpeedIndex]*10
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
    
    def SendTrj(self, firstAddress, RPpacket, RPdata, Veldata, batch, alreadySentDataBatch):
        """發送軌跡參數給DX200(執行續)
        
        """
        b = self.Time.ReadNowTime()
        if self.Line:
            print("發送軌跡")
            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
        else:
            self.Time.time_sleep(0.18)

        a = self.Time.ReadNowTime()
        err = self.Time.TimeError(b, a)
        print("發送一批次軌跡花費: ", err["millisecond"], "ms")

        self.costTime_queue.put(err["millisecond"])
        # # 通訊紀錄
        # self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
        # # 資料(批次)計數器更新
        # alreadySentDataBatch += 1
        # self.alreadySentDataBatch_queue.put(alreadySentDataBatch)
        # if firstAddress == 11:
        #     self.costTime_queue.put("11的通訊時間")
        # else:
        #     self.costTime_queue.put("2的通訊時間")

        
    def feedbackRecords(self, sysTime):
        """由機器手臂反饋回PC的數據紀錄
        """
        # 讀取實際手臂位置
        pos_result, coordinate = self.Udp.getcoordinateMH(101)
        # 儲存實際軌跡資料
        self.EndEffector = np.array([coordinate])
        self.feedbackRecords_Trj[self.feedbackRecords_Counter] = np.array([coordinate])
        self.feedbackRecords_sysTime[self.feedbackRecords_Counter] = sysTime
        self.feedbackRecords_Counter += 1
        
    
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
    
    def finalSaveData(self, FolderPath:str):
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
            self.feedbackRecords_sysTime = self.removeUnnecessaryData(self.feedbackRecords_sysTime)
            self.EventRecord = self.removeUnnecessaryData(self.EventRecord)

            database_PoseMat.Save(self.feedbackRecords_Trj, FolderPath+"feedbackRecords_Trj.csv", mode)
            database_time.Save(self.feedbackRecords_sysTime, FolderPath+"feedbackRecords_sysTime.csv", mode)
            database_time.Save_EventRecords(self.EventRecord, FolderPath+"EventRecords.csv", mode)
            
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
        database_PoseMat.Save(self.communicationRecords_Trj, FolderPath+"communicationRecords_Trj.csv", mode)
        database_Velocity.Save(self.communicationRecords_Speed, FolderPath+"communicationRecords_Speed.csv", mode)
        database_time.Save_costTime(self.costTime, FolderPath+"costTime.csv", mode)
        database_PoseMat.Save(self.trjData, FolderPath+"mergeTrj.csv", mode)
        database_Velocity.Save(self.velData, FolderPath+"mergeSpeed.csv", mode)
        database_time.Save_arcCurrent(self.arcCurrentRecards, FolderPath+"ArcCurrentRecords.csv", mode)
        database_time.Save_weldBeadWidth(self.weldBeadWidthRecards, FolderPath+"weldBeadWidthRecords.csv", mode)
        

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
        # Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
        if self.Line is True:
            RPstatus = self.Udp.multipleWriteRPVar(2, 9, RPpacket)
            Istatus = self.Udp.WriteVar("Integer", 3, Velpacket[0])
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
                    # # 起始變數位置
                    # firstAddress = 11
                    # # 打包需要傳送的變數資料
                    # RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
                    # # 將打包完的資料寫入DX200
                    # # Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                    # RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)

                    # # 通訊紀錄
                    # self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
                    # # 資料(批次)計數器更新
                    # alreadySentDataBatch += 1

                    # I11count+=1
                    
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
                    self.EventRecord[self.EventRecordCounter, 3] = timeLeft_ms
                    self.EventRecord[self.EventRecordCounter, 4] = sysTime
                    
                    # print(f"I000 : {I0}")
                    """
                    防止重複
                    """
                    if Prv_I0[0] != I0[0] and I0[0] == 3:
                        I2Lock = True
                        self.EventRecord[self.EventRecordCounter, 2] = 1
                        # print(f"I0: {I0}，允許寫入I11-I19")
                    elif Prv_I0[0] != I0[0] and I0[0] == 11:
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
                tesrPass = False
                if I2Lock is True:
                    if tesrPass == False:
                        self.EventRecord[self.EventRecordCounter, 5] = sysTime
                        I2_b = self.Time.ReadNowTime()

                        # 起始變數位置
                        firstAddress = 11
                        # 打包需要傳送的變數資料
                        RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
                        # 發送軌跡
                        # communicationThread = threading.Thread(target=self.SendTrj, args=(firstAddress, RPpacket, RPdata, Veldata, batch, alreadySentDataBatch))
                        # communicationThread.start()
                        if self.Line is True:
                            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                            
                        # 通訊紀錄
                        self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
                        # 資料(批次)計數器更新
                        alreadySentDataBatch += 1

                        I2_a = self.Time.ReadNowTime()
                        I2err = self.Time.TimeError(I2_b, I2_a)
                        I2err_ms = I2err["millisecond"]
                        

                    
                        # 由佇列取出執行續送軌跡所花的時間
                        # result = self.costTime_queue.get()
                        # 紀錄送軌跡所花費的時間與變數區間
                        # self.EventRecord[self.EventRecordCounter, 6] = I2err_ms+result
                        self.EventRecord[self.EventRecordCounter, 6] = I2err_ms
                        self.EventRecord[self.EventRecordCounter, 7] = 2
                        self.EventRecordCounter += 1

                        # 紀錄軌跡更新時間
                        updataTrjTime = self.Time.ReadNowTime()

                        I11count+=1
                        I2Lock = False
                        
                        # print(f"發送軌跡參數花費時間: {result} ms")
                        # print(f"發送軌跡參數總花費時間: {I2err_ms+result} ms")
                        # 由佇列取出已發送的資料批數
                        # alreadySentDataBatch = self.alreadySentDataBatch_queue.get()
                        print("I0 = 3")
                    else:
                        I11count+=1
                        I2Lock = False
                        print("I0 = 2")
                    
                elif I11Lock is True:
                    if tesrPass == False:
                        self.EventRecord[self.EventRecordCounter, 5] = sysTime
                        

                        I11_b = self.Time.ReadNowTime()

                        # 起始變數位置
                        firstAddress = 2
                        # 打包需要傳送的變數資料
                        RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, alreadySentDataBatch)
                        # 發送軌跡
                        # communicationThread = threading.Thread(target=self.SendTrj, args=(firstAddress, RPpacket, RPdata, Veldata, batch, alreadySentDataBatch))
                        # communicationThread.start()
                        if self.Line is True:
                            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
                        # 通訊紀錄
                        self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)

                        # 通訊紀錄
                        self.communicationRecords(RPdata, Veldata, alreadySentDataBatch, batch)
                        # 資料(批次)計數器更新
                        alreadySentDataBatch += 1
                            
                        I11_a = self.Time.ReadNowTime()
                        I11_err = self.Time.TimeError(I11_b, I11_a)
                        I11_err_ms = I11_err["millisecond"]

                        
                        # 由佇列取出執行續送軌跡所花的時間
                        # result = self.costTime_queue.get()
                        # 紀錄送軌跡所花費的時間與變數區間
                        # self.EventRecord[self.EventRecordCounter, 6] = result+I11_err_ms
                        self.EventRecord[self.EventRecordCounter, 6] = I11_err_ms
                        self.EventRecord[self.EventRecordCounter, 7] = 1
                        self.EventRecordCounter += 1

                        # 紀錄軌跡更新時間
                        updataTrjTime = self.Time.ReadNowTime()

                        I3count+=1
                        I11Lock = False
                        
                        # print(f"軌跡參數通訊花費時間: {result} ms")
                        # print(f"發送軌跡參數總花費時間: {I11_err_ms+result} ms")
                        # 由佇列取出已發送的資料批數
                        # alreadySentDataBatch = self.alreadySentDataBatch_queue.get()
                        print("I0 = 11")
                    else:
                        I3count+=1
                        I11Lock = False
                        print("I0 = 11")
                else:
                    # 由佇列取出已發送的資料批數
                    # alreadySentDataBatch = self.alreadySentDataBatch_queue.get()
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
                
                # if alreadySentDataBatch == batch or np.linalg.norm(self.EndEffector[0][0:3]-self.Goal)< 0.1:
                if alreadySentDataBatch == batch:
                
                    """結束條件
                    外迴圈數 = 批次數 or 手臂末段點到終點
                    """
                    
                    # -------------------------------------通訊資紀錄與feedback紀錄 | 處理與存檔-----------------------------------
                    # 讀取最後一刻軌跡資料       
                    if self.Line is True:
                        can_End = False
                        print("--------------------等待軌跡結束-----------------------")
                        while True:
                            if np.linalg.norm(self.EndEffector[0][0:3]-self.Goal)< 0.1:
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

                                    self.finalSaveData("dataBase/dynamicllyPlanTEST/")
                                    break
                    else:
                        self.finalSaveData("dataBase/dynamicllyPlanTEST/")
                    
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
                            estimatedWeldingCurrent = Feed_buttWeld.weldCurrentTOweldBeadWidth(self.weldBeadWidth)
                            
                            self.AC = int(round(estimatedWeldingCurrent, 0))
                            
                            if self.AC <= 45 or self.AC >= 55:
                                self.AVP = 90
                            elif self.AC >55 or self.AC <= 65:
                                self.AVP = 95
                            elif self.AC > 65 or self.AC <= 75:
                                self.AVP = 90
                            print(f"經數學模型換算後的理想銲接電流: {self.AC} A ; 填料速度{self.AVP}%")
                            if self.Line:
                                # 更新銲接電流與填料速度
                                Istatus = self.Udp.WriteVar("Integer", 21, self.AC)
                                Istatus = self.Udp.WriteVar("Integer", 22, self.AVP)
                                
                                # 紀錄更新的銲接電流
                                self.recordArcCurrent()

                                # 紀錄新寫入的銲道寬度
                                self.recordWeldBeadWidth(sysTime)
                                
                            else:
                                if self.AC >= 45 and self.AC <= 55:
                                    self.AVP = 90
                                elif self.AC > 55 and self.AC <= 65:
                                    self.AVP = 95
                                elif self.AC > 65 and self.AC <= 75:
                                    self.AVP = 90
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
                            estimatedGoalSpeed = Feed_buttWeld.weldingSpeedTOweldBeadWidth(self.weldBeadWidth)
                            
                            estimatedGoalSpeed = int(estimatedGoalSpeed*10)*0.1
                            self.GoalSpeed = estimatedGoalSpeed

                            if self.GoalSpeed >= 0.8 and self.GoalSpeed <= 1.2:
                                self.AVP = 100
                            elif self.GoalSpeed > 1.2 and self.GoalSpeed <= 1.7:
                                self.AVP = 95
                            elif self.GoalSpeed > 1.7 and self.GoalSpeed <= 2.2:
                                self.AVP = 95

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
                    if (I0 > 8 and I0 < 10) or (I0 >16 and I0 < 19):
                        # 該段軌跡快跑完了，舊資料要與新資料合併時，需要使用已送出的資料在+1批次，否則軌跡會倒退走
                        print("I0鄰進10或19")
                    else:
                        print("正常")
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
                    if self.Line:
                        # 更新速度
                        Istatus = self.Udp.WriteVar("Integer", 3, NewRemixSpeeddata[0])
                    else:
                        print(f"速度已更新: {NewRemixSpeeddata[0]*0.1} mm/s")
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

                    

                    # 計算IK
                    # 讓IK可以跌代
                    self.IKisRunning = True
                    IKThread = GetTreadResult(target=self.simulation, args=(trjUpdataNBR, NewHomogeneousMat,))
                    IKThread.start()

                    a = self.Time.ReadNowTime()
                    err = self.Time.TimeError(b,a)
                    costTime_dataMerge = err["millisecond"]
                    print(f"新軌跡規劃後處理所花時長: {costTime_dataMerge} ms")

                    self.costTime[self.costTimeDataCounter, 0] = costTime_PlanTrj
                    self.costTime[self.costTimeDataCounter, 1] = costTime_dataMerge
                    self.costTimeDataCounter += 1
                
                
                    
                #-----------------------------------------------------------------------------------------------
                singlelooptime2 = self.Time.ReadNowTime()
                singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
                # singleloopCosttime_ms = singleloopCosttime["millisecond"]
                # print(f"單個迴圈花費 {singleloopCosttime_ms} ms")

                # 剩餘時間
                laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
                # self.Time.time_sleep(laveTime*0.001)
            
if __name__ == "__main__":


    trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_test36.csv"
    speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
    Motomancontrol(trjdataPath, speeddataPath).main()
