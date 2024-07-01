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
        WeldBeadWidth = -1.9600000000000004 * Speed + 8.610000000000001
        Speed∈[1, 2]
        """
        Speed = WeldBeadWidth/(-1.96) - 8.61

        return Speed

    @ staticmethod
    def weldCurrentTOweldBeadWidth(WeldBeadWidth):
        """Original equation
        WeldBeadWidth = 0.09750000000000002 * Current - 0.23333333333333428
        Current∈[50, 70]
        """
        Current = (WeldBeadWidth/0.0975) + 0.2333
        
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
        pass

    @ staticmethod
    def weldCurrentTOweldBeadWidth(WeldBeadWidth):
        pass

    @ staticmethod
    def weldSpeedCurrentTOweldBeadWidth(WeldBeadWidth):
        pass