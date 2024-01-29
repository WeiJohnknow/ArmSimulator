
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataBase import dataBase
import os
from Toolbox import TimeTool
import time
from Matrix import Matrix4x4
from dataBase import dataBase
from sklearn.linear_model import LinearRegression

dB = dataBase()

def plot_6_chart_1curve(x, y, z, Rx, Ry, Rz, time, title_header, title, xlable, ylable):
    """畫出六張子圖，每張圖有一條曲線
    - Args: x, y, z, Rx, Ry, Rz, time, title, xlable, ylable
        - data type :list、ndarray
        - title_header : ex:[x, y, z, Rx, Ry, Rz].
        - title :子圖表標題，該曲線名稱，ex: Position curve.
            - title_header + title = "x" + "Position curve"
        - xlable :x軸標量名稱，ex :time(s).
        - ylable :y軸標量名稱，ex :Position.
    """

    # 图1：Px vs. time
    # plt.subplot(3, 5, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(time, x)
    plt.title(f"{title_header[0]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(time, y)
    plt.title(f"{title_header[1]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(time, z)
    plt.title(f"{title_header[2]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)

    # 图4：Px vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(time, Rx)
    plt.title(f"{title_header[3]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)

    # 图5：Py vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(time, Ry)
    plt.title(f"{title_header[4]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)

    # 图6：Pz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(time, Rz)
    plt.title(f"{title_header[5]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)


    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()

def plot_6_chart_2curve(data1, data2, title_header, title, xlable, ylable, line_1_label, line_2_label):
    """畫出六張子圖，每張圖有二條曲線
    - Args: data1, data2
        - data1: [x, y, z, Rx, Ry, Rz, time]
        - data2: [x, y, z, Rx, Ry, Rz, time]
        - title_header : ex:[x, y, z, Rx, Ry, Rz].
        - title :子圖表標題，該曲線名稱，ex: Position curve.
            - title_header + title = "x" + "Position curve"
        - xlable :x軸標量名稱，ex :time(s).
        - ylable :y軸標量名稱，ex :Position.
        - line_1_label :線條1之名稱，通常為實際量測值(真實手臂量測值)。
        - line_2_label :線條2之名稱，通常為期望值(軌跡演算法產生)。
    - data type :list、ndarray
    """

    x1 =  data1[0]
    y1 =  data1[1]
    z1 =  data1[2]
    Rx1 = data1[3]
    Ry1 = data1[4]
    Rz1 = data1[5]
    t1 =  data1[6]

    x2 =  data2[0]
    y2 =  data2[1]
    z2 =  data2[2]
    Rx2 = data2[3]
    Ry2 = data2[4]
    Rz2 = data2[5]
    t2 =  data2[6]


    
    # 图1：Px vs. time
    # plt.subplot(3, 2, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(t1, x1, color='red',  linestyle='-', linewidth=3, label = line_1_label)
    plt.plot(t2, x2, color='blue', linestyle=':', linewidth=3, label = line_2_label)
    plt.title(f"{title_header[0]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(t1, y1, color='red',  linestyle='-', linewidth=3, label = line_1_label)
    plt.plot(t2, y2, color='blue', linestyle=':', linewidth=3, label = line_2_label)
    plt.title(f"{title_header[1]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(t1, z1, color='red',  linestyle='-', linewidth=3, label = line_1_label)
    plt.plot(t2, z2, color='blue', linestyle=':', linewidth=3, label = line_2_label)
    plt.title(f"{title_header[2]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()

    # 图4：Px vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(t1, Rx1, color='red',  linestyle='-', linewidth=3, label = line_1_label)
    plt.plot(t2, Rx2, color='blue', linestyle=':', linewidth=3, label = line_2_label)
    plt.title(f"{title_header[3]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()
    
    # 图5：Py vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(t1, Ry1, color='red',  linestyle='-', linewidth=3, label =  line_1_label)
    plt.plot(t2, Ry2, color='blue', linestyle=':', linewidth=3, label =  line_2_label)
    plt.title(f"{title_header[4]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()

    # 图6：Pz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(t1, Rz1, color='red',  linestyle='-', linewidth=3, label =  line_1_label)
    plt.plot(t2, Rz2, color='blue', linestyle=':', linewidth=3, label =  line_2_label)
    plt.title(f"{title_header[5]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable)
    plt.legend()

    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()

    
def Analyze_Position(PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv( Time_file)
    x=[]
    y=[]
    z=[]
    Rx=[]
    Ry=[]
    Rz=[]
    time = []
    for i in range(len(PoseMat6x1)):
        x.append(PoseMat6x1["X"][i])
        y.append(PoseMat6x1["Y"][i])
        z.append(PoseMat6x1["Z"][i])
        Rx.append(PoseMat6x1["Rx"][i])
        Ry.append(PoseMat6x1["Ry"][i])
        Rz.append(PoseMat6x1["Rz"][i])
        time.append(pathdata_df['time'][i])

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Position curve"
    xlabel = "time(ms)"
    ylable = "Position(mm)"

    # 繪製圖表
    plot_6_chart_1curve(x, y, z, Rx, Ry, Rz, time, title_header, title, xlabel, ylable)


def Analyze_Velocity(sampleTime, PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv(Time_file)

    t = np.zeros((len(PoseMat6x1)))
    x = np.zeros((len(PoseMat6x1)))
    y = np.zeros((len(PoseMat6x1)))
    z = np.zeros((len(PoseMat6x1)))
    Rx = np.zeros((len(PoseMat6x1)))
    Ry = np.zeros((len(PoseMat6x1)))
    Rz = np.zeros((len(PoseMat6x1)))

    vx = np.zeros((len(PoseMat6x1)))
    vy = np.zeros((len(PoseMat6x1)))
    vz = np.zeros((len(PoseMat6x1)))
    vRx = np.zeros((len(PoseMat6x1)))
    vRy = np.zeros((len(PoseMat6x1)))
    vRz = np.zeros((len(PoseMat6x1)))

    for i in range(len(PoseMat6x1)):
        t[i] = pathdata_df['time'][i]
        x[i] = PoseMat6x1["X"][i]
        y[i] = PoseMat6x1["Y"][i]
        z[i] = PoseMat6x1["Z"][i]
        Rx[i] = PoseMat6x1["Rx"][i]
        Ry[i] = PoseMat6x1["Ry"][i]
        Rz[i] = PoseMat6x1["Rz"][i]
        
    # 平均速度
    # for i in range(0, len(x)):
    #     dpx = x[i] - x[i-1]
    #     dpy = x[i] - x[i-1]
    #     dpz = x[i] - x[i-1]
    #     dpRx = x[i] - x[i-1]
    #     dpRy = x[i] - x[i-1]
    #     dpRz = x[i] - x[i-1]

    #     Vx = dpx/sampleTime
    #     Vy = dpy/sampleTime
    #     Vz = dpz/sampleTime
    #     Vrx = dpRx/sampleTime
    #     Vry = dpRy/sampleTime
    #     Vrz = dpRz/sampleTime


    #     vx.append(Vx)
    #     vy.append(Vy)
    #     vz.append(Vz)
    #     vRx.append(Vrx)
    #     vRy.append(Vry)
    #     vRz.append(Vrz)

    # 瞬時速度
    vx = np.diff(x) / sampleTime
    vy = np.diff(y) / sampleTime
    vz = np.diff(z) / sampleTime
    vRx =np.diff(Rx) / sampleTime
    vRy =np.diff(Ry) / sampleTime
    vRz =np.diff(Rz) / sampleTime

    vx = np.insert(vx, 0, 0)
    vy = np.insert(vy , 0, 0)
    vz = np.insert(vz , 0, 0)
    vRx =np.insert(vRx, 0, 0)
    vRy =np.insert(vRy, 0, 0)
    vRz =np.insert(vRz, 0, 0)


    # 線性回歸
    # t = np.zeros((len(pathdata_df['time']), 1))
    # for i in range(len(pathdata_df['time'])):
    #     t[i] = pathdata_df['time'][i]

    # # 添加一列全為1的特徵，以便包含截距
    # X_b = np.c_[np.ones((len(vx), 1)), vx]

    # # 使用最小二乘法計算斜率和截距
    # theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(t)

    # # 獲取斜率和截距
    # slope = theta_best[1][0]
    # intercept = theta_best[0][0]

    # # 顯示結果
    # print(f"斜率：{slope}")
    # print(f"截距：{intercept}")

    # # 繪製散點圖和擬和線
    # plt.scatter(t, vx, color='blue', label='數據點')
    # plt.plot(vx, X_b.dot(theta_best), color='red', linewidth=3, label='擬和線')
    # plt.xlabel('X軸')
    # plt.ylabel('Y軸')
    # plt.legend()
    # plt.show()

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Velocity curve"
    xlabel = "time(ms)"
    ylable = "Velocity(mm/s)"

    plot_6_chart_1curve(vx, vy, vz, vRx, vRy, vRz, t, title_header, title, xlabel, ylable)


def Analyze_Acceleration(sampleTime, PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv(Time_file)
    
    t=[]
    x=[]
    y=[]
    z=[]
    Rx=[]
    Ry=[]
    Rz=[]

    vx=[]
    vy=[]
    vz=[]
    vRx=[]
    vRy=[]
    vRz=[]

    for i in range(len(PoseMat6x1)):
        t.append(pathdata_df['time'][i])
        x.append(PoseMat6x1["X"][i])
        y.append(PoseMat6x1["Y"][i])
        z.append(PoseMat6x1["Z"][i])
        Rx.append(PoseMat6x1["Rx"][i])
        Ry.append(PoseMat6x1["Ry"][i])
        Rz.append(PoseMat6x1["Rz"][i])

    

    # 瞬時速度
    vx = np.diff(x) / sampleTime
    vy = np.diff(y) / sampleTime
    vz = np.diff(z) / sampleTime
    vRx =np.diff(Rx) / sampleTime
    vRy =np.diff(Ry) / sampleTime
    vRz =np.diff(Rz) / sampleTime

    vx = np.insert(vx, 0, 0)
    vy = np.insert(vy , 0, 0)
    vz = np.insert(vz , 0, 0)
    vRx =np.insert(vRx, 0, 0)
    vRy =np.insert(vRy, 0, 0)
    vRz =np.insert(vRz, 0, 0)

    # 算瞬時加速度
    ax = np.diff(vx ) / sampleTime
    ay = np.diff(vy ) / sampleTime
    az = np.diff(vz ) / sampleTime
    aRx =np.diff(vRx) / sampleTime
    aRy =np.diff(vRy) / sampleTime
    aRz =np.diff(vRz) / sampleTime

    ax = np.insert(ax, 0, 0)
    ay = np.insert(ay , 0, 0)
    az = np.insert(az , 0, 0)
    aRx =np.insert(aRx, 0, 0)
    aRy =np.insert(aRy, 0, 0)
    aRz =np.insert(aRz, 0, 0)

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Acceleration curve"
    xlabel = "time(ms)"
    ylable = "Acceleration(mm/s²)"
    
    plot_6_chart_1curve(ax, ay, az, aRx, aRy, aRz, t, title_header, title, xlabel, ylable)


def Analyze_JointAngle(JointAngle_file, Time_file):
    JointAngle6x1 = pd.read_csv(JointAngle_file)
    time_df = pd.read_csv( Time_file)
    S = []
    L = []
    U = []
    R = []
    B = []
    T = []
    t = []
    for i in range(len(JointAngle6x1)):
        t.append(time_df['time'][i])
        S.append(JointAngle6x1["S"][i])
        L.append(JointAngle6x1["L"][i])
        U.append(JointAngle6x1["U"][i])
        R.append(JointAngle6x1["R"][i])
        B.append(JointAngle6x1["B"][i])
        T.append(JointAngle6x1["T"][i])

    title_header = ["S axis", "L axis", "U axis", "R axis", "B axis", "T axis"]
    title = "JointAngle curve"
    xlabel = "time(s)"
    ylable = "JointAngle(deg)"
    
    plot_6_chart_1curve(S, L, U, R, B, T, t,title_header, title, xlabel, ylable)

def Analyze_2curve_Position(PoseMat_file_1, Time_file_1, PoseMat_file_2, Time_file_2):
    """Analyze 2 curve
    - Real : PoseMat_file_1、Time_file_1
    - Simulator : PoseMat_file_2、Time_file_2
    - default: t1 unit is microsecond; t2 unit is second. 
    """
    PoseMat6x1_1 = pd.read_csv(PoseMat_file_1)
    pathdata_df_1 = pd.read_csv( Time_file_1)
    PoseMat6x1_2 = pd.read_csv(PoseMat_file_2)
    pathdata_df_2 = pd.read_csv( Time_file_2)

    # data1
    x1  = []
    y1  = []
    z1  = []
    Rx1 = []
    Ry1 = []
    Rz1 = []
    t1  = []

    # data2
    x2  = []
    y2  = []
    z2  = []
    Rx2 = []
    Ry2 = []
    Rz2 = []
    t2  = []

    for i in range(len(PoseMat6x1_1)):
        x1.append( PoseMat6x1_1["X"][i])
        y1.append( PoseMat6x1_1["Y"][i]) 
        z1.append( PoseMat6x1_1["Z"][i]) 
        Rx1.append(PoseMat6x1_1["Rx"][i])
        Ry1.append(PoseMat6x1_1["Ry"][i])
        Rz1.append(PoseMat6x1_1["Rz"][i])
        t1.append(round(pathdata_df_1["time"][i]/1000000, 3))

    for i in range(len(PoseMat6x1_2)):
        x2.append( PoseMat6x1_2["X"][i])
        y2.append( PoseMat6x1_2["Y"][i]) 
        z2.append( PoseMat6x1_2["Z"][i]) 
        Rx2.append(PoseMat6x1_2["Rx"][i])
        Ry2.append(PoseMat6x1_2["Ry"][i])
        Rz2.append(PoseMat6x1_2["Rz"][i])
        t2.append(pathdata_df_2["time"][i])
    
    data1 = [x1, y1, z1, Rx1, Ry1, Rz1, t1]
    data2 = [x2, y2, z2, Rx2, Ry2, Rz2, t2]

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Position curve"
    xlabel = "time(s)"
    ylable = "Position(mm)"
    line_1_label = "Measured value"
    line_2_label = "Expect value"
        
    plot_6_chart_2curve(data1, data2, title_header, title, xlabel, ylable, line_1_label, line_2_label)

def Analyze_2curve_Velocity(sampleTime, PoseMat_file_1, Time_file_1, PoseMat_file_2, Time_file_2):
    """Analyze 2 curve
    - Real : PoseMat_file_1、Time_file_1
    - Simulator : PoseMat_file_2、Time_file_2
    - default: t1 unit is microsecond; t2 unit is second. 
    """
    PoseMat6x1_1 = pd.read_csv(PoseMat_file_1)
    pathdata_df_1 = pd.read_csv( Time_file_1)
    PoseMat6x1_2 = pd.read_csv(PoseMat_file_2)
    pathdata_df_2 = pd.read_csv( Time_file_2)

    # data1
    x1  = []
    y1  = []
    z1  = []
    Rx1 = []
    Ry1 = []
    Rz1 = []
    t1  = []

    # data2
    x2  = []
    y2  = []
    z2  = []
    Rx2 = []
    Ry2 = []
    Rz2 = []
    t2  = []

    for i in range(len(PoseMat6x1_1)):
        x1.append( PoseMat6x1_1["X"][i])
        y1.append( PoseMat6x1_1["Y"][i]) 
        z1.append( PoseMat6x1_1["Z"][i]) 
        Rx1.append(PoseMat6x1_1["Rx"][i])
        Ry1.append(PoseMat6x1_1["Ry"][i])
        Rz1.append(PoseMat6x1_1["Rz"][i])
        t1.append(round(pathdata_df_1["time"][i]/1000000, 3))

    for i in range(len(PoseMat6x1_2)):
        x2.append( PoseMat6x1_2["X"][i])
        y2.append( PoseMat6x1_2["Y"][i]) 
        z2.append( PoseMat6x1_2["Z"][i]) 
        Rx2.append(PoseMat6x1_2["Rx"][i])
        Ry2.append(PoseMat6x1_2["Ry"][i])
        Rz2.append(PoseMat6x1_2["Rz"][i])
        t2.append(pathdata_df_2["time"][i])
    
    # 瞬時速度
    vx1 = np.diff(x1) / sampleTime
    vy1 = np.diff(y1) / sampleTime
    vz1 = np.diff(z1) / sampleTime
    vRx1 =np.diff(Rx1) / sampleTime
    vRy1 =np.diff(Ry1) / sampleTime
    vRz1 =np.diff(Rz1) / sampleTime

    vx1 = np.insert(vx1, 0, 0)
    vy1 = np.insert(vy1 , 0, 0)
    vz1 = np.insert(vz1 , 0, 0)
    vRx1 =np.insert(vRx1, 0, 0)
    vRy1 =np.insert(vRy1, 0, 0)
    vRz1 =np.insert(vRz1, 0, 0)

     # 瞬時速度
    vx2 = np.diff(x2) / sampleTime
    vy2 = np.diff(y2) / sampleTime
    vz2 = np.diff(z2) / sampleTime
    vRx2 =np.diff(Rx2) / sampleTime
    vRy2 =np.diff(Ry2) / sampleTime
    vRz2 =np.diff(Rz2) / sampleTime

    vx2 = np.insert(vx2, 0, 0)
    vy2 = np.insert(vy2 , 0, 0)
    vz2 = np.insert(vz2 , 0, 0)
    vRx2 =np.insert(vRx2, 0, 0)
    vRy2 =np.insert(vRy2, 0, 0)
    vRz2 =np.insert(vRz2, 0, 0)


    data1 = [vx1, vy1, vz1, vRx1, vRy1, vRz1, t1]
    data2 = [vx2, vy2, vz2, vRx2, vRy2, vRz2, t2]

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Volicity curve"
    xlabel = "time(s)"
    ylable = "Volicity(mm/s)"
        
    line_1_label = "Measured value"
    line_2_label = "Expect value"
        
    plot_6_chart_2curve(data1, data2, title_header, title, xlabel, ylable, line_1_label, line_2_label)

def Analyze_2curve_Acceleration(sampleTime, PoseMat_file_1, Time_file_1, PoseMat_file_2, Time_file_2):
    """Analyze 2 curve
    - Real : PoseMat_file_1、Time_file_1
    - Simulator : PoseMat_file_2、Time_file_2
    - default: t1 unit is microsecond; t2 unit is second. 
    """
    PoseMat6x1_1 = pd.read_csv(PoseMat_file_1)
    pathdata_df_1 = pd.read_csv( Time_file_1)
    PoseMat6x1_2 = pd.read_csv(PoseMat_file_2)
    pathdata_df_2 = pd.read_csv( Time_file_2)

    # data1
    x1  = []
    y1  = []
    z1  = []
    Rx1 = []
    Ry1 = []
    Rz1 = []
    t1  = []

    # data2
    x2  = []
    y2  = []
    z2  = []
    Rx2 = []
    Ry2 = []
    Rz2 = []
    t2  = []

    for i in range(len(PoseMat6x1_1)):
        x1.append( PoseMat6x1_1["X"][i])
        y1.append( PoseMat6x1_1["Y"][i]) 
        z1.append( PoseMat6x1_1["Z"][i]) 
        Rx1.append(PoseMat6x1_1["Rx"][i])
        Ry1.append(PoseMat6x1_1["Ry"][i])
        Rz1.append(PoseMat6x1_1["Rz"][i])
        t1.append(round(pathdata_df_1["time"][i]/1000000, 3))

    for i in range(len(PoseMat6x1_2)):
        x2.append( PoseMat6x1_2["X"][i])
        y2.append( PoseMat6x1_2["Y"][i]) 
        z2.append( PoseMat6x1_2["Z"][i]) 
        Rx2.append(PoseMat6x1_2["Rx"][i])
        Ry2.append(PoseMat6x1_2["Ry"][i])
        Rz2.append(PoseMat6x1_2["Rz"][i])
        t2.append(pathdata_df_2["time"][i])
    
    # 瞬時速度
    vx1 = np.diff(x1) / sampleTime
    vy1 = np.diff(y1) / sampleTime
    vz1 = np.diff(z1) / sampleTime
    vRx1 =np.diff(Rx1) / sampleTime
    vRy1 =np.diff(Ry1) / sampleTime
    vRz1 =np.diff(Rz1) / sampleTime

    vx1 = np.insert(vx1 , 0, 0)
    vy1 = np.insert(vy1 , 0, 0)
    vz1 = np.insert(vz1 , 0, 0)
    vRx1 =np.insert(vRx1, 0, 0)
    vRy1 =np.insert(vRy1, 0, 0)
    vRz1 =np.insert(vRz1, 0, 0)

     # 瞬時速度
    vx2 = np.diff(x2) / sampleTime
    vy2 = np.diff(y2) / sampleTime
    vz2 = np.diff(z2) / sampleTime
    vRx2 =np.diff(Rx2) / sampleTime
    vRy2 =np.diff(Ry2) / sampleTime
    vRz2 =np.diff(Rz2) / sampleTime

    vx2 = np.insert(vx2, 0, 0)
    vy2 = np.insert(vy2 , 0, 0)
    vz2 = np.insert(vz2 , 0, 0)
    vRx2 =np.insert(vRx2, 0, 0)
    vRy2 =np.insert(vRy2, 0, 0)
    vRz2 =np.insert(vRz2, 0, 0)

    # 算瞬時加速度
    ax1 = np.diff(vx1) / sampleTime
    ay1 = np.diff(vy1) / sampleTime
    az1 = np.diff(vz1) / sampleTime
    aRx1 =np.diff(vRx1) / sampleTime
    aRy1 =np.diff(vRy1) / sampleTime
    aRz1 =np.diff(vRz1) / sampleTime

    ax1 = np.insert(ax1, 0, 0)
    ay1 = np.insert(ay1, 0, 0)
    az1 = np.insert(az1, 0, 0)
    aRx1 =np.insert(aRx1, 0, 0)
    aRy1 =np.insert(aRy1, 0, 0)
    aRz1 =np.insert(aRz1, 0, 0)

    # 算瞬時加速度
    ax2 = np.diff(vx2) / sampleTime
    ay2 = np.diff(vy2) / sampleTime
    az2 = np.diff(vz2) / sampleTime
    aRx2 =np.diff(vRx2) / sampleTime
    aRy2 =np.diff(vRy2) / sampleTime
    aRz2 =np.diff(vRz2) / sampleTime

    ax2 = np.insert(ax2, 0, 0)
    ay2 = np.insert(ay2 , 0, 0)
    az2 = np.insert(az2 , 0, 0)
    aRx2 =np.insert(aRx2, 0, 0)
    aRy2 =np.insert(aRy2, 0, 0)
    aRz2 =np.insert(aRz2, 0, 0)


    data1 = [ax1, ay1, az1, aRx1, aRy1, aRz1, t1]
    data2 = [ax2, ay2, az2, aRx2, aRy2, aRz2, t2]

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Acceleration curve"
    xlabel = "time(s)"
    ylable = "Acceleration(mm/s²)"
        
    line_1_label = "Measured value"
    line_2_label = "Expect value"
        
    plot_6_chart_2curve(data1, data2, title_header, title, xlabel, ylable, line_1_label, line_2_label)

def Analyze_2curve_JointAngle(PoseMat_file_1, Time_file_1, PoseMat_file_2, Time_file_2):
    """Analyze 2 curve
    - Real : PoseMat_file_1、Time_file_1
    - Simulator : PoseMat_file_2、Time_file_2
    - default: t1 unit is microsecond; t2 unit is second. 
    """
    PoseMat6x1_1 = pd.read_csv(PoseMat_file_1)
    pathdata_df_1 = pd.read_csv( Time_file_1)
    PoseMat6x1_2 = pd.read_csv(PoseMat_file_2)
    pathdata_df_2 = pd.read_csv( Time_file_2)

    # data1
    S1 = []
    L1 = []
    U1 = []
    R1 = []
    B1 = []
    T1 = []
    t1 = []

    # data2
    S2 = []
    L2 = []
    U2 = []
    R2 = []
    B2 = []
    T2 = []
    t2 = []

    for i in range(len(PoseMat6x1_1)):
        S1.append( PoseMat6x1_1["X"][i])
        L1.append( PoseMat6x1_1["Y"][i]) 
        U1.append( PoseMat6x1_1["Z"][i]) 
        R1.append(PoseMat6x1_1["Rx"][i])
        B1.append(PoseMat6x1_1["Ry"][i])
        T1.append(PoseMat6x1_1["Rz"][i])
        t1.append(round(pathdata_df_1["time"][i]/1000000, 3))

    for i in range(len(PoseMat6x1_2)):
        S2.append( PoseMat6x1_2["X"][i])
        L2.append( PoseMat6x1_2["Y"][i]) 
        U2.append( PoseMat6x1_2["Z"][i]) 
        R2.append(PoseMat6x1_2["Rx"][i])
        B2.append(PoseMat6x1_2["Ry"][i])
        T2.append(PoseMat6x1_2["Rz"][i])
        t2.append(pathdata_df_2["time"][i])
    
    data1 = [S1, L1, U1, R1, B1, T1, t1]
    data2 = [S2, L2, U2, R2, B2, T2, t2]

    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "JointAngle curve"
    xlabel = "time(s)"
    ylable = "JointAngle(deg)"
        
    plot_6_chart_2curve(data1, data2, title_header, title, xlabel, ylable)

if __name__ == "__main__" :
    '''
    Pose Matrix專區
    '''
    # Matrix Planning
    # PoseMat_file = "dataBase/MatrixPathPlanning_PoseMatrix.csv"
    # Time_file = "dataBase/MatrixPathPlanning.csv"

    # Matrix Planning + 4-3-4 Trajectory 
    # PoseMat_file = "dataBase/MatrixPath434_PoseMatrix.csv"
    # Time_file = "dataBase/MatrixPath434.csv"

    # Matrix Planning + S-curve
    # PoseMat_file = "dataBase/MatrixPath_Scurve_PoseMatrix.csv"
    # Time_file = "dataBase/MatrixPath_Scurve.csv"

    PoseMat_file = "Experimental_data/20240129/13_3mms/trajectoryEL.csv"
    Time_file = "Experimental_data/20240129/13_3mms/timeEL.csv"

    Analyze_Position(PoseMat_file, Time_file)
    Analyze_Velocity(0.04, PoseMat_file, Time_file)
    Analyze_Acceleration(0.04, PoseMat_file, Time_file)

    # Real_PoseMat_file = "Experimental_data/Trajectory.csv"
    # Real_Time_file = "Experimental_data/time.csv"
    # Sim_PoseMat_file = "dataBase/MatrixPathPlanning_PoseMatrix.csv"
    # Sim_Time_file = "dataBase/MatrixPathPlanning.csv"

    # sampleTime = 0.04
    # Analyze_2curve_Position(Real_PoseMat_file, Real_Time_file, Sim_PoseMat_file, Sim_Time_file)
    # Analyze_2curve_Velocity(sampleTime, Real_PoseMat_file, Real_Time_file, Sim_PoseMat_file, Sim_Time_file)
    # Analyze_2curve_Acceleration(sampleTime, Real_PoseMat_file, Real_Time_file, Sim_PoseMat_file, Sim_Time_file)



    """
    Joint Angle專區
    """
    # Matrix Planning
    # PoseMat_file = "dataBase/MatrixPathPlanning_JointAngle.csv"
    # Time_file = "dataBase/MatrixPathPlanning.csv"

    # Matrix Planning + 4-3-4 Trajectory
    # PoseMat_file = "dataBase/MatrixPath434_JointAngle.csv"
    # Time_file = "dataBase/MatrixPath434.csv"

    # Analyze_JointAngle(PoseMat_file, Time_file)

    
