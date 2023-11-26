import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv


def analyze():
    # 指定三個 CSV 檔案路徑
    file1_path = 'Data1122\ErrorMat4X4\Mat4X4errorGUN_Welding_1.csv'   
    file2_path = 'Data1122\ErrorMat4X4\Mat4X4errorGUN_Welding_2.csv'
    file3_path = 'Data1122\ErrorMat4X4\Mat4X4errorGUN_Welding_3.csv'

    # 讀取 CSV 檔案
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    df3 = pd.read_csv(file3_path)

    # 獲取 'Pz' 列的數據
    Pz_data1 = df1['Py']
    Pz_data2 = df2['Py']
    Pz_data3 = df3['Py']

    # 繪製折線圖
    plt.plot(Pz_data1, label='Back 1')
    plt.plot(Pz_data2, label='Back 2')
    plt.plot(Pz_data3, label='Back 3')

    # 添加標題和標籤
    plt.title('Px Back')
    plt.xlabel('Count')
    plt.ylabel('Px Error(mm)')

    plt.grid(True)
    # 顯示圖例
    plt.legend()

    # 顯示圖表
    plt.show()

def draw_chart():

    # 讀取 CSV 檔案
    # 假設 CSV 檔案中有一欄名為 '日期'，另一欄名為 '數值'
    # 請根據實際情況修改文件路徑和欄位名稱
    csv_file_path = 'Data/Mat4X4errorGUN_Go_3.csv'
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

    plt.plot(frequency, Pz, linestyle='-', color='b')

    # 設定圖表標題和標籤
    plt.title('Error')
    plt.xlabel('frequency')
    plt.ylabel('Pz(mm)')

    # 顯示網格線
    plt.grid(True)

    # 旋轉日期標籤，以避免重疊
    plt.xticks(rotation=45)

    # 顯示圖表
    plt.show()

analyze()