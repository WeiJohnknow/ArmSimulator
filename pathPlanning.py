import numpy as np
import matplotlib.pyplot as plt

def TP_434(θ1, V1, A1, θ2, θ3, θ4, V4, A4, t1, t2, t3):
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

    sampleIntervals = 0.01
    samplePoint = [int(t1/sampleIntervals), int(t2/sampleIntervals), int(t3/sampleIntervals)]

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

def TrajectoryPlanning_434(θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t1, t2, t3,nowTime=0):
    # Inital
    # Lift-off
    # Set_down
    # Final
    # y = C*x   =>   x = inv(c)*y

    sampleIntervals = 0.01
    samplePoint = [int(t1/sampleIntervals), int(t2/sampleIntervals), int(t3/sampleIntervals)]
    
    # X = [a13, a14, a21, a22, a23, a33, a34]
    P1 = θlift_off - θinit
    P2 = θset_down - θlift_off
    P3 = θfinal - θset_down

    X =  np.array([0, 0, 0, 0, 0, 0, 0])
    C =  np.array([[1, 1, 0, 0, 0, 0, 0],
                [3/t1, 4/t1, -1/t2, 0, 0, 0, 0],
                [6/t1**2, 12/t1**2, 0, -2/t2**2, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [0, 0, 1/t2, 2/t2, 3/t2, -3/t3, 4/t3],
                [0, 0, 0, 2/t2**2, 6/t2**2, 6/t3**2, -12/t3**2],
                [0, 0, 0, 0, 0, 1, -1]])

    Y = np.array([P1-(Ainit*t1**2)/2-Vinit*t1,
                    -Ainit*t1-Vinit,
                    -Ainit/t1,
                    P2,
                    Vfinal-Afinal*t3,
                    Afinal,
                    P3-Vfinal*t3-(Afinal*t3**2)/2])
    
    c_1 = np.linalg.inv(C)

    
    # X = np.array([[Afinal*t1**2*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(-2*t1**2*t2*t3**2 - 6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(-t1**2*t3**2 - 6*t1*t2**3 + 3*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(2*t1**2*t2**3 - t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(-t1**3*t3**2 - 4*t1**2*t2**3 + 2*t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (6*t1**2*t2**2 - 4*t1**2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(4*t1**2*t3**2 + 16*t1*t2**3 - 4*t1*t2*t3**2 + 12*t2**4 - 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [-Afinal*t1**2*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(2*t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(t1**2*t3**2 + 6*t1*t2**3 - 3*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(-2*t1**2*t2**3 + t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(t1**3*t3**2 + 4*t1**2*t2**3 - 2*t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-6*t1**2*t2**2 + 4*t1**2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(-3*t1**2*t3**2 - 12*t1*t2**3 + 4*t1*t2*t3**2 - 6*t2**4 + 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [-Afinal*t1**2*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(2*t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(t1**2*t3**2 + 6*t1*t2**3 - 3*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(-2*t1**2*t2**3 + t1**2*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(-2*t1**2*t2*t3**2 - 6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-6*t1**2*t2**2 + 4*t1**2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(4*t1*t2*t3**2 + 12*t2**4 - 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [-Afinal*t1*t2**3*t3**2/(2*t1**2*t3**2 + 8*t1*t2**3 + 12*t2**4 - 6*t2**2*t3**2) - Ainit*(-t1**2*t2*t3**2 - 4*t1*t2**4 + 2*t1*t2**2*t3**2)/(t1*(2*t1**2*t3**2 + 8*t1*t2**3 + 12*t2**4 - 6*t2**2*t3**2)) + P2*(3*t1*t2*t3**2 + 18*t2**4 - 9*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(-6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(3*t1**2*t2*t3**2 + 12*t1*t2**4 - 6*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-18*t1*t2**3 + 12*t1*t2*t3**2)*(-Afinal*t3**2/2 + P3 - Vfinal*t3)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(-6*t1*t2*t3**2 - 24*t2**4 + 12*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [Afinal*(t1**2*t2**2*t3**2 + 3*t1*t2**3*t3**2)/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*(t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1*(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2)) + P2*(-2*t1*t2**3 - 12*t2**4 + 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(2*t1**2*t2**3 - t1**2*t2*t3**2 + 6*t1*t2**4 - 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1 - Vinit)*(-t1**2*t2*t3**2 - 6*t1*t2**4 + 3*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3**2/2 + P3 - Vfinal*t3)*(6*t1**2*t2**2 - 4*t1**2*t3**2 + 18*t1*t2**3 - 12*t1*t2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Ainit*t1**2/2 + P1 - Vinit*t1**2)*(2*t1*t2*t3**2 + 12*t2**4 - 6*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [Afinal*(-2*t1*t2**3*t3**2 - 3*t2**4*t3**2)/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) + P2*(-t1*t2*t3**2 - 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) - t1*t2**2*t3**2*(-Ainit*t1 - Vinit)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + 2*t2**2*t3**2*(-Ainit*t1**2/2 + P1 - Vinit*t1**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(t1**2*t2*t3**2 + 2*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3**2/2 + P3 - Vfinal*t3)*(4*t1**2*t3**2 + 4*t1*t2**3 + 8*t1*t2*t3**2 + 6*t2**4)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)], 
    #         [Afinal*(-2*t1*t2**3*t3**2 - 3*t2**4*t3**2)/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) - Ainit*t2**2*t3**2/(6*t1**2*t3**2 + 24*t1*t2**3 + 36*t2**4 - 18*t2**2*t3**2) + P2*(-t1*t2*t3**2 - 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + t1*t2**2*t3**2*(-Ainit*t1 - Vinit)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + 2*t2**2*t3**2*(-Ainit*t1**2/2 + P1 - Vinit*t1**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3 + Vfinal)*(t1**2*t2*t3**2 + 2*t1*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2) + (-Afinal*t3**2/2 + P3 - Vfinal*t3)*(3*t1**2*t3**2 + 8*t1*t2*t3**2 + 3*t2**2*t3**2)/(t1**2*t3**2 + 4*t1*t2**3 + 6*t2**4 - 3*t2**2*t3**2)]])
    
    # a10 = θinit
    # a11 = Vinit*t1
    # a12 = (Ainit*t1**2)/2
    # a13 = X[0, 0]
    # a14 = X[1, 0]
    # a20 = θlift_off
    # a21 = X[2, 0]
    # a22 = X[3, 0]
    # a23 = X[4, 0]
    # a30 = θfinal
    # a31 = Vfinal*t3
    # a32 = (Afinal*t3**2)/2
    # a33 = X[5, 0]
    # a34 = X[6, 0]
    X = c_1 @ Y

    a10 = θinit
    a11 = Vinit*t1
    a12 = (Ainit*t1**2)/2
    a13 = X[0]
    a14 = X[1]
    a20 = θlift_off
    a21 = X[2]
    a22 = X[3]
    a23 = X[4]
    a30 = θfinal
    a31 = Vfinal*t3
    a32 = (Afinal*t3**2)/2
    a33 = X[5]
    a34 = X[6]

    PosList = []
    VelList = []
    AccList = []
    # 多項式
    # h1 = a10 + a11*t1 + a12*t1**2 + a13*t1**3 + a14*t1**4
    # h2 = a20 + a21*t2 + a22*t2**2 + a23*t2**3
    # h3 = a30 + a31*t3 + a32*t3**2 + a33*t3**3 + a34*t3**4
    TimeList=[nowTime]
    for dt in range(100):
        t = dt/100
        TimeList.append(TimeList[-1]+0.01*t1)
        P = a10 + a11*t + a12*t**2 + a13*t**3 + a14*t**4
        V = a11 + 2*a12*t + 3*a13*t**2 + 4*a14*t**3
        A = 2*a12 + 6*a13*t + 12*a14*t**2
        PosList.append(P)
        VelList.append(V)
        AccList.append(A)

    for dt in range(100):
        t = dt/100
        TimeList.append(TimeList[-1]+0.01*t2)
        P = a20 + a21*t + a22*t**2 + a23*t**3
        V = a21 + 2*a22*t + 3*a23*t**2
        A = 2*a22 + 6*a23*t
        PosList.append(P)
        VelList.append(V)
        AccList.append(A)

    for dt in range(-100,1):
        t = dt/100
        TimeList.append(TimeList[-1]+0.01*t3)
        P = a30 + a31*t + a32*t**2 + a33*t**3 + a34*t**4
        V = a31 + 2*a32*t + 3*a33*t**2 + 4*a34*t**3
        A = 2*a32 + 6*a33*t + 12*a34*t**2
        PosList.append(P)
        VelList.append(V)
        AccList.append(A)

    del TimeList[0]
    return TimeList,PosList , VelList, AccList, samplePoint
    
def S_curve(Smax, Vmax, Amax, Aavg):
    Sm = Smax
    Vm = Vmax
    Am = Amax
    Aa = Aavg
    
    Ta = Vm/Aa
    Tb = 2*Vm/Am-Ta
    Tc = (Ta-Tb)/2
    Ts = (Sm-Vm*Ta)/Vm

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

    # 取樣間隔
    sampleIntervals = 0.001
    
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

    for t1 in range(0, int(Tc/sampleIntervals)):
        t = t1*sampleIntervals
        TimeList.append(t)

        a1 = Am/Tc*t
        v1 = (Am*t**2)/(2*Tc)
        s1 = (1/6)*Am/Tc*t**3

        AccList.append(a1)
        VelList.append(v1)
        SList.append(s1)

        a1End = a1
        v1End = v1
        S1End = s1

    for t2 in range(int(Tc/sampleIntervals), int((Tb+Tc)/sampleIntervals)):
        t = t2*sampleIntervals
        TimeList.append(t)

        a2 = 0*t+Am
        v2 = v1End + Am*(t-Tc)
        s2 = Am/6*Tc**2-0.5*Am*Tc*t+0.5*Am*t**2

        AccList.append(a2) 
        VelList.append(v2)
        SList.append(s2)

        a2End = a2
        v2End = v2
        s2End = s2

    for t3 in range(int((Tb+Tc)/sampleIntervals), int(Ta/sampleIntervals)):
        t = t3*sampleIntervals
        TimeList.append(t)

        a3 = Am-(Am/Tc)*(t-Tc-Tb)
        v3 = Am*(Tb+Tc)-Am/(2*Tc)*(2*Tc+Tb)**2+Am/Tc*(2*Tc+Tb)*t-Am/(2*Tc)*t**2
        s3 = (0.5*Am*Tc+Am*Tb)*(t-Tc-Tb)+0.5*Am*(t-Tc-Tb)**2-Am/6*Tc*(t-Tc-Tb)**3+Am/6*Tc**2+0.5*Am*Tb*(Tb+Tc)

        AccList.append(a3)
        VelList.append(v3)
        SList.append(s3)

        a3End = a3
        v3End = v3
        s3End = s3

    for t4 in range(int(Ta/sampleIntervals), int((Ts+Ta)/sampleIntervals)):
        t = t4*sampleIntervals
        TimeList.append(t)

        a4 = 0*t
        v4 = 0*t+Vm
        s4 = s3End+Vm*(t-Ta)

        AccList.append(a4)
        VelList.append(v4)
        SList.append(s4)

        a4End = a4
        v4End = v4
        s4End = s4

    for t5 in range(int((Ts+Ta)/sampleIntervals), int((Ta+Ts+Tc)/sampleIntervals)):
        t = t5*sampleIntervals
        TimeList.append(t)

        a5 = -(Am/Tc)*(t-Ta-Ts)
        v5 = v4End-(Am/Tc)/2*(t-Ta-Ts)**2
        s5 = s4End-(Am/Tc)/6*(t-Ta-Ts)**3 + v4End*(t-Ta-Ts)

        AccList.append(a5)
        VelList.append(v5)
        SList.append(s5)

        a5End = a5
        v5End = v5
        s5End = s5

    for t6 in range(int((Ta+Ts+Tc)/sampleIntervals), int((Ta+Ts+Tc+Tb)/sampleIntervals)):
        t = t6*sampleIntervals
        TimeList.append(t)

        a6 = 0*t-Am
        v6 = v5End + 0*t-Am*(t-Ta-Ts-Tc)
        s6 = s5End-(Am/2)*(t-Ta-Ts-Tc)**2 + v5End*(t-Ta-Ts-Tc)

        AccList.append(a6)
        VelList.append(v6)
        SList.append(s6)

        a6End = a6
        v6End = v6
        s6End = s6

    for t7 in range(int((Ta+Ts+Tc+Tb)/sampleIntervals), int((2*Ta+Ts)/sampleIntervals)):
        t = t7*sampleIntervals
        TimeList.append(t)

        a7 = -Am+Am/Tc*(t-Ta-Ts-Tc-Tb)
        v7 = v6End - Am*(t-Ta-Ts-Tc-Tb) + Am/(2*Tc)*(t-Ta-Ts-Tc-Tb)**2
        s7 = s6End-(0.5*Am*(t-Ta-Ts-Tc-Tb)**2)+Am/(6*Tc)*(t-Ta-Ts-Tc-Tb)**3+v6End*(t-Ta-Ts-Tc-Tb)

        AccList.append(a7)
        VelList.append(v7)
        SList.append(s7)

        a7End = a7
        v7End = v7
        s7End = s7

    return AccList, VelList, SList, TimeList

def addGraphTicks(InputData, interval):
    # 資料集的最大最小值
    MaxValue = np.max(InputData)
    MinValue = np.min(InputData)

    yTicks = [-40, -30, -20 -10, 0, 10, 20, 30, 40]
    plt.yticks(yTicks)

def main():

    # 4-3-4 test
    θinit = 0
    Vinit = 0 
    Ainit = 0
    θfinal = np.pi/2 
    Vfinal = 0
    Afinal = 0

    rate = 0.25
    θlift_off = θfinal*rate
    θset_down = θfinal*(1.0-rate)
    t = [0.5, 0.5, 0.5]

    
    # TimeList, PosList , VelList, AccList, samplePoint = TP_434( θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t[0], t[1], t[2])
    TimeList, PosList , VelList, AccList, samplePoint = TrajectoryPlanning_434(θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t[0], t[1], t[2])
    # plt.subplot(3, 1, 1)  
    plt.plot(TimeList,PosList, label='Pos')
    plt.show()
    plt.plot(TimeList,VelList, label='Vel')
    plt.show()
    plt.plot(TimeList,AccList, label='Acc')
    plt.show()
    
    # # 一次輸出三條曲線
    # # 設定Y軸刻度
    # # yTicks = [0, 10, 20, 30, 40]
    # # plt.yticks(yTicks)
    # plt.autoscale(enable=True, axis='y')

    # plt.xlabel('Time')
    # plt.ylabel('Position')
    # plt.title('Position Curve')

    # plt.subplot(3, 1, 2)
    # plt.plot(TimeList,VelList, label='Vel')

    # # 設定Y軸刻度
    # # yTicks = [0, 10, 20, 30, 40]
    # # plt.yticks(yTicks)
    # plt.autoscale(enable=True, axis='y')

    # plt.xlabel('Time')
    # plt.ylabel('velocity')
    # plt.title('Velocity Curve')

    # plt.subplot(3, 1, 3)
    # plt.plot(TimeList,AccList, label='Acc')

    # # 設定Y軸刻度
    # # yTicks = [-40, -30, -20 -10, 0, 10, 20, 30, 40]
    # # plt.yticks(yTicks)
    # plt.autoscale(enable=True, axis='y')

    # plt.xlabel('Time')
    # plt.ylabel('Acceleration')
    # plt.title('Acceleration Curve')
    # plt.tight_layout()
    # plt.show()

    # # 第二段曲線
    # θinit = θfinal
    # Vinit = Vfinal 
    # Ainit = Afinal 
    # Vfinal = 0
    # Afinal = 0
    # θfinal = 150

    # rate = 0.25
    # θlift_off =θinit+ (θfinal-θinit)*rate
    # θset_down =θinit+ (θfinal-θinit)*(1.0-rate)
    # t = [0.5, 0.5, 0.5]

    # TimeList2,PosList2 , VelList2, AccList2, samplePoint = TrajectoryPlanning_434( θinit, Vinit, Ainit, θlift_off, θset_down, θfinal, Vfinal, Afinal, t[0], t[1], t[2],nowTime=TimeList[-1])
    
    # plt.plot(TimeList+TimeList2,PosList+PosList2, label='POS')
    # plt.plot(TimeList+TimeList2,VelList+VelList2, label='Vel')
    # plt.plot(TimeList+TimeList2,AccList+AccList2, label='Acc')
    # plt.title('4-3-4 Trajectory planning')
    # plt.xlabel('time')
    # plt.ylabel('Unit')
    # plt.show()

    # S-curve test
    # AccList, VelList, SList, TimeList = S_curve(100, 38, 35, 30)
    
    # plt.plot(TimeList,AccList, label='Acc')
    # plt.plot(TimeList,VelList, label='Vel')
    # plt.plot(TimeList,SList, label='S')
    # plt.title('S-curve motion planning')
    # plt.xlabel('time')
    # plt.ylabel('Unit')
    # # plt.tight_layout()
    # plt.show()

if __name__ == "__main__":
    main()