"""
Command pattern example.
""" 

# from abc import ABC, abstractmethod

# class Command(ABC):
#     """
#     Interface Command declares a method for executing a command.
#     """

#     @abstractmethod
#     def execute(self) -> None:
#         pass

class Command:
    def __init__(self) -> None:
        pass

class GenTrajectoryCommand(Command):
    def __init__(self, func) -> None:
        self.f = func
        pass

    def execute(self):
        ###
        return self.f.gentrajectory()


class KeyBoard:
    def __init__(self) -> None:
        self.c =  dict() #"char Command"
        pass

    def addCommand(self, key:str, command:Command):
        self.c.update(key, command)

    def execute(self, key: str):
        self.c[key].execute()

# class GarageOpenCommand(Command):
# 	"""
# 	Implements interface Command and provides open garage door functionality
# 	"""

# 	def __init__(self, garage_receiver):
# 		self._garage_receiver = garage_receiver


# 	def execute(self) -> None:
# 		print("Command to open garage door.")
# 		self._garage_receiver.open_door()

# class GarageCloseCommand(Command):
# 	"""
# 	Implements interface Command and provides close garage door functionality
# 	"""

# 	def __init__(self, garage_receiver):
# 		self._garage_receiver = garage_receiver

# 	def execute(self) -> None:
		
# 		print("Command to close garage door")
# 		self._garage_receiver.close_door()

# class GarageReceiver:
# 	"""
# 	Garage door endpoints to open and close the door
# 	"""

# 	def open_door(self):
# 		print("Opening garage door.")

# 	def close_door(self):
# 		print("Closing garage door")

# class ApplicationInvoker:
# 	"""
# 	Application code to provide APIs for opening and closing of the door
# 	"""

# 	def __init__(self):
# 		receiver = GarageReceiver()
# 		self._open_door = GarageOpenCommand(garage_receiver=receiver)
# 		self._close_door = GarageCloseCommand(garage_receiver=receiver)

		

# 	def invoke_open_door(self):
# 		print("App initiated garage door open.")
# 		self._open_door.execute()

# 	def invoke_close_door(self):
# 		print("App initiated garage door close.")
# 		self._close_door.execute()

# if __name__ == '__main__':

# 	# create object for class ApplicationInvoker
# 	app = ApplicationInvoker()

# 	# let's call open door first
# 	app.invoke_open_door()
# 	print()

# 	# let's close the door
# 	app.invoke_close_door()
	

"""
軌跡通訊架構優化
"""
import sys
import cv2
import pygame
import threading
import numpy as np
# from MotomanUdpPacket import MotomanUDP
from dataBase import dataBase
from Toolbox import TimeTool


class MotomanControlUdp():
    def __init__(self):
        self.dB = dataBase()
        self.Time = TimeTool()
        # self.Udp = MotomanUDP()


    # def NormalCmd(self, sysTime, headerFile):
    #     """常態命令
    #     1. Read I0 
    #     2. Read coordinate
    #     """
    #     # Read I000 variable
    #     I0 = self.Udp.ReadVar("Integer", 0)
    #     filePath = headerFile + "MatrixPlan_linear_result_I0.csv"
    #     self.dB.Save_time(I0, filePath)

    #     # Read coordinate and save Pose data to dataBase.
    #     pos_result, coordinate = self.Udp.getcoordinateMH(101)
    #     header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
    #     filePath = headerFile + "MatrixPlan_linear_result.csv"
    #     self.dB.Save_singleData_experiment(coordinate, sysTime, filePath, header)

    #     return coordinate, I0
    
    # def ConditionCmd(self, firstAddress, pathBuffer, VelBuffer):
    #     """條件命令
    #     1. 批量寫入RP(coordinate)
    #     2. 批量寫入Int(velocity)
    #     """
    #     # 單次命令寫入的資料筆數
    #     number = 9

    #     # Data Buffer
    #     RPdata = {'0':[17, 4, 5, 0, pathBuffer[0, 0], pathBuffer[0, 1], pathBuffer[0, 2], pathBuffer[0, 3], pathBuffer[0, 4], pathBuffer[0, 5]],
    #               '1':[17, 4, 5, 0, pathBuffer[1, 0], pathBuffer[1, 1], pathBuffer[1, 2], pathBuffer[1, 3], pathBuffer[1, 4], pathBuffer[1, 5]],
    #               '2':[17, 4, 5, 0, pathBuffer[2, 0], pathBuffer[2, 1], pathBuffer[2, 2], pathBuffer[2, 3], pathBuffer[2, 4], pathBuffer[2, 5]],
    #               '3':[17, 4, 5, 0, pathBuffer[3, 0], pathBuffer[3, 1], pathBuffer[3, 2], pathBuffer[3, 3], pathBuffer[3, 4], pathBuffer[3, 5]],
    #               '4':[17, 4, 5, 0, pathBuffer[4, 0], pathBuffer[4, 1], pathBuffer[4, 2], pathBuffer[4, 3], pathBuffer[4, 4], pathBuffer[4, 5]],
    #               '5':[17, 4, 5, 0, pathBuffer[5, 0], pathBuffer[5, 1], pathBuffer[5, 2], pathBuffer[5, 3], pathBuffer[5, 4], pathBuffer[5, 5]],
    #               '6':[17, 4, 5, 0, pathBuffer[6, 0], pathBuffer[6, 1], pathBuffer[6, 2], pathBuffer[6, 3], pathBuffer[6, 4], pathBuffer[6, 5]],
    #               '7':[17, 4, 5, 0, pathBuffer[7, 0], pathBuffer[7, 1], pathBuffer[7, 2], pathBuffer[7, 3], pathBuffer[7, 4], pathBuffer[7, 5]],
    #               '8':[17, 4, 5, 0, pathBuffer[8, 0], pathBuffer[8, 1], pathBuffer[8, 2], pathBuffer[8, 3], pathBuffer[8, 4], pathBuffer[8, 5]]}
        
    #     IData =[VelBuffer[0], VelBuffer[1], VelBuffer[2], 
    #             VelBuffer[3], VelBuffer[4], VelBuffer[5], 
    #             VelBuffer[6], VelBuffer[7], VelBuffer[8]]
        
    #     # Write #RP002 - #RP20
    #     RPstatus = self.Udp.multipleWriteRPVar(firstAddress, number, RPdata)
        
    #     # Write #I002 - #I020
    #     Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
    
    def calculateDataGroupBatch(self, PathData):
        """Calculate data segmentation groups and batches.
        Group: 組數
        Batch: 批次
        組數: INFORM外層For迴圈的計數值
        - Args: Trajectory data
        - Return: Number of data groups , Number of data batches
        """
        # I1為INFORM FOR外迴圈次數(要自行更改INFORM程式)
        if len(PathData)/18 == 0.0:
            group = len(PathData)//18
            print("INFORM程式 I001 改0 to ", group)
        elif len(PathData)/18 > 0.0:
            group = len(PathData)//18 + 1
            print("INFORM程式 I001 改0 to ", group)

        batch = len(PathData)//9 + 1
        
        return group, batch
    
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
        # Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
        # if Istatus == []:
        #     # return Is_success
        # else:
        #     # return Istatus
        
        # return Istatus
        
    def dataSegmentation(self, trajectoryData, velocityData, batch):
        """
        資料分批處理
        單位: 9筆/批
        """

        RPdata = np.zeros((batch, 9, 6))
        RPdata_count = 0
        # 將資料分割成以批次(一批次有9筆資料)為單位
        for layer in range(batch-1):
            for row in range(9):
                RPdata[layer, row, 0] = trajectoryData["X"][RPdata_count]
                RPdata[layer, row, 1] = trajectoryData["Y"][RPdata_count]
                RPdata[layer, row, 2] = trajectoryData["Z"][RPdata_count]
                RPdata[layer, row, 3] = trajectoryData["Rx"][RPdata_count]*10
                RPdata[layer, row, 4] = trajectoryData["Ry"][RPdata_count]*10
                RPdata[layer, row, 5] = trajectoryData["Rz"][RPdata_count]*10
                RPdata_count += 1
        # 最後一筆資料因軌跡點數除不進，故需額外處理 
        for row in range(9):
            RPdata[-1, row, 0] = trajectoryData["X"][RPdata_count]
            RPdata[-1, row, 1] = trajectoryData["Y"][RPdata_count]
            RPdata[-1, row, 2] = trajectoryData["Z"][RPdata_count]
            RPdata[-1, row, 3] = trajectoryData["Rx"][RPdata_count]*10
            RPdata[-1, row, 4] = trajectoryData["Ry"][RPdata_count]*10
            RPdata[-1, row, 5] = trajectoryData["Rz"][RPdata_count]*10
            if RPdata_count == len(trajectoryData)-1:
                 RPdata_count = len(trajectoryData)-1
            else:
                RPdata_count += 1
        
        # 分割速度資料(9筆歸為1批)
        Veldata  = np.zeros((batch, 9))
        VelData_count = 0
        for row in range(batch-1):
            for col in range(9):
                Veldata[row, col] = int(velocityData["Velocity"][VelData_count]*10)
                VelData_count +=1

        # 最後一筆資料因軌跡點數除不進，故需額外處理 
        for col in range(9):
            Veldata[-1, col] = int(velocityData["Velocity"][VelData_count]*10)
            if VelData_count == len(velocityData)-1:
                VelData_count = len(velocityData)-1
            else:
                VelData_count += 1

        # 對整個array做型別轉換，轉為int
        Veldata = Veldata.astype(int)

        return RPdata, Veldata
    
    def packetRPdataVeldata(self, RPdata, Veldata, dataCount):
        """將一批軌跡與速度資料包裝成可發送的形式
        - Args: RPdata、Veldata、datacount
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
        dataCount+=1

        return RPpacket, Velpacket, dataCount
    
    def writeRPvarINTvar(self, firstAddress, RPpacket, Velpacket):
        """Write multiple variable data
        - Args: RPdata, Veldata
        """
        Is_success = False
        # RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPdata)
        # Istatus = self.Udp.multipleWriteVar(firstAddress, 9, Veldata)
        RPstatus = []
        Istatus =[]

        if RPstatus == [] and Istatus:
            Is_success = True
        else:
            Is_success = False
        
        return Is_success
    
    def dynamicTrjPlan():
        """使用執行緒計算新軌跡資料，並實時傳輸給DX200
        """
        global newPathdata, newVeldata, threadClose
        

    def main(self):
        # 資料路徑標頭檔
        headerFile= "Experimental_data/20240312/"
        # 載入軌跡資料
        PathData = self.dB.Load(headerFile + "MatrixPlan_linear_PoseMatrix.csv")
        VelocityData = self.dB.Load(headerFile + "MatrixPlan_linear_velocity.csv")
         

        # Inital
        #-------------------------------------------------------------------------------------------------
        # 刪除軌跡原始資料的第一筆
        PathData = PathData.drop(PathData.index[0]).reset_index(drop=True)
        VelocityData = VelocityData.drop(VelocityData.index[0]).reset_index(drop=True)
        
        # For loop parameter inital
        firstAddress = 0
        number = 2
        I0, I1 = 0, 0
        IData =[I0, I1]
        # Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)

        # 焊接參數動態變更指令(初始值請填與ARCON指令一樣的參數)
        """
        AC:   I21
        AVP : I22
        """
        firstAddress = 21
        number = 2
        I21, I22 = 40, 50
        IData =[I21, I22]
        # Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
        
        # 紀錄目前已送出的資料筆數
        dataCount = 0

        # 計算資料分割的組數與批數
        group, batch = self.calculateDataGroupBatch(PathData)
        
        # 資料分割
        RPdata, Veldata = self.dataSegmentation(PathData, VelocityData, batch)
        
        #預寫入首9筆資料   
        RPpacket, Velpacket, dataCount = self.packetRPdataVeldata(RPdata, Veldata, dataCount)
        
        Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
        
        # 系統時間與軌跡節點
        sysTime, Node = 0, 0
        startNode = 0
        # 取樣時間
        sampleTime = 0.04
        # 系統時間初始化flag
        sysflag = True
        # 最後一筆資料複寫
        finalDataFlag = True

        #-------------------------------------------------------------------------------------------------
        while True:
            singlelooptime1 = self.Time.ReadNowTime()
            # 更新每禎時間
            nowTime = self.Time.ReadNowTime()
            
            if sysflag is True:
                # 儲存系統開始時間
                startTime = self.Time.ReadNowTime()
                sysflag = False

            sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
            sysTime = round(sysTime/1000, 1)
            # print("系統時間 :", sysTime)

            #####################################################################################################################################

            # 命令執行區
            # coordinate, I0 = self.NormalCmd(sysTime, headerFile)
            
            """
            通訊決策
            * 變數區間:
            1. I02 - I10
            2. I11 - I19
            """
            if I0 == [3] and finalDataFlag is True:
                # 起始變數位置
                firstAddress = 11
                # 打包需要傳送的變數資料
                RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, dataCount)
                # 將打包完的資料寫入DX200
                Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
         
            elif I0 == [11] and finalDataFlag is True:
                # 起始變數位置
                firstAddress = 2
                # 打包需要傳送的變數資料
                RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, dataCount)
                # 將打包完的資料寫入DX200
                Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)

            
            if dataCount == I1 and finalDataFlag is True:
                print("軌跡實驗結束")
                # 將剩下的資料都填完同一點
                if firstAddress == 2:
                    firstAddress = 11
                else:
                    firstAddress = 2
                RPpacket, Velpacket = self.packetRPdataVeldata(RPdata, Veldata, -1)
                Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                
                finalDataFlag = False
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        """改銲接參數
                        AC:   I21
                        AVP : I22
                        """
                        AC = 50
                        AVP = 50
                        status = self.changeWeldingPartmeter(AC, AVP)

                    elif event.key == pygame.K_p:
                        # 創建線程
                        threadClose = True
                        planThread = threading.Thread(target=Trajectoryplan)
                        planThread.start()
            #####################################################################################################################################
            singlelooptime2 = self.Time.ReadNowTime()
            singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
            # 剩餘時間
            laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
            self.Time.time_sleep(laveTime*0.001)
             
if __name__ == "__main__":
    MotomanControlUdp().main()

"""
封裝與繼承 範例
"""

# class personlComputer:
#     def __init__(self):
#         self.screenSize = 15.6
#         self.keybord = 108
#         self.__type = "MXC2024"
        

#     def playVideo(self, mothed):
#         return f"播放{mothed}影片"
    
#     def coding(self, type):
#         return f"撰寫{type}專案程式"
    
#     def publicType(self):
#         return f"型號開頭: ,{self.__type}."

# class ASUS(personlComputer):
#     def __init__(self):
#         self.color = "black"
#         self.keybord = 91
#         # 私有屬性
#         self.__price = 30999

#     def fun(self):
#         fun1 = self.playVideo("youtube")
#         fun2 = self.coding("python")
#         return fun1+fun2
    
#     # 私有方法，只有物件字的的方法可以調用。
#     def __buy(self):
#         return self.__price
    
#     def buy_position(self):
#         return f"光華商場，價錢:{self.__buy()}"
    

    
# myPC = ASUS()
# print("MyPC is", myPC.color, "and it's number of keyboard is", myPC.keybord)
# print("MyPC can do", myPC.fun())
# # print("MyPC price is NT", myPC.__buy())
# print("MyPC price is NT", myPC.buy_position())

# pC = personlComputer()
# print(pC.publicType())

"""
python 繼承 super()使用法則
>> super幫助子類別繼承父類別的建構子與屬性
"""
# class Person:
#     def __init__(self):
#         self.name = "Joy"
#         self.height = "180"
#         self.weight = "70"

# class John(Person):
#     def __init__(self):
#         super().__init__()
#         self.cellphone = "0988246073"

# J = John()
# print(J.name)

"""
Design pattern :責任鍊
"""
# 抽象處理者：大領導類
class Leader:
    def __init__(self, name):
        self._next = None
        self._name = name

    def set_next(self, next_leader):
        self._next = next_leader

    def get_next(self):
        return self._next

    def leave_successed(self, leave_days):
        print(self._name + " approve your " + str(leave_days) + " days leave.")

    def leave_failed(self):
        print("There are too many days of leave, no one approved the leave slip!")

    # 處理請求的方法
    def handle_request(self, leave_days):
        pass

# 實體處理者1：團隊經理
class TeamManager(Leader):
    def __init__(self):
        super().__init__("TeamManager")

    def handle_request(self, leave_days):
        if leave_days <= 7:
            self.leave_successed(leave_days)
        else:
            if self.get_next() is not None:
                self.get_next().handle_request(leave_days)
            else:
                self.leave_failed()

# 實體處理者2：部門經理
class DepartmentManager(Leader):
    def __init__(self):
        super().__init__("DepartmentManager")

    def handle_request(self, leave_days):
        if leave_days <= 10:
            self.leave_successed(leave_days)
        else:
            if self.get_next() is not None:
                self.get_next().handle_request(leave_days)
            else:
                self.leave_failed()

# 實體處理者3：院长类
class TechnicalDirector(Leader):
    def __init__(self):
        super().__init__("TechnicalDirector")

    def handle_request(self, leave_days):
        if leave_days <= 15:
            self.leave_successed(leave_days)
        else:
            if self.get_next() is not None:
                self.get_next().handle_request(leave_days)
            else:
                self.leave_failed()

# 實體處理者4：技術長
class CTO(Leader):
    def __init__(self):
        super().__init__("CTO")

    def handle_request(self, leave_days):
        if leave_days <= 20:
            self.leave_successed(leave_days)
        else:
            if self.get_next() is not None:
                self.get_next().handle_request(leave_days)
            else:
                self.leave_failed()

if __name__ == "__main__":
    # 組裝責任鏈
    team_manager = TeamManager()
    department_manager = DepartmentManager()
    technical_director = TechnicalDirector()
    cto = CTO()
    team_manager.set_next(department_manager)
    department_manager.set_next(technical_director)
    technical_director.set_next(cto)

    # 提交請求
    team_manager.handle_request(19)

