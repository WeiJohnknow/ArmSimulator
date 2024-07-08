
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from dataBase_v0 import dataBase
import os
from Toolbox import TimeTool
import time
from Matrix import Matrix4x4
from dataBase_v0 import dataBase
from sklearn.linear_model import LinearRegression
from scipy.stats import norm
from dataBase_v1 import *
from scipy.interpolate import interp1d


"""
* color:

blue - 蓝色
green - 绿色
red - 红色
cyan - 青色
magenta - 洋红色
yellow - 黄色
black - 黑色
white - 白色
orange - 橙色
purple - 紫色
brown - 棕色
pink - 粉红色
gray/grey - 灰色
turquoise - 绿松石色
gold - 金色
silver - 银色
indigo - 靛蓝色
lavender - 熏衣草色
maroon - 栗色
olive - 橄榄色
"""

def plot_6_chart_1curve(x, y, z, Rx, Ry, Rz, time, title_header, title, xlable, ylable:list):
    """畫出六張子圖，每張圖有一條曲線
    - Args: x, y, z, Rx, Ry, Rz, time, title, xlable, ylable
        - data type :list、ndarray
        - title_header : ex:[x, y, z, Rx, Ry, Rz].
        - title :子圖表標題，該曲線名稱，ex: Position curve.
            - title_header + title = "x" + "Position curve"
        - xlable :x軸標量名稱，ex :time(s).
        - ylable :y軸標量名稱，ex :Position、deg
    """

    # 图1：Px vs. time
    # plt.subplot(3, 5, 1)
    plt.subplot2grid((3, 2), (0, 0))
    plt.plot(time, x)
    plt.title(f"{title_header[0]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable[0])

    # 图2：Py vs. time
    # plt.subplot(3, 2, 2)
    plt.subplot2grid((3, 2), (1, 0))
    plt.plot(time, y)
    plt.title(f"{title_header[1]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable[0])

    # 图3：Pz vs. time
    # plt.subplot(3, 2, 3)
    plt.subplot2grid((3, 2), (2, 0))
    plt.plot(time, z)
    plt.title(f"{title_header[2]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable[0])

    # 图4：Rx vs. time
    # plt.subplot(3, 2, 4)
    plt.subplot2grid((3, 2), (0, 1))
    plt.plot(time, Rx)
    plt.title(f"{title_header[3]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable[1])

    # 图5：Ry vs. time
    # plt.subplot(3, 2, 5)
    plt.subplot2grid((3, 2), (1, 1))
    plt.plot(time, Ry)
    plt.title(f"{title_header[4]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable[1])

    # 图6：Rz vs. time
    # plt.subplot(3, 2, 6)
    plt.subplot2grid((3, 2), (2, 1))
    plt.plot(time, Rz)
    plt.title(f"{title_header[5]} {title}")
    plt.xlabel(xlable)
    plt.ylabel(ylable[1])


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

def plotMean_Std(y_data, x_data, xlabel:str, ylabel:str, title:str):
    """繪製出data的平均值(虛線)與1倍標準差範圍
    - Args:
        - y_data : 主要需要分析的資料集，dataType: ndarray，ex:Velocity
        - x_data : 該資料所對應之x軸資料，ex:時間
    """
    
    # 原數據
    mean = np.mean(y_data)
    std = np.std(y_data)

    # 繪製過濾前資料與mean、std
    plt.plot(x_data, y_data, label = ylabel[0])

    # 绘制平均值水平线
    plt.axhline(mean, color='red', linestyle='--', label='Mean')

    # 在水平线上添加平均值的数值标签
    plt.text(0, mean, f'{mean:.3f}', color='red', ha='right', va='bottom')

    # 绘制標準差  上限與下限
    plt.axhline(mean - std, color='orange', linestyle='-.', label='std')
    plt.axhline(mean + std, color='orange', linestyle='-.', label='std')

    # 添加图例和标签
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel[0])
    plt.title(title)

    # 显示图形
    plt.show()


    # # 過濾後的數據
    # # 利用一倍標準差過濾數據(會移除不符合標準之資料)
    # # filtered_data = y_data[(y_data >= mean - std) & (y_data <= mean + std)]

    # # 将大于一倍标准差的值替换为标准差的上限，将小于一倍标准差的值替换为标准差的下限
    # filtered_data = np.clip(y_data, mean - std, mean + std)

    # filtered_data_mean = np.mean(filtered_data)
    # filtered_data_std = np.std(filtered_data)

    # # 繪製過濾後的資料與其mean與std
    # # 繪製原數據
    # plt.plot(x_data, filtered_data, label = ylabel[0])

    # # 绘制過濾後平均值水平线
    # plt.axhline(filtered_data_mean, color='red', linestyle='--', label='Mean')
    # plt.text(-1, mean, f'{mean:.3f}', color='red', ha='right', va='bottom')

    # # 绘制過濾後標準差  上限與下限
    # plt.axhline(filtered_data_mean - filtered_data_std, color='orange', linestyle='-.', label='std')
    # plt.axhline(filtered_data_mean + filtered_data_std, color='orange', linestyle='-.', label='std')

    # # 添加图例和标签
    # plt.legend()
    # plt.xlabel(xlabel)
    # plt.ylabel(ylabel[0])
    # plt.title(title)

    # # 显示图形
    # plt.show()

def Experimental_data_analysis(PoseMat_file, Time_file, Time_error_file):
    """計算軌跡之歐式距離與平均速度
    - Unit:
        - distance :mm
        - sampleTime :s
        - Time_file: 依原資料之單位為主
    - 注意計算總位移與平均速度時，時間之單位
    """
    
    PoseMat6x1 = database_PoseMat.Load(PoseMat_file)
    Time = database_time.Load(Time_file)
    Time_error = database_time.Load(Time_error_file)
    

    Time = Time.reshape(-1)
    TimeErr = Time_error.reshape(-1)

    # 計算軌跡點間的歐式距離
    PtoPEuclidean_distance = np.zeros((PoseMat6x1.shape[0]-1))
    Coordinate = PoseMat6x1[:, :, :3].reshape(-1, 3)
    for i in range(Coordinate.shape[0]-1):
        PtoPEuclidean_distance[i] = np.linalg.norm(Coordinate[i+1] - Coordinate[i])
    # 插入初值 0
    PtoPEuclidean_distance = np.insert(PtoPEuclidean_distance, 0, 0)

    # 總歐式距離
    TotalEuclidean_distance = np.zeros((PoseMat6x1.shape[0]))
    for i in range(TotalEuclidean_distance.shape[0]):
        TotalEuclidean_distance[i] = TotalEuclidean_distance[i-1] + PtoPEuclidean_distance[i]

    # 每兩軌跡點間的平均速度
    TimeErrSecond = TimeErr/1000 
    PtoPavgSpeed = PtoPEuclidean_distance/TimeErrSecond
    # 找到NaN值的索引
    nan_index = np.isnan(PtoPavgSpeed)
    if nan_index[0] == True:
        PtoPavgSpeed[0] = 0

    print(f"實際速度: {np.mean(PtoPavgSpeed[np.isfinite(PtoPavgSpeed)])}")
    
    # 设置全局字体大小
    plt.rcParams.update({'font.size': 20})

    
    plt.plot(Time, TotalEuclidean_distance, color='blue', label='Euclidean distance', marker='o')
    # plt.plot(time, average_speed, color='green', label='Speed')
    plt.plot(Time, PtoPavgSpeed, color='green', label='Speed', marker='o')

    # 添加图例和标签
    plt.legend()
    plt.xlabel("time(ms)")
    plt.ylabel("Euclidean distance(mm) and speed(mm/s)")
    plt.title("Euclidean distance and speed")

    # 显示图形
    plt.show()
    
    return TotalEuclidean_distance, PtoPEuclidean_distance, PtoPavgSpeed, Time

def Analysis_ExperimentalAndExpect(Experimental_EucDis, Experimental_Speed, Experimental_Time, Expect_EucDis, Expect_Speed, Expect_Time):
    """分析實驗結果與預期之軌跡曲線
    - Unit:
        - distance :mm
        - sampleTime :s
        - Time_file: 依原資料之單位為主
    - 注意計算總位移與平均速度時，時間之單位
    """
    # 時間軸以秒為單位
    Expect_Time *= 1000

    # 繪製垂直線
    # plt.axvline(x=Expect_Time[110], color='r', linestyle='--')

    """
    兩條曲線在同一張圖內
    """
    # # 期望曲線 
    # plt.plot(Expect_Time, Expect_EucDis, color='red', label='Euclidean distance(Expected)')
    # plt.plot(Expect_Time, Expect_Speed, color='green', label='Speed(Expected)')

    # # 實驗曲線
    # plt.plot(Experimental_Time, Experimental_EucDis, color='magenta', label='Euclidean distance(Estimate)')
    # plt.plot(Experimental_Time, Experimental_Speed,  color='turquoise', label='Speed(Estimate)')

    # # 添加图例和标签
    # plt.legend()
    # plt.xlabel("time(ms)")
    # plt.ylabel("Euclidean distance(mm) and speed(mm/s)")
    # plt.title("Euclidean distance and speed")

    # # 显示图形
    # plt.show()

    """
    歐式距離與速度分張
    """


    # 期望歐式距離曲線 
    plt.plot(Expect_Time, Expect_EucDis, color='red', label='Expected')
    # 實驗得到的歐式距離曲線
    plt.plot(Experimental_Time, Experimental_EucDis, color='green', label='Estimate')


    # 開啟圖表背景格線
    plt.grid(True)

    # 添加图例和标签
    plt.legend()
    plt.xlabel("time(ms)")
    plt.ylabel("Euclidean distance(mm)")
    plt.title("Euclidean distance of robot arm TCP movement")

    # 显示图形
    plt.show()


    # 期望的速度曲線
    plt.plot(Expect_Time, Expect_Speed, color='red', label='Expected')
    # 實驗得到的速度曲線
    plt.plot(Experimental_Time, Experimental_Speed,  color='green', label='Estimate')


    # 開啟圖表背景格線
    plt.grid(True)

    # 添加图例和标签
    plt.legend()
    plt.xlabel("time(ms)")
    plt.ylabel("speed(mm/s)")
    plt.title("Robot arm TCP movement speed")

    # 显示图形
    plt.show()
    
def Expect_distance_speed(PoseMat_file, Speed_file, sampleTime):
    """計算軌跡之歐式距離與平均速度
    - Unit:
        - distance :mm
        - sampleTime :s
        - Time_file: 依原資料之單位為主
    - 注意計算總位移與平均速度時，時間之單位
    """
    PoseMat6x1 = database_PoseMat.Load(PoseMat_file)
    Speed = database_Velocity.Load(Speed_file)

    

    # 有時要-0.04 有時不用， 請多加注意
    Time = np.arange(0, (PoseMat6x1.shape[0]*sampleTime), sampleTime)
    # Time = np.arange(0, (PoseMat6x1.shape[0]*sampleTime-0.04), sampleTime)

    # 計算軌跡點間的歐式距離
    PtoPEuclidean_distance = np.zeros((PoseMat6x1.shape[0]-1))
    Coordinate = PoseMat6x1[:, :, :3].reshape(-1, 3)
    for i in range(Coordinate.shape[0]-1):
        PtoPEuclidean_distance[i] = np.linalg.norm(Coordinate[i+1] - Coordinate[i])
    # 插入初值 0
    PtoPEuclidean_distance = np.insert(PtoPEuclidean_distance, 0, 0)

    # 總歐式距離
    TotalEuclidean_distance = np.zeros((PoseMat6x1.shape[0]))
    for i in range(TotalEuclidean_distance.shape[0]):
        TotalEuclidean_distance[i] = TotalEuclidean_distance[i-1] + PtoPEuclidean_distance[i]

    # 每兩軌跡點間的平均速度
    
    timeErrSecond = sampleTime
    PtoPavgSpeed = PtoPEuclidean_distance/timeErrSecond

    # 设置全局字体大小
    plt.rcParams.update({'font.size': 20})

    # 在中位数位置绘制垂直虚线
    # plt.axvline(x=median_time_, color='orange', linestyle='--', label='Median')

    plt.plot(Time, TotalEuclidean_distance, color='blue', label='Euclidean distance')
    # plt.plot(Time, PtoPavgSpeed, color='green', label='Speed')
    plt.plot(Time, Speed, color='green', label='Speed')


    # speed_mean = np.mean(average_speed)
    # 绘制平均值水平线
    # plt.axhline(speed_mean, color='red', linestyle='--', label='Speed mean')

    # 添加图例和标签
    plt.legend()
    plt.xlabel("time(ms)")
    plt.ylabel("Euclidean distance(mm) and speed(mm/s)")
    plt.title("Euclidean distance and speed")

    # 显示图形
    plt.show()
    
    # return TotalEuclidean_distance, PtoPEuclidean_distance, PtoPavgSpeed, Time
    return TotalEuclidean_distance, PtoPEuclidean_distance, Speed, Time

def calculate_distance_speed_2_curve(PoseMat_file, Time_file, ExperimentalData, sampleTime):
    """計算軌跡之歐式距離與平均速度(2曲線)
    - Unit:
        - distance :mm
        - sampleTime :s
        - Time_file: 依原資料之單位為主
    - 注意計算總位移與平均速度時，時間之單位
    """
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv( Time_file)
    ExperimentalData = pd.read_csv( ExperimentalData)
    
    # 期望軌跡資料
    x  = np.zeros(PoseMat6x1.shape[0])
    y  = np.zeros(PoseMat6x1.shape[0])
    z  = np.zeros(PoseMat6x1.shape[0])
    Rx = np.zeros(PoseMat6x1.shape[0])
    Ry = np.zeros(PoseMat6x1.shape[0])
    Rz = np.zeros(PoseMat6x1.shape[0])
    time = np.zeros(pathdata_df.shape[0])

    # 實驗軌跡資料
    x_  = np.zeros(ExperimentalData.shape[0])
    y_  = np.zeros(ExperimentalData.shape[0])
    z_  = np.zeros(ExperimentalData.shape[0])
    Rx_ = np.zeros(ExperimentalData.shape[0])
    Ry_ = np.zeros(ExperimentalData.shape[0])
    Rz_ = np.zeros(ExperimentalData.shape[0])
    time_ = np.zeros(ExperimentalData.shape[0])
    

    for i in range(len(PoseMat6x1)):
        x[i] = PoseMat6x1["X"][i]
        y[i] = PoseMat6x1["Y"][i]
        z[i] = PoseMat6x1["Z"][i]
        Rx[i]= PoseMat6x1["Rx"][i]
        Ry[i]= PoseMat6x1["Ry"][i]
        Rz[i]= PoseMat6x1["Rz"][i]
        time[i] = pathdata_df['time'][i]

    for i in range(len(ExperimentalData)):
        x_[i] = ExperimentalData["X"][i]
        y_[i] = ExperimentalData["Y"][i]
        z_[i] = ExperimentalData["Z"][i]
        Rx_[i]= ExperimentalData["Rx"][i]
        Ry_[i]= ExperimentalData["Ry"][i]
        Rz_[i]= ExperimentalData["Rz"][i]
        time_[i] = round(ExperimentalData['time'][i]/1000,0)
        
    
    Euclidean_distance = np.zeros(PoseMat6x1.shape[0])
    average_speed = np.zeros(PoseMat6x1.shape[0])

    Euclidean_distance_ = np.zeros(ExperimentalData.shape[0])
    average_speed_ = np.zeros(ExperimentalData.shape[0])

    for i in range(PoseMat6x1.shape[0]):
        if i == 0:
            Euclidean_distance[0] = 0
        else:
            Euclidean_distance[i] = Euclidean_distance[i-1] + np.sqrt((x[i] - x[i-1])**2 + (y[i] - y[i-1])**2 + (z[i] - z[i-1])**2)
    
    for i in range(ExperimentalData.shape[0]):
        if i == 0:
            Euclidean_distance_[0] = 0
        else:
            Euclidean_distance_[i] = Euclidean_distance_[i-1] + np.sqrt((x_[i] - x_[i-1])**2 + (y_[i] - y_[i-1])**2 + (z_[i] - z_[i-1])**2)
    
    # 總位移與平均速度
    """
    注意時間單位(以秒為主)，需換算至秒
    """
    totaldistance = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2 + (z[-1] - z[0])**2)
    avgSpeed = totaldistance/(time[-1]/1000)

    totaldistance_ = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2 + (z[-1] - z[0])**2)
    avgSpeed_ = totaldistance_/(time[-1]/1000)

    print("軌跡總位移(mm) :", round(totaldistance, 3))
    print("軌跡平均速度(mm/s) :", round(avgSpeed, 3))
        
    # 瞬時速度
    average_speed = np.diff(Euclidean_distance) / sampleTime
    average_speed = np.insert(average_speed, 0, 0)

    average_speed_ = np.diff(Euclidean_distance_) / sampleTime
    average_speed_ = np.insert(average_speed_, 0, 0)

    # 计算 time 的中位数
    # median_time_ = time[-1]/2

    # 设置全局字体大小
    plt.rcParams.update({'font.size': 20})

    # 在中位数位置绘制垂直虚线
    # plt.axvline(x=median_time_, color='orange', linestyle='--', label='Median')

    # 期望曲線
    plt.plot(time, Euclidean_distance, color='red', label='Euclidean distance(Expected)')
    plt.plot(time, average_speed, color='magenta', label='Speed(Expected)')

    # 實驗曲線
    plt.plot(time_, Euclidean_distance_, color='green', label='Euclidean distance(Estimate)')
    plt.plot(time_, average_speed_, color='turquoise', label='Speed(Estimate)')

    # # 期望與實驗(實際)誤差
    # error = np.zeros((len(Euclidean_distance)))
    # for i in range(len(Euclidean_distance)):
    #     error[i] = Euclidean_distance[i] - Euclidean_distance_[i]
    # plt.plot(time, error, color='blue', label='Error')

    # speed_mean = np.mean(average_speed)
    # # 绘制平均值水平线
    # plt.axhline(speed_mean, color='red', linestyle='--', label='Speed mean')

    # 添加图例和标签
    plt.legend()
    plt.xlabel("time(s)")
    plt.ylabel("Euclidean distance(mm) and speed(mm/s)")
    plt.title("Euclidean distance and speed")

    # 显示图形
    plt.show()
    
    return Euclidean_distance, average_speed

def calculate_sampleTime(time):
    dt = np.diff(time)

    plt.plot(dt, label = "CMD time diff")
    # 绘制平均值水平线
    mean = np.mean(dt)
    plt.axhline(mean, color='red', linestyle='--', label='Mean')

    # 在水平线上添加平均值的数值标签
    plt.text(0, mean, f'{mean:.3f}', color='red', ha='right', va='bottom')
    # 添加图例和标签
    plt.legend()
    # plt.xlabel(xlabel)
    plt.ylabel("CMD time rate of change")
    plt.title("CMD time diff")

    # 显示图形
    plt.show()

    
def Analyze_Position(PoseMat_file, Time_file):
    PoseMat6x1 = pd.read_csv(PoseMat_file)
    pathdata_df = pd.read_csv( Time_file)
    x =np.zeros(PoseMat6x1.shape[0])
    y =np.zeros(PoseMat6x1.shape[0])
    z =np.zeros(PoseMat6x1.shape[0])
    Rx=np.zeros(PoseMat6x1.shape[0])
    Ry=np.zeros(PoseMat6x1.shape[0])
    Rz=np.zeros(PoseMat6x1.shape[0])
    time = np.zeros(pathdata_df.shape[0])

    for i in range(len(PoseMat6x1)):
        x[i] = PoseMat6x1["X"][i]
        y[i] = PoseMat6x1["Y"][i]
        z[i] = PoseMat6x1["Z"][i]
        Rx[i]= PoseMat6x1["Rx"][i]
        Ry[i]= PoseMat6x1["Ry"][i]
        Rz[i]= PoseMat6x1["Rz"][i]
        time[i] = pathdata_df['time'][i]
    
    
    
    title_header = ["x", "y", "z", "Rx", "Ry", "Rz"]
    title = "Position curve"
    xlabel = "time(us)"
    ylable = ["Position(mm)", "Angle(deg.)"]

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
    ylable = ["Velocity(mm/s)", "Angular velocity(deg/s)"]



    # 繪製資料總曲線圖
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
    xlabel = "time(us)"
    ylable = ["Acceleration(mm/s²)", "Angular acceleration(deg/s²)"]
    
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

def make_TimeErrorFile(Time_filePath, SaveCsv_filePath):
    """製作時間差csv檔
    """
    Time = pd.read_csv(Time_filePath)
    Time = np.array(Time).reshape(-1)
    TimeErr = np.zeros((Time.shape[0], 1))

    for i in range(Time.shape[0]):
        if i == 0:
            TimeErr[i] = Time[i]
        else:
            TimeErr[i] = Time[i] - Time[i-1] 
    
    database_time.Save(TimeErr, SaveCsv_filePath, "w")

def I000_SysTime_chart():
    data = pd.read_csv("Experimental_data/20240507/3/I0AndPrvUpdataTimeAndSysTime.csv")
    
    I0 = np.array(data["I0"])
    SysTime = np.array(data["SysTime"])

    indices = np.where((I0 == 2) | (I0 == 11))[0]

    # 设置全局字体大小
    plt.rcParams.update({'font.size': 20})

    for i, index in enumerate(indices):
        x_value = SysTime[index]
        plt.axvline(x=x_value, color='orange', linestyle='--')
        # 交替设置标签位置
        if i % 2 == 0:
            plt.text(x_value, plt.ylim()[1], f'{x_value}', verticalalignment='bottom', horizontalalignment='center', color='red', fontsize=15)
        else:
            plt.text(x_value, plt.ylim()[0], f'{x_value}', verticalalignment='center', horizontalalignment='center', color='red', fontsize=15)

    # 期望曲線 
    # plt.plot(SysTime, I0, color='red', label='Euclidean distance(Expected)', marker="o")
    plt.plot(SysTime, I0, marker="o")

    
   

    # 添加图例和标签
    plt.legend()
    plt.xlabel("Sys time(ms)")
    plt.ylabel("Variable I000")
    plt.title("Communication sequence diagram")

    # 显示图形
    plt.show()
    

  



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

    # PoseMat_file =     "dataBase/MatrixPlan434_Experimental/sampleTime_60ms_1/MatritPlan434_PoseMatrix.csv"
    # Time_file =        "dataBase/MatrixPlan434_Experimental/sampleTime_60ms_1/MatritPlan434.csv"
    # ExperimentalData = "dataBase/MatrixPlan434_Experimental/sampleTime_60ms_1/results/MatrixPlan434_Experimental_data.csv"
    # sampleTime = 0.05

    # Matrix Planning + S-curve
    # PoseMat_file = "dataBase/MatrixPath_Scurve_PoseMatrix.csv"
    # Time_file = "dataBase/MatrixPath_Scurve.csv"

    # PoseMat_file = "Experimental_data/20240129/13_3mms/trajectoryEL.csv"
    # Time_file =    "Experimental_data/20240129/13_3mms/timeEL.csv"

    # sampleTime = 0.46
    # calculate_distance_speed(PoseMat_file, Time_file, sampleTime)

    # PoseMat_file = "Experimental_data/20240306/Teach_mode_Multi_Trajectory_welding.csv"
    # Time_file =    "Experimental_data/20240129/13_3mms/timeEL.csv"
    # calculate_distance_speed(PoseMat_file, Time_file, 0.04)

    # PoseMat_file = "Experimental_data/20240429/Remix_1/testRemix_PoseMat.csv"

    # JointAngle = database_JointAngle.Load("dataBase/dynamicllyPlanTEST/JointAngle_0.csv")
    # JointAngle = np.rad2deg(JointAngle)
    # print(JointAngle)
    """
    製作通訊時序表
    """
    # I000_SysTime_chart()

    # headname = "dataBase/Experimental_data/20240702/VariableSpeed/d/"
    headname = "dataBase/dynamicllyPlanTEST/"
    Time_path =    headname+"feedbackRecords_sysTime.csv"
    TimeErr_path = headname+"feedbackRecords_sysTime_err.csv"
    # 製作時間差的csv檔
    make_TimeErrorFile(Time_path, TimeErr_path)

    # 預期資料
    Expect_PoseMat_file = headname+"mergeTrj.csv"
    Expect_Time_file =    headname+"mergeSpeed.csv"
    # Expect_PoseMat_file = headname+"PoseMat_0.csv"
    # Expect_Time_file =    headname+"mergeSpeed.csv"

    # 實驗結果資料
    Experimental_PoseMat_file =    headname+"feedbackRecords_Trj.csv"
    Experimental_Time_file =       headname+"feedbackRecords_sysTime.csv"
    Experimental_Time_error_file = headname+"feedbackRecords_sysTime_err.csv"


    # 計算理想軌跡之歐式距離與速度
    Expect_TotalEucDis, Expect_PtoPEucDis, Expect_PtoPavgSpeed, Expect_Time = Expect_distance_speed(Expect_PoseMat_file, Expect_Time_file, 0.04)
    # 計算實驗軌跡之歐式距離與速度
    Experimental_TotalEucDis, Experimental_PtoPEucDis, Experimental_PtoPavgSpeed, Experimental_Time = Experimental_data_analysis(Experimental_PoseMat_file, Experimental_Time_file, Experimental_Time_error_file)
    Analysis_ExperimentalAndExpect(Experimental_TotalEucDis, Experimental_PtoPavgSpeed, Experimental_Time, Expect_TotalEucDis, Expect_PtoPavgSpeed, Expect_Time)
    
    # Analyze_Position(PoseMat_file, Time_file)
    # Analyze_Velocity(0.04, PoseMat_file, Time_file)
    # Analyze_Acceleration(0.04, PoseMat_file, Time_file)

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

    
