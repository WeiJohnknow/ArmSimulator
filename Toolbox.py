from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import timeit

class TimeTool:
    def __init__(self) -> None:
        pass

    def ReadNowTime(self):
        Nowtime = datetime.now()
    
        return Nowtime
    
    def TimeError(self, beforeTime, afterTime):
        """Calculate Time error
        - args:
            - Before time
            - After time
        - return: 
            - dtype: dict
            - Key: minute、second、millisecond、microsecond, totalus
            # totalus : Total microsecond difference(若單位過天會有Bug)
        """


        # 時間差
        time_err = afterTime - beforeTime
        # 時差
        hours_err, remainder = divmod(time_err.total_seconds(), 3600)
        # 分差
        minutes_err, seconds_err = divmod(time_err.total_seconds(), 60)
        # 秒差
        second_err = int(seconds_err)
        # 毫秒差
        millisecond_err = int((time_err.microseconds / 1000) + second_err * 1000)
        # 微秒差
        microsecond_err = (time_err.seconds * 1000000) + (time_err.microseconds)

        # 總微秒差
        total_ms_err = int(time_err.microseconds + second_err *1000*1000 + (minutes_err*60*1000*1000) + (hours_err*60*60*1000*1000))

        timeData = {"hour":hours_err,
                    "minute": minutes_err,
                    "second": second_err,
                    "millisecond": millisecond_err,
                    "microsecond": microsecond_err,
                    "totalus": total_ms_err}
        
        return timeData
    
    def sysTime(self, startTime, startNode, nowTime, sampleTime):
        """系統時間 Unit: microscond
        - Args: 
            - startTime
            - startNode: It's int.
            - nowTime
            - sampleTime: Unit is second.
        - Return: 
            - sysTime: 系統時間(由系統開始運作➔此時此刻之時間差)
            - nowNode:　依據系統時間，此時此刻應該要到達的軌跡index
        """
        
        timerr = self.TimeError(startTime, nowTime)
        
        # 軌跡index計算公式
        node = int(timerr["totalus"] // (sampleTime*1000*1000))

        # 依據時間差，應該要到達的軌跡index
        nowNode = startNode + node

        # 系統時間(單位: 微秒)
        sysTime = timerr["totalus"]

        return sysTime, nowNode
    
    def time_sleep(self, seconds):
        """
            - Args: time
            - time unit :second
        """
        start_time = timeit.default_timer()
        target_time = start_time + seconds

        while timeit.default_timer() < target_time:
            pass
        

        

        

    
class CsvTool:
    def __init__(self) -> None:
        pass

    def SaveCsv(self, data, fileName):
        """Save Data to CSV
        
        Input data shape:
            1.One-dimensional Array(大量)

            2.Matrix 4x4(單筆)

            3.Matrix 6x1()

        Args:
            data, fileName
        """
        dataShape = data.shape
        
        if len(dataShape) == 1:
            # 將輸入資料轉換為(n , 1), 並存入CSV
            column = dataShape[0]
            dataBuffer = data.copy().reshape(column,1)
            with open(fileName, mode='a', newline='') as file:
                writer = csv.writer(file)
        
                # 寫入數據
                # writer.writerow(dataBuffer.flatten())
                for row in dataBuffer:
                     writer.writerow(row)

        elif len(dataShape) == 2 :
            # 輸入為4X4
            # 將輸入資料轉換為(1 , 16), 並存入CSV
            data1x16 = np.zeros((1,16))

            # 轉置➜攤平➜複製(不影響Row data)
            data1x16 = data.T.ravel().copy()

            # 標頭檔
            header = np.array([['Xx', 'Xy', 'Xz', '0', 'Yx', 'Yy', 'Yz', '0', 'Zx', 'Zy', 'Zz', '0', 'Px', 'Py', 'Pz', '1']])

            with open(fileName, mode='a', newline='') as file:
                writer = csv.writer(file)

                # 若CSV檔是空的，第一行寫入標題檔
                if file.tell() == 0:
                    writer.writerows(header)
        
                # 寫入數據
                writer.writerow(data1x16.flatten())
            




    def LoadCsv(self, fileName):
        """Load Data is Matrix 1x16

        return:
            type : ndarray
        """
        
        # Load CSV(type is DataFrame)
        dataBuffer = pd.read_csv(fileName)
        # Type: dataframe ➜ ndarray
        data = dataBuffer.values

        return data


    
    def analyze(self):
        # 指定三個 CSV 檔案路徑
        file1_path = 'Data1122\RealMat4X4\Mat4X4GUN_Welding_3.csv'   
        file2_path = 'Data1122\SimularMat4X4\Mat4X4GUN_Welding_3.csv'
        # file3_path = 'Data1122\ErrorMat4X4\Mat4X4errorGUN_Welding_2.csv'

        # 讀取 CSV 檔案
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        # df3 = pd.read_csv(file3_path)

        # 獲取 'Pz' 列的數據
        Pz_data1 = df1['Pz']
        Pz_data2 = df2['Pz']
         
        # Pz_data3 = df3['Px']

        # 繪製折線圖
        plt.plot(Pz_data1, label='Real')
        plt.plot(Pz_data2, label='Simulator')
        # plt.plot(Pz_data3, label='Back 3')

        # 添加標題和標籤
        plt.title('Pz RowData 3')
        plt.xlabel('Count')
        plt.ylabel('Pz(m)')

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

# if __name__ == "__main__":
    # Csv = CsvTool()
    # testdata = np.array([[0,4,8,12],
    #                             [1,5,9,13],
    #                             [2,6,10,14],
    #                             [3,7,11,15]])
    # # testdata = np.array([0,1,2,3,4,5])
    # # Csv.SaveCsv(testdata, "testdata.csv")
    # data = Csv.LoadCsv("testdata.csv")
    # print(data[0, 2])

    # Time = TimeTool()
    # bf = Time.ReadNowTime()
    # node = 0
    # sampleTime = 0.03
    # while True:
    #     af = Time.ReadNowTime()
    #     timerr = Time.TimeError(bf, af)
    #     print(timerr)
    #     # Trajectory counter
    #     node = int(timerr["totalus"] // (sampleTime*1000*1000))
    #     # print(timerr["totalms"] ,node)
    #     if node >= 200:
    #         endt = Time.ReadNowTime()
    #         timerr = Time.TimeError(bf, endt)
    #         print("軌跡已完成,總時間: " , timerr["totalus"], "us")
    #         break


    # 系統時間功能測試
    # startTime = Time.ReadNowTime()
    # startNode = 0
    # sampleTime = 0.03
    # while True:
    #     nowTime = Time.ReadNowTime()
    #     sysTime, nowNode = Time.sysTime(startTime, startNode, nowTime, sampleTime)
    #     print(nowNode)
    #     if nowNode >= 200:
    #         break
        

        

        
