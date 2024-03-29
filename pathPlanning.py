import numpy as np
import matplotlib.pyplot as plt
from dataBase_v0 import dataBase
from Matrix import Matrix4x4
from Kinematics import Kinematics
# from Simulator_v2 import Simulator

class PathPlanning:
    def __init__(self):
        self.dB = dataBase()
        self.Mat = Matrix4x4()
        self.Kin = Kinematics()
        # self.Sim = Simulator()
        
    
    def TP_434(self, θ1, V1, A1, θ2, θ3, θ4, V4, A4, t1, t2, t3, sampleTime):
        # θ = M * C
        θ = np.array([θ1, V1, A1, θ2, θ2, 0, 0, θ3, θ3, 0, 0, θ4, V4, A4])
        M = np.array([[1, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
                            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, t1, t1**2, t1**3, t1**4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 2*t1, 3*t1**2, 4*t1**2, 0, -1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 2, 6*t1, 12*t1**2, 0, 0, -2, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, t2, t2**2, t2**3, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 2*t2, 3*t2**2, 0, -1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 6*t2, 0, 0, -2, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, t3, t3**2, t3**3, t3**4],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2*t3, 3*t3**2, 4*t3**3],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6*t3, 12*t3**2]])
        print(M.shape)
        C = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        # C = [a0, a1, a2, a3, a4, b0, b1, b2, b3, c0, c1, c2, c3, c4]
        M_1 = np.linalg.inv(M)
        C = M_1 @ θ
        a0 = C[0]
        a1 = C[1]
        a2 = C[2]
        a3 = C[3]
        a4 = C[4]
        b0 = C[5]
        b1 = C[6]
        b2 = C[7]
        b3 = C[8]
        c0 = C[9]
        c1 = C[10]
        c2 = C[11]
        c3 = C[12]
        c4 = C[13]    
        
        h1 = a0 + a1*t1 + a2*t1**2 + a3*t1**3 + a4*t1**4
        h2 = b0 + b1*t2 + b3*t2**2 + b3*t2**3
        h3 = c0 + c1*t3 + c2*t3**2 + c3*t3**3 + c4*t3**4

        # Real time
        StartTime = 0
        alltime = np.round(np.linspace(StartTime, t1+t2+t3,  int((t1+t2+t3)/sampleTime)), 3)
        time1_ = np.round(np.linspace(StartTime, t1,  int(t1/sampleTime)), 3)
        time2_ = np.round(np.linspace(t1, t1+t2,  int(t2/sampleTime)), 3)
        time3_ = np.round(np.linspace(t1+t2, t2+t3,  int(t3/sampleTime)), 3)
        time1 = np.round(np.linspace(StartTime, t1,  int(t1/sampleTime)), 3)
        time2 = np.round(np.linspace(StartTime, t2,  int(t2/sampleTime)), 3)
        time3 = np.round(np.linspace(t3, StartTime,  int(t3/sampleTime)), 3)

        # normalized time
        min_time1 = np.min(time1)
        max_time1 = np.max(time1)
        normTime1 = (time1 - min_time1) / (max_time1 - min_time1)

        min_time2 = np.min(time2)
        max_time2 = np.max(time2)
        normTime2 = (time2 - min_time2) / (max_time2 - min_time2)
        

        min_time3 = np.min(time3)
        max_time3 = np.max(time3)
        normTime3 =  -1 + 1* (time3 - min_time3) / (max_time3 - min_time3)

        # TODO 多項式係數有誤
        # t1 curve
        t1_PosCoefficients = [a4, a3, a2, a1, a0]
        t1_VelCoefficients = [4*a4, 3*a3, 2*a2, a1]
        t1_AccCoefficients = [12*a4, 6*a3, 2*a2]
        t1_Poscurve = np.polyval(t1_PosCoefficients, time1)
        t1_Velcurve = np.polyval(t1_VelCoefficients, normTime1)
        t1_Acccurve = np.polyval(t1_AccCoefficients, normTime1)

        # t2 curve
        # b3 = 0
        t2_PosCoefficients = [b3, b2, b1, b0]
        t2_VelCoefficients = [3*b3, 2*b2, b1]
        t2_AccCoefficients = [6*b3, 2*b2]
        t2_Poscurve = np.polyval(t2_PosCoefficients, time2)
        t2_Velcurve = np.polyval(t2_VelCoefficients, normTime2)
        t2_Acccurve = np.polyval(t2_AccCoefficients, normTime2)

        # t3 curve
        t3_PosCoefficients = [c4, c3, c2, c1, c0]
        t3_VelCoefficients = [4*c4, 3*c3, 2*c2, c1]
        t3_AccCoefficients = [12*c4, 6*c3, 2*c2]
        t3_Poscurve = np.polyval(t3_PosCoefficients, time3)
        t3_Velcurve = np.polyval(t3_VelCoefficients, normTime3)
        t3_Acccurve = np.polyval(t3_AccCoefficients, normTime3)



        # 繪製多項式曲線
        # plt.plot(alltime[:t1/sampleTime], t1_Poscurve, color='red', label='Position1')
        # plt.plot(time1, t1_Velcurve, color='green', label='Velocity')
        # plt.plot(time1, t1_Acccurve, color='blue', label='Acceleration')
        # plt.plot(alltime[:t2/sampleTime], t2_Poscurve, color='green', label='Position2')
        # plt.plot(time2, t2_Velcurve, color='green', label='Velocity')
        # plt.plot(time2, t2_Acccurve, color='blue', label='Acceleration')
        # plt.plot(alltime[:t3/sampleTime], t3_Poscurve, color='blue', label='Position3')
        # plt.plot(time3, t3_Velcurve, color='green', label='Velocity')
        # plt.plot(time3, t3_Acccurve, color='blue', label='Acceleration')
        plt.plot(alltime, np.concatenate((t1_Poscurve, t2_Poscurve, t3_Poscurve), axis=0), color='red', label='Position')
        plt.xlabel('time')
        plt.ylabel('Value')
        plt.title('Plot of the Polynomial')
        plt.legend()
        plt.grid(True)
        plt.show()
        

        # sampleIntervals = 0.01
        samplePoint = [int(t1/sampleTime), int(t2/sampleTime), int(t3/sampleTime)]

        TimeList = [0]
        PosList = []
        VelList = []
        AccList = []

        for t in range(samplePoint[0]):
            u = t/100
            Pos = a0 + a1*u + a2*u**2 + a3*u**3 + a4*u**4
            Vel = a1 + 2*a2*u + 3*a3*u**2 + 4*a4*u**3
            Acc = 2*a2 + 6*a3*u + 12*a4*u**2
            TimeList.append(TimeList[-1]+0.01*t1)
            PosList.append(Pos)
            VelList.append(Vel)
            AccList.append(Acc)

        for t in range(samplePoint[1]):
            u = t/100
            Pos = b0 + b1*u + b2*u**2 + b3*u**3 
            Vel = b1 + 2*b2*u + 3*b3*u**2
            Acc = 2*b2 + 6*b3*u 
            TimeList.append(TimeList[-1]+0.01*t2)
            PosList.append(Pos)
            VelList.append(Vel)
            AccList.append(Acc)

        for t in range(samplePoint[2]):
            u = t/100
            Pos = c0 + c1*u + c2*u**2 + c3*u**3 + c4*u**4
            Vel = c1 + 2*c2*u + 3*c3*u**2 + 4*c4*u**3
            Acc = 2*c2 + 6*c3*u + 12*c4*u**2
            TimeList.append(TimeList[-1]+0.01*t3)
            PosList.append(Pos)
            VelList.append(Vel)
            AccList.append(Acc)

        del TimeList[0]

        return TimeList, PosList, VelList, AccList, samplePoint

    # def TrajectoryPlanning_434(self, Pinit, Vinit, Ainit, Plift_off, Pset_down, Pfinal, Vfinal, Afinal, t1, t2, t3, sampleTime=0.001, StartTime=0)
    def TrajectoryPlanning_434(self, Pinit, Plift_off, Pset_down, Pfinal, t1, t2, t3, sampleTime=0.001, Vinit=0, Ainit=0, Vfinal=0, Afinal=0, StartTime=0):
        """
        - Args:
            - Pinit, Plift_off, Pset_down, Pfinal, t1, t2, t3, sampleTime
            - default: sampleTime=0.001, StartTime=0, Plift_off=0, Pset_down=0, Vfinal=0, Afinal=0

        - Retrun:
            timeData, positionData, velocityData, accelerationData
        """

        P1 = Plift_off - Pinit
        P2 = Pset_down - Plift_off
        P3 = Pfinal - Pset_down

        X =  np.array([0, 0, 0, 0, 0, 0, 0])
        C =  np.array([  [      1,        1,     0,        0,       0,       0,         0],
                                [   3/t1,     4/t1, -1/t2,        0,       0,       0,         0],
                                [6/t1**2, 12/t1**2,     0, -2/t2**2,       0,       0,         0],
                                [      0,        0,     1,        1,       1,       0,         0],
                                [      0,        0,  1/t2,     2/t2,    3/t2,   -3/t3,      4/t3],
                                [      0,        0,     0,  2/t2**2, 6/t2**2, 6/t3**2, -12/t3**2],
                                [      0,        0,     0,        0,       0,       1,        -1]])
        if np.linalg.det(C) == 0:
            print("時間參數有問題")
        else:
            print("ok!")

        # Y = np.array([P1-(Ainit*t1**2)/2-Vinit*t1,
        #                 -Ainit*t1-Vinit,
        #                 -Ainit/t1,
        #                 P2,
        #                 Vfinal-Afinal*t3,
        #                 Afinal,
        #                 P3-Vfinal*t3+(Afinal*t3**2)/2])
            
        Y = np.array([P1-((Ainit*t1**2)/2)-(Vinit*t1),
                        -Ainit*t1-Vinit,
                        -Ainit,
                        P2,
                        Vfinal-Afinal*t3,
                        Afinal,
                        P3-Vfinal*t3+(Afinal*t3**2)/2])
            

        
        c_1 = np.linalg.inv(C)
        X = c_1 @ Y 

        a10 = Pinit
        a11 = Vinit*t1
        a12 = (Ainit*t1**2)/2
        a13 = X[0]
        a14 = X[1]
        a20 = Plift_off
        a21 = X[2]
        a22 = X[3]
        a23 = X[4]
        a30 = Pfinal
        a31 = Vfinal*t3
        a32 = (Afinal*t3**2)/2
        a33 = X[5]
        a34 = X[6]


        samplePoint = [int(t1/sampleTime), int(t2/sampleTime), int(t3/sampleTime)]
        
        
        DataSize = samplePoint[0]+samplePoint[1]+samplePoint[2]
        timeData = np.zeros((DataSize))
        positionData = np.zeros((DataSize))
        velocityData = np.zeros((DataSize))
        accelerationData = np.zeros((DataSize))


        # 記憶前一段軌跡的時間節點
        PreviousNode = 0

        for _u in range(0,1*samplePoint[0]+1):
            u = _u/samplePoint[0]
            # TimeList[_u] = round(StartTime + t1*u , 2)
            timeData[_u] = StartTime + t1*u 

            P = a10 + a11*u + a12*u**2 + a13*u**3 + a14*u**4
            V = a11 + 2*a12*u + 3*a13*u**2 + 4*a14*u**3
            A = 2*a12 + 6*a13*u + 12*a14*u**2

            positionData[_u] = P
            velocityData[_u] = V
            accelerationData[_u] = A 
        
        PreviousNode += samplePoint[0]

        for _u in range(0,1*samplePoint[1]):
            u = _u/samplePoint[1]
            timeData[PreviousNode+_u] = timeData[PreviousNode] + t2*u

            P = a20 + a21*u + a22*u**2 + a23*u**3
            V = a21 + 2*a22*u + 3*a23*u**2
            A = 2*a22 + 6*a23*u

            positionData[PreviousNode+_u] = P
            velocityData[PreviousNode+_u] = V
            accelerationData[PreviousNode+_u] = A

        PreviousNode += samplePoint[1]

        # 第三段真實時間
        ut = 0
        counter = 0
        for _u in range(-1*samplePoint[2],1):
            u = _u/samplePoint[2]
            ut += sampleTime

            timeData[PreviousNode+counter] = timeData[PreviousNode-1] + ut

            P = a30 + a31*u + a32*u**2 + a33*u**3 + a34*u**4
            V = a31 + 2*a32*u + 3*a33*u**2 + 4*a34*u**3
            A = 2*a32 + 6*a33*u + 12*a34*u**2

            positionData[PreviousNode+counter] = P
            velocityData[PreviousNode+counter] = V
            accelerationData[PreviousNode+counter] = A

            if counter == samplePoint[1]-1:
                counter = samplePoint[1]-1
            else:
                counter += 1
        
        return timeData, positionData, velocityData, accelerationData
    
    def S_curve(self, Smax, Vmax, Amax, Aavg, sampleTime=0.001):
        '''
        - 0.5Amax <= Aavg < Amax
        - Ts >= 0, Ts = (Sm-Vm*Ta)/Vm, Ta = Vm/Aa
        - Smax >= 2Vmax**2 / Amax  
        '''
        Sm = Smax
        Vm = Vmax
        Am = Amax
        Aa = Aavg
        
        Ta = Vm/Aa
        Tb = 2*Vm/Am-Ta
        Tc = (Ta-Tb)/2
        Ts = (Sm-Vm*Ta)/Vm

        alltime = 2*Ta+Ts
        print("Total time :", alltime)

        if 0.5*Amax <= Aavg and Aavg < Amax:
            print("Aavg is ok!")
            if Smax >= 2*Vmax**2 / Amax:
                print("Smax is ok!")
                if Ts >= 0:
                    print("Ts is ok!")
                else:
                    print("Smax or Vmax 不合理")
            else:
                print("Smax不夠")
        else:
            print("Amax or Aavg 不合理")

        # # Acc-Curve
        # a1 = Am/Tc*t1
        # a2 = 0*t2+Am 
        # a3 = Am-(Am/Tc)*(t3-Tc-Tb)
        # a4 = 0*t4
        # a5 = -(Am/Tc)*(t5-Ta-Ts)
        # a6 = 0*t6-Am
        # a7 = -Am+Am/Tc*(t7-Ta-Ts-Tc-Tb)

        # # Vel-Curve
        # v1 = (Am*t1**2)/(2*Tc)
        # v2 = Am*(t2-Tc)+v1(end)
        # v3 = Am*(Tb+Tc)-Am/(2*Tc)*(2*Tc+Tb)**2+Am/Tc*(2*Tc+Tb)*t3-Am/(2*Tc)*t3**2
        # v4 = 0*t4+Vm
        # v5 = -(Am/Tc)/2*(t5-Ta-Ts)**2+v4(end)
        # v6 = 0*t6-Am*(t6-Ta-Ts-Tc)+v5(end)
        # v7 = -Am*(t7-Ta-Ts-Tc-Tb)+Am/(2*Tc)*(t7-Ta-Ts-Tc-Tb)**2+v6(end)

        # # S-Curve
        # s1 = (1/6)*Am/Tc*t1**3
        # s2 = Am/6*Tc**2-0.5*Am*Tc*t2+0.5*Am*t2**2
        # s3 = (0.5*Am*Tc+Am*Tb)*(t3-Tc-Tb)+0.5*Am*(t3-Tc-Tb)**2-Am/6*Tc*(t3-Tc-Tb)**3+Am/6*Tc**2+0.5*Am*Tb*(Tb+Tc)
        # s4 = s3(end)+Vm*(t4-Ta)
        # s5 = s4(end)-(Am/Tc)/6*(t5-Ta-Ts)**3+v4(end)*(t5-Ta-Ts)
        # s6 = s5(end)-(Am/2)*(t6-Ta-Ts-Tc)**2+v5(end)*(t6-Ta-Ts-Tc)
        # s7 = s6(end)-(0.5*Am*(t7-Ta-Ts-Tc-Tb)**2)+Am/(6*Tc)*(t7-Ta-Ts-Tc-Tb)**3+v6(end)*(t7-Ta-Ts-Tc-Tb)

        # Curve
        AccList = []
        VelList = []
        SList = []

        # 各曲線終值
        a1End, a2End, a3End, a4End, a5End, a6End, a7End = 0, 0, 0, 0, 0, 0, 0
        v1End, v2End, v3End, v4End, v5End, v6End, v7End = 0, 0, 0, 0, 0, 0, 0
        s1End, s2End, s3End, s4End, s5End, s6End, s7End = 0, 0, 0, 0, 0, 0, 0

        
        
        
        # # 時間函數
        # Time1List = []
        # Time2List = []
        # Time3List = []
        # Time4List = []
        # Time5List = []
        # Time6List = []
        # Time7List = []
        # TimeList= [0, Time1List, Time2List, Time3List, Time4List, Time5List, Time6List, Time7List]
        TimeList = []

        for t1 in range(0, int(Tc/sampleTime)):
            t = t1*sampleTime
            TimeList.append(t)

            a1 = Am/Tc*t
            v1 = (Am*t**2)/(2*Tc)
            s1 = (1/6)*Am/Tc*t**3

            # a1 = Am/Tc*t
            # v1 = Am/(2*Tc) * t**2
            # s1 = Am/(6*Tc) * t**3


            AccList.append(a1)
            VelList.append(v1)
            SList.append(s1)

            a1End = a1
            v1End = v1
            S1End = s1

        for t2 in range(int(Tc/sampleTime), int((Tb+Tc)/sampleTime)):
            t = t2*sampleTime
            TimeList.append(t)

            a2 = 0*t+Am
            v2 = v1End + Am*(t-Tc)
            s2 = Am/6*Tc**2-0.5*Am*Tc*t+0.5*Am*t**2

            # a2 = Am+0*t
            # v2 = -0.5*Am*Tc+Am*t
            # s2 = Am/6*Tc**2-0.5*Am*Tc*t+0.5*Am*t**2


            AccList.append(a2) 
            VelList.append(v2)
            SList.append(s2)

            a2End = a2
            v2End = v2
            s2End = s2

        for t3 in range(int((Tb+Tc)/sampleTime), int(Ta/sampleTime)):
            t = t3*sampleTime
            TimeList.append(t)

            a3 = Am-(Am/Tc)*(t-Tc-Tb)
            v3 = Am*(Tb+Tc)-Am/(2*Tc)*(2*Tc+Tb)**2+Am/Tc*(2*Tc+Tb)*t-Am/(2*Tc)*t**2
            s3 = (0.5*Am*Tc+Am*Tb)*(t-Tc-Tb)+0.5*Am*(t-Tc-Tb)**2-Am/6*Tc*(t-Tc-Tb)**3+Am/6*Tc**2+0.5*Am*Tb*(Tb+Tc)

            # a3 = Am/Tc*(2*Tc+Tb)-Am/Tc*t
            # v3 = Am*(Tb+Tc)-Am/(2*Tc)*((2*Tc+Tb)**2)+Am/Tc*(2*Tc+Tb)*t-Am/(2*Tc)*t**2
            # s3 = (0.5*Am*Tc+Am*Tb)*(t-Tc-Tb)+Am/2*(t-Tc-Tb)**2-Am/(6*Tc)*(t-Tc-Tb)**3+Am/6*Tc**2+0.5*Am*Tb*(Tb+Tc)

            AccList.append(a3)
            VelList.append(v3)
            SList.append(s3)

            a3End = a3
            v3End = v3
            s3End = s3

        for t4 in range(int(Ta/sampleTime), int((Ts+Ta)/sampleTime)):
            t = t4*sampleTime
            TimeList.append(t)

            a4 = 0*t
            v4 = 0*t+Vm
            s4 = s3End+Vm*(t-Ta)

            # a4 = 0*t
            # v4 = 0*t+Vm
            # s4 = Vm*t-0.5*Aa*Ta**2

            AccList.append(a4)
            VelList.append(v4)
            SList.append(s4)

            a4End = a4
            v4End = v4
            s4End = s4

        for t5 in range(int((Ts+Ta)/sampleTime), int((Ta+Ts+Tc)/sampleTime)):
            t = t5*sampleTime
            TimeList.append(t)

            a5 = -(Am/Tc)*(t-Ta-Ts)
            v5 = v4End-(Am/Tc)/2*(t-Ta-Ts)**2
            s5 = s4End-(Am/Tc)/6*(t-Ta-Ts)**3 + v4End*(t-Ta-Ts)

            # a5 = 0-Amax/Tc*t
            # v5 = Vmax-(Amax*t**2)/(2*Tc)
            # s5 = Vmax*Ts+0.5*Aavg*Ta**2 +t*Vmax - (Amax*t**3)/(6*Tc)

            AccList.append(a5)
            VelList.append(v5)
            SList.append(s5)

            a5End = a5
            v5End = v5
            s5End = s5

        for t6 in range(int((Ta+Ts+Tc)/sampleTime), int((Ta+Ts+Tc+Tb)/sampleTime)):
            t = t6*sampleTime
            TimeList.append(t)

            a6 = 0*t-Am
            v6 = v5End + 0*t-Am*(t-Ta-Ts-Tc)
            s6 = s5End-(Am/2)*(t-Ta-Ts-Tc)**2 + v5End*(t-Ta-Ts-Tc)

            # a6 = -Amax+0*t
            # v6 = Vmax - (Amax*Tc)/2-(Amax*t)
            # s6 = (15*Ta**2 + Tc*Vmax + Ts*Vmax - (Amax*Tc**2)/6) + (t*(Vmax-(Amax*Tc)/2-(Amax*t)/2))


            AccList.append(a6)
            VelList.append(v6)
            SList.append(s6)

            a6End = a6
            v6End = v6
            s6End = s6

        for t7 in range(int((Ta+Ts+Tc+Tb)/sampleTime), int((2*Ta+Ts)/sampleTime)):
            t = t7*sampleTime
            TimeList.append(t)

            a7 = -Am+Am/Tc*(t-Ta-Ts-Tc-Tb)
            v7 = v6End - Am*(t-Ta-Ts-Tc-Tb) + Am/(2*Tc)*(t-Ta-Ts-Tc-Tb)**2
            s7 = s6End-(0.5*Am*(t-Ta-Ts-Tc-Tb)**2)+Am/(6*Tc)*(t-Ta-Ts-Tc-Tb)**3+v6End*(t-Ta-Ts-Tc-Tb)

            # a7 = -Amax+Amax/Tc*t
            # v7 = Vmax - (Amax*Tc)/2-(Amax*Tb)+(Amax*t*(t - 2*Tc))/(2*Tc)
            # s7 = s6End-(0.5*Am*(t-Ta-Ts-Tc-Tb)**2)+Am/(6*Tc)*(t-Ta-Ts-Tc-Tb)**3+v6End*(t-Ta-Ts-Tc-Tb)

            AccList.append(a7)
            VelList.append(v7)
            SList.append(s7)

            a7End = a7
            v7End = v7
            s7End = s7

        return AccList, VelList, SList, TimeList
    
    def MatrixPathPlanning(self, GoalEnd, NowEnd, allTime, sampleTime = 0.04, startTime=0):
        """Homogeneous matrix interpolation method, it's a Cartesian space trajectory planning method.
        - Args:
            - GoalEnd(Homogeneous matrix), NowEnd(Homogeneous matrix), allTime, filePath
            - default : sampleTime = 0.04, startTime=0
        
        - Return:
            - pathData(Homogeneous matrix), timeData

        - Ref. 2023hurocup file robot.py fun.GetDmat
        """ 
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
        
        Δx = GoalEnd[0,3] - NowEnd[0,3]
        Δy = GoalEnd[1,3] - NowEnd[1,3]
        Δz = GoalEnd[2,3] - NowEnd[2,3]   
        
        sampleInterval = allTime / sampleTime
        # Create Time Point     
        timeData = np.arange(startTime, allTime+sampleTime, sampleTime)

        # 儲存軌跡資料(Homogeneous transformation)
        TBuffer = np.zeros(((int(sampleInterval)+1,4,4)))
        
        for λ_ in range(int(sampleInterval)+1):
            λ = λ_ / int(sampleInterval)
            V = (1-cos(θ*λ))
            
            # Transformation matrix
            D_ = np.array(([ [kx**2*V+cos(θ*λ), kx*ky*V-kz*sin(θ*λ), kx*kz*V+ky*sin(θ*λ), D[0,3]*λ],
                                    [kx*ky*V+kz*sin(θ*λ), ky**2*V+cos(θ*λ), ky*kz*V-kx*sin(θ*λ), D[1,3]*λ],
                                    [kx*kz*V-ky*sin(θ*λ), ky*kz*V+kx*sin(θ*λ), kz**2*V+cos(θ*λ), D[2,3]*λ],
                                    [0, 0, 0, 1]]))
            
            # T 是笛卡兒空間中 NowEnd ➜ GoalEnd 過程中每一個軌跡點的齊次變換矩陣(軌跡點)
            T = NowEnd @ D_ 
            TBuffer[λ_] = T
        
        # 計算速度
        pathData = TBuffer
        Euclidean_distance = np.zeros((len(pathData)))
        velData = np.zeros((len(pathData)))

        for i in range(len(pathData)):
            if i == 0:
                prvx = pathData[0, 0, 3]
                prvy = pathData[0, 1, 3]
                prvz = pathData[0, 2, 3]
                Euclidean_distance[i-1] = 0
            else:
                prvx = pathData[i-1, 0, 3]
                prvy = pathData[i-1, 1, 3]
                prvz = pathData[i-1, 2, 3]

            x = pathData[i, 0, 3]
            y = pathData[i, 1, 3]
            z = pathData[i, 2, 3]

            Euclidean_distance[i] = Euclidean_distance[i-1] + np.sqrt((x-prvx)**2 + (y-prvy)**2 + (z-prvz)**2)
        # velData = np.diff(Euclidean_distance)
        velData = np.diff(Euclidean_distance)/sampleTime
        velData = np.insert(velData, 0, 0)
        
            
        return TBuffer, velData, timeData
    
    # def MatrixPath434(self, GoalEnd, NowEnd, allTime, filePath, sampleTime = 0.04, startTime=0):
    def MatrixPath434(self, GoalEnd, NowEnd, allTime, sampleTime = 0.04, startTime=0):
        """Homogeneous matrix interpolation method
        - Ref. 2023hurocup file robot.py fun.GetDmat
        - Return:
            pathData \n
            timeData 
        """ 
        # 4-3-4
        rate = 0.25
        Pinit, Vinit, Ainit, Vfinal, Afinal = 0, 0, 0, 0, 0
        Pfinal = 1
        Plift_off = Pfinal*rate
        Pset_down = Pfinal*(1-rate)
        t1, t2, t3 = allTime/3, allTime/3, allTime/3
        timeData , λ, VelList, AccList = self.TrajectoryPlanning_434\
        (Pinit, Plift_off, Pset_down, Pfinal, t1, t2, t3, sampleTime)


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
        # kx = (D[2,1]-D[1,2]) / (2*sin(θ))
        # ky = (D[0,2]-D[2,0]) / (2*sin(θ))
        # kz = (D[1,0]-D[0,1]) / (2*sin(θ))
        
        Δx = GoalEnd[0,3] - NowEnd[0,3]
        Δy = GoalEnd[1,3] - NowEnd[1,3]
        Δz = GoalEnd[2,3] - NowEnd[2,3]   
        
        # sampleInterval = allTime / sampleTime
        # # Create Time Point     
        # timeData = np.arange(startTime, allTime+sampleTime, sampleTime)

        # TBuffer = np.zeros(((int(sampleInterval)+1,4,4)))
        pathData = np.zeros(((len(λ),4,4)))
        
        for i in range(len(λ)):
            V = (1-cos(θ*λ[i]))
            
            
            # Transformation matrix
            D_ = np.array(([ [kx**2*V+cos(θ*λ[i]), kx*ky*V-kz*sin(θ*λ[i]), kx*kz*V+ky*sin(θ*λ[i]), D[0,3]*λ[i]],
                                    [kx*ky*V+kz*sin(θ*λ[i]), ky**2*V+cos(θ*λ[i]), ky*kz*V-kx*sin(θ*λ[i]), D[1,3]*λ[i]],
                                    [kx*kz*V-ky*sin(θ*λ[i]), ky*kz*V+kx*sin(θ*λ[i]), kz**2*V+cos(θ*λ[i]), D[2,3]*λ[i]],
                                    [0, 0, 0, 1]]))

            # D_ = np.array(([ [round(kx**2*V+cos(θ*λ[i]), 4),    round(kx*ky*V-kz*sin(θ*λ[i]),4),  round(kx*kz*V+ky*sin(θ*λ[i]), 4), round(D[0,3]*λ[i], 3)],
            #                         [round(kx*ky*V+kz*sin(θ*λ[i]), 4), round(ky**2*V+cos(θ*λ[i]), 4),    round(ky*kz*V-kx*sin(θ*λ[i]), 4), round(D[1,3]*λ[i], 3)],
            #                         [round(kx*kz*V-ky*sin(θ*λ[i]), 4), round(ky*kz*V+kx*sin(θ*λ[i]), 4), round(kz**2*V+cos(θ*λ[i]), 4), round(D[2,3]*λ[i],3)],
            #                         [0, 0, 0, 1]]))
            
            # T 是 NowEnd ➜ GoalEnd 過程的插值矩陣(軌跡點)
            T = NowEnd @ D_ 
            pathData[i] = T
        
        # Save data
        # self.dB.Save(pathData, timeData, filePath)
            
        # 計算速度
        Euclidean_distance = np.zeros((len(pathData)))
        velData = np.zeros((len(pathData)))

        for i in range(len(pathData)):
            if i == 0:
                prvx = pathData[0, 0, 3]
                prvy = pathData[0, 1, 3]
                prvz = pathData[0, 2, 3]
                Euclidean_distance[i-1] = 0
            else:
                prvx = pathData[i-1, 0, 3]
                prvy = pathData[i-1, 1, 3]
                prvz = pathData[i-1, 2, 3]

            x = pathData[i, 0, 3]
            y = pathData[i, 1, 3]
            z = pathData[i, 2, 3]

            Euclidean_distance[i] = Euclidean_distance[i-1] + np.sqrt((x-prvx)**2 + (y-prvy)**2 + (z-prvz)**2)
        # velData = np.diff(Euclidean_distance)
        velData = np.diff(Euclidean_distance)/sampleTime
        velData = np.insert(velData, 0, 0)

        return pathData, velData, timeData
    
    def MatrixPath_Scurve(self, GoalEnd, NowEnd, sampleTime):
        """Homogeneous matrix interpolation method
        - Ref. 2023hurocup file robot.py fun.GetDmat
        - return:
            dshape: n*4*4 \n 
        """ 
        # S-curve
        AccList, VelList, PosList, timeData = self.S_curve(1, 3, 18, 12, sampleTime)
        λ = PosList
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
        # kx = (D[2,1]-D[1,2]) / (2*sin(θ))
        # ky = (D[0,2]-D[2,0]) / (2*sin(θ))
        # kz = (D[1,0]-D[0,1]) / (2*sin(θ))
        
        Δx = GoalEnd[0,3] - NowEnd[0,3]
        Δy = GoalEnd[1,3] - NowEnd[1,3]
        Δz = GoalEnd[2,3] - NowEnd[2,3]   
        
        # sampleInterval = allTime / sampleTime
        # # Create Time Point     
        # timeData = np.arange(startTime, allTime+sampleTime, sampleTime)

        # TBuffer = np.zeros(((int(sampleInterval)+1,4,4)))
        pathData = np.zeros(((len(λ),4,4)))
        
        for i in range(len(λ)):
            V = (1-cos(θ*λ[i]))
            
            
            # Transformation matrix
            D_ = np.array(([ [kx**2*V+cos(θ*λ[i]), kx*ky*V-kz*sin(θ*λ[i]), kx*kz*V+ky*sin(θ*λ[i]), D[0,3]*λ[i]],
                                    [kx*ky*V+kz*sin(θ*λ[i]), ky**2*V+cos(θ*λ[i]), ky*kz*V-kx*sin(θ*λ[i]), D[1,3]*λ[i]],
                                    [kx*kz*V-ky*sin(θ*λ[i]), ky*kz*V+kx*sin(θ*λ[i]), kz**2*V+cos(θ*λ[i]), D[2,3]*λ[i]],
                                    [0, 0, 0, 1]]))

            # D_ = np.array(([ [round(kx**2*V+cos(θ*λ[i]), 4),    round(kx*ky*V-kz*sin(θ*λ[i]),4),  round(kx*kz*V+ky*sin(θ*λ[i]), 4), round(D[0,3]*λ[i], 3)],
            #                         [round(kx*ky*V+kz*sin(θ*λ[i]), 4), round(ky**2*V+cos(θ*λ[i]), 4),    round(ky*kz*V-kx*sin(θ*λ[i]), 4), round(D[1,3]*λ[i], 3)],
            #                         [round(kx*kz*V-ky*sin(θ*λ[i]), 4), round(ky*kz*V+kx*sin(θ*λ[i]), 4), round(kz**2*V+cos(θ*λ[i]), 4), round(D[2,3]*λ[i],3)],
            #                         [0, 0, 0, 1]]))
            
            # T 是 NowEnd ➜ GoalEnd 過程的插值矩陣(軌跡點)
            T = NowEnd @ D_ 
            pathData[i] = T
        
        # Save data
        # self.dB.Save(pathData, timeData, filePath)

        return pathData, timeData
    
    def QuaternionsInterpolation(self, GoalEnd, NowEnd, Alltime, SampleTime=0.03):
        """Quaternions interpolation method

        args:
            - GoalEnd: Homogeneous matrix(4x4)
            - NowEnd:  Homogeneous matrix(4x4)
        """
        # TODO 已完成Rotation Matrix， 但Homogeneous Transformation matrix未完成
        # 四元數差值
        qNow = self.Mat.RotaMat_To_Quaternion(GoalEnd)
        qGoal = self.Mat.RotaMat_To_Quaternion(NowEnd)

        SampleInterval = Alltime / SampleTime

        dw = (qGoal[0]-qNow[0])/SampleInterval
        di = (qGoal[1]-qNow[1])/SampleInterval
        dj = (qGoal[2]-qNow[2])/SampleInterval
        dk = (qGoal[3]-qNow[3])/SampleInterval
        if dw != 0:
            wTrajectory = np.arange(qNow[0], qGoal[0], dw)
        else:
            wTrajectory = 0
        if di != 0:
            iTrajectory = np.arange(qNow[1], qGoal[1], di)
        else:
            iTrajectory = 0
        if dj != 0:
            jTrajectory = np.arange(qNow[2], qGoal[2], dj)
        else:
            jTrajectory = 0
        if dk != 0:
            kTrajectory = np.arange(qNow[3], qGoal[3], dk)
        else:
            kTrajectory = 0

        Trajectory = {'w': wTrajectory, 
                      'i': iTrajectory,
                      'j': jTrajectory,
                      'k': kTrajectory}
        
        self.Mat.Quaternion_To_RotaMat(Trajectory)



    def main(self):
        """
        4-3-4 Trajectory Planning Test
        """
        rate = 0.25
        alltime = 6
        t1, t2, t3 = alltime/3, alltime/3, alltime/3
        # t1, t2, t3 = 0.6, 4.8, 0.6
        Pinit, Vinit, Ainit, Vfinal, Afinal = 0, 0, 0, 0, 0
        Pfinal = 1
        Plift_off = Pfinal*rate
        Pset_down = Pfinal*(1-rate)
        sampleTime = 0.04
        
        TimeData, PosData , VelData, AccData = self.TrajectoryPlanning_434\
            (Pinit, Plift_off, Pset_down, Pfinal, t1, t2, t3, sampleTime)

        plt.plot(TimeData, AccData, label='Acc')
        plt.plot(TimeData, VelData, label='Vel')
        plt.plot(TimeData, PosData, label='S')
        plt.title('4-3-4 motion planning')
        plt.xlabel('time')
        plt.ylabel('Unit')
        # plt.tight_layout()
        plt.show()

        """
        MatrixPathPlanning
        """
        # d2r = np.deg2rad
        # NowEnd = np.eye(4)  
        # GoalEnd = np.eye(4)
        # NowEnd = NowEnd @ self.Mat.TransXYZ(4.85,0,2.34) @ self.Mat.RotaXYZ(d2r(-180), d2r(20.2111), d2r(21.6879))
        # GoalEnd = GoalEnd @ self.Mat.TransXYZ(9,-4,z=-2) @ self.Mat.RotaXYZ(d2r(-165.2922), d2r(-7.1994), d2r(17.5635)) 
        # sampleTime = 0.04
        # alltime = 8
        # file_path = "dataBase/testMatrixPathPlanning.csv"

        # pathData, timeData = self.MatrixPathPlanning(GoalEnd, NowEnd, alltime, file_path, sampleTime)
        # print(pathData)

        """
        MatrixPath + 4-3-4
        """
        # d2r = np.deg2rad
        # NowEnd = np.eye(4)  
        # GoalEnd = np.eye(4)
        # Unit = 1

        # NowEnd = NowEnd @ self.Mat.TransXYZ(485.364*Unit,-1.213*Unit,234.338*Unit) @ self.Mat.RotaXYZ(d2r(179.984), d2r(20.2111), d2r(1.6879)) 
        # GoalEnd = GoalEnd @ self.Mat.TransXYZ(955.386*Unit,-19.8*Unit,z=-75.117*Unit) @ self.Mat.RotaXYZ(d2r(-165.2853), d2r(-7.1884), d2r(17.5443)) 
        # sampleTime = 0.04
        # alltime = 80
        # file_path = "dataBase/testMatrixPathPlanning434.csv"

        # pathData, velData, timeData = self.MatrixPath434(GoalEnd, NowEnd, alltime, sampleTime)
        
        # # plt.plot(timeData, pathData, label='pos')
        # plt.plot(timeData, velData, label='Vel')
        # plt.title('MatrixPlan434 planning')
        # plt.xlabel('time')
        # plt.ylabel('Unit')
        # plt.show()

        """
        S-curve
        """
        # AccList, VelList, SList, TimeList = self.S_curve(314.15925, 38, 35, 30, 0.001)
        # # AccList, VelList, SList, TimeList = self.S_curve(100, 38, 35, 30, 0.001)
        # # AccList, VelList, SList, TimeList = self.S_curve(1, 0.3, 0.2, 0.18, 0.001)
        
        # plt.plot(TimeList,AccList, label='Acc')
        # plt.plot(TimeList,VelList, label='Vel')
        # plt.plot(TimeList,SList, label='S')
        # plt.title('S-curve motion planning')
        # plt.xlabel('time')
        # plt.ylabel('Unit')
        # # plt.tight_layout()
        # plt.show()


        

if __name__ == "__main__":
    PathPlan = PathPlanning()
    PathPlan.main()

    
        
