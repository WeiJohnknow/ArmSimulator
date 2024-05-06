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

    def SingleTreadSentAndRecive(self):

        b = self.Td.ReadNowTime()
        # 取得請求封包的標題與資料
        reqSubHeader, reqData = UdpThread.getCoordinate()

        # 打包請求封包
        reqPacket = UDP_packet(reqSubHeader, reqData).Pack_Req_packet()
        
        time.sleep(0.04)

        # 發送
        self.comUdp._sendCmd(reqPacket)

        # 接收
        AnsPacket = self.comUdp._rceiveAns()
        
        # 解封包
        Ans = UDP_packet.Unpack_Ans_packet(self, AnsPacket)
        result = self.comUdp.Cvt_SignInt(Ans)

        data = {"dataType": result[0],
                "Form": result[1],
                "Toolnumber": result[3],
                "UserCoordinate": result[4]}
        coordinate = [result[5], result[6], result[7], result[8], result[9], result[10]]
        

        a = self.Td.ReadNowTime()
        cmdTime = self.Td.TimeError(b, a)
        cmdTime_ms = cmdTime["millisecond"]

        # print(f"當前位置: {coordinate} | 讀取位置花費: {cmdTime_ms}ms")
        return cmdTime_ms
            
        

    def Send(self, rceive):
        while not rceive.is_alive():
            pass
        
        count = 0
        while True:
            time.sleep(0.04)
            if count == 3:
                break
            # 取得請求封包的標題與資料
            reqSubHeader, reqData = UdpThread.getCoordinate()

            # 打包請求封包
            reqPacket = UDP_packet(reqSubHeader, reqData).Pack_Req_packet()

            # 發送
            self.comUdp._sendCmd(reqPacket)
            
            count += 1
            

    def Rceive(self):
        count = 0
        while True:
            if count == 3:
                break
            # 接收
            AnsPacket = self.comUdp._rceiveAns()

            # 解封包
            Ans = UDP_packet.Unpack_Ans_packet(self, AnsPacket)
            result = self.comUdp.Cvt_SignInt(Ans)
            # print(result)
            count += 1
            
            

    def asynchronousProcessing(self):
        rceive = threading.Thread(target=self.Rceive)
        send = threading.Thread(target=self.Send, args=(rceive,))
        
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
    SinglecostTime = []
    DoublecostTime = []

    

    _count = 0
    while _count<=3:
        count = 0
        costTime = []
        while count<=3:
            
            cmdTime_ms = udp.SingleTreadSentAndRecive()
            costTime.append(cmdTime_ms)
            count+=1
            
        costTime = np.array(costTime)
        total_costTime = np.sum(costTime)
        SinglecostTime.append(total_costTime)
        # print(f"單一執行緒收發，共花費: {total}ms")
        

        err_ms = udp.asynchronousProcessing()
        DoublecostTime.append(err_ms)

        _count+=1
    
    SinglecostTime = np.array(SinglecostTime)
    DoublecostTime = np.array(DoublecostTime)

    total_single = np.mean(SinglecostTime)
    total_double = np.mean(DoublecostTime)
    
    original_value = round(total_single,3)
    new_value = round(total_double,3)

    # 計算百分比變化
    percentage_change = ((new_value - original_value) / original_value) * 100
    percentage_change = round(percentage_change, 3)

    print(f"百分比變化: {percentage_change} %", )
        