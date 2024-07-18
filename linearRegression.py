
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
"""
線性回歸模型
"""

# # 讀取用戶上傳的 CSV 文件
# file_path = 'dataBase/Experimental_data/20240604/VariableSpeedResult.csv'
# data = pd.read_csv(file_path)

# # 分離特徵和目標變量
# X = data[['Speed']].values
# # X = data[['Current']].values
# Y = data['WeldBeadWidth'].values

# # 將數據分為訓練集和測試集
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# # 建立線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X_train, Y_train)

# # 預測
# Y_pred = model.predict(X_test)

# # 評估模型
# mse = mean_squared_error(Y_test, Y_pred)
# r2 = r2_score(Y_test, Y_pred)

# # 顯示模型的係數和截距
# coef = model.coef_[0]
# intercept = model.intercept_

# # 繪製回歸線圖
# plt.scatter(X, Y, color='blue')
# plt.plot(X, model.predict(X), color='red')
# plt.xlabel('Welding speed(mm/s)')
# # plt.xlabel('Welding current(A)')
# plt.ylabel('Weld bead width(mm)')
# plt.title('Model of weld bead width and welding speed(linear regression)')
# # plt.title('Model of weld bead width and welding current(linear regression)')
# plt.show()

# # 顯示回歸方程式和評估結果
# print(mse, r2, coef, intercept)

# # 顯示回歸方程式
# print(f'The linear regression equation is: WeldBeadWidth = {coef} * Speed + {intercept}')
# # print(f'The linear regression equation is: WeldBeadWidth = {coef} * Current + {intercept}')



"""
多項式回歸模型
"""
# file_path = 'dataBase/Experimental_data/20240604/VariableCurrentResult_cde.csv'
# data = pd.read_csv(file_path)

# # Prepare the data
# X = data[['Current']].values
# y = data['WeldBeadWidth'].values


# # 創建多項式特徵
# poly = PolynomialFeatures(degree=2)
# X_poly = poly.fit_transform(X)

# # 擬合多項式回歸模型
# poly_regressor = LinearRegression()
# poly_regressor.fit(X_poly, y)
# y_pred_poly = poly_regressor.predict(X_poly)

# # 生成曲線數據
# X_seq = np.linspace(X.min(), X.max(), 300).reshape(-1, 1)
# X_seq_poly = poly.transform(X_seq)
# y_seq_poly = poly_regressor.predict(X_seq_poly)

# # 繪製多項式回歸曲線
# plt.figure(figsize=(10, 6))
# plt.scatter(X, y, color='blue', label='Data point')
# plt.plot(X_seq, y_seq_poly, color='red', label='Polynomial regression (square)')
# plt.title('Model of welding current and weld bead width (Polynomial regression(square))')
# plt.xlabel('Welding Current(A))')
# plt.ylabel('Weld Bead Width(mm))')
# plt.legend()
# plt.grid(True)
# plt.show()

# # 提取多項式回歸方程式的係數
# coefficients = poly_regressor.coef_
# intercept = poly_regressor.intercept_

# # 顯示方程式
# equation = f"y = {intercept:.2f}"
# for i in range(1, len(coefficients)):
#     equation += f" + ({coefficients[i]:.2f} * X^{i})"
# print(equation)

"""
角接 無填料
二元一次線性回歸
"""

# # 數據輸入
# data1 = {
#     'Speed': [1.5, 1.5, 1, 1, 2, 2, 1.5, 1.5, 1, 1, 2, 2],
#     'WeldBeadWidth': [6.1, 6.7, 7.7, 7.4, 4.9, 5.1, 6.1, 6.3, 7.1, 7.3, 4.9, 5.25]
# }
# data2 = {
#     'Current': [50, 50, 45, 45, 55, 55, 50, 50, 45, 45, 55, 55, 50, 50, 60, 60, 70, 70],
#     'WeldBeadWidth': [6.3, 6.2, 4.8, 5, 6.3, 6.6, 6, 6.3, 4.4, 4.95, 6, 6.5, 6.25, 5.95, 8, 7.9, 9.1, 9.5]
# }

# df1 = pd.DataFrame(data1)
# df2 = pd.DataFrame(data2)

# # 合併數據
# df1['Current'] = None
# df2['Speed'] = None
# df = pd.concat([df1, df2], ignore_index=True)

# # 填充缺失值
# df['Speed'] = df['Speed'].fillna(df['Speed'].mean())
# df['Current'] = df['Current'].fillna(df['Current'].mean())

# # 分離特徵和目標變量
# X = df[['Speed', 'Current']].values
# Y = df['WeldBeadWidth'].values

# # 將數據分為訓練集和測試集
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# # 建立線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X_train, Y_train)

# # 預測
# Y_pred = model.predict(X_test)

# # 評估模型
# mse = mean_squared_error(Y_test, Y_pred)
# r2 = r2_score(Y_test, Y_pred)

# # 顯示模型的係數和截距
# coef = model.coef_
# intercept = model.intercept_

# # 顯示回歸方程式和評估結果
# print(f'Mean Squared Error (MSE): {mse}')
# print(f'R-squared (R2): {r2}')
# print(f'Regression Coefficients: {coef}')
# print(f'Intercept: {intercept}')

# # 顯示回歸方程式
# print(f'The linear regression equation is: WeldBeadWidth = {coef[0]} * Speed + {coef[1]} * Current + {intercept}')

# # 繪製回歸曲線圖
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # 散點圖
# ax.scatter(df['Speed'], df['Current'], df['WeldBeadWidth'], color='blue')

# # 計算平面上的點
# xx, yy = np.meshgrid(np.linspace(df['Speed'].min(), df['Speed'].max(), 10), 
#                      np.linspace(df['Current'].min(), df['Current'].max(), 10))
# zz = coef[0] * xx + coef[1] * yy + intercept

# # 繪製回歸平面
# ax.plot_surface(xx, yy, zz, alpha=0.5, rstride=100, cstride=100)

# ax.set_xlabel('Speed (mm/s)')
# ax.set_ylabel('Current (A)')
# ax.set_zlabel('WeldBeadWidth (mm)')
# ax.set_title('3D Regression Plane')

# plt.show()

"""
二元一次的測試模型
"""
# Speed = 1.5
# Current = 50

# WeldBeadWidth = -2.576858070041016 * Speed + 0.1740194708613152 * Current + 0.9745357641862364
# print(WeldBeadWidth)

"""
相關係數矩陣計算(無填料角接)
銲接電流、銲接速度 對 銲道寬度的影響係數
"""
# # 數據輸入
# data1 = {
#     'Speed': [1.5, 1.5, 1, 1, 2, 2, 1.5, 1.5, 1, 1, 2, 2]+[1.5]*18,
#     'Current': [50]*12+[50, 50, 45, 45, 55, 55, 50, 50, 45, 45, 55, 55, 50, 50, 60, 60, 70, 70],
#     'WeldBeadWidth': [6.1, 6.7, 7.7, 7.4, 4.9, 5.1, 6.1, 6.3, 7.1, 7.3, 4.9, 5.25]+[6.3, 6.2, 4.8, 5, 6.3, 6.6, 6, 6.3, 4.4, 4.95, 6, 6.5, 6.25, 5.95, 8, 7.9, 9.1, 9.5]
# }
# data2 = {
#     'Current': [50, 50, 45, 45, 55, 55, 50, 50, 45, 45, 55, 55, 50, 50, 60, 60, 70, 70],
#     'WeldBeadWidth': [6.3, 6.2, 4.8, 5, 6.3, 6.6, 6, 6.3, 4.4, 4.95, 6, 6.5, 6.25, 5.95, 8, 7.9, 9.1, 9.5]
# }

# df = pd.DataFrame(data1)
# # df2 = pd.DataFrame(data2)

# # # 合併數據
# # df1['Current'] = None
# # df2['Speed'] = None
# # df = pd.concat([df1, df2], ignore_index=True)

# # # 填充缺失值
# # df['Speed'] = df['Speed'].fillna(df['Speed'].mean())
# # df['Current'] = df['Current'].fillna(df['Current'].mean())

# # # 分離特徵和目標變量
# # X = df[['Speed', 'Current']].values
# # Y = df['WeldBeadWidth'].values

# # # 將數據分為訓練集和測試集
# # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# # # 建立線性回歸模型
# # model = LinearRegression()

# # # 訓練模型
# # model.fit(X_train, Y_train)

# # # 預測
# # Y_pred = model.predict(X_test)

# # # 評估模型
# # mse = mean_squared_error(Y_test, Y_pred)
# # r2 = r2_score(Y_test, Y_pred)

# # # 顯示模型的係數和截距
# # coef = model.coef_
# # intercept = model.intercept_

# # # 顯示回歸方程式和評估結果
# # print(f'Mean Squared Error (MSE): {mse}')
# # print(f'R-squared (R2): {r2}')
# # print(f'Regression Coefficients: {coef}')
# # print(f'Intercept: {intercept}')

# # # 顯示回歸方程式
# # print(f'The linear regression equation is: WeldBeadWidth = {coef[0]} * Speed + {coef[1]} * Current + {intercept}')

# # # 繪製回歸曲線圖
# # fig = plt.figure()
# # ax = fig.add_subplot(111, projection='3d')

# # # 散點圖
# # ax.scatter(df['Speed'], df['Current'], df['WeldBeadWidth'], color='blue')

# # # 計算平面上的點
# # xx, yy = np.meshgrid(np.linspace(df['Speed'].min(), df['Speed'].max(), 10), 
# #                      np.linspace(df['Current'].min(), df['Current'].max(), 10))
# # zz = coef[0] * xx + coef[1] * yy + intercept

# # # 繪製回歸平面
# # ax.plot_surface(xx, yy, zz, alpha=0.5, rstride=100, cstride=100)

# # ax.set_xlabel('Speed (mm/s)')
# # ax.set_ylabel('Current (A)')
# # ax.set_zlabel('WeldBeadWidth (mm)')
# # ax.set_title('3D Regression Plane')

# # plt.show()

# # 檢查自變數之間的相關性
# correlation_matrix = df[['Speed', 'Current']].corr()
# print(correlation_matrix)

"""
對接 有填料 變電流 線性回歸
WeldBeadWidth = 0.08000000000000002 * Current + 0.6999999999999993
"""
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score

# # 數據輸入()
# data = {
#     'Current': [50, 50, 50, 60, 60, 60, 70, 70, 70],
#     'Speed': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
#     'FeedSpeed': [90, 90, 90, 95, 95, 95, 100, 100, 100],
#     'WeldBeadWidth': [4.54, 4.49, 4.59, 5.82, 5.7, 5.94, 6.14, 6.06, 6.22]
# }

# df = pd.DataFrame(data)

# # 提取自變數和應變數
# X = df[['Current']].values
# y = df['WeldBeadWidth'].values

# # 創建線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X, y)

# # 預測
# y_pred = model.predict(X)

# # 評估模型
# mse = mean_squared_error(y, y_pred)
# r2 = r2_score(y, y_pred)
# coef = model.coef_[0]
# intercept = model.intercept_

# # 繪製回歸線
# plt.scatter(X, y, color='blue', label='Data Points')
# plt.plot(X, y_pred, color='red', label='Regression Line')
# plt.xlabel('Welding Current')
# plt.ylabel('Weld Bead Width')
# plt.title('Linear Regression: Welding Current vs Weld Bead Width')
# plt.legend()
# plt.show()

# # 顯示結果
# print(f"Mean Squared Error: {mse}")
# print(f"R^2 Score: {r2}")
# print(f"Coefficient: {coef}")
# print(f"Intercept: {intercept}")

# # 顯示回歸方程式
# print(f"回歸方程式: y = {coef} * Current + {intercept}")

"""
對接 有填料 變速度 線性回歸
WeldBeadWidth = -2.205000000000001 * Speed + 8.982500000000002
"""
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score

# # 數據輸入
# data = {
#     'Current': [60, 60, 60, 60, 60, 60, 60, 60, 60],
#     'Speed': [1, 1, 1, 1.5, 1.5, 1.5, 2, 2, 2],
#     'FeedSpeed': [100, 100, 100, 95, 95, 95, 95, 95, 95],
#     'WeldBeadWidth': [6.705, 6.61, 6.8, 5.7, 5.82, 5.94, 4.5, 4.47, 4.53]
# }

# df = pd.DataFrame(data)

# # 提取自變數和應變數
# X = df[['Speed']].values
# y = df['WeldBeadWidth'].values

# # 創建線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X, y)

# # 預測
# y_pred = model.predict(X)

# # 評估模型
# mse = mean_squared_error(y, y_pred)
# r2 = r2_score(y, y_pred)
# coef = model.coef_[0]
# intercept = model.intercept_

# # 繪製回歸線
# plt.scatter(X, y, color='blue', label='Data Points')
# plt.plot(X, y_pred, color='red', label='Regression Line')
# plt.xlabel('Welding Speed(mm/s)')
# plt.ylabel('Weld Bead Width(mm)')
# plt.title('Linear Regression: Welding Speed vs Weld Bead Width')
# plt.legend()
# plt.show()

# # 顯示結果
# print(f"Mean Squared Error: {mse}")
# print(f"R^2 Score: {r2}")
# print(f"Coefficient: {coef}")
# print(f"Intercept: {intercept}")

# # 顯示回歸方程式
# print(f"回歸方程式: y = {coef} * Speed + {intercept}")

"""
對接 有填料 二元一次線性回歸 
y = 0.09750000000000003 * Current + -1.9600000000000004 * Speed + 2.7333333333333325
"""
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score
# from mpl_toolkits.mplot3d import Axes3D

# # 數據輸入
# data = {
#     'Current': [50, 50, 50, 60, 60, 60, 70, 70, 70, 60, 60, 60, 60, 60, 60, 60, 60, 60],
#     'Speed': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1.5, 1.5, 1.5, 2, 2, 2],
#     'FeedSpeed': [90, 90, 90, 95, 95, 95, 90, 90, 90, 90, 90, 90, 95, 95, 95, 90, 90, 90],
#     'WeldBeadWidth': [4.54, 4.49, 4.59, 5.82, 5.7, 5.94, 6.49, 6.28, 6.7, 6.48, 6.575, 6.67, 5.7, 5.82, 5.94, 4.48, 4.75, 4.615]
# }

# df = pd.DataFrame(data)

# # 提取自變數和應變數
# X = df[['Current', 'Speed']].values
# y = df['WeldBeadWidth'].values

# # 創建線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X, y)

# # 預測
# y_pred = model.predict(X)

# # 評估模型
# mse = mean_squared_error(y, y_pred)
# r2 = r2_score(y, y_pred)
# coefficients = model.coef_
# intercept = model.intercept_

# # 顯示結果
# print(f"Mean Squared Error: {mse}")
# print(f"R^2 Score: {r2}")
# print(f"Coefficients: {coefficients}")
# print(f"Intercept: {intercept}")

# # 顯示回歸方程式
# print(f"回歸方程式: y = {coefficients[0]} * Current + {coefficients[1]} * Speed + {intercept}")

# # 繪製回歸平面圖
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(df['Current'], df['Speed'], df['WeldBeadWidth'], color='blue', label='Data Points')

# # 創建網格以繪製平面
# current_surf, speed_surf = np.meshgrid(np.linspace(df['Current'].min(), df['Current'].max(), 10), 
#                                        np.linspace(df['Speed'].min(), df['Speed'].max(), 10))
# weldbeadwidth_surf = model.predict(np.c_[current_surf.ravel(), speed_surf.ravel()]).reshape(current_surf.shape)

# # 繪製回歸平面
# ax.plot_surface(current_surf, speed_surf, weldbeadwidth_surf, color='red', alpha=0.5)
# ax.set_xlabel('Current')
# ax.set_ylabel('Speed')
# ax.set_zlabel('Weld Bead Width')
# ax.set_title('Linear Regression: Current and Speed vs Weld Bead Width')
# plt.show()


"""
角接 有填料 變電流 模型
銲道寬度 = 0.10750000000000001 * 銲接電流  -0.5833333333333339
"""
# # 數據輸入
# data = {
#     '銲接電流': [40, 40, 40, 50, 50, 50, 60, 60, 60],
#     '填料速度': [90, 90, 90, 85, 85, 85, 80, 80, 80],
#     '銲接速度': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
#     '銲道寬度': [3.69, 3.8, 3.745, 4.71, 4.76, 4.735, 6.14, 6.38, 6.26]
# }

# df = pd.DataFrame(data)

# # 提取自變數和應變數
# X = df[['銲接電流']].values
# y = df['銲道寬度'].values

# # 創建線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X, y)

# # 預測
# y_pred = model.predict(X)

# # 評估模型
# mse = mean_squared_error(y, y_pred)
# r2 = r2_score(y, y_pred)
# coef = model.coef_[0]
# intercept = model.intercept_

# # 繪製回歸線
# plt.scatter(X, y, color='blue', label='Data Points')
# plt.plot(X, y_pred, color='red', label='Regression Line')
# plt.xlabel('Welding Current(A)')
# plt.ylabel('Weld Bead Width(mm)')
# plt.title('Linear Regression: Welding Current vs Weld Bead Width')
# plt.legend()
# plt.show()

# # 顯示結果
# print(f"Mean Squared Error: {mse}")
# print(f"R^2 Score: {r2}")
# print(f"Coefficient: {coef}")
# print(f"Intercept: {intercept}")

# # 顯示回歸方程式
# print(f"回歸方程式: 銲道寬度 = {coef} * 銲接電流 + {intercept}")


"""
角接 有填料 變速度 模型
銲道寬度 = 0.12575 * 銲接電流 + -1.3741666666666665
"""
# # 數據輸入
# data = {
#     '銲接電流': [50, 50, 50, 50, 50, 50, 50, 50, 50],
#     '填料速度': [83, 83, 83, 85, 85, 85, 87, 87, 87],
#     '銲接速度': [1, 1, 1, 1.5, 1.5, 1.5, 2, 2, 2],
#     '銲道寬度': [5.75, 5.92, 5.835, 4.71, 4.76, 4.735, 4.09, 4.19, 4.14]
# }

# df = pd.DataFrame(data)

# # 提取自變數和應變數
# X = df[['銲接速度']].values
# y = df['銲道寬度'].values

# # 創建線性回歸模型
# model = LinearRegression()

# # 訓練模型
# model.fit(X, y)

# # 預測
# y_pred = model.predict(X)

# # 評估模型
# mse = mean_squared_error(y, y_pred)
# r2 = r2_score(y, y_pred)
# coef = model.coef_[0]
# intercept = model.intercept_

# # 繪製回歸線
# plt.scatter(X, y, color='blue', label='Data Points')
# plt.plot(X, y_pred, color='red', label='Regression Line')
# plt.xlabel('Welding Speed(mm/s)')
# plt.ylabel('Weld Bead Width(mm)')
# plt.title('Linear Regression: Welding Speed vs Weld Bead Width')
# plt.legend()
# plt.show()

# # 顯示結果
# print(f"Mean Squared Error: {mse}")
# print(f"R^2 Score: {r2}")
# print(f"Coefficient: {coef}")
# print(f"Intercept: {intercept}")

# # 顯示回歸方程式
# print(f"回歸方程式: 銲道寬度 = {coef} * 銲接速度 + {intercept}")

"""
角接 有填料
銲接電流、速度 對 填料速度 數學模型
"""
# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt

# # 準備數據
# data = {
#     '銲接電流': [60, 50, 40, 50, 50, 50],
#     '填料速度': [80, 85, 90, 83, 85, 87],
#     '銲接速度': [1.5, 1.5, 1.5, 1, 1.5, 2]
# }

# df = pd.DataFrame(data)

# # 建立回歸模型
# X = df[['銲接電流', '銲接速度']]
# y = df['填料速度']

# reg = LinearRegression().fit(X, y)

# # 獲取回歸係數和截距
# coef = reg.coef_
# intercept = reg.intercept_

# print("回歸係數:", coef)
# print("截距:", intercept)

# # 預測填料速度
# y_pred = reg.predict(X)

# # 繪製散點圖和回歸線
# plt.figure(figsize=(10, 6))
# plt.scatter(df['銲接電流'], df['填料速度'], color='blue', label='Actual Data')
# plt.scatter(df['銲接電流'], y_pred, color='red', label='Predicted Data')
# plt.xlabel('銲接電流')
# plt.ylabel('填料速度')
# plt.title('Regression Analysis of 銲接電流 and 銲接速度 vs 填料速度')
# plt.legend()
# plt.grid(True)

# # 顯示圖表
# plt.show()

"""
角接 有填料
銲接速度、焊接電流與銲道寬度之關係 二元一次數學模型
銲道寬度 = 0.1258 * 銲接電流 + -1.6950 * 銲接速度 + 1.1633
"""
# # 準備數據
# data = {
#     '銲接電流': [40, 40, 40, 50, 50, 50, 60, 60, 60, 50, 50, 50, 50, 50, 50, 50, 50, 50],
#     '銲接速度': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1, 1, 1, 1.5, 1.5, 1.5, 2, 2, 2],
#     '銲道寬度': [3.69, 3.8, 3.745, 4.71, 4.76, 4.735, 6.14, 6.38, 6.26, 5.75, 5.92, 5.835, 4.71, 4.76, 4.735, 4.09, 4.19, 4.14]
# }

# df = pd.DataFrame(data)

# # 建立回歸模型
# X = df[['銲接電流', '銲接速度']]
# y = df['銲道寬度']

# reg = LinearRegression().fit(X, y)

# # 獲取回歸係數和截距
# coef = reg.coef_
# intercept = reg.intercept_


# # 打印回歸方程式
# print(f'回歸方程式: 銲道寬度 = {coef[0]:.4f} * 銲接電流 + {coef[1]:.4f} * 銲接速度 + {intercept:.4f}')


# # 生成網格數據
# x_range = np.linspace(df['銲接電流'].min(), df['銲接電流'].max(), 100)
# y_range = np.linspace(df['銲接速度'].min(), df['銲接速度'].max(), 100)
# x_grid, y_grid = np.meshgrid(x_range, y_range)
# z_grid = reg.predict(np.c_[x_grid.ravel(), y_grid.ravel()]).reshape(x_grid.shape)

# # 繪製三維曲面圖
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(x_grid, y_grid, z_grid, alpha=0.5, cmap='viridis')
# ax.scatter(df['銲接電流'], df['銲接速度'], df['銲道寬度'], color='r', label='Actual Data')

# ax.set_xlabel('Welding Current(A)')
# ax.set_ylabel('Welding Speed(mm/s)')
# ax.set_zlabel('Weld Bead Width')
# ax.set_title('3D Surface Plot of Welding Current and Welding Speed vs Weld Bead Width')

# plt.legend()
# plt.show()

"""

"""
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from scipy.interpolate import griddata

# # 定義回歸方程
# def equation1(current):
#     return 0.12575 * current - 1.3741666666666665

# def equation2(Speed):
#     return -1.695 * Speed  + 7.446

# # 生成網格數據
# current_range = np.linspace(40, 60, 100)
# speed_range = np.linspace(1, 2, 100)
# current_grid, speed_grid = np.meshgrid(current_range, speed_range)

# # 計算兩個方程的預測值
# z1 = equation1(current_grid)
# z2 = equation2(speed_grid)

# # 將兩個方程的結果組合起來
# current_combined = np.concatenate([current_grid.ravel(), current_grid.ravel()])
# speed_combined = np.concatenate([speed_grid.ravel(), speed_grid.ravel()])
# z_combined = np.concatenate([z1.ravel(), z2.ravel()])


# # 使用三次樣條插值生成曲面
# grid_x, grid_y = np.mgrid[40:60:100j, 1:2:100j]
# grid_z = griddata((current_combined, speed_combined), z_combined, (grid_x, grid_y), method='cubic')

# # 繪製三維曲面圖
# fig = plt.figure(figsize=(12, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', alpha=0.7)

# # 繪製原始的兩個方程的平面
# # ax.scatter(current_grid, speed_grid, z1, color='r', label='Equation 1 Data')
# # ax.scatter(current_grid, speed_grid, z2, color='b', label='Equation 2 Data')

# # 設置標籤和標題
# ax.set_xlabel('銲接電流')
# ax.set_ylabel('銲接速度')
# ax.set_zlabel('銲道寬度')
# ax.set_title('3D Fitted Surface Plot of 銲接電流 and 銲接速度 vs 銲道寬度')

# plt.legend()
# plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from scipy.interpolate import griddata

# 定義回歸方程
def equation1(current):
    return 0.12575 * current - 1.3741666666666665

def equation2(speed):
    return -1.695 * speed + 7.446

# 生成網格數據
current_range = np.linspace(40, 60, 100)
speed_range = np.linspace(1, 2, 100)
current_grid, speed_grid = np.meshgrid(current_range, speed_range)

# 計算兩個方程的預測值
z1 = equation1(current_grid)
z2 = equation2(speed_grid)

# 將兩個方程的結果組合起來
current_combined = np.concatenate([current_grid.ravel(), current_grid.ravel()])
speed_combined = np.concatenate([speed_grid.ravel(), speed_grid.ravel()])
z_combined = np.concatenate([z1.ravel(), z2.ravel()])

# 使用 griddata 進行插值
grid_x, grid_y = np.mgrid[40:60:100j, 1:2:100j]
grid_z = griddata((current_combined, speed_combined), z_combined, (grid_x, grid_y), method='cubic')

# 繪製三維曲面圖
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(grid_x, grid_y, grid_z, cmap='viridis', alpha=0.7)

# 繪製原始的兩個方程的平面
ax.scatter(current_grid, speed_grid, z1, color='r', label='Equation 1 Data')
ax.scatter(current_grid, speed_grid, z2, color='b', label='Equation 2 Data')

# 設置標籤和標題
ax.set_xlabel('銲接電流')
ax.set_ylabel('銲接速度')
ax.set_zlabel('銲道寬度')
ax.set_title('3D Interpolated Surface Plot of 銲接電流 and 銲接速度 vs 銲道寬度')

plt.legend()
plt.show()