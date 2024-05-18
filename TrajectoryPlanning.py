import numpy as np

class Interpolator:
    @staticmethod
    def Curve():
        pass

    @staticmethod
    def Arc():
        pass

    @staticmethod
    def Linear():
        pass

class AxisAngleConverter:
    def __init__(GoalEnd, NowEnd):
        sin = np.sin
        cos = np.cos
        arccos = np.arccos
        inv  = np.linalg.inv
        pi = np.pi
        
        D = inv(NowEnd) @ GoalEnd
        θ = arccos(round((D[0,0] + D[1,1] + D[2,2] - 1.0)/2.0,4))
        if type(θ) !=type(np.arccos(0.5)):
            θ = 0
        if round(θ % pi,4) !=round(0.0,4):
            u = 2.0*sin(θ)
            kx = (D[2,1] - D[1,2]) / u
            ky = (D[0,2] - D[2,0]) / u
            kz = (D[1,0] - D[0,1]) / u
        else:
            u = 0.001
            kx = (D[2,1] - D[1,2]) / u
            ky = (D[0,2] - D[2,0]) / u
            kz = (D[1,0] - D[0,1]) / u
    
    

