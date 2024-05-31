
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# 讀取用戶上傳的 CSV 文件
file_path = 'dataBase/weldBeadWidthToSpeed_1.csv'
data = pd.read_csv(file_path)

# 分離特徵和目標變量
X = data[['Speed']].values
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
plt.xlabel('Speed(mm/s)')
plt.ylabel('Weld bead width(mm)')
plt.title('Model of weld bead width and welding speed(linear regression)')
plt.show()

# 顯示回歸方程式和評估結果
print(mse, r2, coef, intercept)
"""
width = -1.261682802674918*Speed + 6.45529993013275
width = -1.262*Speed + 6.455
"""
