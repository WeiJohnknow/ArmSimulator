import matplotlib.pyplot as plt
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

dB = dataBase()

def Analyze_Position(PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv( Time_file)
    x=[]
    y=[]
    z=[]
    Rx=[]
    Ry=[]
    Rz=[]
    for i in range(len(PoseMat6x1)):
        x.append(PoseMat6x1["X"][i])
        y.append(PoseMat6x1["Y"][i])
        z.append(PoseMat6x1["Z"][i])
        Rx.append(PoseMat6x1["Rx"][i])
        Ry.append(PoseMat6x1["Ry"][i])
        Rz.append(PoseMat6x1["Rz"][i])

    # 图1：Px vs. time
    # plt.subplot(3, 2, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(pathdata_df['time'], x)
    plt.title('x Position curve')
    plt.xlabel('time(s)')
    plt.ylabel('Position(m)')

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(pathdata_df['time'], y)
    plt.title('y Position curve')
    plt.xlabel('time(s)')
    plt.ylabel('Position(m)')

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(pathdata_df['time'], z)
    plt.title('z Position curve')
    plt.xlabel('time(s)')
    plt.ylabel('Position(m)')

    # 图4：Px vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(pathdata_df['time'], Rx)
    plt.title('x Angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(deg)')

    # 图5：Py vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(pathdata_df['time'], Ry)
    plt.title('y Angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(deg)')

    # 图6：Pz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(pathdata_df['time'], Rz)
    plt.title('z Angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(deg)')


    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()


def Analyze_Velocity(sampleTime, PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv(Time_file)
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
        x.append(PoseMat6x1["X"][i])
        y.append(PoseMat6x1["Y"][i])
        z.append(PoseMat6x1["Z"][i])
        Rx.append(PoseMat6x1["Rx"][i])
        Ry.append(PoseMat6x1["Ry"][i])
        Rz.append(PoseMat6x1["Rz"][i])

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
    
    # 图1：Px vs. time
    # plt.subplot(3, 2, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(pathdata_df['time'], vx)
    plt.title('x Velocity curve')
    plt.xlabel('time(s)')
    plt.ylabel('Velocity(m/s)')

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(pathdata_df['time'], vy)
    plt.title('y Velocity curve')
    plt.xlabel('time(s)')
    plt.ylabel('Velocity(m/s)')

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(pathdata_df['time'], vz)
    plt.title('z Velocity curve')
    plt.xlabel('time(s)')
    plt.ylabel('Velocity(m/s)')

    # 图4：Px vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(pathdata_df['time'], vRx)
    plt.title('x Angular velocity curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angular velocity(deg/s)')

    # 图5：Py vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(pathdata_df['time'], vRy)
    plt.title('y Angular velocity curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angular velocity(deg/s)')

    # 图6：Pz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(pathdata_df['time'], vRz)
    plt.title('z Angular velocity curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angular velocity(deg/s)')


    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()

def Analyze_Acceleration(sampleTime, PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv(Time_file)
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
    
    # 图1：Px vs. time
    # plt.subplot(3, 2, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(pathdata_df['time'], ax)
    plt.title('x Acceleration curve')
    plt.xlabel('time(s)')
    plt.ylabel('Acceleration(m/s²)')

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(pathdata_df['time'], ay)
    plt.title('y Acceleration curve')
    plt.xlabel('time(s)')
    plt.ylabel('Acceleration(m/s²)')

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(pathdata_df['time'], az)
    plt.title('z Acceleration curve')
    plt.xlabel('time(s)')
    plt.ylabel('Acceleration(m/s²)')

    # 图4：Px vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(pathdata_df['time'], aRx)
    plt.title('x Angular Acceleration curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angular Acceleration(deg/s²)')

    # 图5：Py vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(pathdata_df['time'], aRy)
    plt.title('y Angular Acceleration curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angular Acceleration(deg/s²)')

    # 图6：Pz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(pathdata_df['time'], aRz)
    plt.title('z Angular Acceleration curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angular Acceleration(deg/s²)')


    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()


def Analyze_JointAngle(PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv( Time_file)
    S=[]
    L=[]
    U=[]
    R=[]
    B=[]
    T=[]
    for i in range(len(PoseMat6x1)):
        S.append(PoseMat6x1["S"][i])
        L.append(PoseMat6x1["L"][i])
        U.append(PoseMat6x1["U"][i])
        R.append(PoseMat6x1["R"][i])
        B.append(PoseMat6x1["B"][i])
        T.append(PoseMat6x1["T"][i])

    # 图1：Px vs. time
    # plt.subplot(3, 2, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(pathdata_df['time'], S)
    plt.title('S axis motor angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(rad)')

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(pathdata_df['time'], L)
    plt.title('L asix motor angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(rad)')

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(pathdata_df['time'], U)
    plt.title('U axis motor angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(rad)')

    # 图4：Px vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(pathdata_df['time'], R)
    plt.title('R axis motor angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(rad)')

    # 图5：Py vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(pathdata_df['time'], B)
    plt.title('B axis motor angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(rad)')

    # 图6：Pz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(pathdata_df['time'], T)
    plt.title('T axis motor angle curve')
    plt.xlabel('time(s)')
    plt.ylabel('Angle(rad)')


    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()

if __name__ == "__main__" :
    # PoseMat_file = "dataBase/MatrixPathPlanning_PoseMatrix.csv"
    # Time_file = "dataBase/MatrixPathPlanning.csv"

    PoseMat_file = "dataBase/MatrixPath434_PoseMatrix.csv"
    Time_file = "dataBase/MatrixPath434.csv"

    # PoseMat_file = "dataBase/MatrixPathPlanning_JointAngle.csv"
    # Time_file = "dataBase/MatrixPathPlanning.csv"

    # PoseMat_file = "dataBase/MatrixPath434_JointAngle.csv"
    # Time_file = "dataBase/MatrixPath434.csv"

    # Analyze_JointAngle(PoseMat_file, Time_file)

    Analyze_Position(PoseMat_file, Time_file)
    Analyze_Velocity(0.03, PoseMat_file, Time_file)
    Analyze_Acceleration(0.03, PoseMat_file, Time_file)
