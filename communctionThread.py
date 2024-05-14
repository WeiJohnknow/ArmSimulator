"""
2024/05/05 
非同步執行 | Udp

"""

from MotomanUdpPacket import *
from dataBase_v1 import *
from Toolbox import TimeTool
import threading, time
import numpy as np

class UdpThread:
    def __init__(self):
        self.comUdp = MotomanUDP()
        self.Td = TimeTool()

    @ staticmethod
    def getCoordinate():
        reqSubHeader = { 'Command_No': (0x75, 0x00),
                         'Instance': [101, 0],
                         'Attribute': 0,
                         'Service':  0x0E,
                         'Padding': (0, 0) }
        reqData = []

        return reqSubHeader, reqData
    
    @ staticmethod
    def signDecide(number, rate):
        """判斷正負符號並編碼成Bytes型別
        """
        if number < 0:
            ans = struct.pack('i', int(number*rate))
        else:
            ans = struct.pack('I', int(number*rate))

        return ans
    
    @ staticmethod
    def multipleWriteRPVar_pack(firstAddress:int, Number:int, data:dict):
        # 寫入的資料個數
        Number_byte = struct.pack('I', Number)

        Packet = Number_byte 

        # 將資料轉為Byte格式
        for n in range(Number):

            dataType = struct.pack('I', data[f'{n}'][0])
            Form = struct.pack('I', data[f'{n}'][1])
            Toolnumber = struct.pack('I', data[f'{n}'][2])
            UserCoordinate = struct.pack('I', data[f'{n}'][3])
            ExtendedForm = struct.pack('I', 0)

            FirstCoordinate  = UdpThread.signDecide(data[f'{n}'][4], 1000)
            SecondCoordinate = UdpThread.signDecide(data[f'{n}'][5], 1000)
            ThirdCoordinate  = UdpThread.signDecide(data[f'{n}'][6], 1000)
            FourthCoordinate = UdpThread.signDecide(data[f'{n}'][7], 1000)
            FifthCoordinate  = UdpThread.signDecide(data[f'{n}'][8], 1000)
            SixthCoordinate  = UdpThread.signDecide(data[f'{n}'][9], 1000)

            SeventhCoordinate = struct.pack('i', 0)
            EighthCoordinate = struct.pack('i', 0)

            # 加入資料封包中
            Packet +=  dataType + Form + Toolnumber + UserCoordinate + ExtendedForm + FirstCoordinate + SecondCoordinate\
                     + ThirdCoordinate + FourthCoordinate + FifthCoordinate + SixthCoordinate + SeventhCoordinate + EighthCoordinate\
                
        Address_hex = hex(firstAddress)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)
        
        reqSubHeader = {'Command_No': (0x07, 0x03),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 0,
                        'Service':  0x34,
                        'Padding': (0, 0)}
        reqData = Packet

        return reqSubHeader, reqData
    
    @ staticmethod
    def multipleWriteVar_pack(firstAddress:int, Number:int, data:list):
  
    
        # 寫入的資料個數
        Number_byte = struct.pack('I', Number)

        Packet = Number_byte 

        # 將資料轉為Byte格式
        for n in range(Number):
            
            var = struct.pack('h', data[n])
        
            # 加入資料封包中
            Packet +=  var
                
        Address_hex = hex(firstAddress)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)
        
        reqSubHeader = {'Command_No': (0x03, 0x03),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 0,
                        'Service':  0x34,
                        'Padding': (0, 0)}
        
        reqData = Packet

        return reqSubHeader, reqData

    def SingleTreadSentAndRecive(self, reqSubHeader, reqData):

        b = self.Td.ReadNowTime()

        # 打包請求封包
        reqPacket = UDP_packet(reqSubHeader, reqData).Pack_Req_packet()
    
        # 發送
        self.comUdp._sendCmd(reqPacket)

        # 接收
        AnsPacket = self.comUdp._rceiveAns()
        
        # 解封包
        Ans = UDP_packet.Unpack_Ans_packet(self, AnsPacket)
        result = self.comUdp.Cvt_SignInt(Ans)

        # data = {"dataType": result[0],
        #         "Form": result[1],
        #         "Toolnumber": result[3],
        #         "UserCoordinate": result[4]}
        # coordinate = [result[5], result[6], result[7], result[8], result[9], result[10]]
        

        a = self.Td.ReadNowTime()
        cmdTime = self.Td.TimeError(b, a)
        cmdTime_ms = cmdTime["millisecond"]

        # print(f"當前位置: {coordinate} | 讀取位置花費: {cmdTime_ms}ms")
        return cmdTime_ms
            
    
    def Send(self, reqSubHeader, reqData, rceive):
        # while not rceive.is_alive():
        #     pass

        # 打包請求封包
        reqPacket = UDP_packet(reqSubHeader, reqData).Pack_Req_packet()

        # 發送
        self.comUdp._sendCmd(reqPacket)
            
            
    def Rceive(self):      
        # 接收
        AnsPacket = self.comUdp._rceiveAns()

        # 解封包
        Ans = UDP_packet.Unpack_Ans_packet(self, AnsPacket)
        result = self.comUdp.Cvt_SignInt(Ans)
        
        

    def asynchronousProcessing(self, reqSubHeader, reqData):
        rceive = threading.Thread(target=self.Rceive)
        send = threading.Thread(target=self.Send, args=(reqSubHeader, reqData, rceive,))
        
        b = self.Td.ReadNowTime()
        send.start()
        rceive.start()

        rceive.join()
        a = self.Td.ReadNowTime()
        err = self.Td.TimeError(b,a)
        err_ms = err["millisecond"] 
        # print(f"非同步收發，共花費: {err_ms}ms")
        return err_ms


    

if __name__ == "__main__":
    udp = UdpThread()
    Td = TimeTool()
    SinglecostTime = []
    DoublecostTime = []


    NBR = 10

    # 取得請求封包的標題與資料
    reqSubHeader, reqData = UdpThread.getCoordinate()

    # 多筆RP變數寫入
    # data = {'0':[17, 4, 5, 0, 958.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '1':[17, 4, 5, 0, 959.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '2':[17, 4, 5, 0, 960.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '3':[17, 4, 5, 0, 961.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '4':[17, 4, 5, 0, 962.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '5':[17, 4, 5, 0, 963.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '6':[17, 4, 5, 0, 964.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '7':[17, 4, 5, 0, 965.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '8':[17, 4, 5, 0, 966.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149]}
    # reqSubHeader, reqData = UdpThread.multipleWriteRPVar_pack(2, 9, data)

    # data = [20, 20, 20, 20, 20, 20, 20, 20, 20]
    # reqSubHeader, reqData = UdpThread.multipleWriteVar_pack(2, 9, data)

    _count = 0
    while _count<=NBR:
        

        err_ms = udp.asynchronousProcessing(reqSubHeader, reqData)
        DoublecostTime.append(err_ms)
        Td.time_sleep(0.08)
        _count+=1

    
    
    count = 0
    costTime = []
    while count<=NBR:
        
        cmdTime_ms = udp.SingleTreadSentAndRecive(reqSubHeader, reqData)
        costTime.append(cmdTime_ms)
        count+=1
        Td.time_sleep(0.08)
    SinglecostTime = np.array(costTime)
    # total_costTime = np.sum(costTime)
    # SinglecostTime.append(costTime)
       
        
    
    SinglecostTime = np.array(SinglecostTime)
    print("單",SinglecostTime)
    DoublecostTime = np.array(DoublecostTime)
    print("雙",DoublecostTime)

    total_single = np.mean(SinglecostTime)
    total_double = np.mean(DoublecostTime)
    
    original_value = round(total_single,3)
    new_value = round(total_double,3)

    # 計算百分比變化
    percentage_change = ((new_value - original_value) / original_value) * 100
    percentage_change = round(percentage_change, 3)

    print(f"讀取位置| 單執行緒平均花費時間:{total_single}ms | 多執行旭平均花費時間:{total_double}ms | 效率比(單相對多執行緒)變化: {percentage_change} %")
    # print(f"多筆寫入(9筆)| 單執行緒平均花費時間:{total_single}ms | 多執行旭平均花費時間:{total_double}ms | 效率比(單相對多執行緒)變化: {percentage_change} %")
        