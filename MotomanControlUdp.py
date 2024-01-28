import threading
import time
import sys
import cv2
from MotomanUdpPacket import MotomanUDP
from dataBase import dataBase
import numpy as np
from Toolbox import TimeTool
import timeit



"""
軌跡實驗
1. 載入已產生之軌跡資料(Carteisn space)
2. 開始(按鈕控制)
3. 讀取位置並存檔
4. 現在位置與資料庫做比對，若有誤差則修正
"""


def readNowPosCMD(sampleTime):
    """現實機械手位置與扭矩資料取樣專用
    - Arg:
        - sampleTime: Unit second.
    """
    global sysTime
    
    startTime = Time.ReadNowTime()
    # Read coordinate
    pos_result, coordinate = udp.getcoordinateMH()

    NowPos[0,0] = coordinate[0]
    NowPos[0,1] = coordinate[1]
    NowPos[0,2] = coordinate[2]
    NowPos[0,3] = coordinate[3]
    NowPos[0,4] = coordinate[4]
    NowPos[0,5] = coordinate[5]
    header = ["S", "L", "U", "R", "B", "T"]
    db.Save_singleData_experiment(NowPos, sysTime, "dataBase/testTrajectory.csv", header)

    # Read Torque
    Torque = udp.getTorqueMH()

    NowTorque[0,0] = Torque[0]
    NowTorque[0,1] = Torque[1]
    NowTorque[0,2] = Torque[2]
    NowTorque[0,3] = Torque[3]
    NowTorque[0,4] = Torque[4]
    NowTorque[0,5] = Torque[5]
    header = ["S", "L", "U", "R", "B", "T"]
    db.Save_singleData_experiment(NowTorque, sysTime, "dataBase/testTrajectory_torque.csv", header)
    
    endTime = Time.ReadNowTime()
    # 計算Read coordinate和Read Torque共花多少時間
    Errtime = Time.TimeError(startTime, endTime)

    # 儲存每個cmd的時間
    db.Save_time(Errtime["millisecond"], "dataBase/ReadcoordCMDtime.csv")

    # 單位轉換 second ➜ millisecond
    sampleTime = sampleTime/1000

    # 計算該取樣時間內，經過讀取位置與扭矩參數後剩餘的時間
    CMDTimeError = sampleTime - Errtime["millisecond"]

    # 剩餘的時間使用time sleep消耗掉，以確保sampleTime的正確性
    Time.time_sleep(CMDTimeError/1000)


def main():
    
    # Servo ON
    Servo_status = udp.ServoMH(1)
    start = True
    startNode = 0

    # status = udp.moveMH(2,1, 500, 17, GoalEnd)

    # 確認Servo Power狀態
    sys_status = udp.getstatusMH()

    if sys_status[4] == 64:
        pass

    while True:
        
        # 儲存系統開始時間
        if start is True: 
            startTime = Time.ReadNowTime()
            start = False

        # 更新每禎時間
        nowTime = Time.ReadNowTime()
        
        sysTime, Node = Time.sysTime(startTime, startNode, nowTime, 0.001)
        # print("系統時間(ms): ", sysTime/1000)


        # cv鍵盤事件
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # 27是'ESC'鍵的ASCII碼
            print('You pressed "ESC". Exiting...')
            print("Hold ON ➜ Servo OFF ➜ Hold OFF ➜ I/O Reset ➜ loop berak")
            status = udp.holdMH(2)
            time.sleep(0.01)
            status = udp.ServoMH(2)
            udp.WriteIO(2701, 0)
            break

        elif key == ord('h'):
            print('Hold on')
            status = udp.holdMH(1)
            time.sleep(5)
        
if __name__ == "__main__":
    db = dataBase()
    Time = TimeTool()
    udp = MotomanUDP()

    # 載入軌跡資訊
    # filepath = "dataBase/MatrixPathPlanning.csv"
    # pathDict, pathDf, pathNp4x4, pathNp6x1 = db.LoadMatrix4x4(filepath)

    # 創建一個控制視窗
    cv2.namedWindow('Control Motoman Window')

    # 設定Goal
    ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
    GoalEnd = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]

    # 暫存器
    NowPos = np.zeros((1, 6))
    NowTorque = np.zeros((1, 6))

    # 系統時間與軌跡節點
    sysTime, Node = 0, 0
    
    main()


    # 釋放資源
    cv2.destroyAllWindows()

    


