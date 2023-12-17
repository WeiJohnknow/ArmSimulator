import pandas as pd
import numpy as np
import os
import sys
from Toolbox import TimeTool

class dataBase:
    def __init__(self) -> None:
        self.Time = TimeTool()
        
    
    def Save(self, data, timeData, filePath):
        # TODO 要做多筆資料儲存
        """Save Homogeneous Transformation Matrix 
        - Args: \n 
            # data: 2-dimensional array, shape is 4x4. \n
            # filePath: "xxxx.csv" (str)
        """
        if os.path.isfile(filePath):
            sys.exit(f"警告: 文件 '{filePath}' 已存在，請確認檔名及其路徑。")

        # Reference dataSet shape is nx4x4(Use MatrixInterpolation method)          
        elif len(data.shape) == 3 and data.shape[1] == 4 and data.shape[2] == 4:
            
            df = pd.DataFrame(columns=['Xx', 'Xy', 'Xz', '0', 'Yx', 'Yy', 'Yz', '0', 'Zx', 'Zy', 'Zz', '0', 'Px', 'Py', 'Pz', '1', 'time'])

            # list用於儲存 Matrix(1x16) 的數據 
            data_list = []
            for dataIndex in range(data.shape[0]):
                data1x16 = data[dataIndex].T.ravel().copy()
                # 新增time
                data1x17 = np.hstack((data1x16, timeData[dataIndex]))
                data_list.append(data1x17.flatten())

            # 把list中的所有數據一次性加到 DataFrame 中
            df = pd.concat([df, pd.DataFrame(data_list, columns=df.columns)], ignore_index=True)

            # 如果 CSV 文件不存在，直接写入；否则追加
            mode = 'w' if not os.path.exists(filePath) else 'a'
            df.to_csv(filePath, mode=mode, index=False)
        
        else:
            print("dtype Error!")
        
        
    def Load(self, filePath):
        """
        Loading data with filename.csv
        """
        try:
            # 使用 pandas 的 read_csv 函数读取整个 CSV 文件
            
            df = pd.read_csv(filePath)
            
            
            # 打印数据框的内容
            # print(df)

            # 返回数据框
            return df

        except FileNotFoundError:
            print(f"找不到文件：{filePath}")
            return None
        
    def LoadMatrix4x4(self, filePath):
        """Load csv file and dtype transform
        - Matrix(1x17) ➔ dict{time: Homogeneous matrix(4x4)}
        """
        databuffer = self.Load(filePath)
        dataShape = databuffer.shape
        path = {}
        if len(dataShape) == 2:
            pathData = np.zeros((dataShape[0], 4, 4))
            for layer in range(dataShape[0]):
                pathData[layer,0,0] = databuffer['Xx'][layer]
                pathData[layer,1,0] = databuffer['Xy'][layer]
                pathData[layer,2,0] = databuffer['Xz'][layer]
                pathData[layer,3,0] = 0
                pathData[layer,0,1] = databuffer['Yx'][layer]
                pathData[layer,1,1] = databuffer['Yy'][layer]
                pathData[layer,2,1] = databuffer['Yz'][layer]
                pathData[layer,3,1] = 0
                pathData[layer,0,2] = databuffer['Zx'][layer]
                pathData[layer,1,2] = databuffer['Zy'][layer]
                pathData[layer,2,2] = databuffer['Zz'][layer]
                pathData[layer,3,2] = 0
                pathData[layer,0,3] = databuffer['Px'][layer]
                pathData[layer,1,3] = databuffer['Py'][layer]
                pathData[layer,2,3] = databuffer['Pz'][layer]
                pathData[layer,3,3] = 1
                # 轉為字典 time : Homogeneous matrix
                path[round(databuffer['time'][layer],2)] = pathData[layer]
            
            return path
        else:
            print("None")


        


# if __name__ == '__main__':
#     db = database()
#     data = np.array([[1, 5,  9, 13],
#                             [2, 6, 10, 14],
#                             [3, 7, 11, 15],
#                             [4, 8, 12, 16]])
    
#     db.Save( data, "database/test4x4.csv")
  