import threading
import time
import sys
import keyboard
from MotomanUdpPacket import MotomanUDP

# flag
flagMOVE_0 = False
flagMOVE_1 = False
flagMOVE_2 = False
flagMOVE_3 = False
flagMOVE_4 = False



# coordinate point
workORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
pre_weldingStart = [958.58, -102.274, -114.748, -165.2922, -7.1994, 17.5635]
weldingStart = [958.58, -102.274, -164.748, -165.2922, -7.1994, 17.5635]
weldingEnd = [956.709, 23.919, -164.373, -165.2942, -7.2005, 17.5837]
pre_backORG = [956.709, 23.919, -114.373, -165.2942, -7.2005, 17.5837]

# System Time
sysTimer = 0

# data
NextPos = []

# class
udp = MotomanUDP() 

def sendMoveCMD(workORG, pre_weldingStart, weldingStart, weldingEnd, pre_backORG):
    """到達上一時刻的目標位置後，寄送下一刻的MOVE CMD
    - Flag: MOVE(only one)
    """
    global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4
    
    if flagMOVE_0 is True:
        print("Servo ON")
        print("Robot GO to 預起弧點")
        status = udp.moveMH(1,10, 17, pre_weldingStart)
        print(status)
        # time.sleep(0.03)
        flagMOVE_0 = False

    elif flagMOVE_1 is True:
        print("Robot GO to 起弧點")
        status = udp.moveMH(1,10, 17, weldingStart)
        print(status)
        # time.sleep(0.03)
        flagMOVE_1 = False

    elif flagMOVE_2 is True:
        print("起弧")
        print("送絲")
        print("Robot GO to 收弧點")
        status = udp.moveMH(1,10, 17, weldingEnd)
        print(status)
        # time.sleep(0.03)
        flagMOVE_2 = False
    
    elif flagMOVE_3 is True:
        print("收弧")
        print("停止送絲")
        print("Robot GO to 預回點")
        status = udp.moveMH(1,10, 17, pre_backORG)
        print(status)
        # time.sleep(0.03)
        flagMOVE_3 = False

    elif flagMOVE_4 is True:
        print("Robot GO to 回原點")
        status = udp.moveMH(1,10, 17, workORG)
        print(status)
        # time.sleep(0.03)
        flagMOVE_4 = False

    else:
        time.sleep(0.01)
        # print("pass")

def readNowPosCMD(workORG, pre_weldingStart, weldingStart, weldingEnd, pre_backORG):
    """無限讀取位置，當位置在預定目標位置上時，提醒可以送下一個目標位置指令
    """
    global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4
    print(sysTimer)

    # Read Now Position 
    result, coordinate = udp.getcoordinateMH()

    # check CMD is OK
    if len(result) == 0x0:
        if coordinate == workORG:
            flagMOVE_0 = True
            print("Go to 預起弧點") 

        elif coordinate == pre_weldingStart:
            flagMOVE_1 = True
            print("Go to 起弧點")
        
        elif coordinate == weldingStart:
            flagMOVE_2 = True
            print("Go to 收弧點")
        
        elif coordinate == weldingEnd:
            flagMOVE_3 = True
            print("Go to 預回原點")

        
        elif coordinate == pre_backORG:
            flagMOVE_4 = True
            print("Go to 回原點")

        else:
            time.sleep(0.025)
            print("readNowpos cmd")

    else:
        # TODO EMS switch (use I/O control)
        sys.exit("Warnning: Motoman read CMD error!!!")

def main():
    global sysTimer
    while True:
        try:
            if keyboard.is_pressed('esc'):
                print('You pressed "ESC". Exiting...')
                break

            # Create a new thread
            sendcmd = threading.Thread(target=sendMoveCMD)
            readcmd = threading.Thread(target=readNowPosCMD)

            # Start the thread
            sendcmd.start()
            readcmd.start()

            # Wait for the thread to finish (optional)
            sendcmd.join()
            readcmd.join()

            sysTimer += 0.1
            sysTimer = round(sysTimer, 2)

        except KeyboardInterrupt:
            break
            

if __name__ == "__main__":
    main()