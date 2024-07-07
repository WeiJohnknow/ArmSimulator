import numpy as np

class noFeed_buttWeld:
    @ staticmethod
    def weldingSpeedTOweldBeadWidth():
        pass

class noFeed_filletWeld:
    @ staticmethod
    def weldingSpeedTOweldBeadWidth(weldBeadWidth):
        """Original equation
        weldBeadWidth = -2.317*weldingSpeed + 9.758

        weldingSpeed∈[1, 2]
        """
        weldingSpeed = (weldBeadWidth-9.758)/(-2.317)

        return weldingSpeed
        
    @ staticmethod
    def weldCurrentTOweldBeadWidth(weldBeadWidth):
        """Original equation
        weldBeadWidth = 0.173*weldingCurrent -2.789

        weldingCurrent∈[45, 55]
        """
        pass
    
    @ staticmethod
    def weldSpeedCurrentTOweldBeadWidth(WeldBeadWidth):
        """Original equation
        WeldBeadWidth = -2.576858070041016 * Speed + 0.1740194708613152 * Current + 0.9745357641862364

        Current∈[45, 55]
        Speed∈[1, 2]
        """
        # WeldBeadWidth = -2.577 * Speed + 0.174 * Current + 0.975
        pass

class Feed_buttWeld:
    @ staticmethod
    def weldingSpeedTOweldBeadWidth(WeldBeadWidth):
        """Original equation
        WeldBeadWidth = -2.205000000000001 * Speed + 8.982500000000002
        WeldBeadWidth = -2.205 * Speed + 8.983
        Speed∈[1, 2]

        arg: WeldBeadWidth(mm)

        return: Weldiing Speed(mm/s)
        """
        Speed = (WeldBeadWidth-8.983)/(-2.205) 

        return Speed

    @ staticmethod
    def weldCurrentTOweldBeadWidth(WeldBeadWidth):
        """Original equation
        WeldBeadWidth = 0.08000000000000002 * Current + 0.6999999999999993
        WeldBeadWidth = 0.08 * Current + 0.7
        Current∈[50, 70]

        arg: WeldBeadWidth(mm)

        return: Weldiing Current(A)
        """
        Current = (WeldBeadWidth-0.7)/0.08
        
        return Current

    @ staticmethod
    def weldSpeedCurrentTOweldBeadWidth(WeldBeadWidth):
        """
        WeldBeadWidth = 0.09750000000000003 * Current + -1.9600000000000004 * Speed + 2.7333333333333325

        Current∈[50, 70]
        Speed∈[1, 2]
        """
        pass

class Feed_filletWeld:
    @ staticmethod
    def weldingSpeedTOweldBeadWidth(WeldBeadWidth):
        """
        WeldBeadWidth = -1.6950000000000007 * Speed + 7.445833333333335
        WeldBeadWidth = -1.695 * Speed + 7.446
        Current∈[40, 60]

        arg: WeldBeadWidth(mm)

        return: Weldiing Speed(mm/s)
        """
        Speed = (WeldBeadWidth-7.446)/(-1.695)

        return Speed

    @ staticmethod
    def weldCurrentTOweldBeadWidth(WeldBeadWidth):
        """
        WeldBeadWidth = 0.10750000000000001 * Current + -0.5833333333333339
        WeldBeadWidth = 0.108 * Current + -0.583
        Speed∈[1, 2]

        arg: WeldBeadWidth(mm)

        return: Weldiing Current(A)
        """
        Current = (WeldBeadWidth+0.583)/0.108

        return Current

    @ staticmethod
    def weldSpeedCurrentTOweldBeadWidth(WeldBeadWidth):
        pass