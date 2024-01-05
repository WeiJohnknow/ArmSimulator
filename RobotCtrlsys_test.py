import threading
import time
import keyboard

# flag
flagMOVE_0 = False
flagMOVE_1 = False
flagMOVE_2 = False
flagMOVE_3 = False
flagMOVE_4 = False
flagMOVE_5 = False
flagArcon = False
flagWireout = False
flagWireback = False


# Data sequence index value extracted from the database
dataIndex = 0
sysTimer = 0

# data
NextPos = []




def sendMoveCMD():
    """到達上一時刻的目標位置後，寄送下一刻的MOVE CMD
    - Flag: MOVE(only one)
    """
    global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4, dataIndex, flagArcon, flagWireout, flagWireback, NextPos
    
    if flagMOVE_0 is True:
        print("Robot GO to 預起弧點")
        time.sleep(0.03)
        flagMOVE_0 = False

    elif flagMOVE_1 is True:
        print("Robot GO to 起弧點")
        time.sleep(0.03)
        flagMOVE_1 = False

    elif flagMOVE_2 is True:
        print("起弧")
        print("送絲")
        print("Robot GO to 收弧點")
        time.sleep(0.03)
        flagMOVE_2 = False
    
    elif flagMOVE_3 is True:
        print("收弧")
        print("停止送絲")
        print("Robot GO to 預回點")
        time.sleep(0.03)
        flagMOVE_3 = False

    elif flagMOVE_4 is True:
        print("Robot GO to 回原點")
        time.sleep(0.03)
        flagMOVE_4 = False

    else:
        time.sleep(0.01)
        # print("pass")

def readNowPosCMD():
    """無限讀取位置，當位置在預定目標位置上時，提醒可以送下一個目標位置指令
    """
    global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4, dataIndex, sysTimer, flagArcon, flagWireout, flagWireback, NextPos
    print(sysTimer)
    # TODO 有問題
    if sysTimer == 0:
        flagMOVE_0 = True
        print("Go to 預起弧點") 

    elif round(sysTimer, 2) == 3:
        flagMOVE_1 = True
        print("Go to 起弧點")
    
    elif round(sysTimer, 2) == 5:
        flagMOVE_2 = True
        print("Go to 收弧點")
    
    elif round(sysTimer, 2) == 7:
        flagMOVE_3 = True
        print("Go to 預回原點")

    
    elif round(sysTimer, 2) == 10:
        flagMOVE_4 = True
        print("Go to 回原點")

    else:
        time.sleep(0.025)
        print("readNowpos cmd")
    
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