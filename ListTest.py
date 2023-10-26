import numpy as np
pi = np.pi

# # 创建一个大小为6x1的数组
# norm_array = np.array([[0.78539816],
#                   [-0.48669496],
#                   [0.84806208],
#                   [33.0623015],
#                   [2.84790716],
#                   [-21.06274625]])
# for i in range(6):
#     while(norm_array[i,0]>pi or norm_array[i,0]<-pi):
#         if norm_array[i,0] >= pi:
#             norm_array[i,0] -= pi
#             print(norm_array[i,0])
#         elif norm_array[i,0] <= -pi:
#             norm_array[i,0] += pi
#             print(norm_array[i,0])
#         else:
#             pass
#             print(norm_array[i,0])

# print("正規化", norm_array)

Test = np.zeros((100,2))
Test[2] = 100
T21 = Test[2,1]
print(Test)