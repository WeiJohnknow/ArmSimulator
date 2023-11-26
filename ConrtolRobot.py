from MotomanEthernet import *
from TimeTool import *
from Kinematics import *
import numpy as np

class ControlMA1440:
    def __init__(self) -> None:
        self.mh = MotomanConnector()
        self.kin = Kinematics()
        pass

    def main(self):
        # 建立socket連線
        self.mh.connectMH()

        # Servo ON
        self.mh.servoMH(True)

        # test cmd
        status = self.mh.statusMH()
        job = self.mh.readCurrJobMH()
        Jobname = "ORG"
        self.mh.startJobMH(Jobname)


        '''
        Test:
        Point Info.:
            [x, y, z, Rx, Ry, Rz]
            ORG =   485.267, -1.225, 234.322, 179.9840, 20.2243, 1.6886
            start = 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523
            end =   955.326, -178.005, -154.700, -168.3718, -2.9293, 7.0363
        Order:
            ORG➜ MOVJ(start)➜ MOVL(end)➜ MOVJ(ORG)
        '''
        #　MOVJ cmd = f"{Speed(%)},{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}\r"
        ORGcmd = [2, 1, 485.267, -1.225, 234.322, 179.9840, 20.2243, 1.6886, 0, 5, 0, 0, 0, 0, 0, 0]
        Startcmd = [2, 1, 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523, 0, 5, 0, 0, 0, 0, 0, 0]
        
        # MOVL cmd = f"{Speed(0 or 1)},{speed(mm/s or deg/s)}{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}"
        Lcmd_Start = [0, 20, 1, 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523, 0, 5, 0, 0, 0, 0, 0, 0]
        Endcmd = [0, 20, 1, 955.326, -178.005, -154.700, -168.3718, -2.9293, 7.0363, 0, 5, 0, 0, 0, 0, 0, 0]

        worldCoordinate = np.eye(4)
        # state flag
        P1 = False

        while True:
        
            # Get mh12 JointAngle
            gJA =  self.mh.getJointAnglesMH()
            gJA = d2r(gJA)
            Base, Saxis, Laxis, Uaxis, Raxis, Baxis, Taxis, EndEffector = \
                self.kin.Mh12_FK(worldCoordinate, gJA[0], gJA[1], gJA[2], gJA[3], gJA[4], gJA[5])
            Px = EndEffector[0, 3]
            Py = EndEffector[1, 3]
            Pz = EndEffector[2, 3]
            
            if P1 == False:
                self.mh.MOVJ(Startcmd)
                P1 = True

            if Px == Startcmd[2] and Py == Startcmd[3] and Startcmd[4] :
                self.mh.MOVL(Endcmd)

            if Px == Endcmd[2] and Py == Endcmd[3] and Endcmd[4]:
                self.mh.MOVJ(ORGcmd)

            if Px == ORGcmd[2] and Py == ORGcmd[3] and ORGcmd[4]:
                print("Job finish!!!")
                break

        # Servo OFF
        self.mh.servoMH(False)

        # 關閉socket連線
        self.mh.disconnectMH()
        

if __name__ == "__main__":
    ctrl = ControlMA1440()
    ctrl.main()


