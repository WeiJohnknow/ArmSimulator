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
    def Save(self, data):
        pass

    def Load(self, filePath):
        pass


class database_HomogeneousMat(Database_interface):

    @ staticmethod
    def Save(HomogeneousMatData, timeData, filePath, mode:str):
        columns = ['Xx', 'Xy', 'Xz', '0', 'Yx', 'Yy', 'Yz', '0', 'Zx', 'Zy', 'Zz', '0', 'Px', 'Py', 'Pz', '1', 'time']
        num_rows = HomogeneousMatData.shape[0]

        # 預先指定DataFrame大小
        df = pd.DataFrame(index=range(num_rows), columns=columns)

        # 使用列表推倒式建構data list，不包括timeData
        data_list = [np.concatenate([datum.T.ravel(), [0]]) for datum in HomogeneousMatData]

        # 寫入csv
        with open(filePath, mode) as f:
            f.write(','.join(columns[:-1]) + '\n')  # 不包括time
            for row in data_list:
                f.write(','.join(map(str, row[:-1])) + '\n')  # 不包括time

 
    @ staticmethod
    def Load(filePath):
        try:
            df = pd.read_csv(filePath)
            # TrajectoryData is ndarray
            HomogeneousMat = typeConversion.HomogeneousMat_dataframeToNdarray(df)
            return HomogeneousMat

        except FileNotFoundError:
            print(f"找不到文件：{filePath}")
            return None

class database_PoseMat(Database_interface):
    
    @ staticmethod
    def Save(PoseMatData, filePath, mode:str):
        """
        PoseMatData(n*1*6)
        """
        columns = ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']
        
        num_rows = PoseMatData.shape[0]

        # 預先指定DataFrame大小
        df = pd.DataFrame(index=range(num_rows), columns=columns)

        # 使用列表推倒式建構data list，不包括timeData
        data_list = [datum.T.ravel() for datum in PoseMatData]

        # 寫入csv
        with open(filePath, mode) as f:
            f.write(','.join(columns) + '\n')  
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')  
    
        
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
    def Load(filePath):
        try:
            df = pd.read_csv(filePath)
            # TrajectoryData is ndarray
            PoseMat_ndarry = typeConversion.PoseMatdataframeToNdarray(df)
            
            return PoseMat_ndarry

        except FileNotFoundError:
            print(f"找不到文件：{filePath}")
            return None

class database_Velocity():
    @ staticmethod
    def Save(VelocityData, filePath, mode: str):
        columns = ["Velocity"]
        num_rows = VelocityData.shape[0]

        # 預先指定DataFrame大小
        df = pd.DataFrame(index=range(num_rows), columns=columns)

        # 使用列表推倒式建構data list，將速度數據填入
        data_list = [datum.T.ravel() for datum in VelocityData]

        # 寫入csv
        with open(filePath, mode) as f:
            f.write(','.join(columns) + '\n')  # 更新columns
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')

        
    def Load(filePath):
        try:
            df = pd.read_csv(filePath)
            # TrajectoryData is ndarray
            Velocity_ndarry = typeConversion.VelocitydataframeToNdarray(df)
            
            return Velocity_ndarry

        except FileNotFoundError:
            print(f"找不到文件：{filePath}")
            return None

class database_JointAngle(Database_interface):
    @ staticmethod
    def Save(JointAngleData, filePath, mode:str):
        columns = ["S", "L", "U", "R", "B", "T"]
        num_rows = JointAngleData.shape[0]

        # 預先指定DataFrame大小
        df = pd.DataFrame(index=range(num_rows), columns=columns)

        # 使用列表推倒式建構data list，將速度數據填入
        data_list = [datum.T.ravel() for datum in JointAngleData]

        # 寫入csv
        with open(filePath, mode) as f:
            f.write(','.join(columns) + '\n')  # 更新columns
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')

    
    @ staticmethod
    def Load(filePath):
        try:
            df = pd.read_csv(filePath)
            # TrajectoryData is ndarray
            JointAngle_ndarry = typeConversion.JointAngleDataframeToNdarray(df)
            
            return JointAngle_ndarry

        except FileNotFoundError:
            print(f"找不到文件：{filePath}")
            return None

class database_time(Database_interface):
    @ staticmethod
    def Save(Time, filePath, mode:str):
        columns = ["Time"]
        num_rows = Time.shape[0]

        # 預先指定DataFrame大小
        df = pd.DataFrame(index=range(num_rows), columns=columns)

        # 使用列表推倒式建構data list，將速度數據填入
        data_list = [datum.T.ravel() for datum in Time]

        # 寫入csv
        with open(filePath, mode) as f:
            f.write(','.join(columns) + '\n')  # 更新columns
            for row in data_list:
                f.write(','.join(map(str, row)) + '\n')
    
    @ staticmethod
    def Load(filePath):
        try:
            df = pd.read_csv(filePath)
            # TrajectoryData is ndarray
            Time_ndarry = typeConversion.TimedataframeToNdarray(df)
            
            return Time_ndarry

        except FileNotFoundError:
            print(f"找不到文件：{filePath}")
            return None
        TimedataframeToNdarray(dataframe)


class typeConversion():
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