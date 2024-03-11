# import threading
# import time
# import sys
# import cv2
# # from MotomanUdpPacket import MotomanUDP
# from dataBase import dataBase
# import numpy as np
# from Toolbox import TimeTool
# import timeit



"""
雙軌跡過渡期實驗:
1. 載入已產生之軌跡資料(Carteisn space)
2. 開始(按鈕控制)
3. 讀取位置並存檔
4. 現在位置與資料庫做比對，若有誤差則修正
"""


# def readNowPosCMD(sampleTime, sysTime):
#     """現實機械手位置與扭矩資料取樣專用
#     - Arg:
#         - sampleTime: Unit second.
#     """
    
    
#     startTime = Time.ReadNowTime()
#     # Read coordinate
#     pos_result, coordinate = udp.getcoordinateMH(101)

#     NowPos[0,0] = coordinate[0]
#     NowPos[0,1] = coordinate[1]
#     NowPos[0,2] = coordinate[2]
#     NowPos[0,3] = coordinate[3]
#     NowPos[0,4] = coordinate[4]
#     NowPos[0,5] = coordinate[5]
#     # header = ["S", "L", "U", "R", "B", "T", "Time"]
#     header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#     db.Save_singleData_experiment(NowPos, sysTime, "Experimental_data/20240129/6_6mms/ResponseTime_Equal_length.csv", header)

#     sys_status = udp.getstatusMH()
#     # Read Torque
#     # Torque = udp.getTorqueMH()

#     # NowTorque[0,0] = Torque[0]
#     # NowTorque[0,1] = Torque[1]
#     # NowTorque[0,2] = Torque[2]
#     # NowTorque[0,3] = Torque[3]
#     # NowTorque[0,4] = Torque[4]
#     # NowTorque[0,5] = Torque[5]
#     # header = ["S", "L", "U", "R", "B", "T"]
#     # db.Save_singleData_experiment(NowTorque, sysTime, "dataBase/testTrajectory_torque.csv", header)
    
#     endTime = Time.ReadNowTime()
#     # 計算Read coordinate和Read Torque共花多少時間
#     Errtime = Time.TimeError(startTime, endTime)

#     # 儲存每個cmd的時間
#     # db.Save_time(Errtime["millisecond"], "dataBase/ReadcoordCMDtime.csv")

#     # 單位轉換 second ➜ millisecond
#     sampleTime = sampleTime*1000

#     # 計算該取樣時間內，經過讀取位置與扭矩參數後剩餘的時間
#     CMDTimeError = sampleTime - Errtime["millisecond"]

#     # 剩餘的時間使用time sleep消耗掉，以確保sampleTime的正確性
#     Time.time_sleep(CMDTimeError/1000)

#     return sys_status

# def main():
#     flag1 = True
#     flag2 = False
#     # Servo ON
#     Servo_status = udp.ServoMH(1)
#     start = True
#     startNode = 0

#     # 確認Servo Power狀態
#     sys_status = udp.getstatusMH()

#     if sys_status[4] == 64:
#         print("Servo ON")
        
#         while True:
            
#             # 儲存系統開始時間
#             if start is True: 
#                 startTime = Time.ReadNowTime()
#                 start = False
        
#             # 更新每禎時間
#             nowTime = Time.ReadNowTime()

#             sysTime, Node = Time.sysTime(startTime, startNode, nowTime, 0.001)
#             sysTime = round(sysTime/1000, 1)
#             # print("系統時間(ms): ", sysTime/1000)

#             sys_status = readNowPosCMD(0.04, sysTime)
#             speed = 66

            
#             if flag1 is True:
#                 status = udp.moveMH(2,1, speed, 17, test1)
#                 # print(status)
#                 flag1 = False
#                 flag2 = True

#             elif sys_status[0] == 194 and flag2 == True:
#                 status = udp.moveMH(2,1, speed, 17, testTotal)
#                 print("下段軌跡已接續")
#                 flag2 = False

#             elif sys_status[0] == 194 and flag1 == False and flag2 == False:
#                 print("實驗結束")
#                 status = udp.holdMH(2)
#                 time.sleep(0.01)
#                 status = udp.ServoMH(2)
#                 break



#             # cv鍵盤事件
#             key = cv2.waitKey(1) & 0xFF
#             if key == 27:  # 27是'ESC'鍵的ASCII碼
#                 print('You pressed "ESC". Exiting...')
#                 print("Hold ON ➜ Servo OFF ➜ Hold OFF ➜ I/O Reset ➜ loop berak")
#                 status = udp.holdMH(2)
#                 time.sleep(0.01)
#                 status = udp.ServoMH(2)
#                 udp.WriteIO(2701, 0)
#                 break

#             elif key == ord('h'):
#                 print('Hold on')
#                 status = udp.holdMH(1)
#                 status = udp.holdMH(2)
#                 # status = udp.moveMH(2,1, 100, 17, GoalEnd)

#             elif key == ord('r'):
#                 result, coordinate = udp.getcoordinateMH(101)
#                 print(coordinate)
#     else:
#         print("mode error!")
            
        
# if __name__ == "__main__":
#     db = dataBase()
#     Time = TimeTool()
#     udp = MotomanUDP()

#     # 載入軌跡資訊
#     # filepath = "dataBase/MatrixPathPlanning.csv"
#     # pathDict, pathDf, pathNp4x4, pathNp6x1 = db.LoadMatrix4x4(filepath)

#     # 創建一個控制視窗
#     cv2.namedWindow('Control Motoman Window')

#     # 設定Goal
#     ORG =[485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
#     GoalEnd = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]
#     test1 =     [544.116, -3.536, 195.656, 179.984, 20.2111, 1.6879]
#     testTotal = [602.869, -5.859, 156.974, 179.984, 20.2111, 1.6879]
#     # 暫存器
#     NowPos = np.zeros((1, 6))
#     NowTorque = np.zeros((1, 6))

#     # 系統時間與軌跡節點
#     sysTime, Node = 0, 0
    
#     main()
#     # 釋放資源
#     cv2.destroyAllWindows()

##############################################################################

"""
各命令發送時間:
* Readcoordinate  : 21ms
* ReadPulse       : 10ms 

* Writecoordinate : 20ms
* GetSySstatus    : 10ms
* Servo on/off    : 3ms 
"""

"""
MatrixPlan+434 軌跡實驗(上機)
邏輯測試版本 ver. 1
"""


# import sys
# import cv2
# # from MotomanUdpPacket import MotomanUDP
# from dataBase import dataBase
# from Toolbox import TimeTool


# class MotomanControlUdp():
#     def __init__(self):
#         self.dB = dataBase()
#         self.Time = TimeTool()
#         # self.Udp = MotomanUDP()


#     def Cmd(self, pathData, velocityData, sysTime, Node, runNumber):

#         # Read coordinate
#         # pos_result, coordinate = self.Udp.getcoordinateMH(101)
#         coordinate = [1, 2, 3, 4, 5, 6]
#         self.Time.time_sleep(0.021)

#         # 儲存現在位置至資料庫
#         header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#         self.dB.Save_singleData_experiment(coordinate, sysTime, "dataBase/MatrixPlan434_test/results/test_MatrixPlan434_Experimental_data.csv", header)

#         # 讀取機器人狀態
#         # sys_status = self.Udp.getstatusMH()
#         self.Time.time_sleep(0.01)
#         sys_status = [194]

#         if sys_status[0] == 194:
#             if Node >= len(velocityData):
#                 Node = len(velocityData)-1
#             if int(round(velocityData["Velocity"][Node],1)*10) < 1:
#                 speed = 1
#             else:
#                 speed = int(round(velocityData["Velocity"][Node],1)*10)

#             print(speed)

#             # status = self.Udp.moveCoordinateMH(2,1, speed, 17, pathData[Node, 0])
#             self.Time.time_sleep(0.02)
#             status = '0x0'
#             # data = [status, Node]
#             data = Node
#             self.dB.Save_time(data, "dataBase/MatrixPlan434_test/results/test_MatrixPlan434_moveCMD_is_success.csv")

#             # 紀錄寫入次數
#             runNumber+=1
           
#             # print("此刻位置 :", pathData[Node], "此刻速度 :", round(velocityData["Velocity"][Node],1), "此刻時間(ms) :", round(sysTime/1000, 3), "軌跡節點 :", Node)

#         return coordinate, runNumber
    
#     def main(self):
#         # 載入軌跡資訊
#         filepath = "dataBase/MatrixPlan434_test/MatritPlan434.csv"
#         pathDict, pathDf, pathNp4x4, pathNp6x1 = self.dB.LoadMatrix4x4(filepath)
#         filepath = "dataBase/MatrixPlan434_test/MatritPlan434_velocity.csv"
#         velocityData = self.dB.Load(filepath)

#         # 創建一個控制視窗
#         # cv2.namedWindow('Control Motoman Window')


#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0

#         # Servo ON
#         # Servo_status = self.Udp.ServoMH(1)
#         self.Time.time_sleep(0.003)
#         startNode = 0

#         # 確認Servo Power狀態
#         # sys_status = self.Udp.getstatusMH()
#         self.Time.time_sleep(0.01)
#         sys_status = [0,0,0,0,64]

#         sampleTime = 0.06
#         runNumber = 0

#         if sys_status[4] == 64:
#             print("Servo ON")

#             # 儲存系統開始時間
#             startTime = self.Time.ReadNowTime()
 
#             while True:
#                 singlelooptime1 = self.Time.ReadNowTime()
#                 # 更新每禎時間
#                 nowTime = self.Time.ReadNowTime()

#                 sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                 sysTime = round(sysTime/1000, 1)
#                 print("系統時間 :", sysTime)


#                 coordinate, runNumber = self.Cmd(pathNp6x1, velocityData, sysTime, Node, runNumber)

#                 GoalEnd = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]
#                 if coordinate >= GoalEnd :
#                     print("軌跡實驗結束")
#                     print("共寫入(次) :", runNumber)
#                     break
#                 # cv鍵盤事件
#                 # key = cv2.waitKey(1) & 0xFF
#                 # if key == 27:  # 27是'ESC'鍵的ASCII碼
#                 #     print('You pressed "ESC". Exiting...')
#                 #     print("Hold ON ➜ Servo OFF ➜ Hold OFF ➜ I/O Reset ➜ loop berak")


#                 #     # status = self.Udp.holdMH(2)
#                 #     # time.sleep(0.01)
#                 #     # status = self.Udp.ServoMH(2)
#                 #     # self.Udp.WriteIO(2701, 0)
#                 #     self.Time.time_sleep(0.010)


#                 #     # 釋放資源
#                 #     cv2.destroyAllWindows()
#                 #     break
                    

#                 # elif key == ord('h'):
#                 #     print('Hold on')
#                 #     status = self.Udp.holdMH(1)
#                 #     status = self.Udp.holdMH(2)
#                 #     self.Time.time_sleep(0.005)
                    

#                 # elif key == ord('r'):
#                 #     print("讀取一次現在位置")
#                 #     # result, coordinate = self.Udp.getcoordinateMH(101)
#                 #     # print(coordinate)
#                 #     self.Time.time_sleep(0.005)
                    

#                 singlelooptime2 = self.Time.ReadNowTime()
#                 singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#                 print("單循環動作花費時間(ms)  :", singleloopCosttime["millisecond"])

#                 # 剩餘時間
#                 laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]

#                 if laveTime>0:
#                     self.Time.time_sleep(laveTime/1000)
#                 final =  self.Time.ReadNowTime()
#                 test = self.Time.TimeError(singlelooptime1, final)
#                 print("單個迴圈花費時間(ms)  :", test["millisecond"])

           
#         else:
#             print("mode error!")
#             # 釋放資源
#             # cv2.destroyAllWindows()

#     # def Experiment_cmd_costTime(self):
#     #     status = self.Udp.ServoMH(1)
#     #     for i in range(100):
#     #         b = self.Time.ReadNowTime()

#     #         GoalEnd = [-13.775254284519994, 4.050292217779145, -45.61383771621431, -71.65996494483967, -32.04448071822077, 87.91071035847811]
#     #         coordinate = [485.334, -1.208, 234.333, 179.9829, 20.2152, 1.6982]
            
#     #         self.Udp.moveJointSapceMH(1, 1, 1, GoalEnd)

#     #         a = self.Time.ReadNowTime()
#     #         err = self.Time.TimeError(b, a)
#     #         filePath = "Experimental_data/20240220/moveJointSapceMH_CostTime.csv"
#     #         self.dB.Save_time(err["millisecond"], filePath)
            
        
# if __name__ == "__main__":
#     MotomanControlUdp().main()
#     # MotomanControlUdp().Experiment_cmd_costTime()

##############################################################################

"""
各命令發送時間:
* Readcoordinate  : 21ms
* ReadPulse       : 10ms 

* Writecoordinate : 20ms
* GetSySstatus    : 10ms
* Servo on/off    : 3ms 
"""

"""
MatrixPlan+434 軌跡實驗(上機)
上機版本 ver. 1
* 讀取位置資訊
* 讀取系統狀態
    若is not Running :
    * 下MOVE指令
"""

# import sys
# import cv2
# from MotomanUdpPacket import MotomanUDP
# from dataBase import dataBase
# from Toolbox import TimeTool

# class MotomanControlUdp():
#     def __init__(self):
#         self.dB = dataBase()
#         self.Time = TimeTool()
#         self.Udp = MotomanUDP()


#     def Cmd(self, pathData, velocityData, sysTime, Node, runNumber):

#         # Read coordinate
#         pos_result, coordinate = self.Udp.getcoordinateMH(101)
        
#         # 儲存現在位置至資料庫
#         header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#         self.dB.Save_singleData_experiment(coordinate, sysTime, "dataBase/MatrixPlan434_test/results/test_MatrixPlan434_Experimental_data.csv", header)

#         # 讀取機器人狀態
#         sys_status = self.Udp.getstatusMH()

#         if sys_status[0] == 194:
#             if Node >= len(velocityData):
#                 Node = len(velocityData)-1
#             if int(round(velocityData["Velocity"][Node],1)*10) < 1:
#                 speed = 1
#             else:
#                 speed = int(round(velocityData["Velocity"][Node],1)*10)

#             print(speed)

#             status = self.Udp.moveCoordinateMH(2,1, speed, 17, pathData[Node, 0])
            
#             self.dB.Save_time(Node, "dataBase/MatrixPlan434_test/results/test_MatrixPlan434_moveCMD_is_success.csv")

#             # 紀錄寫入次數
#             runNumber+=1
        
#         return coordinate, runNumber
    
#     def main(self):
#         # 載入軌跡資訊
#         filepath = "dataBase/MatrixPlan434_test/MatritPlan434.csv"
#         pathDict, pathDf, pathNp4x4, pathNp6x1 = self.dB.LoadMatrix4x4(filepath)
#         filepath = "dataBase/MatrixPlan434_test/MatritPlan434_velocity.csv"
#         velocityData = self.dB.Load(filepath)

#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0

#         # Servo ON
#         Servo_status = self.Udp.ServoMH(1)
#         startNode = 0

#         # 確認Servo Power狀態
#         sys_status = self.Udp.getstatusMH()

#         sampleTime = 0.06
#         runNumber = 0

#         if sys_status[4] == 64:
#             print("Servo ON")

#             # 儲存系統開始時間
#             startTime = self.Time.ReadNowTime()
 
#             while True:
#                 singlelooptime1 = self.Time.ReadNowTime()
#                 # 更新每禎時間
#                 nowTime = self.Time.ReadNowTime()

#                 sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                 sysTime = round(sysTime/1000, 1)
#                 print("系統時間 :", sysTime)


#                 coordinate, runNumber = self.Cmd(pathNp6x1, velocityData, sysTime, Node, runNumber)

#                 GoalEnd = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]
#                 if coordinate >= GoalEnd :
#                     print("軌跡實驗結束")
#                     print("共寫入(次) :", runNumber)
#                     break


#                 singlelooptime2 = self.Time.ReadNowTime()
#                 singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#                 print("單循環動作花費時間(ms)  :", singleloopCosttime["millisecond"])

#                 # 剩餘時間
#                 laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]

#                 if laveTime>0:
#                     self.Time.time_sleep(laveTime/1000)
#                 final =  self.Time.ReadNowTime()
#                 test = self.Time.TimeError(singlelooptime1, final)
#                 print("單個迴圈花費時間(ms)  :", test["millisecond"])

           
#         else:
#             print("mode error!")

        
# if __name__ == "__main__":
#     MotomanControlUdp().main()

##############################################################################

"""
各命令發送時間:
* Readcoordinate  : 21ms
* ReadPulse       : 10ms 

* Writecoordinate : 20ms
* GetSySstatus    : 10ms
* Servo on/off    : 3ms 
"""

"""
MatrixPlan+434 軌跡實驗(上機)
上機版本 ver. 2
* 讀取系統狀態
    若is not Running :
    1.下MOVE指令
    2.讀取coordinate
"""

# import sys
# import cv2
# from MotomanUdpPacket import MotomanUDP
# from dataBase import dataBase
# from Toolbox import TimeTool

# class MotomanControlUdp():
#     def __init__(self):
#         self.dB = dataBase()
#         self.Time = TimeTool()
#         self.Udp = MotomanUDP()


#     def Cmd(self, pathData, velocityData, sysTime, Node, runNumber):
#         # 讀取機器人狀態
#         sys_status = self.Udp.getstatusMH()

#         if sys_status[0] == 194:
#             if Node >= len(velocityData):
#                 Node = len(velocityData)-1
#             if int(round(velocityData["Velocity"][Node],1)*10) < 1:
#                 speed = 1
#             else:
#                 speed = int(round(velocityData["Velocity"][Node],1)*10)
            
#             self.dB.Save_time(speed/10, "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/results/MatrixPlan434_moveCMD_w_speed.csv")
#             print(speed)

#             status = self.Udp.moveCoordinateMH(2,1, speed, 17, pathData[Node, 0])
#             self.dB.Save_time(Node, "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/results/MatrixPlan434_moveCMD_is_success.csv")

#             # Read coordinate
#             pos_result, coordinate = self.Udp.getcoordinateMH(101)
            
#             # 儲存現在位置至資料庫
#             header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#             self.dB.Save_singleData_experiment(coordinate, sysTime, "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/results/MatrixPlan434_Experimental_data.csv", header)

#             # 紀錄寫入次數
#             runNumber+=1

#             return coordinate, runNumber
#         else:
#             # Read coordinate
#             pos_result, coordinate = self.Udp.getcoordinateMH(101)
            
#             # 儲存現在位置至資料庫
#             header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#             self.dB.Save_singleData_experiment(coordinate, sysTime, "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/results/MatrixPlan434_Experimental_data.csv", header)
            
#             runNumber = runNumber
#             return coordinate, runNumber
    
#     def main(self):
#         # 載入軌跡資訊
#         filepath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434.csv"
#         pathDict, pathDf, pathNp4x4, pathNp6x1 = self.dB.LoadMatrix4x4(filepath)
#         filepath = "dataBase/MartixPlan434_Exp_weld_seam_10cm/sampleTime_40ms/MatritPlan434_velocity.csv"
#         velocityData = self.dB.Load(filepath)

#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0

#         # # Read coordinate
#         # pos_result, coordinate = self.Udp.getcoordinateMH(101)

#         # Servo ON
#         Servo_status = self.Udp.ServoMH(1)
#         startNode = 0

#         # 確認Servo Power狀態
#         sys_status = self.Udp.getstatusMH()

#         sampleTime = 0.04
#         runNumber = 0

#         if sys_status[4] == 64:
#             print("Servo ON")

#             # 儲存系統開始時間
#             startTime = self.Time.ReadNowTime()
 
#             while True:
#                 singlelooptime1 = self.Time.ReadNowTime()
#                 # 更新每禎時間
#                 nowTime = self.Time.ReadNowTime()

#                 sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#                 sysTime = round(sysTime/1000, 1)
#                 print("系統時間 :", sysTime)


#                 coordinate, runNumber = self.Cmd(pathNp6x1, velocityData, sysTime, Node, runNumber)

#                 GoalEnd = [956.3, -9.275, -159.871, -165.291, -7.1738, 17.5332]
#                 if coordinate[1] >= GoalEnd[1] :
#                     print("軌跡實驗結束")
#                     print("共寫入(次) :", runNumber)
#                     self.Udp.ServoMH(2)
#                     break


#                 singlelooptime2 = self.Time.ReadNowTime()
#                 singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#                 print("單循環動作花費時間(ms)  :", singleloopCosttime["millisecond"])

#                 # 剩餘時間
#                 laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]

#                 if laveTime>0:
#                     self.Time.time_sleep(laveTime/1000)
#                 final =  self.Time.ReadNowTime()
#                 test = self.Time.TimeError(singlelooptime1, final)
#                 print("單個迴圈花費時間(ms)  :", test["millisecond"])

           
#         else:
#             print("mode error!")

        
# if __name__ == "__main__":
#     MotomanControlUdp().main()



"""
測試示教模式下的軌跡速度是否連續
"""


import sys
import cv2
from MotomanUdpPacket import MotomanUDP
from dataBase import dataBase
from Toolbox import TimeTool

class MotomanControlUdp():
    def __init__(self):
        self.dB = dataBase()
        self.Time = TimeTool()
        self.Udp = MotomanUDP()


    def Cmd(self, sysTime, Node, runNumber, headerFile):
        
        # Read coordinate
        pos_result, coordinate = self.Udp.getcoordinateMH(101)
        
        # 儲存現在位置至資料庫
        header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
        filePath = headerFile + "Velocity_test.csv"
        self.dB.Save_singleData_experiment(coordinate, sysTime, filePath, header)

        # 紀錄寫入次數
        runNumber+=1

        return coordinate, runNumber
    
    def main(self):
        # 載入軌跡資訊
        headerFile= "Experimental_data/20240311/"

        # 系統時間與軌跡節點
        sysTime, Node = 0, 0

        sampleTime = 0.04
        runNumber = 0
        startNode = 0

        # 儲存系統開始時間
        startTime = self.Time.ReadNowTime()

        while True:
            singlelooptime1 = self.Time.ReadNowTime()
            # 更新每禎時間
            nowTime = self.Time.ReadNowTime()

            sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
            sysTime = round(sysTime/1000, 1)
            print("系統時間 :", sysTime)


            self.Cmd(sysTime, Node, runNumber, headerFile)


            singlelooptime2 = self.Time.ReadNowTime()
            singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
            print("單循環動作花費時間(ms)  :", singleloopCosttime["millisecond"])

            # 剩餘時間
            laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]

            if laveTime>0:
                self.Time.time_sleep(laveTime/1000)
            # final =  self.Time.ReadNowTime()
            # test = self.Time.TimeError(singlelooptime1, final)
            # print("單個迴圈花費時間(ms)  :", test["millisecond"])

        
if __name__ == "__main__":
    MotomanControlUdp().main()








    
    


