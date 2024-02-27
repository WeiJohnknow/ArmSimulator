import numpy as np
import matplotlib.pyplot as plt

def timeNormalized():
    Tstart = 0
    Tend = 5
    for t in range(Tend+1):
        u = (t - Tstart)/(Tend - Tstart)
        t = Tstart + (Tend-Tstart)*u
        print("t :", t, "u :", u)

def Scurve(Amax, Aavg, Vmax, Smax, sampleTime=0.001):

    
    Ta = Vmax/Aavg
    Tb = 2*Vmax/Amax-Ta
    Tc = (Ta-Tb)/2
    Ts = (Smax-Vmax*Ta)/Vmax

    t1Point = int(Tc/sampleTime)+1
    t2Point = int(Tb/sampleTime)+1
    t3Point = int(Tc/sampleTime)+1
    t4Point = int(Ts/sampleTime)+1
    t5Point = int(Tc/sampleTime)+1
    t6Point = int(Tb/sampleTime)+1
    t7Point = int(Tc/sampleTime)+1

    
    t1 = np.zeros((t1Point))
    t2 = np.zeros((t2Point))
    t3 = np.zeros((t3Point))
    t4 = np.zeros((t4Point))
    t5 = np.zeros((t5Point))
    t6 = np.zeros((t6Point))
    t7 = np.zeros((t7Point))

    A1 = np.zeros((t1Point))
    V1 = np.zeros((t1Point))
    S1 = np.zeros((t1Point))

    A2 = np.zeros((t2Point))
    V2 = np.zeros((t2Point))
    S2 = np.zeros((t2Point))

    A3 = np.zeros((t3Point))
    V3 = np.zeros((t3Point))
    S3 = np.zeros((t3Point))

    A4 = np.zeros((t4Point))
    V4 = np.zeros((t4Point))
    S4 = np.zeros((t4Point))

    A5 = np.zeros((t5Point))
    V5 = np.zeros((t5Point))
    S5 = np.zeros((t5Point))

    A6 = np.zeros((t6Point))
    V6 = np.zeros((t6Point))
    S6 = np.zeros((t6Point))

    A7 = np.zeros((t7Point))
    V7 = np.zeros((t7Point))
    S7 = np.zeros((t7Point))


    Ta = 1.2666666666666666 
    Tb = 0.9047619047619047
    Tc = 0.18095238095238098 
    Ts = 7.000682017543859

    # Ta = 1.266
    # Tb = 0.904
    # Tc = 0.180 
    # Ts = 7.000
    
    count = 0
    t = 0
    while count < t1Point:
        
        a1 = (Amax-0)/Tc*t
        v1 = (0.5*Amax-0)/Tc*t**2
        s1 = (Amax-0)/(6*Tc)*t**3

        # 自己的
        # a1 = Amax/Tc*t
        # v1 = 0.5*Amax/Tc*t**2
        # s1 = Amax/(6*Tc)*t**3

        A1[count] = a1
        V1[count] = v1
        S1[count] = s1
        t1[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("Tc :", Tc)

    count = 0
    t=Tc
    print(Tc+Tb)
    while  count < t2Point:
        # v2家欣的有錯

        a2 = Amax+0*t
        v2 = Amax*t+0*t + V1[-1]
        s2 = (Amax*Tc**2)/6 -0.5*Amax*Tc*t +0.5*Amax*t**2

        # a2 = 0*t + Amax
        # v2 =  Amax*t - 0.5*Amax*Tc
        # s2 = Amax/(6*Tc)*Tc**3 + Amax*t**2/2 - Amax*Tc*t/2

        A2[count] = a2
        V2[count] = v2
        S2[count] = s2
        t2[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("Tc+Tb :", Tc+Tb)

    count = 0
    t=Tc+Tb
    while  count < t3Point:
        # a3. v3 我的有錯
        # a3家欣的也錯， 用老師的


        a3 = Amax/Tc*(2*Tc+Tb) - Amax/Tc*t
        # a3 = Amax+(0-Amax)/Tc*t
        # v3 = Amax*(Tb+Tc) - Amax/(2*Tc)*(2*Tc+Tb)**2 + Amax/Tc*(2*Tc+Tb)*t - Amax/2*Tc*t**2
        # v3 = V2[-1] + Amax*t + (0-0.5*Amax)/Tc*t**2
        v3 = Amax*(Tb+Tc)-Amax/(2*Tc)*(2*Tc+Tb)**2+Amax/Tc*(2*Tc+Tb)*t-Amax/(2*Tc)*t**2
        s3 = (Amax*Tc/2+Amax*Tb)*(t-Tc-Tb) + Amax/2*(t-Tc-Tb)**2 - Amax/(6*Tc)*(t-Tc-Tb)**3 + Amax/6*Tc**2 + Amax*Tb/2*(Tb+Tc)
        A3[count] = a3
        V3[count] = v3
        S3[count] = s3
        t3[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("Ta :", Ta)
    # count = 0
    # t=Ta
    # while  count < t4Point:

    #     a4 = 0*t
    #     v4 = V3[-1] + 0*t
    #     # s4 = S3[-1] + Vmax*t
    #     s4 = S3[-1] + Vmax*(t-Ta)
    #     A4[count] = a4
    #     V4[count] = v4
    #     S4[count] = s4
    #     t4[count] = t

    #     count += 1
    #     t += sampleTime
    #     print(t)

    # count = 0
    # t = Ta + Ts
    # while  count < t5Point: 
        
    #     # 家欣的，他有用時間正規化
    #     # a5 = (0-Amax)/Tc*t
    #     # v5 = (0-0.5*Amax)/Tc*t + V4[-1]
    #     # s5 = Vmax*(t-Ta-Ts)-Amax*(t-Ta-Ts)**3/(6*Tc)

    #     # 使用我自己的(時間未正規化)
    #     a5 = -(Amax/Tc)*(t-Ta-Ts)
    #     v5 = V4[-1]-(Amax/Tc)/2*(t-Ta-Ts)**2
    #     s5 = S4[-1]-(Amax/Tc)/6*(t-Ta-Ts)**3 + V4[-1]*(t-Ta-Ts)

    #     A5[count] = a5
    #     V5[count] = v5
    #     S5[count] = s5
    #     t5[count] = t

    #     count += 1
    #     t += sampleTime
    #     print(t)

    # # 第六段曲線
    # count = 0
    # t = Ta + Ts + Tc
    # while  count < t6Point: 

    #     # 使用我自己的(時間未正規化)
    #     a6 = 0*t-Amax
    #     v6 = V5[-1] + 0*t-Amax*(t-Ta-Ts-Tc)
    #     s6 = S5[-1] - (Amax/2)*(t-Ta-Ts-Tc)**2 + V5[-1]*(t-Ta-Ts-Tc)


    #     A6[count] = a6
    #     V6[count] = v6
    #     S6[count] = s6
    #     t6[count] = t

    #     count += 1
    #     t += sampleTime
    #     print(t)

    # # 第七段曲線
    # count = 0
    # t = Ta + Ts + Tc + Tb
    # while  count < t7Point: 

    #     # 使用我自己的(時間未正規化)
    #     a7 = -Amax + Amax/Tc*(t-Ta-Ts-Tc-Tb)
    #     v7 = V6[-1] - Amax*(t-Ta-Ts-Tc-Tb) + Amax/(2*Tc)*(t-Ta-Ts-Tc-Tb)**2
    #     s7 = S6[-1] - (0.5*Amax*(t-Ta-Ts-Tc-Tb)**2) + Amax/(6*Tc)*(t-Ta-Ts-Tc-Tb)**3 + V6[-1]*(t-Ta-Ts-Tc-Tb)


    #     A7[count] = a7
    #     V7[count] = v7
    #     S7[count] = s7
    #     t7[count] = t

    #     count += 1
    #     t += sampleTime
    #     print(t)

    # acc = np.concatenate((A1, A2, A3, A4, A5, A6, A7), 0)
    # vel = np.concatenate((V1, V2, V3, V4, V5, V6, V7), 0)
    # pos = np.concatenate((S1, S2, S3, S4, S5, S6, S7), 0)
    # t =   np.concatenate((t1, t2, t3, t4, t5, t6, t7), 0)

    acc = np.concatenate((A1, A2, A3), 0)
    vel = np.concatenate((V1, V2, V3), 0)
    pos = np.concatenate((S1, S2, S3), 0)
    t =   np.concatenate((t1, t2, t3), 0)


    return acc, vel, pos, t

def S_curve_(Jmax, Amax, Aavg, Vs, Vmax, Smax, sampleTime):
    """
    Ref. https://www.intechopen.com/chapters/87210
    """
    Ta = Vmax/Aavg
    Tb = 2*Vmax/Amax-Ta
    Tc = (Ta-Tb)/2
    Ts = (Smax-Vmax*Ta)/Vmax

    Jmax = Amax/Tc
    


    t1Point = int(Tc/sampleTime)+1
    t2Point = int(Tb/sampleTime)+1
    t3Point = int(Tc/sampleTime)+1
    t4Point = int(Ts/sampleTime)+1
    t5Point = int(Tc/sampleTime)+1
    t6Point = int(Tb/sampleTime)+1
    t7Point = int(Tc/sampleTime)+1

    
    t1 = np.zeros((t1Point))
    t2 = np.zeros((t2Point))
    t3 = np.zeros((t3Point))
    t4 = np.zeros((t4Point))
    t5 = np.zeros((t5Point))
    t6 = np.zeros((t6Point))
    t7 = np.zeros((t7Point))

    J1 = np.zeros((t1Point))
    A1 = np.zeros((t1Point))
    V1 = np.zeros((t1Point))
    S1 = np.zeros((t1Point))

    J2 = np.zeros((t2Point))
    A2 = np.zeros((t2Point))
    V2 = np.zeros((t2Point))
    S2 = np.zeros((t2Point))

    J3 = np.zeros((t3Point))
    A3 = np.zeros((t3Point))
    V3 = np.zeros((t3Point))
    S3 = np.zeros((t3Point))

    J4 = np.zeros((t4Point))
    A4 = np.zeros((t4Point))
    V4 = np.zeros((t4Point))
    S4 = np.zeros((t4Point))

    J5 = np.zeros((t5Point))
    A5 = np.zeros((t5Point))
    V5 = np.zeros((t5Point))
    S5 = np.zeros((t5Point))

    J6 = np.zeros((t6Point))
    A6 = np.zeros((t6Point))
    V6 = np.zeros((t6Point))
    S6 = np.zeros((t6Point))

    J7 = np.zeros((t7Point))
    A7 = np.zeros((t7Point))
    V7 = np.zeros((t7Point))
    S7 = np.zeros((t7Point))

    count = 0
    t = 0
    while count < t1Point:
        
        j1 = Jmax
        a1 = Jmax*t
        v1 = Vs + 0.5*Jmax*t**2
        s1 = Vs*t + (1/6)*Jmax*t**3

        J1[count] = j1
        A1[count] = a1
        V1[count] = v1
        S1[count] = s1
        t1[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T1 :", Tc)

    # A1end = Jmax*Tc
    # V1end = Vs + 0.5*Jmax*Tc**2
    # S1end = Vs*t + (1/6)*Jmax*Tc**3
    # V1[-1] = V1end
    # S1[-1] = S1end

    V1end = V1[-1]
    S1end = S1[-1]


    count = 0
    t = Tc
    while count < t2Point:   
        j2 = 0
        a2 = Jmax*Tc
        # v2 = V1[-1] + Jmax*Tc*(t-Tc)
        # s2 = S1[-1] + V1[-1]*(t-Tc) + 0.5*Jmax*Tc*(t-Tc)**2
        v2 = V1end + Jmax*Tc*(t-Tc)
        s2 = S1end + V1end*(t-Tc) + 0.5*Jmax*Tc*(t-Tc)**2

        J2[count] = j2
        A2[count] = a2
        V2[count] = v2
        S2[count] = s2
        t2[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T2 :", Tc+Tb)

    # A2end = Jmax*Tc
    # V2end = V1end + Jmax*Tc*((Tc+Tb)-Tc)
    # S2end = S1end + V1end*((Tc+Tb)-Tc) + 0.5*Jmax*Tc*((Tc+Tb)-Tc)**2
    # V2[-1] = V2end
    # S2[-1] = S2end

    V2end = V2[-1]
    S2end = S2[-1]

    count = 0
    t = Tc + Tb
    while count < t3Point:   
        j3 = -Jmax
        a3 = Jmax*Tc-Jmax*(t-(Tc+Tb))
        # v3 = V2[-1] + Jmax*Tc*(t-(Tc+Tb)) - 0.5*Jmax*(t-(Tc+Tb))**2
        # s3 = S2[-1] + V2[-1]*(t-(Tc+Tb)) + 0.5*Jmax*Tc*(t-(Tc+Tb))**2 - (1/6)*Jmax*Tc*(t-(Tc+Tb))**3
        v3 = V2end + Jmax*Tc*(t-(Tc+Tb)) - 0.5*Jmax*(t-(Tc+Tb))**2
        s3 = S2end + V2end*(t-(Tc+Tb)) + 0.5*Jmax*Tc*(t-(Tc+Tb))**2 - (1/6)*Jmax*Tc*(t-(Tc+Tb))**3

        J3[count] = j3
        A3[count] = a3
        V3[count] = v3
        S3[count] = s3
        t3[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T3 :", Tc+Tb+Tc)

    # A3end = Jmax*Tc-Jmax*(Ta-(Tc+Tb))
    # V3end = V2end + Jmax*Tc*(Ta-(Tc+Tb)) - 0.5*Jmax*(Ta-(Tc+Tb))**2
    # S3end = S2end + V2end*(Ta-(Tc+Tb)) + 0.5*Jmax*Tc*(Ta-(Tc+Tb))**2 - (1/6)*Jmax*Tc*(Ta-(Tc+Tb))**3
    # V3[-1] = V3end
    # S3[-1] = S3end

    V3end = V3[-1]
    S3end = S3[-1]

    count = 0
    t = Ta
    while count < t4Point:   
        j4 = 0
        a4 = 0
        # v4 = V3[-1]
        # s4 = S3[-1] + V3[-1]*(t-Ta)
        v4 = V3end
        s4 = S3end + V3end*(t-Ta)

        J4[count] = j4
        A4[count] = a4
        V4[count] = v4
        S4[count] = s4
        t4[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T4 :", Ta+Ts)

    # A4end = 0
    # V4end = V3end
    # S4end = S3end + V3end*((Ts+Ta)-Ta)
    # V4[-1] = V4end
    # S4[-1] = S4end

    V4end = V4[-1]
    S4end = S4[-1]

    count = 0
    t = Ta+Ts
    while count < t5Point:   
        j5 = -Jmax
        a5 = -Jmax*(t-(Ta+Ts))
        # v5 = V4[-1] - 0.5*Jmax*(t-(Ta+Ts))**2
        # s5 = S4[-1] + V4[-1]*(t-(Ta+Ts)) - (1/6)*Jmax*(t-(Ta+Ts))**3
        v5 = V4end - 0.5*Jmax*(t-(Ta+Ts))**2
        s5 = S4end + V4end*(t-(Ta+Ts)) - (1/6)*Jmax*(t-(Ta+Ts))**3

        J5[count] = j5
        A5[count] = a5
        V5[count] = v5
        S5[count] = s5
        t5[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T5 :", Ta+Ts+Tc)

    # A5end = -Jmax*((Ta+Ts+Tc)-(Ta+Ts))
    # V5end = V4end - 0.5*Jmax*((Ta+Ts+Tc)-(Ta+Ts))**2
    # S5end = S4end + V4end*((Ta+Ts+Tc)-(Ta+Ts)) - (1/6)*Jmax*((Ta+Ts+Tc)-(Ta+Ts))**3
    # V5[-1] = V5end
    # S5[-1] = S5end

    V5end = V5[-1]
    S5end = S5[-1]

    count = 0
    t = Ta+Ts+Tc
    while count < t6Point:   
        j6 = 0
        a6 = -Jmax*Tc
        # v6 = V5[-1] - Jmax*Tc*(t-(Ta+Ts+Tc))
        # s6 = S5[-1] + V5[-1]*(t-(Ta+Ts+Tc)) - 0.5*Jmax*Tc*(t-(Ta+Ts+Tc))**2
        v6 = V5end - Jmax*Tc*(t-(Ta+Ts+Tc))
        s6 = S5end + V5end*(t-(Ta+Ts+Tc)) - 0.5*Jmax*Tc*(t-(Ta+Ts+Tc))**2

        J6[count] = j6
        A6[count] = a6
        V6[count] = v6
        S6[count] = s6
        t6[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T6 :", Ta+Ts+Tc+Tb)

    # A6end = -Jmax*Tc
    # V6end = V5end - Jmax*Tc*((Ta+Ts+Tc+Tb)-(Ta+Ts+Tc))
    # S6end = S5end + V5end*((Ta+Ts+Tc+Tb)-(Ta+Ts+Tc)) - 0.5*Jmax*Tc*((Ta+Ts+Tc+Tb)-(Ta+Ts+Tc))**2
    # V6[-1] = V6end
    # S6[-1] = S6end

    V6end = V6[-1]
    S6end = S6[-1]

    count = 0
    t = Ta+Ts+Tc+Tb
    while count < t7Point:   
        j7 = Jmax
        a7 = -Jmax*Tc + Jmax*(t-(Ta+Ts+Tc+Tb))
        # v7 = V6[-1] - Jmax*Tc*(t-(Ta+Ts+Tc+Tb)) + 0.5*Jmax*(t-(Ta+Ts+Tc+Tb))**2
        # s7 = S6[-1] + V6[-1]*(t-(Ta+Ts+Tc+Tb)) - 0.5*Jmax*Tc*(t-(Ta+Ts+Tc+Tb))**2 + (1/6)*Jmax*(t-(Ta+Ts+Tc+Tb))**3
        v7 = V6end - Jmax*Tc*(t-(Ta+Ts+Tc+Tb)) + 0.5*Jmax*(t-(Ta+Ts+Tc+Tb))**2
        s7 = S6end + V6end*(t-(Ta+Ts+Tc+Tb)) - 0.5*Jmax*Tc*(t-(Ta+Ts+Tc+Tb))**2 + (1/6)*Jmax*(t-(Ta+Ts+Tc+Tb))**3

        J7[count] = j7
        A7[count] = a7
        V7[count] = v7
        S7[count] = s7
        t7[count] = t

        count += 1
        t += sampleTime
        print(t)
    print("T7 :", Ta+Ts+Ta)

    # A7end = -Jmax*Tc + Jmax*((Ta+Ts+Ta)-(Ta+Ts+Tc+Tb))
    # V7end = V6end - Jmax*Tc*((Ta+Ts+Ta)-(Ta+Ts+Tc+Tb)) + 0.5*Jmax*((Ta+Ts+Ta)-(Ta+Ts+Tc+Tb))**2
    # S7end = S6end + V6end*((Ta+Ts+Ta)-(Ta+Ts+Tc+Tb)) - 0.5*Jmax*Tc*((Ta+Ts+Ta)-(Ta+Ts+Tc+Tb))**2 + (1/6)*Jmax*((Ta+Ts+Ta)-(Ta+Ts+Tc+Tb))**3
    # V7[-1] = V7end
    # S7[-1] = S7end

    V7end = V7[-1]
    S7end = S7[-1]



    jerk = np.concatenate((J1, J2, J3, J4, J5, J6, J7), 0)
    acc  = np.concatenate((A1, A2, A3, A4, A5, A6, A7), 0)
    vel  = np.concatenate((V1, V2, V3, V4, V5, V6, V7), 0)
    pos  = np.concatenate((S1, S2, S3, S4, S5, S6, S7), 0)
    t =    np.concatenate((t1, t2, t3, t4, t5, t6, t7), 0)

    # jerk = J1
    # acc = A1
    # vel = V1
    # pos = S1
    # t =   t1


    return jerk ,acc, vel, pos, t



if __name__ == "__main__":
    # Amax, Aavg, Vmax, Smax = 35, 30, 38, 314.15925
    # acc, vel, pos, t = Scurve(Amax, Aavg, Vmax, Smax, 0.001)

    # plt.plot(t, acc, label = "Acc", color = "red")
    # plt.plot(t, vel, label = "Vel", color = "green")
    # plt.plot(t, pos, label = "Pos", color = "blue")

    # 193.421052631579
    # Amax = Jmax * Tc
    Jmax, Amax, Aavg, Vs, Vmax, Smax, sampleTime = 0, 35, 30, 0, 38, 314.15925, 0.001
    jerk, acc, vel, pos, t = S_curve_(Jmax, Amax, Aavg, Vs, Vmax, Smax, sampleTime)
    plt.plot(t, jerk, label = "jerk", color = "yellow")
    plt.plot(t, acc, label = "Acc", color = "red")
    plt.plot(t, vel, label = "Vel", color = "green")
    plt.plot(t, pos, label = "Pos", color = "blue")

    plt.show()

