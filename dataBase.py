import pandas as pd
import numpy as np
import os
import sys
from Toolbox import TimeTool
from Matrix import Matrix4x4
r2d = np.rad2deg
class dataBase:
    def __init__(self) -> None:
        self.Time = TimeTool()
        self.Mat = Matrix4x4()
        
    
    def Save(self, data, timeData, filePath):
        # TODO 重複檔案處理方式未完成，暫時使用程式結束來提醒。
        """Save Homogeneous Transformation Matrix 
        - Args: \n 
            # data: 2-dimensional array, shape is 4x4. \n
            # filePath: "xxxx.csv" (str)
        """
        mode = ""
        # 文件寫入模式判定
        if os.path.isfile(filePath):
            # 如果該檔名已存在
            Ans = input("該檔案名稱存在，請選擇處理方式 :\nw.覆寫 \na.追加 \no.程式結束，請重設檔案名稱 \nAnswer :")
            """
            df mode:
            "w" : 寫入模式（默認），會覆蓋已有文件，如果文件不存在則創建新文件。
            "a" : 追加模式，將新的內容追加到已有文件的末尾。
            "x" : 獨佔創建模式，僅在文件不存在時創建新文件，否則引發 FileExistsError。
            "r" : 只讀模式，僅用於讀取文件。
            "rb": 以二進制只讀模式打開文件，用於讀取二進制文件。
            """
            if Ans == "w":
                # 覆寫
                mode = "w"
            elif Ans == "a":
                # 追加
                mode = "a"
            else: 
                sys.exit("Please rename the file")
        else:
            mode = "x"
        
            
        if len(data.shape) == 3 and data.shape[1] == 4 and data.shape[2] == 4:
            # Reference dataSet shape is nx4x4(Use MatrixInterpolation method)
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
            
            # 寫入csv檔
            df.to_csv(filePath, mode=mode, index=False)

        elif len(data.shape) == 3 and data.shape[1] == 6 and data.shape[2] == 1 :
            """Save IK calculate Answer ➔ Joint Angle
            """
            df = pd.DataFrame(columns=['S', 'L', 'U', 'R', 'B', 'T'])
            # list用於儲存 Matrix(1x6) 的數據 
            data_list = []
            for dataIndex in range(data.shape[0]):
                data1x6 = data[dataIndex].copy()
                data_list.append(data1x6.flatten())

            # 把list中的所有數據一次性加到 DataFrame 中
            df = pd.concat([df, pd.DataFrame(data_list, columns=df.columns)], ignore_index=True)

            # 寫入csv檔
            df.to_csv(filePath, mode=mode, index=False)

        elif len(data.shape) == 3 and data.shape[1] == 1 and data.shape[2] == 6 :
            """Save pose matrix (1X6)
            """
            # TODO 未測試
            df = pd.DataFrame(columns=['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz'])
            # list用於儲存 Matrix(1x6) 的數據 
            data_list = []
            for dataIndex in range(data.shape[0]):
                data1x6 = data[dataIndex].copy()
                data_list.append(data1x6.flatten())

            # 把list中的所有數據一次性加到 DataFrame 中
            df = pd.concat([df, pd.DataFrame(data_list, columns=df.columns)], ignore_index=True)

            # 寫入csv檔
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
        - Args: filePath
        - Return: path_dict, path_df, path_np_4X4, path_np_6X1
        """
        path_df = self.Load(filePath)
        dataShape = path_df.shape
        path_dict = {}
        if len(dataShape) == 2:
            # dtype :ndarray ,shape :4X4
            path_np_4X4 = np.zeros((dataShape[0], 4, 4))
            # dtype :ndarray ,shape :1X6
            path_np_6X1 = np.zeros((dataShape[0], 1, 6))
            for layer in range(dataShape[0]):
                path_np_4X4[layer,0,0] = path_df['Xx'][layer]
                path_np_4X4[layer,1,0] = path_df['Xy'][layer]
                path_np_4X4[layer,2,0] = path_df['Xz'][layer]
                path_np_4X4[layer,3,0] = 0
                path_np_4X4[layer,0,1] = path_df['Yx'][layer]
                path_np_4X4[layer,1,1] = path_df['Yy'][layer]
                path_np_4X4[layer,2,1] = path_df['Yz'][layer]
                path_np_4X4[layer,3,1] = 0
                path_np_4X4[layer,0,2] = path_df['Zx'][layer]
                path_np_4X4[layer,1,2] = path_df['Zy'][layer]
                path_np_4X4[layer,2,2] = path_df['Zz'][layer]
                path_np_4X4[layer,3,2] = 0
                path_np_4X4[layer,0,3] = path_df['Px'][layer]
                path_np_4X4[layer,1,3] = path_df['Py'][layer]
                path_np_4X4[layer,2,3] = path_df['Pz'][layer]
                path_np_4X4[layer,3,3] = 1
                # pose matrix 1*6
                poseMat = self.Mat.MatToAngle(path_np_4X4[layer])
                # rad to deg
                poseMat_ = [round(poseMat[0], 3), round(poseMat[1], 3), round(poseMat[2], 3), round(r2d(poseMat[3]), 4), round(r2d(poseMat[4]), 4), round(r2d(poseMat[5]), 4)]
                path_np_6X1[layer] = poseMat_
                # 轉為dict time : Homogeneous matrix
                path_dict[round(path_df['time'][layer],3)] = path_np_4X4[layer]
                
            return path_dict, path_df, path_np_4X4, path_np_6X1
        else:
            print("None")


        


# if __name__ == '__main__':
#     db = database()
#     data = np.array([[1, 5,  9, 13],
#                             [2, 6, 10, 14],
#                             [3, 7, 11, 15],
#                             [4, 8, 12, 16]])
    
#     db.Save( data, "database/test4x4.csv")
  