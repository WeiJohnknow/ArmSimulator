import numpy as np
import matplotlib.pyplot as plt

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

    count = 0
    t = 0
    Ta = 1.2666666666666666 
    Tb = 0.9047619047619047
    Tc = 0.18095238095238098 
    Ts = 7.000682017543859

    Ta = 1.266
    Tb = 0.904
    Tc = 0.180 
    Ts = 7.000
    while count < t1Point:
        
        a1 = Amax/Tc*t
        v1 = 0.5*Amax/Tc*t**2
        s1 = Amax/(6*Tc)*t**3

        A1[count] = a1
        V1[count] = v1
        S1[count] = s1
        t1[count] = t

        count += 1
        t += sampleTime
        print(t)

    count = 0
    t=Tc
    print(Tc+Tb)
    while  count < t2Point:
        # v2家欣的有錯

        a2 = 0*t + Amax
        # v2 = Amax*t + Amax/(2*Tc)*Tc**2
        v2 =  Amax*t - 0.5*Amax*Tc
        s2 = Amax/(6*Tc)*Tc**3 + Amax*t**2/2 - Amax*Tc*t/2

        A2[count] = a2
        V2[count] = v2
        S2[count] = s2
        t2[count] = t

        count += 1
        t += sampleTime
        print(t)

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

    count = 0
    t=Ta
    while  count < t4Point:

        a4 = 0*t
        v4 = V3[-1] + 0*t
        # s4 = S3[-1] + Vmax*t
        s4 = S3[-1] + Vmax*(t-Ta)
        A4[count] = a4
        V4[count] = v4
        S4[count] = s4
        t4[count] = t

        count += 1
        t += sampleTime
        print(t)

    count = 0
    t = Ta + Ts
    while  count < t5Point: 
        
        # 家欣的，他有用時間正規化
        # a5 = (0-Amax)/Tc*t
        # v5 = (0-0.5*Amax)/Tc*t + V4[-1]
        # s5 = Vmax*(t-Ta-Ts)-Amax*(t-Ta-Ts)**3/(6*Tc)

        # 使用我自己的(時間未正規化)
        a5 = -(Amax/Tc)*(t-Ta-Ts)
        v5 = V4[-1]-(Amax/Tc)/2*(t-Ta-Ts)**2
        s5 = S4[-1]-(Amax/Tc)/6*(t-Ta-Ts)**3 + V4[-1]*(t-Ta-Ts)

        A5[count] = a5
        V5[count] = v5
        S5[count] = s5
        t5[count] = t

        count += 1
        t += sampleTime
        print(t)

    # 第六段曲線
    count = 0
    t = Ta + Ts + Tc
    while  count < t6Point: 

        # 使用我自己的(時間未正規化)
        a6 = 0*t-Amax
        v6 = V5[-1] + 0*t-Amax*(t-Ta-Ts-Tc)
        s6 = S5[-1] - (Amax/2)*(t-Ta-Ts-Tc)**2 + V5[-1]*(t-Ta-Ts-Tc)


        A6[count] = a6
        V6[count] = v6
        S6[count] = s6
        t6[count] = t

        count += 1
        t += sampleTime
        print(t)

    # 第七段曲線
    count = 0
    t = Ta + Ts + Tc + Tb
    while  count < t7Point: 

        # 使用我自己的(時間未正規化)
        a7 = -Amax + Amax/Tc*(t-Ta-Ts-Tc-Tb)
        v7 = V6[-1] - Amax*(t-Ta-Ts-Tc-Tb) + Amax/(2*Tc)*(t-Ta-Ts-Tc-Tb)**2
        s7 = S6[-1] - (0.5*Amax*(t-Ta-Ts-Tc-Tb)**2) + Amax/(6*Tc)*(t-Ta-Ts-Tc-Tb)**3 + V6[-1]*(t-Ta-Ts-Tc-Tb)


        A7[count] = a7
        V7[count] = v7
        S7[count] = s7
        t7[count] = t

        count += 1
        t += sampleTime
        print(t)

    acc = np.concatenate((A1, A2, A3, A4, A5, A6, A7), 0)
    vel = np.concatenate((V1, V2, V3, V4, V5, V6, V7), 0)
    pos = np.concatenate((S1, S2, S3, S4, S5, S6, S7), 0)
    t =   np.concatenate((t1, t2, t3, t4, t5, t6, t7), 0)


    return acc, vel, pos, t

if __name__ == "__main__":
    Amax, Aavg, Vmax, Smax = 35, 30, 38, 314.15925
    acc, vel, pos, t = Scurve(Amax, Aavg, Vmax, Smax, 0.001)

    plt.plot(t, acc, label = "Acc", color = "red")
    plt.plot(t, vel, label = "Vel", color = "green")
    plt.plot(t, pos, label = "Pos", color = "blue")



    # plt.plot(t1+t2, A2, label = "Acc", color = "red")
    # plt.plot(t1+t2, V2, label = "Vel", color = "green")
    # plt.plot(t1+t2, S2, label = "Pos", color = "blue")
    # plt.plot(t3, A3, label = "Acc", color = "red")
    # plt.plot(t3, V3, label = "Vel", color = "green")
    # plt.plot(t3, S3, label = "Pos", color = "blue")
    plt.show()

