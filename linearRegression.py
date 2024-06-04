
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

"""
線性回歸模型
"""

# 讀取用戶上傳的 CSV 文件
file_path = 'dataBase/Experimental_data/20240604/VariableSpeedResult.csv'
data = pd.read_csv(file_path)

# 分離特徵和目標變量
X = data[['Speed']].values
# X = data[['Current']].values
Y = data['WeldBeadWidth'].values

# 將數據分為訓練集和測試集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 建立線性回歸模型
model = LinearRegression()

# 訓練模型
model.fit(X_train, Y_train)

# 預測
Y_pred = model.predict(X_test)

# 評估模型
mse = mean_squared_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

# 顯示模型的係數和截距
coef = model.coef_[0]
intercept = model.intercept_

# 繪製回歸線圖
plt.scatter(X, Y, color='blue')
plt.plot(X, model.predict(X), color='red')
plt.xlabel('Welding speed(mm/s)')
# plt.xlabel('Welding current(A)')
plt.ylabel('Weld bead width(mm)')
plt.title('Model of weld bead width and welding speed(linear regression)')
# plt.title('Model of weld bead width and welding current(linear regression)')
plt.show()

# 顯示回歸方程式和評估結果
print(mse, r2, coef, intercept)

# 顯示回歸方程式
print(f'The linear regression equation is: WeldBeadWidth = {coef} * Speed + {intercept}')
# print(f'The linear regression equation is: WeldBeadWidth = {coef} * Current + {intercept}')



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