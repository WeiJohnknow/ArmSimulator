import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataBase_v0 import dataBase
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

# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.animation import FuncAnimation
# from dataBase import dataBase



# dB = dataBase()
# JointAngleData, JDnp = dB.LoadJointAngle("dataBase/MatrixPathPlanning_JointAngle.csv")



# # 曲线名称
# name = ['S', 'L', 'U', 'R', 'B', 'T']

# # 繪圖設定
# fig, axs = plt.subplots(3, 2, figsize=(6, 10))  # 2行3列的子图布局
# fig.suptitle('Dynamic Curves')

# # 初始化六条曲线
# lines = [axs[i // 2, i % 2].plot([], [], label=f'{name[i]} Axis Angle')[0] for i in range(6)]

# # Set legend for the first time
# for ax in axs.flat:
#     ax.legend()

# t = np.linspace(0, len(JointAngleData), len(JointAngleData))

# # 初始y轴范围
# y_axis_ranges = [(min(JDnp[i]), max(JDnp[i])) for i in range(6)]

# # 更新函数
# def update(frame):
#     for i, ax in enumerate(axs.flat):
#         line = lines[i]
#         line.set_data(t[:frame], JDnp[i, :frame])
#         ax.set_xlim(0, len(t)+1)
#         ax.set_ylim(y_axis_ranges[i])
#         ax.set_title(f'{name[i]}Axis Angle')

#     fig.subplots_adjust(hspace=0.4, wspace=0.3)
#     return lines

# # 创建动画对象
# ani = FuncAnimation(fig, update, frames=range(1, len(t)+1, 10), blit=True)

# plt.show()

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

# import cv2

# # 創建VideoCapture對象，0表示默認的攝影機（第一個可用的USB攝影機）
# cap = cv2.VideoCapture(0)

# # 檢查攝影機是否成功打開
# if not cap.isOpened():
#     print("無法打開攝影機。")
#     exit()

# # 創建一個新的窗口
# cv2.namedWindow('Camera Feed', cv2.WINDOW_NORMAL)

# # 開始捕獲視頻
# while True:
#     # 讀取一幀
#     ret, frame = cap.read()

#     # 檢查視頻是否成功讀取
#     if not ret:
#         print("無法讀取視頻流。")
#         break

#     # 顯示視頻流在新的窗口中
#     cv2.imshow('Camera Feed', frame)

#     # 按下 'q' 鍵退出迴圈
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 釋放資源
# cap.release()
# cv2.destroyAllWindows()
#%%
Time = TimeTool()
# count = 0
# e_ = []
# E_ = []
# while True:
#     if count >20:
#         break
#     b = Time.ReadNowTime()
#     start_process_time = time.process_time()
#     time.sleep(0.03)
#     a = Time.ReadNowTime()
#     end_process_time = time.process_time()
#     e = Time.TimeError(b,a)
#     elapsed_process_time = end_process_time - start_process_time
#     e_.append(e["millisecond"])
#     E_.append(elapsed_process_time)
#     count+=1
# print(e_)
# print(E_)
#%%

"""
精準time sleep
"""
# import time
# import timeit

# def time_sleep(seconds):
#     """
#     - Args: time
#         - time unit :second
#     """
#     start_time = timeit.default_timer()
#     target_time = start_time + seconds

#     while timeit.default_timer() < target_time:
#         pass

# count = 0
# e_ = []
# while count <= 20:
#     # Example: Sleep for 0.1 milliseconds
#     b = Time.ReadNowTime()
#     time_sleep(0.03)
#     a = Time.ReadNowTime()
#     e = Time.TimeError(b,a)
#     e_.append(e["millisecond"])
#     count+=1
# print(e_)

"""
計算CPU運算時間
"""
# import time

# # Record the starting process time
# start_process_time = time.process_time()

# # Perform some time-consuming operation
# for _ in range(1000000):
#     pass

# # Record the ending process time
# end_process_time = time.process_time()

# # Calculate the elapsed process time
# elapsed_process_time = end_process_time - start_process_time

# print(f"Elapsed process time: {elapsed_process_time} seconds")
#%%
# import matplotlib.pyplot as plt

# # 示例数据
# t1 = [0, 1, 2, 3, 4]
# x1 = [0, 1, 4, 9, 16]

# # 绘制红色虚线
# plt.plot(t1, x1, color='red', linestyle='--', linewidth=2, label='Line 1')

# # 添加其他设置，如标题和标签
# plt.title('My Plot')
# plt.xlabel('Time')
# plt.ylabel('Values')

# # 显示图例
# plt.legend()

# # 显示图形
# plt.show()
#%%
"""
使numpy矩陣輸出時不帶有科學記號表示法
"""
# import numpy as np

# # 定義矩陣
# matrix = np.array([[ 9.38000e-01,  3.00000e-02, -3.45000e-01,  4.85364e+02],
#                    [ 2.80000e-02, -1.00000e+00, -1.00000e-02, -1.21300e+00],
#                    [-3.45000e-01,  0.00000e+00, -9.38000e-01,  2.34338e+02],
#                    [ 0.00000e+00,  0.00000e+00,  0.00000e+00,  1.00000e+00]])

# # 將科學符號格式化為非科學符號
# np.set_printoptions(suppress=True)

# # 顯示矩陣
# print(matrix)
#%%
"""
PyQt5 與 OpenGL 結合
"""
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget
# from PyQt5.QtGui import QOpenGLShader, QOpenGLShaderProgram, QSurfaceFormat
# from PyQt5.QtCore import Qt

# from OpenGL.GL import *


# class OpenGLWidget(QOpenGLWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
    
#     def initializeGL(self):
#         # 設置 OpenGL 版本和相關參數
#         glClearColor(0.0, 0.0, 0.0, 1.0)
#         glEnable(GL_DEPTH_TEST)  # 啟用深度測試
        
#     def resizeGL(self, width, height):
#         # 窗口大小變化時調整 OpenGL 視口
#         glViewport(0, 0, width, height)
        
#     def paintGL(self):
#         # 繪製 OpenGL 圖形
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glBegin(GL_TRIANGLES)
#         glColor3f(1.0, 0.0, 0.0)
#         glVertex3f(0.0, 1.0, 0.0)
#         glColor3f(0.0, 1.0, 0.0)
#         glVertex3f(-1.0, -1.0, 0.0)
#         glColor3f(0.0, 0.0, 1.0)
#         glVertex3f(1.0, -1.0, 0.0)
#         glEnd()


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PyQt5 OpenGL Demo")
#         self.setGeometry(100, 100, 800, 600)
        
#         # 創建 OpenGLWidget 並將其設置為主窗口的中心控件
#         self.glWidget = OpenGLWidget(self)
#         self.setCentralWidget(self.glWidget)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
    
#     # 設置 OpenGL 版本
#     format = QSurfaceFormat()
#     format.setVersion(2, 1)  # 將版本設置為 2.1
#     format.setProfile(QSurfaceFormat.CoreProfile)
#     QSurfaceFormat.setDefaultFormat(format)
    
#     mainWindow = MainWindow()
#     mainWindow.show()
    
#     sys.exit(app.exec_())
#%% 
# import sys
# import pygame
# from pygame.locals import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QOpenGLWidget
# from PyQt5.QtCore import QTimer

# # 定義立方體的頂點和面
# class paintGL:
#     def __init__(self):
#         self.roatdirection = True
#         pass

#     def Cube(self):
#         vertices = (
#         (1, -1, -1),
#         (1, 1, -1),
#         (-1, 1, -1),
#         (-1, -1, -1),
#         (1, -1, 1),
#         (1, 1, 1),
#         (-1, -1, 1),
#         (-1, 1, 1)
#         )

#         edges = (
#             (0,1),
#             (1,2),
#             (2,3),
#             (3,0),
#             (0,4),
#             (1,5),
#             (2,6),
#             (3,7),
#             (4,5),
#             (5,6),
#             (6,7),
#             (7,4)
#         )
#         glBegin(GL_LINES)
#         for edge in edges:
#             for vertex in edge:
#                 glVertex3fv(vertices[vertex])
#         glEnd()

#     def draw(self):
#         glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
#         if self.roatdirection is True:
#             glRotatef(1, 3, 1, 1)
#         else:
#             glRotatef(-5, 3, 1, 1)
#         self.Cube()
#         pygame.display.flip()
#         pygame.time.wait(10)

#     def main(self):
#         pygame.init()
#         display = (800,600)
#         pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
#         gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
#         glTranslatef(0.0,0.0, -5)

#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     quit()
#             self.draw()

# class MainWindow(QMainWindow, paintGL):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PyQt5 OpenGL Control")
#         self.setGeometry(100, 100, 400, 200)

#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)

#         self.start_button = QPushButton("forward Rotation")
#         self.stop_button = QPushButton("backward Rotation")

#         layout = QVBoxLayout()
#         layout.addWidget(self.start_button)
#         layout.addWidget(self.stop_button)
#         self.central_widget.setLayout(layout)

#         self.start_button.clicked.connect(self.forward_rotation)
#         self.stop_button.clicked.connect(self.backward_rotation)

#         self.rotating = False

#     def forward_rotation(self):
#         self.roatdirection = True

#     def backward_rotation(self):
#         self.roatdirection = False

#     def update_rotation(self):
#         self.draw()
# # TODO　無法更新旋轉狀態
# if __name__ == "__main__":
#     GL = paintGL()
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     GL.main()
#     sys.exit(app.exec_())
#%%
import struct
"""
用16bit表示12bit
"""
# data_12_bits = 0b101010101010  # 假設您有一個 12 位元的資料

# # 將 12 位元資料左移 4 位元，以將其放置在 16 位元資料中的最高位元組
# data_16_bits = data_12_bits << 4

# # 打包成16位元無符號整數
# packed_data = struct.pack('>H', data_16_bits)

# print(packed_data)

# Data = 65535
# packet = struct.pack('H', Data)
# print(packet)
# for Pin in range(540, 563):
#     print("Pin", Pin)
#     Pin_hex = hex(Pin)

#     # 移除 '0x' 前綴並填充零，確保至少有兩個字元
#     Pin_hex = Pin_hex[2:].zfill(4)
    
#     # 將十六進位表示法分為高位元和低位元
#     high_byte = int(Pin_hex[:2], 16)
#     low_byte = int(Pin_hex[2:], 16)
#     print("打包前 :", low_byte, high_byte)

#     inf = [low_byte , high_byte]
#     byte_low = struct.pack('B', inf[0])
#     byte_high = struct.pack('B', inf[1])

#     print("打包後 :", byte_low, byte_high)
#%%
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import norm

# # 生成 x 值范围
# x = np.linspace(-5, 5, 1000)

# # 标准正态分布的均值和标准差
# mean = 0
# std_dev = 2

# # 计算正态分布的概率密度函数（PDF）
# pdf = norm.pdf(x, mean, std_dev)

# # 绘制正态分布曲线
# plt.plot(x, pdf, label='正态分布')

# # 添加标签和图例
# plt.xlabel('x')
# plt.ylabel('Probability Density')
# plt.title('Standard Normal Distribution')
# plt.legend()

# # 显示图形
# plt.show()
#%%
"""
繪製常態分布圖
"""
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import norm

# # 生成身高数据，平均值为 170 厘米，标准差为 5 厘米，共 30 人
# mean_height = 170
# std_deviation = 5
# heights = np.random.normal(loc=mean_height, scale=std_deviation, size=30)

# # 生成 x 值范围
# x = np.linspace(mean_height - 3 * std_deviation, mean_height + 3 * std_deviation, 100)

# # 计算身高的正态分布概率密度函数（PDF）
# pdf = norm.pdf(x, mean_height, std_deviation)

# # 绘制曲线图
# plt.plot(x, pdf, label='身高分布曲线')

# # 添加标签和标题
# plt.xlabel('身高 (厘米)')
# plt.ylabel('概率密度')
# plt.title('班级30人的身高分布')

# # 显示图形
# plt.legend()
# plt.grid(True)
# plt.show()
#%%
# ORG =[485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
# testTotal = [602.869, -5.859, 156.974, 179.984, 20.2111, 1.6879]
# dis = np.sqrt((testTotal[0] - ORG[0])**2 + (testTotal[1] - ORG[1])**2 + (testTotal[2] - ORG[2])**2)
# print(round(dis,4))
#%%

"""
Pyqt5 + pyOpenGL
"""
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QOpenGLWidget, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QGroupBox
# from PyQt5.QtCore import pyqtSignal, Qt
# from PyQt5.QtGui import QColor
# from OpenGL.GL import *


# class MyGLWidget(QOpenGLWidget):
#     def __init__(self, parent=None):
#         super(MyGLWidget, self).__init__(parent)
#         self.setMinimumSize(640, 480)
#         self.triangle_color = QColor(255, 255, 255)

#     def initializeGL(self):
#         glClearColor(0.0, 0.0, 0.0, 1.0)

#     def paintGL(self):
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glColor3f(self.triangle_color.redF(), self.triangle_color.greenF(), self.triangle_color.blueF())
#         glBegin(GL_TRIANGLES)
#         glVertex3f(-0.5, -0.5, 0.0)
#         glVertex3f(0.5, -0.5, 0.0)
#         glVertex3f(0.0, 0.5, 0.0)
#         glEnd()

#     def resizeGL(self, w, h):
#         glViewport(0, 0, w, h)
#         glMatrixMode(GL_PROJECTION)
#         glLoadIdentity()
#         glOrtho(-1, 1, -1, 1, -1, 1)
#         glMatrixMode(GL_MODELVIEW)


# class ControlWindow(QWidget):
#     colorChanged = pyqtSignal(QColor)

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Control Panel")
#         layout = QVBoxLayout(self)

#         self.colorLabel = QLabel("Triangle Color: ", self)
#         layout.addWidget(self.colorLabel)

#         self.redSlider = QSlider(Qt.Horizontal, self)
#         self.redSlider.setRange(0, 255)
#         self.redSlider.setValue(255)
#         self.redSlider.valueChanged.connect(self.updateColor)
#         layout.addWidget(self.redSlider)

#         self.greenSlider = QSlider(Qt.Horizontal, self)
#         self.greenSlider.setRange(0, 255)
#         self.greenSlider.setValue(255)
#         self.greenSlider.valueChanged.connect(self.updateColor)
#         layout.addWidget(self.greenSlider)

#         self.blueSlider = QSlider(Qt.Horizontal, self)
#         self.blueSlider.setRange(0, 255)
#         self.blueSlider.setValue(255)
#         self.blueSlider.valueChanged.connect(self.updateColor)
#         layout.addWidget(self.blueSlider)

#     def updateColor(self):
#         color = QColor(self.redSlider.value(), self.greenSlider.value(), self.blueSlider.value())
#         self.colorChanged.emit(color)


# class DisplayWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("OpenGL Display")

#         self.glWidget = MyGLWidget(self)
#         self.setCentralWidget(self.glWidget)

#     def setColor(self, color):
#         self.glWidget.triangle_color = color
#         self.glWidget.update()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     controlWindow = ControlWindow()
#     displayWindow = DisplayWindow()

#     controlWindow.colorChanged.connect(displayWindow.setColor)

#     controlWindow.show()
#     displayWindow.show()

#     sys.exit(app.exec_())

"""
class繼承實作
"""
# class A:
#     def __init__(self, a_value):
#         self.a_value = a_value
#         self. var = 10

#     def print_a(self):
#         print("Value of A:", self.a_value)
    
#     def move(self, value):
#         print("move", value)


# class B(A):  # B 继承自 A
#     def __init__(self, a_value, b_value):
#         super().__init__(a_value)  # 调用父类 A 的构造函数
#         self.b_value = b_value

#     def print_b(self):
#         print("Value of B:", self.b_value)


# B(10, 20).move(200)

"""
函數參數
"""
# # Arbitrary Arguments
# def add(*args):
#     result = 0
#     for num in args:
#         result += num
#     for i in range(args[-1]):
#         print(args[i])
#     # return result
# a, b, c, d, e = 1, 1, 1, 1, 1
# add(a, b, c, d, e)
# # print(add(1, 2, 3, 4, 5))  # Output: 15

# def greet(**kwargs):
#     # for key, value in kwargs.items():
#     #     print(f"{key}: {value}")
#     print(kwargs["sampleTime"])
#     print(kwargs["alltime"])

# greet(sampleTime=0.04, alltime=12)  # Output: name: Alice, message: How are you?

# def my_function(**kwargs):
#     """
#     Process keyword arguments and print them along with a default value.
    
#     Args:
#         **kwargs: Arbitrary keyword arguments.
#     """
#     default_value = kwargs.get("default", "No default value specified")  # 获取默认值
#     for key, value in kwargs.items():
#         print(f"{key}: {value}")
#     print(f"Default value: {default_value}")

# # 使用不定长关键字参数调用函数，其中一个参数使用默认值
# my_function(name="Alice", age=30, city="New York", default="N/A")

"""
時間正規化
"""
# Tstart = 0
# Tend = 5
# for t in range(Tend+1):
#     u = (t - Tstart)/(Tend - Tstart)
#     t = Tstart + (Tend-Tstart)*u
#     print("t :", t, "u :", u)

"""
牛頓插值法(用於動態新增數據點)
"""
# def divided_differences(x, y):
#     n = len(x)
#     F = [[None] * n for _ in range(n)]  # 创建一个二维数组来存储差商
#     for i in range(n):
#         F[i][0] = y[i]

#     for j in range(1, n):
#         for i in range(n - j):
#             F[i][j] = (F[i + 1][j - 1] - F[i][j - 1]) / (x[i + j] - x[i])

#     return [F[0][i] for i in range(n)]  # 返回一阶到n阶的差商列表


# def newton_interpolation(x, y, target):
#     coeffs = divided_differences(x, y)  # 计算差商
#     n = len(x)
#     result = coeffs[0]
#     for i in range(1, n):
#         term = coeffs[i]
#         for j in range(i):
#             term *= (target - x[j])
#         result += term

#     return result


# # 示例数据
# x = [0, 1, 2, 3]
# y = [1, 2, 3, 4]

# # 目标点
# target_point = 2.5

# # 计算目标点的插值
# interpolated_value = newton_interpolation(x, y, target_point)
# print(f"在 x={target_point} 处的插值为：{interpolated_value}")

"""
貝塞爾曲線
"""
# import numpy as np
# import matplotlib.pyplot as plt

# def cubic_bezier(t, p0, p1, p2, p3):
#     x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
#     y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]

    
#     # return xData, yData
#     return x, y

# # Example usage:
# # Define control points
# P0 = (5, 0)
# P1 = (1, 5)
# P2 = (1, -5)
# P3 = (5, 0)


# xData = np.zeros((101))
# yData = np.zeros((101))
# tData = np.zeros((101))

# # Calculate points on the curve for t ranging from 0 to 1
# for t in range(0, 101):  # Increment t from 0 to 1 in steps of 0.01
    
#     u = t/100.0
#     x, y = cubic_bezier(u, P0, P1, P2, P3)
#     tData[t] = u
#     xData[t] = x
#     yData[t] = y
    

# # 使用 plt.plot() 函數繪製曲線圖
# plt.plot(xData, yData)

# # 添加標題和標籤
# plt.title('Sample Curve')
# plt.xlabel('X-axis')
# plt.ylabel('Y-axis')

# # 顯示曲線圖
# plt.show()


"""
使用UDP傳送軌跡資訊實驗 後分析
演算法: Matrix+434
"""
# import matplotlib.pyplot as plt
# dB = dataBase()


# filePath = "dataBase/MatrixPlan434_Experimental/sampleTime_40ms_1/results/MatrixPlan434_moveCMD_is_success.csv"
# Vel_index = dB.Load(filePath)

# filePath = "dataBase/MatrixPlan434_Experimental/sampleTime_40ms_1/results\MatrixPlan434_moveCMD_w_speed.csv"
# Vel = dB.Load(filePath)


# # 實驗
# filePath = "dataBase/MatrixPlan434_Experimental/sampleTime_60ms_2/results\MatrixPlan434_Experimental_data.csv"
# path_df = dB.Load(filePath)

# # 期望
# filePath = "dataBase/MatrixPlan434_Experimental/sampleTime_60ms_1/EstimateData/MatritPlan434_PoseMatrix_time.csv"
# expectTime = dB.Load(filePath)



# # 軌跡更新之資料索引
# Vel_index_data = np.zeros((len(Vel_index)))
# # 軌跡速度
# Vel_data = np.zeros((len(Vel)))
# # 軌跡時間
# Time = np.zeros(len(path_df))
# # 軌跡實際更新時間
# validTime = np.zeros((len(Vel)))
# # 期望軌跡時間
# expectTime_ = np.zeros((len(expectTime)))

# # for i in range(len(Vel_index)):
# #     Vel_index_data[i] = Vel_index["Time"][i]
# #     Vel_data[i] = Vel["Time"][i]

# # # 取出所有實際軌跡時間
# # for i in range(len(path_df)):
# #     Time[i] = path_df["time"][i]

# # # 計算出命令更新之系統時間
# # for i in range(len(Vel_index)):
# #     index = Vel_index_data[i]
# #     validTime[i] = path_df["time"][index]

# # 實際軌跡時間
# for i in range(len(path_df)):
#     Time[i] = path_df["time"][i]

# # 期望軌跡時間
# for i in range(len(expectTime_)):
#     expectTime_[i] = expectTime["time(ms)"][i]

# difftime = np.diff(validTime)
# difftime = np.insert(difftime, 0, 0)

# plt.rcParams.update({'font.size': 20})

# # plt.plot(Vel_index_data, difftime)
# plt.plot(expectTime_, color='red', label='Expect Time')
# plt.plot(Time, color='green', label='Estimated Time')
# # plt.plot(validTime, Vel_data, marker='o', linestyle='-')

# plt.legend()
# plt.xlabel("Index")
# plt.ylabel("Time(ms)")
# plt.title("Trajectory Time Phase")

# plt.show()

"""
字串格式語法
"""
# dict={}

# dict = {'0':[2,3,4,5],
#         '1':[3,4,5,6]}
# for i in range(2):
#     print(dict[str(i)][0])
#     print(dict[f'{i}'][0])

# a = np.ones((5))
# for i in range(len(a)):
#         a[i] = i
# print(a)
# a = a.astype(int)  # 將 a 陣列中的元素型別轉換為整數
# print(a)

# import numpy as np

# a = np.array([1, 2, 3, 4, 5])  # 假設這是你的陣列

# # 刪除第一個元素
# a = a[1:]

# print(a)

"""
CSV同時讀/寫實驗
結果: 可以
讀與寫要有一個微小時間差 先寫後讀
"""
# import threading
# import time
# from dataBase import dataBase


# def write(counter):
#     dB.Save_time(counter, "test.csv")
#     print("寫: ", counter)
    
# def read(counter):
#     result = dB.Load("test.csv")
#     print(f"讀{counter}: ", result["Time"][counter])
    

# if __name__ == "__main__":
#     dB = dataBase()
#     controlSignal = False
#     counter = 0
#     # dB.Save_time(counter, "test.csv")
#     while True:
#         counter+=1
#         # 創建線程
#         thread1 = threading.Thread(target=write, args=(counter,))
#         thread2 = threading.Thread(target=read, args=(counter,))
#         # 啟動線程
#         thread1.start()
#         thread2.start()
#         # 等待線程結束
#         thread1.join()
#         thread2.join()
#         print("test")

#         if counter == 10:
#             break

"""
雙執行緒應變處理架構實驗
"""
# import threading
# import time
# import pygame
# from Toolbox import TimeTool
# from dataBase import dataBase


# def Trajectoryplan():
#     global data, threadClose
    
#     threadRunning = True
#     count = 1
#     while threadRunning:
#         data += count
#         time.sleep(0.02)
#         if threadClose is False or data >= 100:
#             threadRunning = False
#     print("--------------------------------------------------------------計算完成----------------------------------------------------------")

# def main():
#     # 初始化Pygame
#     pygame.init()
#     # 设置屏幕大小，但不需要显示窗口
#     screen = pygame.display.set_mode((400, 300))

#     # data = dB.Load("test.csv")
#     global data, threadClose
#     data = 0
#     threadClose = True
    
#     mainRunning = True
#     while mainRunning:
#         b = Time.ReadNowTime()
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_p:
#                     print("--------------------------------------------------------------重新規劃軌跡----------------------------------------------------------")
#                     # 創建線程
#                     threadClose = True
#                     planThread = threading.Thread(target=Trajectoryplan)
#                     planThread.start()
#                     # planThread.join()
#                 elif event.key == pygame.K_e:
#                     threadClose = False
#                     data = 0
                    
#                 elif event.key == pygame.K_q:
#                     # Main loop end
#                     # threadClose = False
#                     time.sleep(0.01)
#                     mainRunning = False

#             elif event.type == pygame.QUIT:
#                 mainRunning = False
#         #----------------------------------Main-------------------------------------------
#         print(data)
        
#         pygame.time.wait(1)
#         a = Time.ReadNowTime()
#         err = Time.TimeError(b, a)
#         print(err["millisecond"])
        

# if __name__ == "__main__":
#     dB = dataBase()
#     Time = TimeTool()
#     main()
#     controlSignal = False
#     counter = 0
    
"""
pygame 鍵盤事件(可比cv2快速處理)
"""
# import pygame
# from Toolbox import TimeTool

# Time = TimeTool()
# # 初始化Pygame
# pygame.init()

# # 设置屏幕大小，但不需要显示窗口
# screen = pygame.display.set_mode((400, 300))
# pygame.display.iconify()

# 允许 Pygame 捕获键盘事件
# pygame.event.set_grab(True)

# 循环检测键盘事件
# running = True
# while running:
#    # 解除鼠标锁定
#    # pygame.event.set_grab(False)
#    b = Time.ReadNowTime()

#    """
#    pygame.event.get(): 用於單次觸發
#    pygame.key.get_pressed(): 用於連續觸發
#    """
#    for event in pygame.event.get():
#       if event.type == pygame.KEYDOWN:
#          if event.key == pygame.K_y:
#                print("按下 'y' 键")
#          elif event.key == pygame.K_u:
#                print("按下 'u' 键")
#          elif event.key == pygame.K_q:
#                running = False
#       elif event.type == pygame.QUIT:
#          running = False

   
#    keys = pygame.key.get_pressed()
   
#    # 觀察者視角移動
#    if keys[pygame.K_a]:
#       print("按下 'a' 键")
#    elif keys[pygame.K_d]:
#       print("按下 'd' 键")
#    elif keys[pygame.K_w]:
#       print("按下 'w' 键")
#    elif keys[pygame.K_s]:
#       print("按下 's' 键")
#    a = Time.ReadNowTime()
#    err = Time.TimeError(b, a)
#    print(err["millisecond"])

    

#     # 处理窗口事件以确保事件被正确处理
#     # pygame.event.pump()
    
#     pygame.display.flip()
#     pygame.time.wait(1)
#     a = Time.ReadNowTime()
#     err = Time.TimeError(b, a)
#     print(err["millisecond"])

"""
cv2鍵盤事件
"""
# import cv2
# from Toolbox import TimeTool

# Time = TimeTool()
# # 建立一個空視窗
# cv2.namedWindow('Empty Window')


    

# while True:
#     b = Time.ReadNowTime()

#     key = cv2.waitKey(1) & 0xFF
#     if key != 255:  # 检查是否有按键按下
#         if key == ord('q'):
#             print("按下q鍵")
#         elif key == ord('r'):
#             print("按下r鍵")
#         elif key == ord('t'):
#             print("按下t鍵")
#         elif key == ord('y'):
#             print("按下y鍵")

#     a = Time.ReadNowTime()
#     err = Time.TimeError(b, a)
#     print(err["millisecond"])


# # 關閉視窗
# cv2.destroyAllWindows()


"""
staticmethod 靜態方法
- 特點: 可以不實例化該類別，直接使用調用靜態方法。
>> 不可變更類別的屬性與狀態，但可進行計算或資料傳輸。
"""
# class Person:

#     @ staticmethod
#     def run():
#         print("跑步")
#         return 10

# # 實例化調用靜態方法
# P = Person()
# status = P.run()
# print(status, "圈")

# # 不實例化類別，直接調用方法
# Person.run()

"""
classmethod 類別方法
>> 1.存取類別方法、類別變數(無法存取實例變數)
   2.類別方法，存取並改變類別變數
"""

# 類別方法，存取並改變類別變數，實例
# class Math:
#    # 圓周率(類別變數)
#    pi = 3.14  
#    def __init__(self):
#       # 實例變數
#       self.pi = 3.15

#    @classmethod
#    def calculate_circle_area(cls, radius):
#       # cls.pi = 4
#       return cls.pi * (radius ** 2)
   
#    def variable_type(self, var_name, obj):
#         if hasattr(obj, var_name):
#             return "Instance variable" if var_name in obj.__dict__ else "Class variable"
#         else:
#             return "Local variable"
   


# # 原本的
# m = Math()


# # 使用類別方法計算圓的面積
# radius = 5
# area = Math.calculate_circle_area(radius)
# print("圓的面積:", area)  # 輸出: 圓的面積: 78.5

# print("經過類別方法的圓周率", Math.pi)
# print("經過類別方法後的實例類別屬性", m.pi)

# # 類別方法，存取類別方法，實例
# class Calculator:
#     @classmethod
#     def add(cls, x, y):
#         return x + y

#     @classmethod
#     def multiply(cls, x, y):
#         # 在 multiply 方法中調用 add 方法
#         product = 0
#         for _ in range(y):
#             product = cls.add(product, x)
#         return product

# # 使用類別方法進行計算
# result = Calculator.multiply(3, 4)
# print("3 * 4 =", result)  # 輸出: 3 * 4 = 12

"""
Abstract Method
>> 
1.需要由另一個類別繼承抽象類別才可進行實例化，抽象類別不能實例化。
2.繼承抽象類別的其他類別，必須要實作抽象類別的抽象方法，否則一樣視為抽象方法。
3.抽象類別可以當作介面來使用
4.可用於實現物件導向中多形概念
5.每次其他類繼承抽象類別，並使用抽象類別的方法時，都會覆寫(Method Overriding)父類的公同方法

"""
# from abc import ABC, abstractmethod
# # 登入類別
# class Login(ABC):
#     @abstractmethod
#     def login(self):
#         pass

# # Facebook登入機制
# class FacebookLogin(Login):
#     def login(self):
#         print("Facebook login implementation.")

# #Google登入機制
# class GoogleLogin(Login):
#     def login(self):
#         print("Google login implementation.")

# #Twitter登入機制
# class TwitterLogin(Login):
#     def login(self):
#         print("Twitter login implementation.")

# fb = FacebookLogin()
# fb.login()
# google = GoogleLogin()
# google.login()
# twitter = TwitterLogin()
# twitter.login()

# from abc import ABC, abstractmethod
# import pandas as pd
# import numpy as np
# import os
# import sys
# from Toolbox import TimeTool
# from Matrix import Matrix4x4
# r2d = np.rad2deg

# class Database_interface(ABC):
#     @abstractmethod
#     def Save(self, data):
#         pass

#     def Load(self, filePath):
#         pass

#     def dataframeToNdarray():
#         pass

# class database_HomogeneousMat(Database_interface):

#     @ staticmethod
#     def Save(data, filePath):
#         print("將軌跡點以齊次矩陣形式儲存", data)

#     @ staticmethod
#     def dataframeToNdarray(dataFrame):
#         """data type: dataframe conversion ndarray
#         """
#         dataShape = dataFrame.shape
#         dataNdarray = np.zeros((dataShape[0], 4, 4))
#         for layer in range(dataShape[0]):
#                 dataNdarray[layer,0,0] = dataFrame['Xx'][layer]
#                 dataNdarray[layer,1,0] = dataFrame['Xy'][layer]
#                 dataNdarray[layer,2,0] = dataFrame['Xz'][layer]
#                 dataNdarray[layer,3,0] = dataFrame
#                 dataNdarray[layer,0,1] = dataFrame['Yx'][layer]
#                 dataNdarray[layer,1,1] = dataFrame['Yy'][layer]
#                 dataNdarray[layer,2,1] = dataFrame['Yz'][layer]
#                 dataNdarray[layer,3,1] = dataFrame
#                 dataNdarray[layer,0,2] = dataFrame['Zx'][layer]
#                 dataNdarray[layer,1,2] = dataFrame['Zy'][layer]
#                 dataNdarray[layer,2,2] = dataFrame['Zz'][layer]
#                 dataNdarray[layer,3,2] = 0
#                 dataNdarray[layer,0,3] = dataFrame['Px'][layer]
#                 dataNdarray[layer,1,3] = dataFrame['Py'][layer]
#                 dataNdarray[layer,2,3] = dataFrame['Pz'][layer]
#                 dataNdarray[layer,3,3] = 1
#         return dataNdarray
#     @ staticmethod
#     def Load(filePath):
#         try:
#             df = pd.read_csv(filePath)
#             # TrajectoryData is ndarray
#             TrajectoryData = database_HomogeneousMat.dataframeToNdarray(df)
            
#             return TrajectoryData

#         except FileNotFoundError:
#             print(f"找不到文件：{filePath}")
#             return None

    

# class database_PoseMat(Database_interface):
#     @ staticmethod
#     def Save(data, filePath):
#         print("將軌跡點以位姿矩陣形式儲存", data)
    
#     @ staticmethod
#     def Load(self, filePath):
#         print("將軌跡點以位姿矩陣形式載入", filePath)

# class database_JointAngle(Database_interface):
#     @ staticmethod
#     def Save(self, data, filePath):
#         print("將軌跡點以關節角度形式儲存", data)
    
#     @ staticmethod
#     def Load(self, filePath):
#         print("將軌跡點以關節角度形式載入", filePath)

# class database_time(Database_interface):
#     @ staticmethod
#     def Save(self, data, filePath):
#         print("將軌跡點以關節角度形式儲存", data)
    
#     @ staticmethod
#     def Load(self, filePath):
#         print("將軌跡點以關節角度形式載入", filePath)

# class convertData():
#     Mat = Matrix4x4()
#     @staticmethod
#     def HomogeneousMatToPoseMat(filePath):
#         """
#         - Args: trajectoryData(type: DataFrame)
#         - Return: trajectoryData(type: ndarray)
#         """
#         pass


# database_HomogeneousMat.Save(121514, "dataBase/test.csv")
# database_HomogeneousMat.Load("dataBase/test.csv")

# from dataBase_v0 import *
# import matplotlib.pyplot as plt
# filePath = "dataBase/IK_itrationTime.csv"
# dB = dataBase()
# data = dB.Load(filePath)
# plt.plot(data)
# plt.title("Jacobian matrix iteration time")
# plt.ylabel('Cost time(ms)')
# plt.show()

"""
重構資料庫測試
"""

# from dataBase_v1 import *

# data1 = np.array([[999]])
# data6 = np.array([[10,56,33,78,106,99], [10,56,33,78,106,99]])
# data16 = np.array([[0.9461547750003523,0.298668255044473,0.12485357492968502,0.0,0.3213919563739074,-0.912805168919898,-0.2519800269292565,0.0,0.03870855360492394,0.2785390403907611,-0.9596445440140889,0.0,958.521,-37.126,-164.943,1.0], 
#                            [0.9461547750003523,0.298668255044473,0.12485357492968502,0.0,0.3213919563739074,-0.912805168919898,-0.2519800269292565,0.0,0.03870855360492394,0.2785390403907611,-0.9596445440140889,0.0,958.52296,-28.012489999999996,-164.9381,1.0]])

# filePath = "dataBase/test0329HomogeneousMat.csv"
# database_HomogeneousMat.Save(data16, filePath, "w")
# HomogeneousMat = database_HomogeneousMat.Load(filePath)

# PoseMat = database_PoseMat.HomogeneousMatToPoseMat(HomogeneousMat)

# filePath = "dataBase/test0329PoseMat.csv"
# database_PoseMat.Save(data6, filePath, "w")
# PoseMat = database_PoseMat.Load(filePath)

# filePath = "dataBase/test0329JointAngle.csv"
# database_JointAngle.Save(data6, filePath, "w")
# JointAngle = database_JointAngle.Load(filePath)

# filePath = "dataBase/test0329Time.csv"
# database_time.Save(data1, filePath, "w")
# Time = database_time.Load(filePath)

# filePath = "dataBase/test0329Velocity.csv"
# database_Velocity.Save(data1, filePath, "w")
# Velocity = database_Velocity.Load(filePath)

# print()

"""
利用pygame介面輸入值
"""
# import pygame
# import sys

# # 初始化Pygame
# pygame.init()

# # 設置畫面寬高
# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("輸入數值")

# # 設置字體
# font = pygame.font.SysFont(None, 40)

# def input_number():
#     number = ''
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                pygame.quit()
#                sys.exit()
               
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:  # 當按下Enter鍵時，返回輸入的數值
#                     return int(number)
#                 elif event.key == pygame.K_BACKSPACE:  # 當按下Backspace鍵時，刪除最後一個字符
#                     number = number[:-1]
#                 else:
#                     number += event.unicode  # 將按鍵對應的字符添加到數值字符串中
        
#         screen.fill((255, 255, 255))
#         text_surface = font.render("Enter a number: " + number, True, (0, 0, 0))
#         screen.blit(text_surface, (50, 50))
#         pygame.display.update()

# # 主程式
# def main():
#    while True:
#       number = input_number()
#       print("You entered:", number)

# if __name__ == "__main__":
#     main()

"""
矩陣軌跡法改版測試 | 指定速度版本
"""
# from PathPlanning import PathPlanning
# from Matrix import Matrix4x4
# from Toolbox import TimeTool

# Time = TimeTool()
# Mat = Matrix4x4()
# d2r = np.deg2rad
# NowEnd = np.eye(4)
# GoalEnd = np.eye(4)

# NowPoseMat = [958.521, -150.126, -164.943, -165.2876, -7.1723, 17.5191]
# GoalPoseMat = [958.525, -0.527, -164.933, -165.2873, -7.1725, 17.5181]

# NowEnd = NowEnd @ Mat.TransXYZ(NowPoseMat[0], NowPoseMat[1], NowPoseMat[2]) @ Mat.RotaXYZ(d2r(NowPoseMat[3]), d2r(NowPoseMat[4]), d2r(NowPoseMat[5])) 
# GoalEnd = GoalEnd @ Mat.TransXYZ(GoalPoseMat[0], GoalPoseMat[1], GoalPoseMat[2]) @ Mat.RotaXYZ(d2r(GoalPoseMat[3]), d2r(GoalPoseMat[4]), d2r(GoalPoseMat[5]))
# speed = 0
# sampleTime = 0.04

# b = Time.ReadNowTime()

# GoalSpeed = 1.6
# # 矩陣軌跡法 | 指定速度
# trjData, velData, timeData = PathPlanning.MatrixPathPlanSpeed(GoalEnd, NowEnd, GoalSpeed, sampleTime)

# a = Time.ReadNowTime()
# err = Time.TimeError(b, a)
# print(velData[2])
# print("迭代時間: ", err)
"""
取出執行續運算結果
"""
# import threading
# import time

# class MyThread(threading.Thread):
#     def __init__(self, target, args=()):
#         super().__init__(target=target, args=args)
#         self._result = None

#     def run(self):
#         self._result = self._target(*self._args)

#     def get_result(self):
#         return self._result

# # 使用範例
# def calculate_sum(start, end):
#     time.sleep(1)
#     return sum(range(start, end + 1))

# # 建立並執行自定義的執行緒
# thread = MyThread(target=calculate_sum, args=(1, 100))
# thread.start()
# # thread.join()

# while True:
#    """
#    is_alive():
#    執行續運轉中 >>> True
#    執行續結束   >>> False
#    """

#    if thread.is_alive():
#       print("執行續計算中")
      
#    else:
#        # 獲取執行緒計算的結果
#       result = thread.get_result()
#       print("計算結果:", result)
#       break
       
"""
執行續池與進程池應用範例
1. 執行續池 >>> 適合I/O密集型任務。
2. 進程池   >>> 適用CPU並行運算任務。
"""
# import concurrent.futures
# import time

# def task():
#     print("任務開始執行")
#     time.sleep(3)  # 模擬任務執行時間
#     print("任務執行完成")
#     return "任務結果"

# def main():
#     # 建立進程池
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         # 提交任務到進程池
#         future = executor.submit(task)

#         # 檢查任務是否在執行中
#         while True:
        
#             # 檢查任務是否完成
#             if future.done():
#                 result = future.result()
#                 print("任務已完成，結果為:", result)
#                 break
#             else:
#                 print("任務仍在執行...")

# if __name__ == "__main__":
#     main()


"""
進程池效能測試
"""
# import concurrent.futures
# import time
# from armControl import Generator
# import threading

# def task():
#     print("任務開始執行")
#     time.sleep(3)  # 模擬任務執行時間
#     print("任務執行完成")
#     return "任務結果"

# def main():
#     d2r = np.deg2rad
#     Time = TimeTool()
#     # NowEnd = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
#     NowEnd = [958.521, -25.142, -164.943, -165.2876, -7.1723, 17.5191]
#     GoalEnd = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
#     Goalspeed = 1
#     sampleTime = 0.04
    
#     # HomogeneousMatData, PoseMatData, VelocityData, TimeData = Generator.generateTrajectory(NowEnd, GoalEnd, sampleTime, Goalspeed)
    
#     # 建立進程池
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         b = Time.ReadNowTime()
#         # 提交任務到進程池
#         future = executor.submit(Generator.generateTrajectory, NowEnd, GoalEnd, sampleTime, Goalspeed)

#         # 檢查任務是否在執行中
#         while True:
        
#             # 檢查任務是否完成
#             if future.done():
#                 a = Time.ReadNowTime()
#                 calerr = Time.TimeError(b, a)
#                 print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")

#                 result = future.result()
#                 print("任務已完成，結果為:", result)
                
#                 break
#             else:
#                 print("任務仍在執行...")

# if __name__ == "__main__":
#     main()


# def main():
#     d2r = np.deg2rad
#     Time = TimeTool()
#     # NowEnd = [958.521, -37.126, -164.943, -165.2876, -7.1723, 17.5191]
#     NowEnd = [958.521, -25.142, -164.943, -165.2876, -7.1723, 17.5191]
#     GoalEnd = [958.525, -18.527, -164.933, -165.2873, -7.1725, 17.5181]
#     Goalspeed = 1
#     sampleTime = 0.04
#     planThread = threading.Thread(target=Generator.generateTrajectory, args=(NowEnd, GoalEnd, sampleTime, Goalspeed))
#     planThread.start()
#     b = Time.ReadNowTime()

#     while True:
#         # time.sleep(2)
#         if planThread.is_alive() is False:
#             a = Time.ReadNowTime()
#             calerr = Time.TimeError(b, a)
#             print("計算新軌跡總共花費: ", calerr["millisecond"], "ms")
#             break
#         else:
#             print("計算中......")

# if __name__ == "__main__":
#     main()

"""
CSV資料合併操作
"""
# import pandas as pd

# def mergeTrajectoryData():
#     Path_name = ["HomogeneousMat", "PoseMat", "Velocity", "Time", "JointAngle"]
#     for i in range(len(Path_name)):
#         # 指定兩個 CSV 檔案的路徑
#         path1 = "database/dynamicllyPlanTEST/" + Path_name[i] + ".csv"
#         path2 = "database/dynamicllyPlanTEST/" + "new" + Path_name[i] + ".csv"

#         # 讀取第一個 CSV 檔案
#         data1 = pd.read_csv(path1)

#         # 讀取第二個 CSV 檔案
#         data2 = pd.read_csv(path2)

#         # 移除第一筆資料，保留從第二筆開始的所有資料
#         data2 = data2.iloc[1:]  

#         # 找到第一個 CSV 檔案中第 170 列的索引 (注意索引從 0 開始)
#         index_to_replace = 168  # 如果要覆蓋第 170 列以後的資料，索引就是 169

#         if Path_name[i] == "Time":
#             data2["Time"] += data1["Time"][index_to_replace-1]

#         # 從第一個 CSV 檔案中取得要保留的資料（覆蓋第 170 列以後的部分）
#         data1_subset = data1.iloc[:index_to_replace]  # 包括第 170 列在內的所有資料

#         # 從第二個 CSV 檔案中取得要覆蓋到第一個檔案的資料
#         data2_to_append = data2  

#         # 將第二個 CSV 檔案的資料覆蓋到第一個 CSV 檔案中的特定部分
#         merged_data = pd.concat([data1_subset, data2_to_append], ignore_index=True)

#         # 儲存合併後的資料到新的 CSV 檔案
#         output_path = "database/dynamicllyPlanTEST/" + "Remix_" + Path_name[i] + ".csv"
#         merged_data.to_csv(output_path, index=False)

#         print("----------------軌跡資料合併完畢----------------")

"""
csv 合併檔案
"""
# import numpy as np

# # 將原始資料寫入到 CSV 檔案
# with open('dataBase/mergeData/file1.csv', 'w') as file:
#     file.write('1.11,1.12,1.13,1.14,1.15,1.16\n')
#     file.write('1.21,1.22,1.23,1.24,1.25,1.26\n')

# with open('dataBase/mergeData/file2.csv', 'w') as file:
#     file.write('2.11,2.12,2.13,2.14,2.15,2.16\n')
#     file.write('2.21,2.22,2.23,2.24,2.25,2.26\n')

# # 讀取第一個 CSV 檔案中的數組
# file1_data = np.genfromtxt('dataBase/mergeData/file1.csv', delimiter=',', dtype=np.float64, encoding='utf-8')
# # array1 = file1_data.reshape(2, 1, 6)

# # 讀取第二個 CSV 檔案中的數組
# file2_data = np.genfromtxt('dataBase/mergeData/file2.csv', delimiter=',', dtype=np.float64, encoding='utf-8')
# # array2 = file2_data.reshape(2, 1, 6)

# # 合併兩個數組，指定 axis=1
# merged_array = np.concatenate((file1_data, file2_data), axis=1)

# # 將合併後的數組存儲為新的 CSV 檔案
# np.savetxt('dataBase/mergeData/Remix_arrays.csv', merged_array.reshape(4, 6), delimiter=',', fmt='%.4f', encoding='utf-8')

"""
搜尋最相似的資料
"""
# import numpy as np

# # 定義二維矩陣，每一行是一筆資料
# data_matrix = np.array([
#     [958.522, -30.256, -164.939, 147.124, -71.723, 175.191],
#     [958.522, -30.192, -164.939, 148.4929, -71.8822, 173.3322],
#     [958.522, -30.129, -164.939, 149.8889, -72.0274, 171.4464]])

# # 定義目標資料
# target_data = np.array([958.522, -30.172, -164.939, 148.4929, -71.8822, 173.3322])

# # 計算每一筆資料與目標資料的歐氏距離
# distances = np.linalg.norm(data_matrix - target_data, axis=1)

# # 找出距離最小的資料的索引
# closest_index = np.argmin(distances)

# # 找出距離最小的資料
# closest_data = data_matrix[closest_index]

# # 打印最相近的資料
# print("距離最近的資料：")
# print(closest_data)
# print("最近的資料索引")
# print(closest_index)

"""
pandas資料合併與垂直堆疊
"""
# import numpy as np
# import pandas as pd

# data_frame1 = pd.read_csv("dataBase/dynamicllyPlanTEST/PoseMat.csv", delimiter=',', dtype=np.float64, encoding='utf-8')
# data_frame2 = pd.read_csv("dataBase/dynamicllyPlanTEST/newPoseMat.csv", delimiter=',', dtype=np.float64, encoding='utf-8')

# # 提取需要的df資料
# data_frame1 = data_frame1.iloc[:3]
# data_frame2 = data_frame2.iloc[:3]

# stacked_df = pd.concat([data_frame1, data_frame2], axis=0)
# stacked_df.to_csv("dataBase/dynamicllyPlanTEST/test1Remix_PoseMat.csv", index=False,  header=True)

"""
開啟執行緒所花的時間
"""
# import threading
# from Toolbox import TimeTool
# def test():
#     a = 0
#     while True:
#         a += 1
#         if a == 100:
#             break

# def test1():
#     a = 0
#     while True:
#         a += 1
#         if a == 100:
#             break

# def test2():
#     a = 0
#     while True:
#         a += 1
#         if a == 100:
#             break

# def main():
#     Time = TimeTool()
#     b = Time.ReadNowTime()
#     t = threading.Thread(target=test)
#     t1 = threading.Thread(target=test1)
#     t2 = threading.Thread(target=test2)
#     t.start()
#     t1.start()
#     t2.start()
    
#     a = Time.ReadNowTime()
#     err = Time.TimeError(b,a)
#     print(err["millisecond"])

# if __name__ == "__main__":
#     main()

"""
利用queue傳遞與控管資料
"""
# import queue
# import threading
# import time

# # 定义生产者函数，向队列中放入数据
# def producer(q):
#     for i in range(5):
#         item = f"Item {i}"
#         q.put(item)
#         print(f"生产者放入数据：{item}")
#         time.sleep(1)  # 模拟生产数据的耗时操作

# # 定义消费者函数，从队列中取出数据
# def consumer(q):
#     while True:
#         item = q.get()
#         if item is None:
#             break
#         print(f"消费者取出数据：{item}")
#         time.sleep(2)  # 模拟消费数据的耗时操作

# # 创建队列对象
# q = queue.Queue()

# # 创建生产者线程和消费者线程
# producer_thread = threading.Thread(target=producer, args=(q,))
# consumer_thread = threading.Thread(target=consumer, args=(q,))

# # 启动线程
# producer_thread.start()
# consumer_thread.start()

# # 等待生产者线程结束
# producer_thread.join()

# # 队列中放入结束信号（None），通知消费者线程退出
# q.put(None)

# # 等待消费者线程结束
# consumer_thread.join()

# print("所有数据处理完毕.")

"""
DX200端 執行軌跡架構 Updata:2024/04/28
"""
# dataLen = 225
# # I001 = 100//18 + 1

# # I001改用batch為單位
# I001 = dataLen//9 + 1 
# I000 = 2
# I028 = 0
# while I001>=I028: # INFORM邏輯稍微有些不同 要使用>  python使用>=
#     # 確認是否已傳送完n組的數據
#     # if I028 > I001:
#     #     break

#     # 通訊
#     print(f"送出封包，內容是I0: {I000}")

#     # 下一筆要傳送的資料
#     I000 += 1
    
#     # 如果資料已傳送18筆(2批)，要重製批次號，代表1組資料已傳完畢
#     if I000 == 11:
#         I028 += 1 
#         print(f"I001: {I028}")
#     elif I000 > 19:
#         I028 += 1
#         I000 = 2
#         print(f"I001: {I028}")


"""
獲得兩個數組的距離
"""
# import numpy as np

# # 示例数组
# a = np.array([ 958.521 ,  -37.042 , -164.943 , -165.2876,   -7.1723,   17.5191])
# b = np.array([ 958.519 ,  -37.198 , -164.956 , -164.288 ,   -7.1705,   17.5168])

# # 计算欧几里得距离
# distance = np.linalg.norm(a - b)

# print("a与b的欧几里得距离:", distance)

"""
UI介面通訊
"""
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QTimer, QThread
# import sys, time, queue, threading
# from UI_model import MyModel
# from UI_view import MyView
# from UI_control import MyController
# from MotomanControlUdp import *

# class ParameterThread(QThread):
    
#     def __init__(self, controller, model):
#         super().__init__()
#         self.controller = controller
#         self.model = model
#         self.WeldingParameter = 0
#         self.WeldingSpeed = 0

#     def run(self):
#         time.sleep(2)  # 這裡的休眠是為了等待 UI 界面啟動
        
#         while True:
#             WeldingParameter_buffer = self.model.get_WeldingParameter()
#             WeldingSpeed_buffer = self.model.get_WeldingSpeed()

#             if len(WeldingParameter_buffer) >= 1:
#                 self.WeldingParameter = WeldingParameter_buffer[-1]
#             if len(WeldingSpeed_buffer) >= 1:
#                 self.WeldingSpeed = WeldingSpeed_buffer[-1]
            
#             print(f"銲接參數: {self.WeldingParameter}, 銲接走速:{self.WeldingSpeed}")



#             time.sleep(0.01)


# def main():
#     app = QApplication(sys.argv)

#     model = MyModel()
#     view = MyView()
#     controller = MyController(model, view)

#     view.show()

#     trjdataPath = "dataBase/dynamicllyPlanTEST/PoseMat_0.csv"
#     speeddataPath = "dataBase/dynamicllyPlanTEST/Speed_0.csv"
#     Motoman = Motomancontrol(trjdataPath, speeddataPath)
#     Motoman.main()

    

#     parameter_thread = ParameterThread(controller, model)
#     parameter_thread.start()

#     # sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()

"""
queue
"""
# import queue
# # 建立一個Queue
# my_queue = queue.Queue()

# # 放入1~10
# # for i in range(1, 11):
# #     my_queue.put(i)

# my_queue.put(1)

# # 取出第5個元素
# # for i in range(5):
# #     value = my_queue.get()
# value = my_queue.get()

# print("第5個元素:", value)

"""
"""
# import pygame
# import queue

# screen_width = 800
# screen_height = 600
# screen = pygame.display.set_mode((screen_width, screen_height))

# my_queue = queue.Queue()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_k:
#                 my_queue.put(1)
#             elif event.key == pygame.K_l:
#                 if my_queue.empty() is False:
#                     value = my_queue.get()
#                     print(value)
#                 else:
#                     print("Queue是空的!")
#     time.sleep(0.01)
            
            
"""
傅立葉變換
"""

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.fft import fft
# import pandas as pd

# df = pd.read_excel('WeldingData/weld_and_tungsten_data.xlsx', sheet_name="Original Weld Widths")
# df = np.array(df)[:, 1]
# # 定義信號參數
# totalTime = 87
# dataNBR = 2575
# fs = totalTime/dataNBR # 取樣頻率(秒/次)
# T = 1 / fs  # 取樣間隔
# t = np.arange(0, 87, fs)  # 時間軸
# t = t[1:]

# # 取梯度
# gradient_df = np.gradient(df)

# # 取平均值、標準差
# gradient_mean = np.mean(gradient_df)
# gradient_std = np.std(gradient_df)

# mean = np.mean(df)
# std = np.std(df)

# # # 使用一倍標準差過濾梯度
# # gradient_df[gradient_df > mean + std] = mean + std
# # gradient_df[gradient_df < -mean - std] = -mean - std
# threshold = 0.2


# indices_positive = np.where(np.abs(gradient_df) > threshold)[0]


# # 滤除梯度大于1的数据
# filtered_df = np.delete(df, indices_positive+1)
# filtered_t = np.delete(t, indices_positive+1)


# # 原始
# plt.subplot(3, 1, 1)
# plt.plot(t, df, marker="o")
# plt.xlabel('Time [s]')
# plt.ylabel('Weld bead width [mm]')
# plt.title('Original Data (Time Domain)')

# plt.subplot(3, 1, 2)
# plt.plot(filtered_t, filtered_df)
# plt.xlabel('Time [s]')
# plt.ylabel('Weld bead width [mm]')
# plt.title('filtered Data (Time Domain)')

# plt.subplot(3, 1, 3)
# plt.plot(t, gradient_df)
# plt.xlabel('Time [s]')
# plt.ylabel('Weld bead width [mm]')
# plt.title('gradient Data (Time Domain)')
# plt.tight_layout()

# # 執行傅立葉變換
# X = fft(df)

# # 計算頻率軸
# N = len(t)
# freqs = np.fft.fftfreq(N, T)

# # 繪製原始信號和頻域表示
# plt.figure(figsize=(10, 6))

# # 原始信號
# plt.subplot(2, 1, 1)
# plt.plot(t, df, marker="o")
# plt.xlabel('Time [s]')
# plt.ylabel('Amplitude')
# plt.title('Original Signal (Time Domain)')

# # 頻域表示
# plt.subplot(2, 1, 2)
# plt.plot(freqs, np.abs(X), marker="o")
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Magnitude')
# plt.title('Frequency Domain Representation')
# plt.tight_layout()
# plt.show()

"""
數組 融合
"""
# import numpy as np

# # 创建示例矩阵
# matrix1 = np.zeros((223, 1, 6))
# matrix2 = np.ones((223, 1, 1))

# # 将两个矩阵按行融合
# result = np.concatenate((matrix1, matrix2), axis=2)

# print("行逐行融合后的矩阵：\n", result)

# import numpy as np

# # 定义两个示例数组
# array1 = np.array([[958.425, -18.627, -164.833, -1652.876, -71.723, 175.191]])
# array2 = np.array([[958.525, -18.527, -164.933, -1652.876, -71.723, 175.191]])

# # 计算两个数组之间的欧式距离
# euclidean_distance = np.linalg.norm(array1 - array2)

# print("数组之间的欧式距离：", euclidean_distance)


"""
32bit Integer >> 16bit char
"""
# def list_to_char_string(lst):
#     # 將列表中的數字轉換為對應的ASCII字元並組成字串
#     char_string = ''.join([chr(num) for num in lst])
#     return char_string

# # 測試
# lst = [50, 49, 49, 52, 47, 49, 48, 47, 49, 56, 32, 48, 49, 58, 52, 57]
# char_string = list_to_char_string(lst)
# print(char_string)


# def time_str_to_int(time_str):
#     # 分割時間字串，取得秒、分、時
#     total_seconds_str, minutes_seconds_str = time_str.split(':')
#     minutes, seconds = map(int, minutes_seconds_str.split("'"))
    
#     # 計算總秒數
#     total_seconds = int(total_seconds_str)
#     total_seconds += minutes * 60 + seconds
    
#     # 將總秒數轉換為 32 位元整數
#     int_value = total_seconds & 0xFFFFFFFF  # 只保留低 32 位元
#     return int_value

# # 測試
# time_str = "667828:07'45"
# int_value = time_str_to_int(time_str)
# print(int_value)

"""
生成弧線
"""
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # 定義圓弧的參數
# r = 1  # 半徑
# theta1 = 0  # 起始角度
# theta2 = np.pi / 2  # 結束角度（90度）

# # 生成圓弧上的點
# theta = np.linspace(theta1, theta2, 100)  # 在起始角度和結束角度之間均勻分佈的角度值
# x = r * np.cos(theta)
# y = r * np.sin(theta)
# z = np.zeros_like(x)  # 在xy平面上

# # 取樣40個點
# num_samples = 40
# indices = np.linspace(0, len(theta) - 1, num_samples, dtype=int)
# x_samples = x[indices]
# y_samples = y[indices]
# z_samples = z[indices]

# # 輸出40個點的座標
# for i in range(num_samples):
#     print(f"Point {i+1}: ({x_samples[i]}, {y_samples[i]}, {z_samples[i]})")

# # 繪製圓弧
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(x, y, z)

# # 設置圖形屬性
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('3D Circle Arc')

# # 顯示圖形
# plt.show()

"""
Spline
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# # 定義a、b和c的座標
# a = np.array([0, 0, 0])
# b = np.array([6, 1, 0])
# c = np.array([7, 7, 0])

# # 設置控制點
# x = [a[0], b[0], c[0]]
# y = [a[1], b[1], c[1]]
# z = [a[2], b[2], c[2]]

# # 使用樣條插值函數
# t = [0, 1, 2]  # 參數t的範圍
# cs_x = CubicSpline(t, x, bc_type='natural')
# cs_y = CubicSpline(t, y, bc_type='natural')
# cs_z = CubicSpline(t, z, bc_type='natural')

# # 生成樣條曲線上的點
# t_new = np.linspace(0, 2, 40)  # 新的參數範圍
# x_spline = cs_x(t_new)
# y_spline = cs_y(t_new)
# z_spline = cs_z(t_new)

# # 繪製曲線
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(x_spline, y_spline, z_spline)

# # 將控制點繪製到曲線上
# ax.scatter(x, y, z, color='red', label='Control Points')

# # 設置圖形屬性
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('Spline Curve Connecting Points A, B, and C')

# # 顯示圖形
# plt.show()

# def cubicSpline(startPoint, endPoint):
#     """
#     Args:
#         startPoint: [x, y, z], type:ndarray.
#         endPoint: [x, y, z], type:ndarray.

#     """ 
#     # 設置控制點
#     x = [startPoint[0], (endPoint[0]-startPoint[0])*0.88, endPoint[0]]
#     y = [startPoint[1], (endPoint[1]-startPoint[1])*0.12, endPoint[1]]
#     z = [startPoint[2], (endPoint[2]-startPoint[2])/2   , endPoint[2]]
#     controlPoint = np.array([x, y, z])

#     # 使用樣條插值函數
#     t = [0, 1, 2]  # 參數t的範圍
#     cs_x = CubicSpline(t, x, bc_type='natural')
#     cs_y = CubicSpline(t, y, bc_type='natural')
#     cs_z = CubicSpline(t, z, bc_type='natural')

#     # 生成樣條曲線上的點
#     t_new = np.linspace(0, 2, 40)  # 新的參數範圍
#     x_spline = cs_x(t_new)
#     y_spline = cs_y(t_new)
#     z_spline = cs_z(t_new)
    
#     return x_spline, y_spline, z_spline, controlPoint

# startPoint = [0, 0, 0]
# endPoint   = [7, 7, 0]
# x_spline, y_spline, z_spline, controlPoint = cubicSpline(startPoint, endPoint)

# # 繪製曲線
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(x_spline, y_spline, z_spline)

# # 將控制點繪製到曲線上
# ax.scatter(controlPoint[0], controlPoint[1], controlPoint[2], color='red', label='Control Points')

# # 設置圖形屬性
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.set_title('Spline Curve Connecting Points A, B, and C')

# # 顯示圖形
# plt.show()

"""
B-Spline
"""
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import BSpline

# # 控制點
# # points = np.array([[0, 0], [1, 1], [2, -1], [3, 0], [4, 2]])
# points = np.array([[0, 0], [4, 0], [6, 2], [6, 5]])

# # 次數
# degree = 3

# # 節點向量
# num_knots = len(points) + degree + 1
# knots = np.linspace(0, 1, num_knots)

# # 生成 B-spline 曲線
# bspline = BSpline(knots, points, degree)

# # 生成曲線上的點
# num_points = 1000
# t_new = np.linspace(0, 1, num_points)
# curve_points = bspline(t_new)



# # 繪製曲線
# plt.plot(points[:, 0], points[:, 1], 'bo-', label='Control Points')
# plt.plot(curve_points[:, 0], curve_points[:, 1], 'r-', label='B-spline Curve')
# plt.title('B-spline Curve')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.axis('equal')
# plt.show()

import numpy as np

# 創建兩個形狀為 (993, 1) 和 (998, 1) 的 NumPy 數組
a = np.random.rand(993, 1)
b = np.random.rand(998, 1)

# 計算需要填充的行數
num_rows_to_pad = b.shape[0] - a.shape[0]

# 將數組 a 進行填充
a_padded = np.pad(a, ((0, num_rows_to_pad), (0, 0)), mode='constant')

# 垂直堆疊 a 和 b
result = np.vstack((a, b))

# 輸出結果的形狀
print(result.shape)