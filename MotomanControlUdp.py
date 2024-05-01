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

        # 創建一個控制視窗
        # cv2.namedWindow('Control Motoman Window')


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
2024/03/06
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


#     def Cmd(self, sysTime, Node, runNumber, headerFile):
        
#         # Read coordinate
#         pos_result, coordinate = self.Udp.getcoordinateMH(101)
        
#         # 儲存現在位置至資料庫
#         header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#         filePath = headerFile + "Velocity_test.csv"
#         self.dB.Save_singleData_experiment(coordinate, sysTime, filePath, header)

#         # 紀錄寫入次數
#         runNumber+=1

#         return coordinate, runNumber
    
#     def main(self):
#         # 載入軌跡資訊
#         headerFile= "Experimental_data/20240306/"

#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0

#         sampleTime = 0.04
#         runNumber = 0
#         startNode = 0

#         # 系統flag
#         sysflag = True

#         while True:
#             singlelooptime1 = self.Time.ReadNowTime()
#             # 更新每禎時間
#             nowTime = self.Time.ReadNowTime()
            
#             if sysflag is True:
#                 # 儲存系統開始時間
#                 startTime = self.Time.ReadNowTime()
#                 sysflag = False

#             sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#             sysTime = round(sysTime/1000, 1)
#             print("系統時間 :", sysTime)


#             self.Cmd(sysTime, Node, runNumber, headerFile)


#             singlelooptime2 = self.Time.ReadNowTime()
#             singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#             # print("單循環動作花費時間(ms)  :", singleloopCosttime["millisecond"])

#             # 剩餘時間
#             laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
#             # self.Time.time_sleep(laveTime/1000)

#             if laveTime>0:
#                 self.Time.time_sleep(laveTime/1000)
#             # final =  self.Time.ReadNowTime()
#             # test = self.Time.TimeError(singlelooptime1, final)
#             # print("單個迴圈花費時間(ms)  :", test["millisecond"])

        
# if __name__ == "__main__":
#     MotomanControlUdp().main()


"""
2024/03/12
* 軌跡實驗
    * 演算法: 矩陣軌跡法(線性插值)
    * 架構: 主體為INFORM，UDP配合寫入變數。
"""

# import sys
# import cv2
# import numpy as np
# import threading
# from MotomanUdpPacket import MotomanUDP
# from dataBase_v0 import dataBase
# from Toolbox import TimeTool

# class MotomanControlUdp():
#     def __init__(self):
#         self.dB = dataBase()
#         self.Time = TimeTool()
#         self.Udp = MotomanUDP()


#     def NormalCmd(self, sysTime, headerFile):
#         """常態命令
#         1. Read I0 
#         2. Read coordinate
#         """
#         # Read I000 variable
#         I0 = self.Udp.ReadVar("Integer", 0)
#         filePath = headerFile + "MatrixPlan_linear_result_I0.csv"
#         self.dB.Save_time(I0, filePath)

#         # Read coordinate and save Pose data to dataBase.
#         pos_result, coordinate = self.Udp.getcoordinateMH(101)
#         header = ["X", "Y", "Z", "Rx", "Ry", "Rz", "time"]
#         filePath = headerFile + "MatrixPlan_linear_result.csv"
#         self.dB.Save_singleData_experiment(coordinate, sysTime, filePath, header)

#         return coordinate, I0
    
#     def ConditionCmd(self, firstAddress, pathBuffer, VelBuffer):
#         """條件命令
#         1. 批量寫入RP(coordinate)
#         2. 批量寫入Int(velocity)
#         """
#         # 單次命令寫入的資料筆數
#         number = 9

#         # Data Buffer
#         RPdata = {'0':[17, 4, 5, 0, pathBuffer[0, 0], pathBuffer[0, 1], pathBuffer[0, 2], pathBuffer[0, 3], pathBuffer[0, 4], pathBuffer[0, 5]],
#                   '1':[17, 4, 5, 0, pathBuffer[1, 0], pathBuffer[1, 1], pathBuffer[1, 2], pathBuffer[1, 3], pathBuffer[1, 4], pathBuffer[1, 5]],
#                   '2':[17, 4, 5, 0, pathBuffer[2, 0], pathBuffer[2, 1], pathBuffer[2, 2], pathBuffer[2, 3], pathBuffer[2, 4], pathBuffer[2, 5]],
#                   '3':[17, 4, 5, 0, pathBuffer[3, 0], pathBuffer[3, 1], pathBuffer[3, 2], pathBuffer[3, 3], pathBuffer[3, 4], pathBuffer[3, 5]],
#                   '4':[17, 4, 5, 0, pathBuffer[4, 0], pathBuffer[4, 1], pathBuffer[4, 2], pathBuffer[4, 3], pathBuffer[4, 4], pathBuffer[4, 5]],
#                   '5':[17, 4, 5, 0, pathBuffer[5, 0], pathBuffer[5, 1], pathBuffer[5, 2], pathBuffer[5, 3], pathBuffer[5, 4], pathBuffer[5, 5]],
#                   '6':[17, 4, 5, 0, pathBuffer[6, 0], pathBuffer[6, 1], pathBuffer[6, 2], pathBuffer[6, 3], pathBuffer[6, 4], pathBuffer[6, 5]],
#                   '7':[17, 4, 5, 0, pathBuffer[7, 0], pathBuffer[7, 1], pathBuffer[7, 2], pathBuffer[7, 3], pathBuffer[7, 4], pathBuffer[7, 5]],
#                   '8':[17, 4, 5, 0, pathBuffer[8, 0], pathBuffer[8, 1], pathBuffer[8, 2], pathBuffer[8, 3], pathBuffer[8, 4], pathBuffer[8, 5]]}
        
#         IData =[VelBuffer[0], VelBuffer[1], VelBuffer[2], 
#                 VelBuffer[3], VelBuffer[4], VelBuffer[5], 
#                 VelBuffer[6], VelBuffer[7], VelBuffer[8]]
        
#         # Write #RP002 - #RP20
#         RPstatus = self.Udp.multipleWriteRPVar(firstAddress, number, RPdata)
        
#         # Write #I002 - #I020
#         Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)


    
#     def main(self):
#         # 資料路徑標頭檔
#         headerFile= "Experimental_data/20240312/"
#         # 載入軌跡資料
#         PathData = self.dB.Load(headerFile + "MatrixPlan_linear_PoseMatrix.csv")
#         VelocityData = self.dB.Load(headerFile + "MatrixPlan_linear_velocity.csv")
         

#         # Inital

#         # # 創建一個控制視窗
#         # cv2.namedWindow('Control Motoman Window')

#         # 刪除軌跡原始資料的第一筆
#         PathData = PathData.drop(PathData.index[0]).reset_index(drop=True)
#         VelocityData = VelocityData.drop(VelocityData.index[0]).reset_index(drop=True)
        
#         # For loop parameter inital
#         firstAddress = 0
#         number = 2
#         I0, I1 = 0, 0
#         IData =[I0, I1]
#         Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)

#         # 焊接參數動態變更指令(初始值請填與ARCON指令一樣的參數)
#         """
#         AC:   I21
#         AVP : I22
#         """
#         firstAddress = 21
#         number = 2
#         I21, I22 = 40, 50
#         IData =[I21, I22]
#         Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)

#         # 資料分批
#         # 紀錄目前已送出的資料筆數
#         dataCount = 0

#         # I1為INFORM FOR外迴圈次數(要自行更改INFORM程式)
#         if len(PathData)/18 == 0.0:
#             I1 = len(PathData)//18
#             print("INFORM程式 I001 改0 to ", I1)
#         elif len(PathData)/18 > 0.0:
#             I1 = len(PathData)//18 + 1
#             print("INFORM程式 I001 改0 to ", I1)
        
#         I1 = len(PathData)//9 + 1
        
#         # 分割軌跡資料(9筆歸為1批)
#         RPdata = np.zeros((I1, 9, 6))
#         RPdata_count = 0
#         for layer in range(I1-1):
#             for row in range(9):
#                 RPdata[layer, row, 0] = PathData["X"][RPdata_count]
#                 RPdata[layer, row, 1] = PathData["Y"][RPdata_count]
#                 RPdata[layer, row, 2] = PathData["Z"][RPdata_count]
#                 RPdata[layer, row, 3] = PathData["Rx"][RPdata_count]*10
#                 RPdata[layer, row, 4] = PathData["Ry"][RPdata_count]*10
#                 RPdata[layer, row, 5] = PathData["Rz"][RPdata_count]*10
#                 RPdata_count += 1
#         # 最後一筆資料因軌跡點數除不進，故需額外處理 
#         for row in range(9):
#             RPdata[-1, row, 0] = PathData["X"][RPdata_count]
#             RPdata[-1, row, 1] = PathData["Y"][RPdata_count]
#             RPdata[-1, row, 2] = PathData["Z"][RPdata_count]
#             RPdata[-1, row, 3] = PathData["Rx"][RPdata_count]*10
#             RPdata[-1, row, 4] = PathData["Ry"][RPdata_count]*10
#             RPdata[-1, row, 5] = PathData["Rz"][RPdata_count]*10
#             if RPdata_count == len(PathData)-1:
#                  RPdata_count = len(PathData)-1
#             else:
#                 RPdata_count += 1

#         # 分割速度資料(9筆歸為1批)
#         Veldata  = np.zeros((I1, 9))
#         VelData_count = 0
#         for row in range(I1-1):
#             for col in range(9):
#                 Veldata[row, col] = int(VelocityData["Velocity"][VelData_count]*10)
#                 VelData_count +=1
#         # 最後一筆資料因軌跡點數除不進，故需額外處理 
#         for col in range(9):
#             Veldata[-1, col] = int(VelocityData["Velocity"][VelData_count]*10)
#             if VelData_count == len(VelocityData)-1:
#                 VelData_count = len(VelocityData)-1
#             else:
#                 VelData_count += 1
#         # 對整個array做型別轉換，轉為int
#         Veldata = Veldata.astype(int)

#         # # 預寫入首18筆資料   
#         # firstAddress_ = 2
#         # for layer in range(2):
            
#         #     RPdataBuffer = {'0':[17, 4, 5, 0, RPdata[layer][0][0], RPdata[layer][0][1], RPdata[layer][0][2], RPdata[layer][0][3], RPdata[layer][0][4], RPdata[layer][0][5]],
#         #                     '1':[17, 4, 5, 0, RPdata[layer][1][0], RPdata[layer][1][1], RPdata[layer][1][2], RPdata[layer][1][3], RPdata[layer][1][4], RPdata[layer][1][5]],
#         #                     '2':[17, 4, 5, 0, RPdata[layer][2][0], RPdata[layer][2][1], RPdata[layer][2][2], RPdata[layer][2][3], RPdata[layer][2][4], RPdata[layer][2][5]],
#         #                     '3':[17, 4, 5, 0, RPdata[layer][3][0], RPdata[layer][3][1], RPdata[layer][3][2], RPdata[layer][3][3], RPdata[layer][3][4], RPdata[layer][3][5]],
#         #                     '4':[17, 4, 5, 0, RPdata[layer][4][0], RPdata[layer][4][1], RPdata[layer][4][2], RPdata[layer][4][3], RPdata[layer][4][4], RPdata[layer][4][5]],
#         #                     '5':[17, 4, 5, 0, RPdata[layer][5][0], RPdata[layer][5][1], RPdata[layer][5][2], RPdata[layer][5][3], RPdata[layer][5][4], RPdata[layer][5][5]],
#         #                     '6':[17, 4, 5, 0, RPdata[layer][6][0], RPdata[layer][6][1], RPdata[layer][6][2], RPdata[layer][6][3], RPdata[layer][6][4], RPdata[layer][6][5]],
#         #                     '7':[17, 4, 5, 0, RPdata[layer][7][0], RPdata[layer][7][1], RPdata[layer][7][2], RPdata[layer][7][3], RPdata[layer][7][4], RPdata[layer][7][5]],
#         #                     '8':[17, 4, 5, 0, RPdata[layer][8][0], RPdata[layer][8][1], RPdata[layer][8][2], RPdata[layer][8][3], RPdata[layer][8][4], RPdata[layer][8][5]]}
#         #     # Write #RP002 - #RP20
#         #     RPstatus = self.Udp.multipleWriteRPVar(firstAddress_, 9, RPdataBuffer)
        
#         #     # Write #I002 - #I020
#         #     VelDataBuffer =[Veldata[layer, 0], 
#         #                     Veldata[layer, 1], 
#         #                     Veldata[layer, 2], 
#         #                     Veldata[layer, 3], 
#         #                     Veldata[layer, 4], 
#         #                     Veldata[layer, 5], 
#         #                     Veldata[layer, 6], 
#         #                     Veldata[layer, 7], 
#         #                     Veldata[layer, 8]]
#         #     Istatus = self.Udp.multipleWriteVar(firstAddress_, 9, VelDataBuffer)
#         #     firstAddress_+=9
#         #     dataCount +=1

#         #預寫入首9筆資料   
#         RPdataBuffer = {'0':[17, 4, 5, 0, RPdata[0][0][0], RPdata[0][0][1], RPdata[0][0][2], RPdata[0][0][3], RPdata[0][0][4], RPdata[0][0][5]],
#                         '1':[17, 4, 5, 0, RPdata[0][1][0], RPdata[0][1][1], RPdata[0][1][2], RPdata[0][1][3], RPdata[0][1][4], RPdata[0][1][5]],
#                         '2':[17, 4, 5, 0, RPdata[0][2][0], RPdata[0][2][1], RPdata[0][2][2], RPdata[0][2][3], RPdata[0][2][4], RPdata[0][2][5]],
#                         '3':[17, 4, 5, 0, RPdata[0][3][0], RPdata[0][3][1], RPdata[0][3][2], RPdata[0][3][3], RPdata[0][3][4], RPdata[0][3][5]],
#                         '4':[17, 4, 5, 0, RPdata[0][4][0], RPdata[0][4][1], RPdata[0][4][2], RPdata[0][4][3], RPdata[0][4][4], RPdata[0][4][5]],
#                         '5':[17, 4, 5, 0, RPdata[0][5][0], RPdata[0][5][1], RPdata[0][5][2], RPdata[0][5][3], RPdata[0][5][4], RPdata[0][5][5]],
#                         '6':[17, 4, 5, 0, RPdata[0][6][0], RPdata[0][6][1], RPdata[0][6][2], RPdata[0][6][3], RPdata[0][6][4], RPdata[0][6][5]],
#                         '7':[17, 4, 5, 0, RPdata[0][7][0], RPdata[0][7][1], RPdata[0][7][2], RPdata[0][7][3], RPdata[0][7][4], RPdata[0][7][5]],
#                         '8':[17, 4, 5, 0, RPdata[0][8][0], RPdata[0][8][1], RPdata[0][8][2], RPdata[0][8][3], RPdata[0][8][4], RPdata[0][8][5]]}
#         # Write #RP002 - #RP20
#         RPstatus = self.Udp.multipleWriteRPVar(2, 9, RPdataBuffer)
    
#         # Write #I002 - #I020
#         VelDataBuffer =[Veldata[0, 0], 
#                         Veldata[0, 1], 
#                         Veldata[0, 2], 
#                         Veldata[0, 3], 
#                         Veldata[0, 4], 
#                         Veldata[0, 5], 
#                         Veldata[0, 6], 
#                         Veldata[0, 7], 
#                         Veldata[0, 8]]
#         Istatus = self.Udp.multipleWriteVar(2, 9, VelDataBuffer)
#         dataCount +=1

#         # 系統時間與軌跡節點
#         sysTime, Node = 0, 0
#         startNode = 0

#         # 取樣時間
#         sampleTime = 0.04
    
#         # 系統時間初始化flag
#         sysflag = True
#         # 最後一筆資料複寫
#         finalDataFlag = True
#         # 變更焊接參數旗標
#         ChangWPFlag = True

#         while True:
#             singlelooptime1 = self.Time.ReadNowTime()
#             # 更新每禎時間
#             nowTime = self.Time.ReadNowTime()
            
#             if sysflag is True:
#                 # 儲存系統開始時間
#                 startTime = self.Time.ReadNowTime()
#                 sysflag = False

#             sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
#             sysTime = round(sysTime/1000, 1)
#             # print("系統時間 :", sysTime)

#              #####################################################################################################################################

#             # 命令執行區
#             coordinate, I0 = self.NormalCmd(sysTime, headerFile)
            

#             # # test
#             # # cv鍵盤事件
#             # key = cv2.waitKey(1) & 0xFF
#             # if key == ord('w'):  # 27是'ESC'鍵的ASCII碼
#             #     I0 = 2
#             # elif key == ord('s'):
#             #     I0 = 11


#             """
#             * 變數區間:
#             1. I02 - I10
#             2. I11 - I19
#             """
            

#             if I0 == [3] and finalDataFlag is True:
#                 firstAddress = 11
#                 # 更新DX200 RP、Int變數
#                 self.ConditionCmd(firstAddress, RPdata[dataCount], Veldata[dataCount])
#                 dataCount += 1
                
#             elif I0 == [11] and finalDataFlag is True:
#                 firstAddress = 2
#                 # 更新DX200 RP、Int變數
#                 self.ConditionCmd(firstAddress, RPdata[dataCount], Veldata[dataCount])
#                 dataCount += 1

            
#             if dataCount == int(I1/2) and ChangWPFlag is True:
#                 """
#                 AC:   I21
#                 AVP : I22
#                 """
#                 firstAddress = 21
#                 number = 2
#                 I21, I22 = 50, 50
#                 IData =[I21, I22]
#                 Istatus = self.Udp.multipleWriteVar(firstAddress, number, IData)
#                 print("變更焊接參數AC: ", I21, "AVP: ", I22)
#                 ChangWPFlag = False
            
#             if dataCount == I1 and finalDataFlag is True:
#                 print("軌跡實驗結束")
#                 # 將剩下的資料都填完同一點
#                 if firstAddress == 2:
#                     firstAddress = 11
#                 else:
#                     firstAddress = 2
#                 self.ConditionCmd(firstAddress, RPdata[-1], Veldata[-1])
#                 finalDataFlag = False
                
#             #####################################################################################################################################
#             singlelooptime2 = self.Time.ReadNowTime()
#             singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
#             # 剩餘時間
#             laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
#             self.Time.time_sleep(laveTime*0.001)
             
# if __name__ == "__main__":
#     MotomanControlUdp().main()
#     # # 釋放資源
#     # cv2.destroyAllWindows()
    
"""
動態軌跡規劃與通訊實驗(模擬實驗架構)
20240401
"""
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

        # 機器手臂實際軌跡資料(模擬)
        self.RealTrajectoryData = np.zeros((10000, 9, 6))
        self.RealSpeedData = np.zeros((10000, 9))
        self.RealDataCounter = 0

        # 機器手臂實際軌跡資料(實際)
        self.RealTrajectory = np.zeros((10000, 1, 6))
        self.RealsysTime = np.zeros((10000, 1))
        
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
        # # Calculate group(About: I001)
        # quotient_group, remainder_group = divmod(TrajectoryData.shape[0], 18)
        # if remainder_group != 0:
        #     # 餘數不等於0，表示原始資料分組(18筆為1組)時，最後一組不足18筆，故要+1組
        #     group = quotient_group + 1
        # else:
        #     group = quotient_group

        # # 修改DX200變數暫存器值
        # if self.Line is True:
        #     print("INFORM程式 I001: ", group)
        #     status = self.Udp.WriteVar("Integer", 1, group)

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
        
        # return group, batch
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
        dataCount+=1

        return RPpacket, Velpacket, dataCount
    
    
    def writeRPvarINTvar(self, firstAddress, RPpacket, Velpacket):
        """Write multiple variable data
        - Args: RPdata, Veldata
        """
        Is_success = False
        
        if self.Line is True:
            RPstatus = self.Udp.multipleWriteRPVar(firstAddress, 9, RPpacket)
            Istatus = self.Udp.multipleWriteVar(firstAddress, 9, Velpacket)
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

        return HomogeneousMatData, PoseMatData, SpeedData, TimeData
    
    def simulation(self):
        d2r = np.deg2rad
        b = self.Time.ReadNowTime()
        newHomogeneousMat = database_HomogeneousMat.Load("dataBase/dynamicllyPlanTEST/newHomogeneousMat.csv")
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
        database_JointAngle.Save(JointAngleData, "dataBase/dynamicllyPlanTEST/newJointAngle.csv", "w")
        # self.Sim.paitGL(JointAngleData, newHomogeneousMat)

    def NormalCmd(self, RPdata, Veldata, alreadySentNBR, sysTime, I0, batch):
        """基本任務
        1.讀取機器手臂位置
        2.讀取DX200 I000變數值
        """
        if self.Line is True:
            # 讀取實際手臂位置
            pos_result, coordinate = self.Udp.getcoordinateMH(101)
            # # 讀取I000變數
            # I0 = self.Udp.ReadVar("Integer", 0)
            # 儲存實際軌跡資料
            self.RealTrajectory[self.RealDataCounter] = np.array([coordinate])
            self.RealsysTime[self.RealDataCounter] = sysTime

    
        else:
            # 模擬讀取實際手臂位置並儲存
            if alreadySentNBR == batch:
                self.RealTrajectoryData[self.RealDataCounter] = RPdata[batch-1]
                self.RealSpeedData[self.RealDataCounter] = Veldata[batch-1]
            else:    
                self.RealTrajectoryData[self.RealDataCounter] = RPdata[alreadySentNBR]
                self.RealSpeedData[self.RealDataCounter] = Veldata[alreadySentNBR]
            self.RealDataCounter += 1

            # 模擬I0變換
            if I0 == [3]:
                I0 = [11]
            else:
                I0 = [3]
        
        return I0


    def main(self):
        #---------------------------------------------Inital-----------------------------------------------
        # 初始化Pygame
        pygame.init()

        # 設置畫面寬高
        screen_width = 800
        screen_height = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        # 紀錄UDP目前已送出的資料筆數
        alreadySentNBR = 0
        # 系統時間與軌跡節點
        sysTime, Node = 0, 0
        startNode = 0
        # 取樣時間
        sampleTime = 0.04
        # 系統時間初始化flag
        sysflag = True
        # 最後一筆資料覆寫
        finalDataFlag = True

        # 計算資料分割的組數與批數
        batch = self.calculateDataGroupBatch(self.trjData)
        
        # 資料分割
        RPdata, Veldata = self.dataSegmentation(self.trjData, self.velData, batch)
        
        # 包裝並寫入首9筆資料   
        RPpacket, Velpacket, alreadySentNBR = self.packetRPdataVeldata(RPdata, Veldata, alreadySentNBR)
        Is_success = self.writeRPvarINTvar(2, RPpacket, Velpacket)
        self.RealTrajectoryData[self.RealDataCounter] = RPdata[0]
        self.RealSpeedData[self.RealDataCounter] = Veldata[0]
        self.RealDataCounter+=1
        
        # 軌跡規劃執行緒
        Thread_started = False
        planThread = GetNewTrj(target=self.PlanNewTrj)

        # 軌跡資料儲存容器(驗證資料)
        
        #-------------------------------------------------------------------------------------------------
        
        if self.Line is False:
            # I0模擬
            self.I0 = [2]

        # 實驗三段變速實驗用
        Threadcount = 0

        # 主迴圈旗標 | 開關
        mainLoop = False
        while True:
            if self.Line is True:
                pos_result, coordinate = self.Udp.getcoordinateMH(101)
                if np.linalg.norm(np.array(coordinate) - self.trjData[0, 0]) <= 0.12:
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
                # 儲存系統開始時間
                startTime = self.Time.ReadNowTime()
                sysflag = False

                

            sysTime, Node = self.Time.sysTime(startTime, startNode, nowTime, sampleTime)
            sysTime = round(sysTime/1000, 1)
            
            
            #----------------------------------------------命令執行區-----------------------------------------
            # 常規命令>>讀取位置與I000
            # self.I0 = self.NormalCmd(RPdata, Veldata, alreadySentNBR, sysTime, self.I0, batch)
            # 讀取I000變數
            
            # 讀取I0
            if self.Line is True:
                self.I0 = self.Udp.ReadVar("Integer", 0)

            else:
                # 模擬I0變換
                if self.I0 == [3]:
                    self.I0 = [11]
                else:
                    self.I0 = [3]
            
            #----------------------------------------------資料通訊區-----------------------------------------
            """
            通訊
            * 變數區間:
            1. I02 - I10
            2. I11 - I19
            """
            
            if self.I0 == [3] and finalDataFlag is True:
                # 起始變數位置
                firstAddress = 11
                # 打包需要傳送的變數資料
                RPpacket, Velpacket, alreadySentNBR = self.packetRPdataVeldata(RPdata, Veldata, alreadySentNBR)
                # 將打包完的資料寫入DX200
                Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)

                # 紀錄通訊所傳輸的資料
                if self.Line is True:
                    if alreadySentNBR == batch:
                        self.RealTrajectoryData[self.RealDataCounter] = RPdata[batch-1]
                        self.RealSpeedData[self.RealDataCounter] = Veldata[batch-1]
                    else:    
                        self.RealTrajectoryData[self.RealDataCounter] = RPdata[alreadySentNBR]
                        self.RealSpeedData[self.RealDataCounter] = Veldata[alreadySentNBR]
                    self.RealDataCounter += 1
                else:
                    # 模擬通訊時間
                    self.Time.time_sleep(0.36)

            elif self.I0 == [11] and finalDataFlag is True:
                # 起始變數位置
                firstAddress = 2
                # 打包需要傳送的變數資料
                RPpacket, Velpacket, alreadySentNBR = self.packetRPdataVeldata(RPdata, Veldata, alreadySentNBR)
                # 將打包完的資料寫入DX200
                Is_success = self.writeRPvarINTvar(firstAddress, RPpacket, Velpacket)
                
                # 紀錄通訊所傳輸的資料
                if self.Line is True:
                    if alreadySentNBR == batch:
                        self.RealTrajectoryData[self.RealDataCounter] = RPdata[batch-1]
                        self.RealSpeedData[self.RealDataCounter] = Veldata[batch-1]
                    else:    
                        self.RealTrajectoryData[self.RealDataCounter] = RPdata[alreadySentNBR]
                        self.RealSpeedData[self.RealDataCounter] = Veldata[alreadySentNBR]
                    self.RealDataCounter += 1

                else:
                    # 模擬通訊時間
                    self.Time.time_sleep(0.36)
            
            
            self.I0 = self.NormalCmd(RPdata, Veldata, alreadySentNBR, sysTime, self.I0, batch)

            if alreadySentNBR == batch and finalDataFlag is True:
                """結束條件
                外迴圈數 = 批次數
                """
                print("軌跡實驗結束")

                finalDataFlag = False
                print(sysTime)

                # -------------------------------------驗證軌跡與速度資料集-----------------------------------
                # 讀取最後一刻軌跡資料
                
                if self.Line is True:
                    
                    can_End = False
                    while True:
                        self.I0 = self.NormalCmd(RPdata, Veldata, alreadySentNBR, sysTime, self.I0, batch)
                        # 讀取I000變數
                        self.I0 = self.Udp.ReadVar("Integer", 0)
                        quotient, remainder = divmod(RPdata.shape[0]*RPdata.shape[1], 18)
                        
                        if remainder == 9 and self.I0 == [11]:
                            can_End = True
                        elif remainder == 0 and self.I0 == [2]:
                            can_End = True
                        else: 
                            can_End = False

                        if can_End is True:
                            # feedback的軌跡資料
                            # 濾除整個row為0的部分
                            non_zero_rows_Trajectory = np.any(self.RealTrajectory != 0, axis=(1, 2))
                            non_zero_rows_Time = np.any(self.RealsysTime != 0, axis=1)

                            self.RealTrajectory = self.RealTrajectory[non_zero_rows_Trajectory]
                            self.RealsysTime = self.RealsysTime[non_zero_rows_Time]
                            database_PoseMat.Save(self.RealTrajectory, "dataBase/dynamicllyPlanTEST/RealTrajectory.csv", "w")
                            database_time.Save(self.RealsysTime, "dataBase/dynamicllyPlanTEST/RealsysTime.csv", "w")
                            
                            # 儲存通訊所送出的軌跡資料
                            self.RealTrajectoryData = self.RealTrajectoryData.reshape(-1, 1, 6)
                            self.RealSpeedData = self.RealSpeedData.reshape(-1, 1)
                            # 濾除整個row為0的部分
                            non_zero_rows_Trajectory = np.any(self.RealTrajectoryData != 0, axis=(1, 2))
                            non_zero_rows_Speed = np.any(self.RealSpeedData != 0, axis=1)

                            self.RealTrajectoryData = self.RealTrajectoryData[non_zero_rows_Trajectory]
                            self.RealSpeedData = self.RealSpeedData[non_zero_rows_Speed]
                            database_PoseMat.Save(self.RealTrajectoryData, "dataBase/dynamicllyPlanTEST/verifyTrajectory.csv", "w")
                            database_Velocity.Save(self.RealSpeedData, "dataBase/dynamicllyPlanTEST/verifySpeed.csv", "w")
                            
                            break
                else:
                    self.RealTrajectoryData = self.RealTrajectoryData.reshape(-1, 1, 6)
                    self.RealSpeedData = self.RealSpeedData.reshape(-1, 1)
                    # 濾除整個row為0的部分
                    non_zero_rows_Trajectory = np.any(self.RealTrajectoryData != 0, axis=(1, 2))
                    non_zero_rows_Speed = np.any(self.RealSpeedData != 0, axis=1)

                    self.RealTrajectoryData = self.RealTrajectoryData[non_zero_rows_Trajectory]
                    self.RealSpeedData = self.RealSpeedData[non_zero_rows_Speed]
                    database_PoseMat.Save(self.RealTrajectoryData, "dataBase/dynamicllyPlanTEST/verifyTrajectory.csv", "w")
                    database_Velocity.Save(self.RealSpeedData, "dataBase/dynamicllyPlanTEST/verifySpeed.csv", "w")

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
                        startPlan_alreadySentNBR = alreadySentNBR
                        
                        if self.Line is True:
                            # 讀取當下位置
                            pos_result, coordinate = self.Udp.getcoordinateMH(101)
                            # 設定新軌跡起點
                            NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]]
                        else:
                            # 模擬讀取當下位置
                            coordinate = RPdata[startPlan_alreadySentNBR, 0]
                            # 設定新軌跡起點
                            NowEnd = [coordinate[0], coordinate[1], coordinate[2], coordinate[3]/10, coordinate[4]/10, coordinate[5]/10]

                        

                        # 終點與原軌跡保持一致
                        GoalEnd = [self.trjData[-1, 0, 0], self.trjData[-1, 0, 1], self.trjData[-1, 0, 2], self.trjData[-1, 0, 3], self.trjData[-1, 0, 4], self.trjData[-1, 0, 5]]
                        
                        # TODO 預計由UI寫入
                        # GoalSpeed = float(input("請輸入走速："))
                        if Threadcount == 0:
                            GoalSpeed = 1.5
                        else: 
                            GoalSpeed = 2
                        print(f"理想速度: {GoalSpeed} mm/s")
                        
                        # 執行緒
                        planThread = GetNewTrj(target=self.PlanNewTrj, args=(NowEnd, GoalEnd, sampleTime, GoalSpeed))
                        planThread.start()

                        # 改變狀態旗標>>> 執行續已被啟動過
                        Thread_started = True
                        Threadcount += 1
                        

            if planThread.is_alive() is False and Thread_started is True:
                # 取出執行緒計算結果
                b = self.Time.ReadNowTime()
                result = planThread.get_result()
                
                NewHomogeneousMat = result[0]
                NewPoseMatData = result[1]
                NewSpeedData = result[2]
                NewTimeData = result[3]

                
                # 存檔(新軌跡資料) 
                mode = "w"
                database_HomogeneousMat.Save(NewHomogeneousMat, "dataBase/dynamicllyPlanTEST/newHomogeneousMat.csv", mode)
                database_PoseMat.Save(NewPoseMatData, "dataBase/dynamicllyPlanTEST/newPoseMat.csv", mode)
                database_Velocity.Save(NewSpeedData, "dataBase/dynamicllyPlanTEST/newSpeed.csv", mode)
                database_time.Save(NewTimeData,"dataBase/dynamicllyPlanTEST/newTime.csv", mode)
                
                # 規劃完時，紀錄舊軌跡已經寫入的資料批數
                endPlan_alreadySentNBR = alreadySentNBR
                # 計算規劃時，時間差所產生的資料落後批數
                dataErr = endPlan_alreadySentNBR-startPlan_alreadySentNBR
                print("系統反應時間所消耗的資料(批次)數: ", dataErr)

                
                # TODO 資料整併只支援1段變速，並不支援2段變速
                # -----------------------------------資料整併(軌跡)--------------------------------------------------------------
                oldFile_PoseMat = "dataBase/dynamicllyPlanTEST/PoseMat.csv"
                newFile_PoseMat = "dataBase/dynamicllyPlanTEST/newPoseMat.csv"
                RemixFile_PoseMat = "dataBase/dynamicllyPlanTEST/testRemix_PoseMat.csv"
                data_frame1 = pd.read_csv(oldFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
                data_frame2 = pd.read_csv(newFile_PoseMat, delimiter=',', dtype=np.float64, encoding='utf-8')
                # 取得舊資料切換新資料時的最後一筆資料
                # 提取舊資料
                oldFileIndex = endPlan_alreadySentNBR*9
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
                oldFile_Speed = "dataBase/dynamicllyPlanTEST/Speed.csv"
                newFile_Speed = "dataBase/dynamicllyPlanTEST/newSpeed.csv"
                RemixFile_Speed = "dataBase/dynamicllyPlanTEST/testRemix_Speed.csv"
                data_frame1 = pd.read_csv(oldFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
                data_frame2 = pd.read_csv(newFile_Speed, delimiter=',', dtype=np.float64, encoding='utf-8')
                # 取得舊資料切換新資料時的最後一筆資料
                # 提取舊資料
                oldFileIndex = endPlan_alreadySentNBR*9
                dfBuffer1 = data_frame1.iloc[:oldFileIndex]
                # 找相似的資料
                targetData = data_frame1.iloc[oldFileIndex]
                # 要合併的新資料
                dfBuffer2 = data_frame2.iloc[closestIndex+1:]
                Remix_Speed_df = pd.concat([dfBuffer1, dfBuffer2], axis=0)
                Remix_Speed_df.to_csv(RemixFile_Speed, index=False,  header=True)
                Remix_Speed = np.array(Remix_Speed_df)

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
                # alreadySentNBR += dataErr
                # 更新Batch，將總批次數更新成與合併後的軌跡檔案相符的
                batch = NewRemixBatch
                
                Thread_started = False
                print("--------------新軌跡資料已覆寫---------------")

                a = self.Time.ReadNowTime()
                err = self.Time.TimeError(b,a)
                err = err["millisecond"]
                print(f"新軌跡規劃後處理所花時長: {err} ms")

                # 計算IK
                SimThread = threading.Thread(target=self.simulation)
                SimThread.start()
            #-----------------------------------------------------------------------------------------------
            singlelooptime2 = self.Time.ReadNowTime()
            singleloopCosttime = self.Time.TimeError(singlelooptime1, singlelooptime2)
            # 剩餘時間
            laveTime = sampleTime*1000 - singleloopCosttime["millisecond"]
            self.Time.time_sleep(laveTime*0.001)
            # print("迴圈剩餘時間: ", laveTime, "ms")


            
if __name__ == "__main__":
    trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat.csv"
    speeddataPath = "dataBase/dynamicllyPlanTEST/Speed.csv"
    Motomancontrol(trjdataPath, speeddataPath).main()



