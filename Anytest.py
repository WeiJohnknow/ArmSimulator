# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataBase import dataBase

# # 生成三维坐标的数据
# x = np.linspace(0, 3, 100)
# y = np.linspace(0, 4, 100)
# z = np.sin(x) + np.cos(y)

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

df = dataBase().Load("dataBase\MatrixPathPlanning.csv")
Px =[]
Py=[]
Pz=[]
t=[]
data = {'Px': Px,
        'Py': Py,
        'Pz': Pz,
        'time': t}

for i in range(df.shape[0]):
    Px.append(df['Px'][i])
    Py.append(df['Py'][i])
    Pz.append(df['Pz'][i])
    t.append(df['time'][i])


# 绘制三张图
plt.figure(figsize=(10, 6))

# 图1：Px vs. time
plt.subplot(3, 1, 1)
plt.plot(data['time'], data['Px'])
plt.title('Px vs. time')
plt.xlabel('time')
plt.ylabel('Px')

# 图2：Py vs. time
plt.subplot(3, 1, 2)
plt.plot(data['time'], data['Py'])
plt.title('Py vs. time')
plt.xlabel('time')
plt.ylabel('Py')

# 图3：Pz vs. time
plt.subplot(3, 1, 3)
plt.plot(data['time'], data['Pz'])
plt.title('Pz vs. time')
plt.xlabel('time')
plt.ylabel('Pz')

# 调整布局
plt.tight_layout()

# 显示图形
plt.show()


# # 两个点的坐标
# point1 = (4.85, 0, 2.34)
# point2 = (4.87075, -0.02, 2.3183)

# # 计算距离
# distance = np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2 + (point2[2] - point1[2])**2)

# # 输出距离
# print(f"The distance between the two points is: {distance}")
# v = round((distance*1000)/0.03, 3)
# print("速度",v,"mm/s")