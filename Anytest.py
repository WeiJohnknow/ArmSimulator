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

# # 生成三维坐标的数据
# x = np.linspace(0, 3, 100)
# y = np.linspace(0, 4, 100)
# z = np.sin(x) + np.cos(y)
#%%
# 計算速度
# # 计算变化量
# dx = np.gradient(x)
# dy = np.gradient(y)
# dz = np.gradient(z)

# # 创建 3D 图形对象
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # 绘制变化量
# ax.quiver(x, y, z, dx, dy, dz, length=0.1, normalize=True, color='b', label='Change Vector')

# # 设置图形属性
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('3D Change Vector')
# ax.legend()

# # 显示图形
# plt.show()

#%%
# # 畫出Rotaion變化
# Mat=Matrix4x4()
# databuffer = pd.read_csv("dataBase\MatrixPathPlanning.csv")
# dataShape = databuffer.shape
# pathData = np.zeros((dataShape[0], 4, 4))
# PoseMat = np.zeros((dataShape[0], 6))
# for layer in range(dataShape[0]):
#     pathData[layer,0,0] = databuffer['Xx'][layer]
#     pathData[layer,1,0] = databuffer['Xy'][layer]
#     pathData[layer,2,0] = databuffer['Xz'][layer]
#     pathData[layer,3,0] = 0
#     pathData[layer,0,1] = databuffer['Yx'][layer]
#     pathData[layer,1,1] = databuffer['Yy'][layer]
#     pathData[layer,2,1] = databuffer['Yz'][layer]
#     pathData[layer,3,1] = 0
#     pathData[layer,0,2] = databuffer['Zx'][layer]
#     pathData[layer,1,2] = databuffer['Zy'][layer]
#     pathData[layer,2,2] = databuffer['Zz'][layer]
#     pathData[layer,3,2] = 0
#     pathData[layer,0,3] = databuffer['Px'][layer]
#     pathData[layer,1,3] = databuffer['Py'][layer]
#     pathData[layer,2,3] = databuffer['Pz'][layer]
#     pathData[layer,3,3] = 1
#     PoseMat[layer] = Mat.MatToAngle(pathData[layer])
# Rx = [0]
# Ry = [0]
# Rz = [0]
# for i in range(PoseMat.shape[0]):
#     Rx.append(PoseMat[i][3])
#     Ry.append(PoseMat[i][4])
#     Rz.append(PoseMat[i][5])
# Rx_err = [Rx[i+1] - Rx[i] for i in range(len(Rx)-1)]
# Ry_err = [Ry[i+1] - Ry[i] for i in range(len(Ry)-1)]
# Rz_err = [Rz[i+1] - Rz[i] for i in range(len(Rz)-1)]

# # 绘制三张图
# plt.figure(figsize=(10, 6))

# # 图1：Px vs. time
# plt.subplot(3, 1, 1)
# plt.plot(databuffer['time'], Rx_err)
# plt.title('x Angular velocity curve')
# plt.xlabel('time(s)')
# plt.ylabel('Angular velocity(rad/s)')

# # 图2：Py vs. time
# plt.subplot(3, 1, 2)
# plt.plot(databuffer['time'], Ry_err)
# plt.title('y Angular velocity curve')
# plt.xlabel('time(s)')
# plt.ylabel('Angular velocity(rad/s)')

# # 图3：Pz vs. time
# plt.subplot(3, 1, 3)
# plt.plot(databuffer['time'], Rz_err)
# plt.title('z Angular velocity curve')
# plt.xlabel('time(s)')
# plt.ylabel('Angular velocity(rad/s)')

# # 调整布局
# plt.tight_layout()

# # 显示图形
# plt.show()
#%%

# # 畫出軌跡曲線
# # df = dataBase().Load("dataBase\MatrixPathPlanning.csv")
# df = pd.read_csv("dataBase\MatrixPathPlanning.csv")
# Px =[]
# Py=[]
# Pz=[]
# t=[]
# data = {'Px': Px,
#         'Py': Py,
#         'Pz': Pz,
#         'time': t}

# for i in range(df.shape[0]):
#     Px.append(df['Px'][i])
#     Py.append(df['Py'][i])
#     Pz.append(df['Pz'][i])
#     t.append(df['time'][i])


# # 绘制三张图
# plt.figure(figsize=(10, 6))

# # 图1：Px vs. time
# plt.subplot(3, 1, 1)
# plt.plot(data['time'], data['Px'])
# plt.title('Px vs. time')
# plt.xlabel('time')
# plt.ylabel('Px')

# # 图2：Py vs. time
# plt.subplot(3, 1, 2)
# plt.plot(data['time'], data['Py'])
# plt.title('Py vs. time')
# plt.xlabel('time')
# plt.ylabel('Py')

# # 图3：Pz vs. time
# plt.subplot(3, 1, 3)
# plt.plot(data['time'], data['Pz'])
# plt.title('Pz vs. time')
# plt.xlabel('time')
# plt.ylabel('Pz')

# # 调整布局
# plt.tight_layout()

# # 显示图形
# plt.show()
#%%
# # 算瞬時速率
# # 讀取 CSV 檔案
# df = pd.read_csv("dataBase\MatrixPathPlanning.csv")

# # 計算 x 方向上的速度並新增一個 "x速度" 欄位
# # df['Vx'] = df['Px'].diff() 
# Vx =[]
# t = []
# # Vx = np.gradient(round(df['Py'], 3))
# Vx = df['Pz'].diff().values

# # 將單位由公尺 換 毫米
# df[['Px', 'Py', 'Pz']] *= 100
# print(df[['Px', 'Py', 'Pz']])
# Vxyz = np.linalg.norm(df[['Px', 'Py', 'Pz']].diff().values, axis=1)
# # print(Vxyz)
# Vxyz = np.round(Vxyz, 3)

# # 繪製 x 方向上的速度曲線
# plt.plot(df['time'], Vxyz)
# plt.xlabel('time(s)')
# plt.ylabel('Velocity(mm/s)')
# plt.title('speed curve')
# plt.show()

# Ans = 30*10**(-12)+3.607564968
# print(Ans)
#%%

# 算平均速率
# 計算每點的平均速度並新增一個 "平均速度" 欄位
# df['Avg_velocity'] = np.nan
# df['Avg_velocity'][1:] = np.linalg.norm(df[['Px']].diff().values, axis=1) / df['time'][1:]

# # 繪製平均速度曲線
# plt.plot(df['time'], df['Avg_velocity'], marker='o')
# plt.xlabel('time')
# plt.ylabel('Avg_velocity')
# plt.title('Avg velocity')
# plt.show()

# 三維空間算距離
# now = np.array([4.85, 0, 2.34])
# goal = np.array([9, -4, -2])

# # 計算移動距離
# distance = np.linalg.norm(goal - now)
# print(round(distance,3))
#%%
# 計算三維空間兩點距離並加入時間 算速度
# # 两个点的坐标
# point1 = (4.85, 0, 2.34)
# point2 = (4.87075, -0.02, 2.3183)

# # 计算距离
# distance = np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)

# # 输出距离
# print(f"The distance between the two points is: {distance}")
# v = round((distance*1000)/0.03, 3)
# print("速度",v,"mm/s")
#%%
# IO_NO = 999
# number_hex = hex(IO_NO)

# # 移除 '0x' 前綴並填充零，確保至少有兩個字元
# number_hex = number_hex[2:].zfill(4)

# # 將十六進位表示法分為高位元和低位元
# high_byte_hex = number_hex[:2]
# low_byte_hex = number_hex[2:]

# print("高位元:", high_byte_hex)
# print("低位元:", low_byte_hex)
#%%
# decimal_number = 999

# # 轉換為十六進制表示法
# hex_representation = hex(decimal_number)

# # 移除 '0x' 前綴並填充零，確保至少有三個字元
# hex_representation = hex_representation[2:].zfill(3)

# # 拆分成 12 位的高位元和低位元
# high_bits = int(hex_representation[:-1], 16)  # 取出除最後一個字元的部分
# low_bits = int(hex_representation[-1], 16)  # 取出最後一個字元

# print("高位元:", hex(high_bits))
# print("低位元:", hex(low_bits))
# %%
# io2511 = [[32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [96], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32], [32]]
# io3511 = [[64], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [1], [1], [1], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [3], [1], [1], [1], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [65], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [64], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [65], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]

# # 起弧成功
# io2511 = [64, 65, 65, 65, 65, 65, 65, 65, 65, 65
#           , 65, 0, 0, 0, 0, 0, 0, 0, 0, 0
#           , 0, 0, 0, 0, 0, 1, 1, 1, 1, 3
#           , 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
#           , 3, 1, 1, 1, 64, 64, 64, 64, 64, 64
#           , 64, 64, 64, 64, 64, 64, 65, 64, 64, 64
#           , 64, 64, 64, 64, 64, 64, 64, 64, 64, 64
#           , 65, 65, 65, 65, 65, 65, 65, 65, 65, 65
#           , 65, 65, 65, 65, 65, 65, 65, 65, 65, 65
#           , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# io3511 = [64, 65, 65, 65, 65, 65, 65, 65, 65, 65
#           , 65, 65, 65, 0, 0, 0, 0, 0, 0, 0
#           , 0, 0, 2, 2, 2, 2, 2, 2, 2, 2
#           , 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
#           , 3, 3, 3, 3, 3, 3, 3, 3, 3, 3
#           , 3, 3, 3, 3, 3, 3, 3, 66, 66, 66
#           , 66, 66, 66, 66, 66, 67, 67, 67, 67, 67
#           , 67, 67, 67, 67, 67, 67, 67, 67, 2, 2
#           , 2, 2, 2, 2, 2, 2, 2, 3, 3, 3
#           , 3, 3, 3, 1, 1, 1, 1, 1, 1, 64]


# df = pd.DataFrame(columns=['io_3511', "io_2511"])

# # 將列表資料添加到 DataFrame
# df['io_3511'] = io3511
# df['io_2511'] = io2511

# # 寫入 CSV 文件
# csv_filename = "dataBase/io_data_1.csv"
# df.to_csv(csv_filename, index=False)
#%%
# Time = TimeTool()
# tb = Time.ReadNowTime()
# time.sleep(0.03)
# ta = Time.ReadNowTime()
# err = Time.TimeError(tb, ta)
# print(err)
#%%
# start_time = time.time()

# while time.time() - start_time < 6:
#     # 列印數字 1
#     print(1)

#     # 等待 0.03 秒
#     time.sleep(0.03)

#%%
# import keyboard

# while True:
#     try:
#         # 检测是否按下 'esc' 键
#         if keyboard.is_pressed('esc'):
#             print('You pressed "ESC". Exiting...')
#             break
#         print("Pass")
#         # 在这里添加其他键盘事件的检测
#     except KeyboardInterrupt:
#         break
#%%
# from PathPlanning import PathPlanning
# from Matrix import Matrix4x4
# from dataBase import dataBase
# from Toolbox import TimeTool
# from Kinematics import Kinematics
# import time

# Plan = PathPlanning()
# Mat = Matrix4x4()
# dB = dataBase()
# Time = TimeTool()
# Kin = Kinematics()

# d2r = np.deg2rad
# r2d = np.rad2deg

# NowEnd = np.eye(4)  
# GoalEnd = np.eye(4)

# """
# weldstart = [955.410, -102.226, -166.726, -165.2919, -7.1991, 17.5642]
# weldend = [955.404, 14.865, -166.749, -165.2902, -7.1958, 17.5569]
# """

# NowEnd = NowEnd @ Mat.TransXYZ(4.85,0,2.34) @ Mat.RotaXYZ(d2r(-180), d2r(20.2111), d2r(21.6879))
# GoalEnd = GoalEnd @ Mat.TransXYZ(9,-4,z=-2) @ Mat.RotaXYZ(d2r(-165.2922), d2r(-7.1994), d2r(17.5635))   

# # 矩陣差值法
# alltime = 6
# sampleTime = 0.03
# startTime = 0
# PosBuffer4X4 = Plan.MatrixPathPlanning("dataBase/test.csv", GoalEnd, NowEnd, alltime, startTime, sampleTime)


# # 由資料庫取得路徑資訊
# path_dict_4X4, path_df_4X4, path_np_4X4, path_np_6X1 = dB.LoadMatrix4x4("dataBase/test.csv")
# dB.Save(path_np_6X1, 0, "dataBase/test_PoseMatrix.csv")

# # # 轉換 pose matrix (6*1)d
# # test = Mat.MatToAngle(path_np_4X4[0]) 
# # print(test)

# # IK : coordinate To Joint angle
# NowJA = np.zeros((6, 1))
# JointAngle = np.zeros((len(path_np_4X4), 6, 1))
# for i in range(len(path_np_4X4)):
#     JointAngle[i] = Kin.IK_4x4(path_np_4X4[i], NowJA) 
# dB.Save(JointAngle, 0, "dataBase/test_JointAngle.csv")
# print("test") 

# # main
# startTime = Time.ReadNowTime()
# startNode = 0
# while True:
#     nowTime = Time.ReadNowTime()
#     Systime, node =  Time.sysTime(startTime, startNode, nowTime, sampleTime)

#     if node >= len(pathData):
#         print("軌跡完成，總花費時間: ", Systime/(1000*1000), "s")
#         break

#     cmd = pathData[node]
#     print("Now cmd pos: ", cmd)




#%%
# import pandas as pd

# # 创建一个DataFrame
# data = {'Name': ['Alice', 'Bob', 'Charlie'],
#         'Age': [25, 30, 35],
#         'City': ['New York', 'San Francisco', 'Los Angeles']}
# df = pd.DataFrame(data)

# # 将DataFrame写入CSV文件
# csv_file_path = 'dataBase/test.csv'
# df.to_csv(csv_file_path, index=False)
# # print(f'DataFrame saved to {csv_file_path}')

# # 从CSV文件读取DataFrame
# read_df = pd.read_csv(csv_file_path)
# # print('\nDataFrame read from CSV:')
# print(read_df)

# # df.loc[row_label, column_label]
# # df.iloc[row_index, column_index]

# df利用某個col(label)的值，找出該值整個row的值
# selected_rows = df[df['City'] == 'New York']

#%%
# try:
#     # Code that might raise an exception
#     while True:
#         x = int(input("Enter a number: "))
#         result = 10 / x
#         print("Result:", result)

# except Exception as e:
#     # Handle any type of exception
#     print(f"An error occurred: {e}")

# else:
#     # This block is executed if no exception occurs
#     print("No exceptions occurred.")

# finally:
#     # This block is always executed, regardless of whether an exception occurred or not
#     print("Finally block: This will always be executed.")
#%%
# x = [0, 3]
# ans = np.diff(x)/0.03
# Ans = x[1] - x[0]/0.03


# np.sin()
# import sympy as sp

# # 假设 t 是时间符号，x 是位置函数关于 t 的表达式
# t = sp.symbols('t')
# x = 3

# # 计算位置函数关于时间 t 的导数，即瞬时速度
# velocity = sp.diff(x, t)

# # 将速度函数转换为可调用的 Lambda 函数
# velocity_function = sp.lambdify(t, velocity, 'numpy')

# # 假设有一个时间点 t_value，你可以使用以下方式计算在该时间点的瞬时速度
# t_value = 0.03  # 例如，时间点为2秒
# instantaneous_speed = velocity_function(t_value)

# print(f"The instantaneous speed at t = {t_value} is {instantaneous_speed}")

# # diff測試
# t = np.linspace(0, 3, 1000)  # 从0到3秒，生成1000个时间点
# x = np.sin(2 * np.pi * t)  # sin函数作为位置函数
# # x = np.insert(x, 0, 0)
# v = np.diff(x)
# v = np.insert(v, 0, 0)
# a = np.diff(v)
# a = np.insert(a, 0, 0)
# plt. plot(t, x)
# plt. plot(t, v)
# plt. plot(t, a)
# plt.show()



#%%
"""Dynamically draw curves 
"""
# x = []
# y = []  
# fig, ax = plt.subplots()
# for i in range(50):
#     x.append(i)
#     y.append(i/5)

#     # 清除資料
#     ax.cla()
#     ax.plot(x, y, "r", lw=1)

#     # 暫停更新XX秒
#     plt.pause(0.03)
# plt.show()

"""
Dynamically draw curves(增量式)
1. while loop版本
2. for loop版本
"""

# # 迭代次數
# iter = 100
# NowPos = 0

# # Data buffer
# posBuffer = np.zeros((iter))
# t = np.linspace(0, iter, iter)

# # 繪圖設定
# fig, ax = plt.subplots()

# # Initialize lines
# line,  = ax.plot([], [], label='Curve')

# # Set legend for the first time
# ax.legend()

# # 產生資料集
# for i in range(iter):
#     NowPos += 2*i+1
#     posBuffer[i] = NowPos

# """
# while loop ver.
# """
# loopIter = 0
# while True:
#     if loopIter == len(posBuffer)+1:
#         break
#     # 增量式繪圖(速度較快)
#     line.set_data(t[:loopIter+1], posBuffer[:loopIter+1])

#     # Update plot without clearing
#     ax.set_xlim(0, iter)  # Ensure correct x-axis range
#     ax.set_ylim(min(posBuffer) - 5, max(posBuffer) + 5)  # Adjust y-axis range
    
#     # Update plot without clearing
#     ax.set_title('Dynamic Curve')

#     # 調整圖間距
#     fig.subplots_adjust(hspace=0.4)

#     plt.draw()
#     plt.pause(0.03)
#     loopIter += 1
# plt.show()

# """
# for loop ver.
# """
# # for loopIter in range(iter):
    
# #     # 增量式繪圖(速度較快)
# #     line.set_data(t[:loopIter+1], posBuffer[:loopIter+1])

# #     # Update plot without clearing
# #     ax.set_xlim(0, iter)  # Ensure correct x-axis range
# #     ax.set_ylim(min(posBuffer) - 5, max(posBuffer) + 5)  # Adjust y-axis range
    
# #     # Update plot without clearing
# #     ax.set_title('Dynamic Curve')

# #     # 調整圖間距
# #     fig.subplots_adjust(hspace=0.4)

# #     plt.draw()
# #     plt.pause(0.03)
    
# # plt.show()
"""
一張圖同時畫六條曲線
"""
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.animation import FuncAnimation

# # 迭代次數
# iter = 100
# NowPos1 = 0
# NowPos2 = 0
# NowPos3 = 0
# NowPos4 = 0
# NowPos5 = 0
# NowPos6 = 0

# # Data buffer
# posBuffer = np.zeros((iter, 6))
# t = np.linspace(0, iter, iter)

# # Curve name
# name = ['S', 'L', 'U', 'R', 'B', 'T']

# # 繪圖設定
# fig, ax = plt.subplots()

# # Initialize lines with color and label
# lines = [ax.plot([], [], label=f'{name[i]} Joint Angle')[0] for i in range(6)]

# # Set legend for the first time
# ax.legend()

# # 產生資料集
# for i in range(iter):
#     NowPos1 += 2*i
#     NowPos2 += 2*i+5
#     NowPos3 += 2*i+10
#     NowPos4 += 2*i+15
#     NowPos5 += 2*i+20
#     NowPos6 += 2*i+25
    
#     posBuffer[i, 0] = NowPos1 
#     posBuffer[i, 1] = NowPos2
#     posBuffer[i, 2] = NowPos3
#     posBuffer[i, 3] = NowPos4
#     posBuffer[i, 4] = NowPos5
#     posBuffer[i, 5] = NowPos6

# # 更新函数
# def update(frame):
#     for i in range(6):
#         lines[i].set_data(t[:frame], posBuffer[:frame, i])

#     ax.set_xlim(0, iter)  # Ensure correct x-axis range
#     ax.set_ylim(posBuffer.min(), posBuffer.max())  # Adjust y-axis range
#     ax.set_title('Dynamic Curves')
#     fig.subplots_adjust(hspace=0.4)
#     return lines

# # 创建动画对象
# ani = FuncAnimation(fig, update, frames=range(1, iter+1), blit=True)

# plt.show()
"""
同時畫六張圖 一張圖一條曲線
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from dataBase import dataBase



dB = dataBase()
JointAngleData, JDnp = dB.LoadJointAngle("dataBase/MatrixPathPlanning_JointAngle.csv")



# 曲线名称
name = ['S', 'L', 'U', 'R', 'B', 'T']

# 繪圖設定
fig, axs = plt.subplots(3, 2, figsize=(6, 10))  # 2行3列的子图布局
fig.suptitle('Dynamic Curves')

# 初始化六条曲线
lines = [axs[i // 2, i % 2].plot([], [], label=f'{name[i]} Axis Angle')[0] for i in range(6)]

# Set legend for the first time
for ax in axs.flat:
    ax.legend()

t = np.linspace(0, len(JointAngleData), len(JointAngleData))

# 初始y轴范围
y_axis_ranges = [(min(JDnp[i]), max(JDnp[i])) for i in range(6)]

# 更新函数
def update(frame):
    for i, ax in enumerate(axs.flat):
        line = lines[i]
        line.set_data(t[:frame], JDnp[i, :frame])
        ax.set_xlim(0, len(t)+1)
        ax.set_ylim(y_axis_ranges[i])
        ax.set_title(f'{name[i]}Axis Angle')

    fig.subplots_adjust(hspace=0.4, wspace=0.3)
    return lines

# 创建动画对象
ani = FuncAnimation(fig, update, frames=range(1, len(t)+1, 10), blit=True)

plt.show()

# # 迭代次數
# iter = 100
# NowPos1 = 0
# NowPos2 = 0
# NowPos3 = 0
# NowPos4 = 0
# NowPos5 = 0
# NowPos6 = 0

# # Data buffer
# posBuffer = np.zeros((iter, 6))
# t = np.linspace(0, iter, iter)

# # 曲线名称
# name = ['S', 'L', 'U', 'R', 'B', 'T']

# # 繪圖設定
# fig, axs = plt.subplots(3, 2, figsize=(6, 10))  # 2行3列的子图布局
# fig.suptitle('Dynamic Curves')

# # 初始化六条曲线
# lines = [axs[i // 2, i % 2].plot([], [], label=f'Curve {name[i]}')[0] for i in range(6)]

# # Set legend for the first time
# for ax in axs.flat:
#     ax.legend()

# # 產生資料集
# for i in range(iter):
#     NowPos1 += 1*i
#     NowPos2 += -1.5*i
#     NowPos3 += 2*i
#     NowPos4 += -2.5*i
#     NowPos5 += 3*i
#     NowPos6 += -3.5*i
    
#     posBuffer[i, 0] = NowPos1 
#     posBuffer[i, 1] = NowPos2
#     posBuffer[i, 2] = NowPos3
#     posBuffer[i, 3] = NowPos4
#     posBuffer[i, 4] = NowPos5
#     posBuffer[i, 5] = NowPos6

# # 初始y轴范围
# y_axis_ranges = [(min(posBuffer[i]), max(posBuffer[i])) for i in range(100)]

# # 更新函数
# def update(frame):
#     for i, ax in enumerate(axs.flat):
#         line = lines[i]
#         line.set_data(t[:frame], posBuffer[:frame, i])
#         ax.set_xlim(0, iter)
#         ax.set_ylim(posBuffer.min(), posBuffer.max())
#         ax.set_title(f'Curve {name[i]}')

#     fig.subplots_adjust(hspace=0.4, wspace=0.3)
#     return lines

# # 创建动画对象
# ani = FuncAnimation(fig, update, frames=range(1, iter+1), blit=True)

# plt.show()


#%%
"""
Python Keyboard events
"""
# import keyboard
# import time

# while True:
#     if keyboard.is_pressed('esc'):
#         print('You pressed "ESC". Exiting...')
#         break  # 跳出無窮迴圈
#     if keyboard.is_pressed('q') and not q_pressed:
#         print('You pressed "q"')
#         q_pressed = True
#         # 在這裡加入相應的動作
#     elif not keyboard.is_pressed('q'):
#         q_pressed = False

#     time.sleep(0.01)
#%%
"""OpenCV Keyboard events
"""
# import cv2

# # 創建一個空視窗
# cv2.namedWindow('Empty Window')

# while True:
#     # 等待鍵盤事件，並取得按下的鍵
#     key = cv2.waitKey(1) & 0xFF

#     # 檢查按下的鍵
#     if key == 27:  # 27是'ESC'鍵的ASCII碼
#         print('You pressed "ESC". Exiting...')
#         break
#     elif key == ord('q'):
#         print('You pressed "q"')
#         # 在這裡加入相應的動作
#     elif key == ord('r'):
#         print('You pressed "r"')
#         # 在這裡加入相應的動作

# # 釋放資源
# cv2.destroyAllWindows()
#%%
"""
linear regression mothod 1
"""
# import numpy as np
# import matplotlib.pyplot as plt

# # 生成一些示例資料
# np.random.seed(42)
# x = 2 * np.random.rand(100, 1)
# y = 4 + 3 * x + np.random.randn(100, 1)

# # 添加一列全為1的特徵，以便包含截距
# X_b = np.c_[np.ones((100, 1)), x]

# # 使用最小二乘法計算斜率和截距
# theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

# # 獲取斜率和截距
# slope = theta_best[1][0]
# intercept = theta_best[0][0]

# # 顯示結果
# print(f"斜率：{slope}")
# print(f"截距：{intercept}")

# # 繪製散點圖和擬和線
# plt.scatter(x, y, color='blue', label='數據點')
# plt.plot(x, X_b.dot(theta_best), color='red', linewidth=3, label='擬和線')
# plt.xlabel('X軸')
# plt.ylabel('Y軸')
# plt.legend()
# plt.show()

"""
linear regression mothod 2
"""
# import numpy as np
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt

# # 生成一些示例資料
# np.random.seed(42)
# x = 2 * np.random.rand(100, 1)
# y = 4 + 3 * x + np.random.randn(100, 1)

# # 初始化線性回歸模型
# model = LinearRegression()

# # 適應模型
# model.fit(x, y)

# # 獲取斜率和截距
# slope = model.coef_[0][0]
# intercept = model.intercept_[0]

# # 顯示結果
# print(f"斜率：{slope}")
# print(f"截距：{intercept}")

# # 繪製散點圖和擬和線
# plt.scatter(x, y, color='blue', label='數據點')
# plt.plot(x, model.predict(x), color='red', linewidth=3, label='擬和線')
# plt.xlabel('X軸')
# plt.ylabel('Y軸')
# plt.legend()
# plt.show()
#%%
"""
Polynomial regression
"""
# import numpy as np
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt

# # 生成一些示例資料
# np.random.seed(42)
# x = 2 * np.random.rand(100, 1)
# y = 4 + 3 * x + 1.5 * x**2 + 4*x*3 + np.random.randn(100, 1)

# # 轉換特徵矩陣，添加多項式項
# poly_features = PolynomialFeatures(degree=2, include_bias=False)
# X_poly = poly_features.fit_transform(x)

# # 初始化線性回歸模型
# model = LinearRegression()

# # 適應模型
# model.fit(X_poly, y)

# # 繪製散點圖和多項式擬和線
# x_new = np.linspace(0, 2, 100).reshape(-1, 1)
# X_new_poly = poly_features.transform(x_new)
# y_new = model.predict(X_new_poly)

# plt.scatter(x, y, color='blue', label='數據點')
# plt.plot(x_new, y_new, color='red', label='多項式擬和線')
# plt.xlabel('X軸')
# plt.ylabel('Y軸')
# plt.legend()
# plt.show()
#%%
"""
多項式求值 numpy版本
"""
# import numpy as np

# # 定義多項式的係數
# coefficients = [1, 2]

# # 定義 u 的值
# u_values = [0,1,2]  # 使用200個點以獲得光滑的曲線，你可以根據需要調整點的數量

# # 使用 polyval 函數求值
# polynomial_values = np.polyval(coefficients, u_values)

# # 繪製多項式曲線
# plt.plot(u_values, polynomial_values, label='Polynomial: $10 + 11u + 12u^2 + 13u^3 + 14u^4$')
# plt.xlabel('u')
# plt.ylabel('Polynomial Value')
# plt.title('Plot of the Polynomial')
# plt.legend()
# plt.grid(True)
# plt.show()

