from MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one
from Kinematics import *
from TimeTool import *
import numpy as np

kin = Kinematics
mh = MotomanConnector() #Create connector
time = TimeTool()

mh.connectMH()  #Connect
ONt1 = time.ReadNowTime()
# Servo ON/OFF  ON cmd大約750ms左右; OFF cmd大約320ms
# mh.Servo_ON_OFF('ON')
# ONt2 = time.ReadNowTime()
mh.Servo_ON_OFF('OFF')
ONt2 = time.ReadNowTime()

#　MOVJ cmd = f"{Speed(%)},{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}\r"
ORGcmd = [2, 1, 485.267, -1.225, 234.322, 179.9840, 20.2243, 1.6886, 0, 5, 0, 0, 0, 0, 0, 0]
Startcmd = [2, 1, 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523, 0, 5, 0, 0, 0, 0, 0, 0]

# Movet1 = time.ReadNowTime()
mh.MOVJ(ORGcmd) 
# Movet2 = time.ReadNowTime()

# MOVL cmd = f"{Speed(0 or 1)},{speed(mm/s or deg/s)}{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}"
MOVLcmd_Start = [0, 20, 1, 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523, 0, 5, 0, 0, 0, 0, 0, 0]
MOVLcmd_End = [0, 20, 1, 955.326, -178.005, -154.700, -168.3718, -2.9293, 7.0363, 0, 5, 0, 0, 0, 0, 0, 0]

Movet1 = time.ReadNowTime()
# mh.MOVL(MOVLcmd_End)
Movet2 = time.ReadNowTime()

mh.disconnectMH() #Disconnect
print('Servo ON/OFF cost time', time.TimeError(ONt1,ONt2))
print('MOVL cmd cost time', time.TimeError(Movet1,Movet2))
print('end')