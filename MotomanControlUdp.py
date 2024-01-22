import threading
import time
import sys
import cv2
# from MotomanUdpPacket import MotomanUDP
from dataBase import dataBase
import numpy as np
from Toolbox import TimeTool




"""
軌跡實驗
1. 載入已產生之軌跡資料(Carteisn space)
2. 開始(按鈕控制)
3. 讀取位置並存檔
4. 現在位置與資料庫做比對，若有誤差則修正
"""



def readNowPosCMD():
    global t1, sysTime, Node
    # 讀取位置後存檔
    # pos_result, coordinate = udp.getcoordinateMH()
    # print(coordinate)
    NowPos[0,0] = round(955.398-t1, 4)
    NowPos[0,1] = round(-87.132+t1, 4)
    NowPos[0,2] = round(-166.811-t1, 4)
    NowPos[0,3] = round(-165.2914+t1, 4)
    NowPos[0,4] = round(-7.1824-t1, 4)
    NowPos[0,5] = round(17.5358+t1, 4)

    # NowPos[0,0] = coordinate[0]
    # NowPos[0,1] = coordinate[1]
    # NowPos[0,2] = coordinate[2]
    # NowPos[0,3] = coordinate[3]
    # NowPos[0,4] = coordinate[4]
    # NowPos[0,5] = coordinate[5]
    
    db.Save_singleData_experiment(NowPos, sysTime, "dataBase/testTrajectory.csv")
    
    print("讀取")
    t1 +=1
    # print("t1: ", t1)
    
def sendMoveCMD():
    global t2, sysTime, Node, GoalEnd

    print("寫入Goal位置")
    
    # status = udp.moveMH(2,1, 14, 17, GoalEnd)

    t2 +=1
    # print("t2 :", t2)
    
def main():
    global sysTime, Node
    # Servo ON
    # Servo_status = udp.ServoMH(1)
    start = True
    startNode = 0
    while True:
        
        sendcmd = threading.Thread(target=sendMoveCMD)
        readcmd = threading.Thread(target=readNowPosCMD)

        # 將執行緒設置為守護執行緒
        sendcmd.daemon = True
        readcmd.daemon = True

        # Start the thread
        sendcmd.start()
        readcmd.start()
        if start is True: 
            startTime = Time.ReadNowTime()
            start = False

        nowTime = Time.ReadNowTime()
        
        sysTime, Node = Time.sysTime(startTime, startNode, nowTime, 0.001)
        print("系統時間(ms): ", sysTime/1000)

        # # Wait for the thread to finish (optional)
        # sendcmd.join()
        # readcmd.join()

        # cv鍵盤事件
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # 27是'ESC'鍵的ASCII碼
            print('You pressed "ESC". Exiting...')
            print("Hold ON ➜ Servo OFF ➜ Hold OFF ➜ I/O Reset ➜ loop berak")
            # status = udp.holdMH(2)
            # time.sleep(0.01)
            # status = udp.ServoMH(2)
            # udp.WriteIO(2701, 0)
            break

        elif key == ord('h'):
            print('Hold on')
            # status = udp.holdMH(1)
            time.sleep(5)
        
if __name__ == "__main__":
    db = dataBase()
    Time = TimeTool()
    # udp = MotomanUDP()

    # 載入軌跡資訊
    filepath = "dataBase/MatrixPathPlanning.csv"
    pathDict, pathDf, pathNp4x4, pathNp6x1 = db.LoadMatrix4x4(filepath)

    # 創建一個空視窗
    cv2.namedWindow('Control Motoman Window')

    # 設定Goal
    GoalEnd = [955.398, -87.132, -166.811, -165.2914, -7.1824, 17.5358]

    # 位置暫存器
    NowPos = np.zeros((1, 6))

    # 系統時間
    t1 = 0
    t2 = 1
    sysTime, Node = 0, 0
    
    # Servo ON
    # Servo_status = udp.ServoMH(1)

    # 確認Servo Power狀態
    # sys_status = udp.getstatusMH()
    sys_status = 64

    # if sys_status[4] == 64:
    if sys_status == 64:
        main()
        # 釋放資源
        cv2.destroyAllWindows()

    else:
        print("Servo ON失敗")


#%%
# # Servo ON
# Servo_status = udp.ServoMH(1)

# # 讀取是否Servo ON成功
# sys_status = udp.getstatusMH()
# print(sys_status)

# if sys_status[4] == 64:
#     print("Servo ON is success")
#     # 0: speed * 0.01 %
#     # 1: speed * 0.1 mm/s
#     # 2: speed * 0.1 deg/s
    
    
#     while True:
#         # 等待鍵盤事件，並取得按下的鍵
#         key = cv2.waitKey(1) & 0xFF

#         # 離開
#         if key == 27:  # 27是'ESC'鍵的ASCII碼
#             print('You pressed "ESC". Exiting...')
#             print("Hold ON ➜ Servo OFF ➜ Hold OFF ➜ I/O Reset ➜ loop berak")
#             # status = udp.holdMH(2)
#             # time.sleep(0.01)
#             # status = udp.ServoMH(2)
#             # udp.WriteIO(2701, 0)
#             break

#         elif key == ord('h'):
#             print('Hold on')
#             # status = udp.holdMH(1)
        
#         elif key == ord('w'):
#             print('Send Position Error')
#             print("Hold on ➜ Hold OFF ➜ Send Position error cmd")
            
#             # status = udp.holdMH(1)
#             # time.sleep(0.01)
#             # status = udp.holdMH(2)

#             # 增量型
#             # dp = [10, 0, 0, 0, 0, 0]
#             # status = udp.moveMH(3, 1, 100, 17, dp)
#             # print(status)

#             while True:
#                 print("讀取是否運轉中")
                
#                 # sys_status = udp.getstatusMH()
#                 # print(sys_status)

#                 if sys_status[0] == 194:
#                     # 回歸原本路徑
#                     print("誤差已校正，須給New Goal End")
                    
#                     # status = udp.moveMH(2,1, 100, 17, weldend)
#                     # print(status)
#                     break
#                 else:
#                     print("Manipulator operating!!")
#                     time.sleep(0.01)
            
#         elif key == ord('r'):
#             print('Hold off and Servo off')
#             time.sleep(0.02)
#             # status = udp.holdMH(2)
#             # time.sleep(0.01)
#             # status = udp.ServoMH(2)

#         elif key == ord('s'):
#             print('Read Position and Torque')
#             time.sleep(0.02)
#             # pos_result, coordinate = udp.getcoordinateMH()
#             # print(coordinate)
#             # sys_result = udp.getstatusMH()
#             # print(sys_result)
#             # torque = udp.getTorqueMH()
#             # print(torque)

#         elif key == ord('n'):
#             print('Arc ON')
#             time.sleep(0.03)
#             # udp.WriteIO(2701, 12)
#             # status = udp.moveMH(2,1, 14, 17, weldend)
#             # print(status)

#         elif key == ord('f'):
#             print('Arc OFF')
#             time.sleep(0.03)
#             # udp.WriteIO(2701, 0)

#     # 釋放資源
#     cv2.destroyAllWindows()
# else:
#     print(Servo_status)



#%%
# # flag
# flagMOVE_0 = False
# flagMOVE_1 = False
# flagMOVE_2 = False
# flagMOVE_3 = False
# flagMOVE_4 = False



# # coordinate point
# workORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
# pre_weldingStart = [958.58, -102.274, -114.748, -165.2922, -7.1994, 17.5635]
# weldingStart = [958.58, -102.274, -164.748, -165.2922, -7.1994, 17.5635]
# weldingEnd = [956.709, 23.919, -164.373, -165.2942, -7.2005, 17.5837]
# pre_backORG = [956.709, 23.919, -114.373, -165.2942, -7.2005, 17.5837]

# # System Time
# sysTimer = 0

# # data
# NextPos = []

# # class
# udp = MotomanUDP() 

# def sendMoveCMD(workORG, pre_weldingStart, weldingStart, weldingEnd, pre_backORG):
#     """到達上一時刻的目標位置後，寄送下一刻的MOVE CMD
#     - Flag: MOVE(only one)
#     """
#     global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4
    
#     if flagMOVE_0 is True:
#         print("Servo ON")
#         print("Robot GO to 預起弧點")
#         status = udp.moveMH(1,10, 17, pre_weldingStart)
#         print(status)
#         # time.sleep(0.03)
#         flagMOVE_0 = False

#     elif flagMOVE_1 is True:
#         print("Robot GO to 起弧點")
#         status = udp.moveMH(1,10, 17, weldingStart)
#         print(status)
#         # time.sleep(0.03)
#         flagMOVE_1 = False

#     elif flagMOVE_2 is True:
#         print("起弧")
#         print("送絲")
#         print("Robot GO to 收弧點")
#         status = udp.moveMH(1,10, 17, weldingEnd)
#         print(status)
#         # time.sleep(0.03)
#         flagMOVE_2 = False
    
#     elif flagMOVE_3 is True:
#         print("收弧")
#         print("停止送絲")
#         print("Robot GO to 預回點")
#         status = udp.moveMH(1,10, 17, pre_backORG)
#         print(status)
#         # time.sleep(0.03)
#         flagMOVE_3 = False

#     elif flagMOVE_4 is True:
#         print("Robot GO to 回原點")
#         status = udp.moveMH(1,10, 17, workORG)
#         print(status)
#         # time.sleep(0.03)
#         flagMOVE_4 = False

#     else:
#         time.sleep(0.01)
#         # print("pass")

# def readNowPosCMD(workORG, pre_weldingStart, weldingStart, weldingEnd, pre_backORG):
#     """無限讀取位置，當位置在預定目標位置上時，提醒可以送下一個目標位置指令
#     """
#     global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4
#     print(sysTimer)

#     # Read Now Position 
#     result, coordinate = udp.getcoordinateMH()

#     # check CMD is OK
#     if len(result) == 0x0:
#         if coordinate == workORG:
#             flagMOVE_0 = True
#             print("Go to 預起弧點") 

#         elif coordinate == pre_weldingStart:
#             flagMOVE_1 = True
#             print("Go to 起弧點")
        
#         elif coordinate == weldingStart:
#             flagMOVE_2 = True
#             print("Go to 收弧點")
        
#         elif coordinate == weldingEnd:
#             flagMOVE_3 = True
#             print("Go to 預回原點")

        
#         elif coordinate == pre_backORG:
#             flagMOVE_4 = True
#             print("Go to 回原點")

#         else:
#             time.sleep(0.025)
#             print("readNowpos cmd")

#     else:
#         # TODO EMS switch (use I/O control)
#         sys.exit("Warnning: Motoman read CMD error!!!")

# def main():
#     global sysTimer
#     while True:
#         try:
#             if keyboard.is_pressed('esc'):
#                 print('You pressed "ESC". Exiting...')
#                 break

#             # Create a new thread
#             sendcmd = threading.Thread(target=sendMoveCMD)
#             readcmd = threading.Thread(target=readNowPosCMD)

#             # Start the thread
#             sendcmd.start()
#             readcmd.start()

#             # Wait for the thread to finish (optional)
#             sendcmd.join()
#             readcmd.join()

#             sysTimer += 0.1
#             sysTimer = round(sysTimer, 2)

#         except KeyboardInterrupt:
#             break
            

# if __name__ == "__main__":
#     main()