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
import threading
import time

# flag
flagMOVE_0 = False
flagMOVE_1 = False
flagMOVE_2 = False
flagMOVE_3 = False
flagMOVE_4 = False
flagMOVE_5 = False
flagArcon = False
flagWireout = False
flagWireback = False

# Data sequence index value extracted from the database
dataIndex = 0
sysTimer = 0

# data
NextPos = []


def sendMoveCMD():
    """到達上一時刻的目標位置後，寄送下一刻的MOVE CMD
    - Flag: MOVE(only one)
    """
    global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4, dataIndex, flagArcon, flagWireout, flagWireback, NextPos
    
    if flagMOVE_0 is True:
        print("Robot GO to 預起弧點")
        time.sleep(0.03)
        flagMOVE_0 = False

    elif flagMOVE_1 is True:
        print("Robot GO to 起弧點")
        time.sleep(0.03)
        flagMOVE_1 = False

    elif flagMOVE_2 is True:
        print("Robot GO to 收弧點")
        time.sleep(0.03)
        flagMOVE_2 = False
    
    elif flagMOVE_3 is True:
        print("Robot GO to 預回點")
        time.sleep(0.03)
        flagMOVE_3 = False

    elif flagMOVE_4 is True:
        print("Robot GO to 回原點")
        time.sleep(0.03)
        flagMOVE_4 = False

    else:
        time.sleep(0.01)
        print("pass")

def readNowPosCMD():
    """無限讀取位置，當位置在預定目標位置上時，提醒可以送下一個目標位置指令
    """
    global flagMOVE_0, flagMOVE_1, flagMOVE_2, flagMOVE_3, flagMOVE_4, dataIndex, sysTimer, flagArcon, flagWireout, flagWireback, NextPos
    print(sysTimer)
    # TODO 有問題
    if sysTimer == 0:
        flagMOVE_0 = True
        print("Go to 預起弧點") 

    elif round(sysTimer, 2) == 10:
        flagMOVE_1 = True
        print("Go to 起弧點")
    
    elif round(sysTimer, 2) == 50:
        flagMOVE_2 = True
        print("Go to 收弧點")
    
    elif round(sysTimer, 2) == 60:
        flagMOVE_3 = True
        print("Go to 預回原點")
    
    elif round(sysTimer, 2) == 70:
        flagMOVE_4 = True
        print("Go to 回原點")

    else:
        time.sleep(0.025)
        print("readNowpos cmd")
    

while True:
    
    # Create a new thread
    sendcmd = threading.Thread(target=sendMoveCMD)
    readcmd = threading.Thread(target=readNowPosCMD)

    # Start the thread
    sendcmd.start()
    readcmd.start()

    # Wait for the thread to finish (optional)
    sendcmd.join()
    readcmd.join()

    sysTimer += 0.1
    if sysTimer >= 70:
        break

