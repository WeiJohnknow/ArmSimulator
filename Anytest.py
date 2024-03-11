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
dict={}

dict = {'0':[2,3,4,5],
        '1':[3,4,5,6]}
for i in range(2):
    print(dict[str(i)][0])
    print(dict[f'{i}'][0])
