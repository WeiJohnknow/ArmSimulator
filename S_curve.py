import numpy as np
import matplotlib.pyplot as plt

def Scurve(Amax, Aavg, Vmax, Smax):

    Ta = Vmax/Aavg
    Tb = 2*Vmax/Amax-Ta
    Tc = (Ta-Tb)/2
    Ts = (Smax-Vmax*Ta)/Vmax
    
    sampleTime = 0.001
    # t1 = np.linspace(0, Tc, Tc/sampleTime)
    # t2 = np.linspace(Tc, Tc+Tb, (Tc+Tb)/sampleTime)
    # t3 = np.linspace(Tc+Tb, Ta, Ta/sampleTime)


    # A1 = np.zeros((len(t1)))
    # V1 = np.zeros((len(t1)))
    # S1 = np.zeros((len(t1)))

    # A2 = np.zeros((len(t2)))
    # V2 = np.zeros((len(t2)))
    # S2 = np.zeros((len(t2)))

    # A3 = np.zeros((len(t3)))
    # V3 = np.zeros((len(t3)))
    # S3 = np.zeros((len(t3)))


    t1Point = int(Tc/sampleTime)
    t2Point = int(Tb/sampleTime)-1
    t3Point = int(Tc/sampleTime)
    # t4Point = int(Ts/sampleTime)
    # t3Point = int(Tc/sampleTime)
    # t3Point = int(Tb/sampleTime)
    # t3Point = int(Tc/sampleTime)
    
    t1 = np.zeros((t1Point))
    t2 = np.zeros((t2Point))
    t3 = np.zeros((t3Point))

    A1 = np.zeros((t1Point))
    V1 = np.zeros((t1Point))
    S1 = np.zeros((t1Point))

    A2 = np.zeros((t2Point))
    V2 = np.zeros((t2Point))
    S2 = np.zeros((t2Point))

    A3 = np.zeros((t3Point))
    V3 = np.zeros((t3Point))
    S3 = np.zeros((t3Point))

    count = 0
    t = 0
    while t < round(Tc,2):
        
        a1 = Amax/Tc*t
        v1 = Amax/(2*Tc)*t**2
        s1 = Amax/(6*Tc)*t**3

        A1[count] = a1
        V1[count] = v1
        S1[count] = s1
        t1[count] = t

        count += 1
        t += sampleTime

    count = 0
    t = Tc
    while  t <= Tb+Tc:
        
        a2 = 0*t + Amax
        v2 = Amax*t + Amax/(2*Tc)*Tc**2
        s2 = Amax/(6*Tc)*Tc**3 + Amax*t**2/2 - Amax*Tc*t/2

        A2[count] = a2
        V2[count] = v2
        S2[count] = s2
        t2[count] = t

        count += 1
        t += sampleTime

    # for t_ in range(0, int(Tc*(1/sampleTime))):
    #     t = t_ / (1/sampleTime)

    #     a1 = Amax/Tc*t
    #     v1 = Amax/(2*Tc)*t**2
    #     s1 = Amax/(6*Tc)*t**3

    #     A1[t_] = a1
    #     V1[t_] = v1
    #     S1[t_] = s1
    
    # for t_ in range(int(Tc), int((Tc+Tb)*(1/sampleTime))):
    #     t = t_ / (1/sampleTime)

    #     a2 = 0*t + Amax
    #     v2 = Amax*t + Amax/(2*Tc)*Tc**2
    #     # v2 = Amax*t - Amax*Tc/2
    #     s2 = Amax/(6*Tc)*Tc**3 + Amax*t**2/2 - Amax*Tc*t/2
    #     # s2 = Amax/6*Tc**2-Amax*Tc*t/2+Amax*t**2/2

    #     A2[t_] = a2
    #     V2[t_] = v2
    #     S2[t_] = s2

    # for t_ in range(int((Tc+Tb)*(1/sampleTime)), int(Ta*(1/sampleTime))):
    #     t = t_ / (1/sampleTime)

    #     a3 = Amax/Tc*(2*Tc+Tc)-Amax/Tc*t
    #     v3 = Amax*(Tb+Tc) - Amax/(2*Tc)*(2*Tc+Tb)**2 + Amax/Tc*(2*Tc+Tb)*t - Amax/2*Tc*t**2
    #     s3 = (Amax*Tc/2+Amax*Tb)*(t-Tc-Tb) + Amax/2*(t-Tc-Tb)**2 - Amax/(6*Tc)*(t-Tc-Tb)**3 + Amax/6*Tc**2 + Amax*Tb/2*(Tb+Tc)
        

    #     A3[u] = a3
    #     V3[u] = v3
    #     S3[u] = s3


    
    return t1, A1, V1, S1, t2, A2, V2, S2, t3, A3, V3, S3

if __name__ == "__main__":
    Amax, Aavg, Vmax, Smax = 35, 30, 38, 314.15925
    t1, A1, V1, S1, t2, A2, V2, S2, t3, A3, V3, S3 = Scurve(Amax, Aavg, Vmax, Smax)
    plt.plot(t2, A2, label = "Acc", color = "red")
    plt.plot(t2, V2, label = "Vel", color = "green")
    plt.plot(t2, S2, label = "Pos", color = "blue")
    # plt.plot(t3, A3, label = "Acc", color = "red")
    # plt.plot(t3, V3, label = "Vel", color = "green")
    # plt.plot(t3, S3, label = "Pos", color = "blue")
    plt.show()

