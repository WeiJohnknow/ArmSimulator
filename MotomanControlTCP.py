from MotomanEthernet import MotomanConnector
from MotomanEthernetUDP import UdpPacket, UdpPacket_Ans, UdpPacket_Req
from TimeTool import *
from Kinematics import *
import numpy as np

class ControlMA1440:
    def __init__(self) -> None:
        self.mh = MotomanConnector()
        self.kin = Kinematics()
        self.time = TimeTool()
        pass

    def testCmd(self):
        self.mh.connectMH()
        '''
        RSTART = 74
        Data1
            mode: Play 64
            cycle : Yes  2
            Running(與示教器START狀態一致) : Yes 8
        RSTART = 66
        Data1
            mode: teach 32
            cycle : Yes  2
            Running : Yes 8

        RJSEQ
        Data1 : line No.
        Data2 : Step No.(運動指令)
        '''
        # status = self.mh.statusMH()
        # job = self.mh.readCurrJobMH()
        self.mh.servoMH(True)
        Jobname = "ORG"
        
        self.mh.startJobMH(Jobname)
        
        # self.mh.servoMH(False)
        self.mh.disconnectMH()

    def errorXYZ(self, Unit, realx, realy, realz, simx, simy, simz):
        errx = simx - realx*Unit
        erry = simy -realy*Unit
        errz = simz -realz*Unit
        error = [abs(errx), abs(erry), abs(errz)]

        return error

    def main(self):
        # 建立socket連線
        OpenTime1 = self.time.ReadNowTime()
        self.mh.connectMH()
        OpenTime2 = self.time.ReadNowTime()
        print(self.mh.getJointAnglesMH())
        # Servo ON
        servoONTime1 = self.time.ReadNowTime()
        self.mh.servoMH(True)
        servoONTime2 = self.time.ReadNowTime()

        
        '''
        Point Info.:
            [x, y, z, Rx, Ry, Rz]
            ORG =   485.267, -1.225, 234.322, 179.9840, 20.2243, 1.6886
            start = 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523
            end =   955.326, -178.005, -154.700, -168.3718, -2.9293, 7.0363

            鎢棒間距約 = 2mm
            prep Start = 953.504, -108.680, -128.700, -163.1780, -1.2651, 15.2709
            weld Start = 953.516, -108.653, -166.604, -163.1818, -1.2683, 15.2796

            weld End = 953.519, 15.671, -166.621, -163.1767, -1.2631, 15.2617
            prep End = 953.530, -15.690, -85.288, -163.1824, -1.2716, 15.2635
            
        Order:
            ORG➜ MOVJ(start)➜ MOVL(end)➜ MOVJ(ORG)
            ORG➜ MOVJ(prep Start)➜ MOVL(weld Start)➜ MOVL(weld End)➜ MOVL(prep End)➜ MOVJ(ORG)

        Work:
            ORG➜ MOVJ(prep Start)➜ call AutoARC(ON)➜ MOVL(weld Start)➜ MOVL(weld End)➜ call AutoARC(ON) ➜ MOVL(prep End)➜ MOVJ(ORG)
        '''

        # MOVJ cmd = f"{Speed(%)},{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}\r"
        ORGcmd = [2, 1, 485.267, -1.225, 234.322, 179.9840, 20.2243, 1.6886, 0, 5, 0, 0, 0, 0, 0, 0]
        perpStartcmd = [2, 1, 953.504, -88.216, -128.700, -163.1780, -1.2651, 15.2709, 0, 5, 0, 0, 0, 0, 0, 0]
        

        # MOVL cmd = f"{Speed(0 or 1)},{speed(mm/s or deg/s)}{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}"
        weldStartcmd = [0, 20, 1, 953.516, -88.216, -165.642, -163.1818, -1.2652, 15.2706, 0, 5, 0, 0, 0, 0, 0, 0]
        weldEndcmd = [0, 1.66, 1, 953.513, 24.856, -165.647, -163.1923, -1.2652, 15.2743, 0, 5, 0, 0, 0, 0, 0, 0]
        prepEndcmd = [0, 20, 1, 953.530, -15.690, -85.288, -163.1824, -1.2716, 15.2635, 0, 5, 0, 0, 0, 0, 0, 0]

        worldCoordinate = np.eye(4)

        # state flag
        prepStart = False
        weldStart = False
        arcON = False
        weldEnd = False
        arcOFF = False
        preEnd = False
        backOrg = False
        

        Unit = 0.01
        while True:
            # Get mh12 JointAngle
            GetJATime1 = self.time.ReadNowTime()
            gJA =  self.mh.getJointAnglesMH()
            GetJATime2 = self.time.ReadNowTime()
            gJA = d2r(gJA)
            Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = \
                self.kin.Mh12_FK(worldCoordinate, gJA[0], gJA[1], gJA[2], gJA[3], gJA[4], gJA[5])
            Px = EndEffector[0, 3]
            Py = EndEffector[1, 3]
            Pz = EndEffector[2, 3]
            
            # 誤差計算
            errPrepStart = self.errorXYZ(Unit, perpStartcmd[2], perpStartcmd[3], perpStartcmd[4], Px, Py, Pz)
            errweldStart = self.errorXYZ(Unit, weldStartcmd[3], weldStartcmd[4], weldStartcmd[5], Px, Py, Pz)
            errweldEnd = self.errorXYZ(Unit, weldEndcmd[3], weldEndcmd[4], weldEndcmd[5], Px, Py, Pz)
            errPrepEnd = self.errorXYZ(Unit, prepEndcmd[3], prepEndcmd[4], prepEndcmd[5], Px, Py, Pz)
            errOrg = self.errorXYZ(Unit, ORGcmd[2], ORGcmd[3], ORGcmd[4], Px, Py, Pz)

            # 誤差標準
            std = 0.001

            if prepStart == False:
                # 移動至預備銲接點
                P1ts = self.time.ReadNowTime()
                self.mh.MOVJ(perpStartcmd)
                P1te = self.time.ReadNowTime()
                prepStart = True
                print('prep Welding')

            if errPrepStart[0]<=std and errPrepStart[1]<=std and errPrepStart[2]<=std and prepStart == True and weldStart == False:
                # 移動至銲接起點
                P2ts = self.time.ReadNowTime()
                self.mh.MOVL(weldStartcmd)
                P2te = self.time.ReadNowTime()
                print('Can start Welding')
                weldStart = True
            
            if errweldStart[0]<=std and errweldStart[1]<=std and errweldStart[2]<=std and weldStart == True and arcON == False:
                # 呼叫起弧作業
                Jobname = "AUTOARCON"
                # self.mh.startJobMH(Jobname)
                print('ARC ON')
                arcON = True

            if arcON == True and weldEnd == False:
                # 開始銲接
                P3ts = self.time.ReadNowTime()
                self.mh.MOVL(weldEndcmd)
                P3te = self.time.ReadNowTime()
                print('welding')
                weldEnd = True

            if errweldEnd[0]<=std and errweldEnd[1]<=std and errweldEnd[2]<=std and weldEnd == True and arcOFF == False:
                # 銲接結束
                Jobname = "AUTOARCOFF"
                # self.mh.startJobMH(Jobname)
                arcOFF = True

            if arcOFF == True and preEnd == False:
                P4ts = self.time.ReadNowTime()
                self.mh.MOVL(prepEndcmd)
                P4te = self.time.ReadNowTime()
                print('prep End')
                preEnd = True

            if errPrepEnd[0]<=std and errPrepEnd[1]<=std and errPrepEnd[2]<=std and preEnd == True and backOrg == False:
                # 回工作原點
                P5ts = self.time.ReadNowTime()
                self.mh.MOVJ(ORGcmd)
                P5te = self.time.ReadNowTime()
                backOrg = True

            if errOrg[0]<=std and errOrg[1]<=std and errOrg[2]<=std and backOrg == True:
                print("Job finish!!!")
                break

        # Servo OFF
        servoOFTime1 = self.time.ReadNowTime()
        self.mh.servoMH(False)
        servoOFTime2 = self.time.ReadNowTime()

        # 關閉socket連線
        closeTime1 = self.time.ReadNowTime()
        self.mh.disconnectMH()
        closeTime2 = self.time.ReadNowTime()

        # cmd  time
        # connect/close socket
        OpenPort = self.time.TimeError(OpenTime1, OpenTime2)
        ClosePort = self.time.TimeError(closeTime1, closeTime2)
        # ON/OFF Servo
        servoON = self.time.TimeError(servoONTime1, servoONTime2)
        servoOFF = self.time.TimeError(servoOFTime1, servoOFTime2)
        # MOVJ
        P1 = self.time.TimeError(P1ts, P1te)
        # MOVL
        P2 = self.time.TimeError(P2ts, P2te)
        P3 = self.time.TimeError(P3ts, P3te)
        P4 = self.time.TimeError(P4ts, P4te)
        # MOVJ
        P5 = self.time.TimeError(P5ts, P5te)
        # RPOSJ        
        getJA = self.time.TimeError(GetJATime1, GetJATime2)

        timeList = [OpenPort, ClosePort, servoON, servoOFF, P1, P2, P2, P4, P5, getJA]
        print(timeList)
        
        

if __name__ == "__main__":
    ctrl = ControlMA1440()
    ctrl.main()
    # ctrl.testCmd()


