import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取 CSV 檔案
# 假設 CSV 檔案中有一欄名為 '日期'，另一欄名為 '數值'
# 請根據實際情況修改文件路徑和欄位名稱
csv_file_path = 'Data/Mat4X4errorGUN_Go_1.csv'
df = pd.read_csv(csv_file_path)

# 顯示 CSV 檔案的前幾行
print(df.head())

# CSV檔案形狀
num_rows = df.shape

# 次數
frequency = np.arange(df.shape[0])


# 提取 '日期' 和 '數值' 欄位的數據
Px = df['Px']
Py = df['Py']
Pz = df['Pz']

# 設定圖表
plt.figure(figsize=(10, 6))
'''
plt.plot(x, y, label='sin(x)', color='blue', linestyle='-', marker='o', markersize=5)
x 和 y: 要繪製的數據的 x 和 y 值。
label: 線條的標籤，用於圖例。
color: 線條的顏色，可以是字符串（如 'red'）或 RGB 值（如 (0.2, 0.4, 0.6)）。
linestyle: 線條的風格，例如 '-'（實線）、'--'（虛線）、':'（點線）等。
marker: 標記數據點的符號，例如 'o'（圓點）、's'（正方形）、'^'（三角形）等。
markersize: 標記的大小。
'''

plt.plot(frequency, Py, linestyle='-', color='b')

# 設定圖表標題和標籤
plt.title('ErrorX')
plt.xlabel('Px(mm)')
plt.ylabel('frequency')

# 顯示網格線
plt.grid(True)

# 旋轉日期標籤，以避免重疊
plt.xticks(rotation=45)

# 顯示圖表
plt.show()