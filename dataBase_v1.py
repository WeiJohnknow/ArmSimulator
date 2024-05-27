from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import os
import sys
from Toolbox import TimeTool
from Matrix import Matrix4x4
r2d = np.rad2deg

"""
df mode:
"w" : 寫入模式（默認），會覆蓋已有文件，如果文件不存在則創建新文件。
"a" : 追加模式，將新的內容追加到已有文件的末尾。
"x" : 獨佔創建模式，僅在文件不存在時創建新文件，否則引發 FileExistsError。
"r" : 只讀模式，僅用於讀取文件。
"rb": 以二進制只讀模式打開文件，用於讀取二進制文件。
"""

class Database_interface(ABC):
    @abstractmethod
    def Save(data):
        pass
    
    @abstractmethod
    def Load(filePath):
        pass


class database_HomogeneousMat(Database_interface):
    @ staticmethod
    def Save(HomogeneousMatData, filePath:str, mode:str):
        """
        - Args: PoseMatData(type: ndarray)(shape: 3D)
        """
        dataTypeConverter.ndarrayTOdataframe(HomogeneousMatData, ['Xx', 'Xy', 'Xz', '0', 'Yx', 'Yy', 'Yz', '0', 'Zx', 'Zy', 'Zz', '0', 'Px', 'Py', 'Pz', '1'], filePath, mode)
        
            
    @ staticmethod
    def PoseMatToHomogeneousMat(PoseMat_ndarray):
        """
        - Arg: PoseMat(type: ndarray(3D))
        - Return: HomogeneousMat(type: ndarray(3D))
        """
        Mat = Matrix4x4()
        HomogeneousMat = np.zeros((PoseMat_ndarray.shape[0], 4, 4))
        for layer in range(PoseMat_ndarray.shape[0]):
            HomogeneousMat[layer] = Mat.AngletoMat(PoseMat_ndarray[layer].reshape(6, 1))
        
        return HomogeneousMat

    @ staticmethod
    def Load(filePath:str):
        df = validator.Is_existence(filePath)
        HomogeneousMat = dataTypeConverter.HomogeneousMat_dataframeToNdarray(df)

        return HomogeneousMat

class database_PoseMat(Database_interface):
    @ staticmethod
    def Save(PoseMatData, filePath:str, mode:str):
        """
        - Args: PoseMatData(type: ndarray)(shape: 3D)
        """
        dataTypeConverter.ndarrayTOdataframe(PoseMatData, ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz'], filePath, mode)

    @ staticmethod
    def HomogeneousMatToPoseMat(HomogeneousMat_ndarray):
        """
        - Arg: HomogeneousMat(type: ndarray(3D))
        - Return: PoseMat(type: ndarray(3D))
        """
        Mat = Matrix4x4()
        poseMat = np.zeros((HomogeneousMat_ndarray.shape[0], 1, 6))
        for layer in range(HomogeneousMat_ndarray.shape[0]):
            poseMat_ = Mat.MatToAngle(HomogeneousMat_ndarray[layer])
            poseMat[layer] = [round(poseMat_[0], 3), 
                        round(poseMat_[1], 3), 
                        round(poseMat_[2], 3), 
                        round(r2d(poseMat_[3]), 4), 
                        round(r2d(poseMat_[4]), 4), 
                        round(r2d(poseMat_[5]), 4)]
        return poseMat
    
    @ staticmethod
    def Load(filePath:str):
        df = validator.Is_existence(filePath)
        PoseMat_ndarry = dataTypeConverter.PoseMatdataframeToNdarray(df)
        
        return PoseMat_ndarry

class database_Velocity():
    @ staticmethod
    def Save(VelocityData, filePath, mode: str):
        """
        - Args: Velocity(type: ndarray)(shape: 2D) 
        """
        dataTypeConverter.ndarrayTOdataframe(VelocityData, ["Velocity"], filePath, mode)
        
        
    def Load(filePath):
        df = validator.Is_existence(filePath)
        Velocity_ndarry = dataTypeConverter.VelocitydataframeToNdarray(df)
        
        return Velocity_ndarry

class database_JointAngle(Database_interface):
    @ staticmethod
    def Save(JointAngleData, filePath, mode:str):
        """
        - Args: JointAngleData(type: ndarray)(shape: 2D) 
        """
        dataTypeConverter.ndarrayTOdataframe(JointAngleData, ["S", "L", "U", "R", "B", "T"], filePath, mode)

    @ staticmethod
    def Load(filePath):
        df = validator.Is_existence(filePath)
        JointAngle_ndarry = dataTypeConverter.JointAngleDataframeToNdarray(df)

        return JointAngle_ndarry

class database_time(Database_interface):
    @ staticmethod
    def Save(Time, filePath, mode:str):
        """
        - Args: Time(type: ndarray)(shape: 2D) 
        """
        dataTypeConverter.ndarrayTOdataframe(Time, ["Time"], filePath, mode)
    
    @ staticmethod
    def Save_costTime(costTime, filePath, mode:str):
        """
        - Args: Cost Time(type: ndarray)(shape: 2D) 
        """
        dataTypeConverter.ndarrayTOdataframe(costTime, ["Trj_Algorithm", "Data_merge", "IK_Iterate"], filePath, mode)

    @ staticmethod
    def Save_EventRecords(EventRecord, filePath, mode:str):
        """
        """
        dataTypeConverter.ndarrayTOdataframe(EventRecord, ["I0", "Prv_I0", "Write permission", "PrvUpdataTime", "SysTime", "WriteTrjSysTime", "WriteTrjCostTime", "WriteInterval"], filePath, mode)
    
    @ staticmethod
    def Save_PoseMat_Time(PoseMatAndTime, filePath, mode:str):
        dataTypeConverter.ndarrayTOdataframe(PoseMatAndTime, ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz', "Time"], filePath, mode)

    @ staticmethod
    def Load(filePath):
        df = validator.Is_existence(filePath)
        Time_ndarry = dataTypeConverter.TimedataframeToNdarray(df)

        return Time_ndarry



class validator:
    @staticmethod
    def Is_existence(filePath):
        """Verify file exists
        """
        if os.path.exists(filePath):
            return pd.read_csv(filePath)
        else:
            sys.exit(f"找不到文件：{filePath}")

class dataTypeConverter:
    @ staticmethod
    def ndarrayTOdataframe(data, columns:list, filePath:str, mode:str):
        """Write ndarray into the database as dataframe type.
        - Arg: ndarray
        - Return: dataframe
        """
        columns = columns
        num_rows = data.shape[0]

        # 預先指定DataFrame大小
        df = pd.DataFrame(index=range(num_rows), columns=columns)

        # 使用列表推倒式建構data list，將速度數據填入
        data_list = [datum.T.ravel() for datum in data]

        # 寫入csv
        with open(filePath, mode) as f:
            f.write(','.join(columns) + '\n')  # 更新columns
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')

    @ staticmethod
    def HomogeneousMat_dataframeToNdarray(dataframe):
        """dataframe To Ndarray
        - Arg: dataframe
        - Return: ndarray
        """
        dataShape = dataframe.shape
        ndarray = np.zeros((dataShape[0], 4, 4))
        for layer in range(dataShape[0]):
            ndarray[layer,0,0] = dataframe['Xx'][layer]
            ndarray[layer,1,0] = dataframe['Xy'][layer]
            ndarray[layer,2,0] = dataframe['Xz'][layer]
            ndarray[layer,3,0] = 0
            ndarray[layer,0,1] = dataframe['Yx'][layer]
            ndarray[layer,1,1] = dataframe['Yy'][layer]
            ndarray[layer,2,1] = dataframe['Yz'][layer]
            ndarray[layer,3,1] = 0
            ndarray[layer,0,2] = dataframe['Zx'][layer]
            ndarray[layer,1,2] = dataframe['Zy'][layer]
            ndarray[layer,2,2] = dataframe['Zz'][layer]
            ndarray[layer,3,2] = 0
            ndarray[layer,0,3] = dataframe['Px'][layer]
            ndarray[layer,1,3] = dataframe['Py'][layer]
            ndarray[layer,2,3] = dataframe['Pz'][layer]
            ndarray[layer,3,3] = 1
        return ndarray
    
    
    @ staticmethod
    def PoseMatdataframeToNdarray(dataframe):
        """dataframe To Ndarray
        - Arg: dataframe
        - Return: ndarray
        """
        dataShape = dataframe.shape
        ndarray = np.zeros(((dataShape[0], 1, 6)))
        for layer in range(dataShape[0]):
            ndarray[layer,0,0] = dataframe['X'][layer]
            ndarray[layer,0,1] = dataframe['Y'][layer]
            ndarray[layer,0,2] = dataframe['Z'][layer]
            ndarray[layer,0,3] = dataframe['Rx'][layer]
            ndarray[layer,0,4] = dataframe['Ry'][layer]
            ndarray[layer,0,5] = dataframe['Rz'][layer]

        return ndarray
    
    @ staticmethod
    def VelocitydataframeToNdarray(dataframe):
        """dataframe To Ndarray
        - Arg: dataframe
        - Return: ndarray
        """
        dataShape = dataframe.shape
        ndarray = np.zeros(((dataShape[0],1)))
        for layer in range(dataShape[0]):
            ndarray[layer,0] = dataframe['Velocity'][layer]
            
        return ndarray
    
    @ staticmethod
    def JointAngleDataframeToNdarray(dataframe):
        """dataframe To Ndarray
        - Arg: dataframe
        - Return: ndarray
        """
        dataShape = dataframe.shape
        ndarray = np.zeros((dataShape[0], 6))
        for layer in range(dataShape[0]):
            ndarray[layer,0] = dataframe['S'][layer]
            ndarray[layer,1] = dataframe['L'][layer]
            ndarray[layer,2] = dataframe['U'][layer]
            ndarray[layer,3] = dataframe['R'][layer]
            ndarray[layer,4] = dataframe['B'][layer]
            ndarray[layer,5] = dataframe['T'][layer]
            
        return ndarray
    
    @ staticmethod
    def TimedataframeToNdarray(dataframe):
        """dataframe To Ndarray
        - Arg: dataframe
        - Return: ndarray
        """
        dataShape = dataframe.shape
        ndarray = np.zeros(((dataShape[0],1)))
        for layer in range(dataShape[0]):
            ndarray[layer,0] = dataframe['Time'][layer]
            
        return ndarray

class dataOperating:
    @ staticmethod
    def Merge(oldFilePath:str, newFilePath:str, RemixfilePath:str, oldFileNode:int, newFileNode:int):
        """整併新與舊的軌跡檔案
        - Args:
            - oldFilePath: 舊軌跡檔案路徑
            - newFilePath: 新軌跡檔案路徑
            - RemixfilePath: 新、舊軌跡檔案結合後的檔案路徑
            - oldFileNode: 舊與新軌跡檔案的交接節點(計算新軌跡結束時)
            - newFileNode: 計算新軌跡期間(由按下重新規劃案件到計算完成)時所產生的時間差(單位:批次) 
        """
        # 讀取舊與新的軌跡檔案
        data_frame1 = pd.read_csv(oldFilePath, delimiter=',', dtype=np.float64, encoding='utf-8')
        data_frame2 = pd.read_csv(newFilePath, delimiter=',', dtype=np.float64, encoding='utf-8')

        # 提取舊資料
        oldFileIndex = oldFileNode*9
        data_frame1 = data_frame1.iloc[:oldFileIndex]

        # 提取新資料(由)
        data_frame2 = data_frame2.iloc[:newFileNode]

        stacked_df = pd.concat([data_frame1, data_frame2], axis=0)
        stacked_df.to_csv(RemixfilePath, index=False,  header=True)


    @ staticmethod
    def searchSimilarTrj(PoseMatDataSet:np.ndarray, targetPoseMatData:np.ndarray):
        """Search for the closest trajectory data.

        args:
            - PoseMatDataSet: shape is n*1*6.
            - targetPoseMatData: shape is 1*6.
        
        return:
            - mostSimilarData(np.ndarray): Profile most similar to target, shape is 1*6.
            - mostSimilarIndex(int): Index of data most similar to the target data.

        """
        # 將資料拆分成位置與姿態
        Position = PoseMatDataSet[:, :, :3].reshape(-1, 3)
        Posture = PoseMatDataSet[:, :, 3:].reshape(-1, 3)

        targetPosition = targetPoseMatData[:, :3].reshape(-1)
        targetPosture = targetPoseMatData[:, 3:].reshape(-1)

        # 計算每一筆資料與目標資料的歐氏距離
        diffPosition = np.linalg.norm(Position-targetPosition, axis=1)
        diffPosture =  np.linalg.norm(Posture-targetPosture, axis=1)

        # 使用 np.all 檢查數組中的所有元素是否為 0
        is_diffPosition_zero = np.all(diffPosition == 0)
        is_diffPosture_zero = np.all(diffPosture == 0)

        # 判斷歐式距離array是否為0
        # 0表示無變動
        # 從有變動的array中找最小歐式距離
        # 即可得到最接近目標資料的資料索引
        if is_diffPosition_zero:
            mostSimilarIndex = np.argmin(diffPosture)
        elif is_diffPosture_zero:
            mostSimilarIndex = np.argmin(diffPosition)
        else:
            print("軌跡有問題，變動率為0")
            # 兩個都不為0，以位置為主
            mostSimilarIndex = np.argmin(diffPosition)
    
        # 找出最接近目標資料的資料
        mostSimilarData = PoseMatDataSet[mostSimilarIndex]

        return mostSimilarData, mostSimilarIndex

