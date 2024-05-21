import struct
import socket
import pandas as pd
from Toolbox import TimeTool
from dataBase_v0 import dataBase
import numpy as np

class UDP_packet:
    def __init__(self, Sub_header, data=[]) -> None:
        # Request Packet

        # main format
        # 4 Byte
        self.identifier  = 'YERC'
        # 2 Byte
        self.Header_part_size = [0x20, 0x00]
        # 2 Byte
        self.Data_part_size   = [0x00, 0x00]
        # 1 Byte
        self.Reserve_1 = 3
        # 1 Byte
        self.Processing_division = 1
        # 1 Byte
        self.ACK = 0
        # 1 Byte
        self.Request_ID = 0
        # 4 Byte
        self.Block_No = [0, 0, 0, 0]
        # 8 Byte
        self.Reserve_2 = "99999999"

        # Sub-header format
        # 2 Byte
        self.Command_No = [0,0]
        self.Command_No[0] = Sub_header["Command_No"][0]
        self.Command_No[1] = Sub_header["Command_No"][1]
        # 2 Byte
        self.Instance = [0,0]
        self.Instance[0] = Sub_header["Instance"][0]
        self.Instance[1] = Sub_header["Instance"][1]
        # 1 Byte
        self.Attribute = Sub_header["Attribute"]
        # 1 Byte
        self.Service = Sub_header["Service"]
        # 2 Byte
        self.padding = [0,0]
        self.padding[0] = Sub_header['Padding'][0]
        self.padding[1] = Sub_header['Padding'][1]

        # 填入Data_part_size
        dataSize = hex(len(data))

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        dataSize = dataSize[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        dataSize_high_byte = int(dataSize[:2], 16)
        dataSize_low_byte = int(dataSize[2:], 16)

        # 資料長度在4byte範圍內時
        if len(data) <= 255 :
            # self.Data_part_size[0] = len(data)
            # self.Data_part_size[1] = 0
            self.Data_part_size[0] = dataSize_low_byte
            self.Data_part_size[1] = dataSize_high_byte

        # 資料長度超過4byte時
        else:
            # self.Data_part_size[0] = 255
            # self.Data_part_size[1] = len(data)-self.Data_part_size[0]
            self.Data_part_size[0] = dataSize_low_byte
            self.Data_part_size[1] = dataSize_high_byte
            

        self.Data = data

    
    def Pack_Req_packet(self):
        """Pack Request Packet
        """
        # main
        packet = self.identifier.encode('utf-8')
        packet += struct.pack('B', self.Header_part_size[0])
        packet += struct.pack('B', self.Header_part_size[1])
        packet += struct.pack('B', self.Data_part_size[0])
        packet += struct.pack('B', self.Data_part_size[1])
        
        packet += struct.pack('B', self.Reserve_1)
        packet += struct.pack('B', self.Processing_division)
        packet += struct.pack('B', self.ACK)
        packet += struct.pack('B', self.Request_ID)
        packet += struct.pack('B', self.Block_No[0])
        packet += struct.pack('B', self.Block_No[1])
        packet += struct.pack('B', self.Block_No[2])
        packet += struct.pack('B', self.Block_No[3])
        packet += self.Reserve_2.encode("utf-8")
        
        # Sub-header
        packet += struct.pack('B', self.Command_No[0])
        packet += struct.pack('B', self.Command_No[1])
        packet += struct.pack('B', self.Instance[0])
        packet += struct.pack('B', self.Instance[1])
        packet += struct.pack('B', self.Attribute)
        packet += struct.pack('B', self.Service)
        packet += struct.pack('B', self.padding[0])
        packet += struct.pack('B', self.padding[1])

        # 判斷資料型別是否為Bytes
        if isinstance(self.Data, bytes):
            packet += self.Data
        else:
            for i in range(self.Data_part_size[0] + self.Data_part_size[1]):
                packet += struct.pack('B', self.Data[i])

    
        return packet
    
    def Unpack_Ans_packet(self, Ans_packet):
        """Unpack Answer Packet
        """

        # 封包執行狀態
        status = hex(Ans_packet[25])
        add_status_size = Ans_packet[26]
        # [Low, High]
        add_status=[0,0]
        add_status[0] = hex(Ans_packet[28])
        add_status[1] = hex(Ans_packet[29])

        # 資料回傳處理
        dataSize = [Ans_packet[6], Ans_packet[7]]
        
        
        # size = 4 * dataSize[1] * 256 + dataSize[0]
        size =  dataSize[1] * 256 + dataSize[0]
        data = [0] * size
        for i in range(size):
            # self.data[i] = ord(ans_str[32 + i])
            data[i] = Ans_packet[32 + i]
        

        if status == '0x0':
            # print('udp ok!!')
            udp_flag = "0x0"
            return data
        
        elif status == '0x8':
            Error = ['Error code: 0x08','Requested command is not defined!!']
            return Error
        
        elif status == "0x1f":
            add_status[0] = hex(Ans_packet[28])
            add_status[1] = hex(Ans_packet[29])

            if add_status[0] == '0xa7' and  add_status[1] == '0xe4':
                Error = ['Error code: E4A7','Packet format error(the size of the requested command and received frame are different)!!']
                return Error
            elif add_status[0] == '0x1' and add_status[1] == '0xa0':
                Error = ['Error code: A001','Instance error!!']
                return Error
            elif add_status[0] == '0x80' and add_status[1] == '0x20':
                Error = ['Error code: 2080','Incorrect mode!!']
                return Error
            elif add_status[0] == '0xa' and add_status[1] == '0xb0':
                Error = ['Error code: B00A','Operating speed is not setting!!']
                return Error
            elif add_status[0] == '0x70' and add_status[1] == '0x20':
                Error = ['Error code: 2070','Servo OFF!!']
                return Error
            elif add_status[0] == '0x10' and add_status[1] == '0x20':
                Error = ['Error code: 2010','Manipulator operating!!']
                return Error
            elif add_status[0] == '0x50' and add_status[1] == '0x34':
                Error = ['Error code: 3450','Servo power cannot be turned ON, Plase check in Robot mode.']
                return Error
            elif add_status[0] == '0x50' and add_status[1] == '0x20':
                Error = ['Error code: 2050','Command Hold.']
                return Error
            elif add_status[0] == '0x4' and add_status[1] == '0xb0':
                Error = ['Error code: B004','Outside the data.']
                return Error
            elif add_status[0] == '0x9' and add_status[1] == '0xb0':
                Error = ['Error code: B009','Speed setting error.']
                return Error
            elif add_status[0] == '0x3' and add_status[1] == '0xb0':
                Error = ['Error code: B003','Requiring data size error.']
                return Error
            elif add_status[0] == '0x2' and add_status[1] == '0xa0':
                Error = ['Error code: A002','Attribute error.']
                return Error
            elif add_status[0] == '0x0' and add_status[1] == '0xc8':
                Error = ['Error code: C800','System error.']
                return Error
            else:
                return add_status
        

            

          
class MotomanUDP:
    def __init__(self,ip="192.168.255.200",S_pulse = 1435.4, L_pulse = 1300.4, U_pulse = 1422.2, R_pulse = 969.9, B_pulse = 980.2, T_pulse = 454.7) -> None:
        """
        Yaskawa motoman MA1440 
        deg/pulse
        - S_pulse (float, optional): S-Axis encoder pulses per degree. Defaults to 1435.4.
        - L_pulse (float, optional): L-Axis encoder pulses per degree. Defaults to 1300.4.
        - U_pulse (float, optional): U-Axis encoder pulses per degree. Defaults to 1422.2.
        - R_pulse (float, optional): R-Axis encoder pulses per degree. Defaults to 969.9.
        - B_pulse (float, optional): B-Axis encoder pulses per degree. Defaults to 980.2.
        - T_pulse (float, optional): T-Axis encoder pulses per degree. Defaults to 454.7.
        """
        self.S_pulse = S_pulse
        self.L_pulse = L_pulse
        self.U_pulse = U_pulse
        self.R_pulse = R_pulse
        self.B_pulse = B_pulse
        self.T_pulse = T_pulse

        # socket UDP setting
        self.s = socket.socket(socket.AF_INET,          #Internet socket type
                               socket.SOCK_DGRAM)
        # Set time out , unit is second.
        self.s.settimeout(0.5)

        # IP and Port
        self.UDP_IP = ip
        self.UDP_PORT = 10040

        # Tool
        self.Time = TimeTool()

    def sendCmd(self, reqSubHeader, reqData, procDiv=1):
        # Make Request Packet
        req_packet = UDP_packet(reqSubHeader, reqData).Pack_Req_packet()

        

        # Send Request Packet
        self.s.sendto( req_packet,                             #UDP packet
                           (self.UDP_IP, self.UDP_PORT) )
        
        # Rceive Answer Packet
        (Ans_packet, address) = self.s.recvfrom(512)

        return Ans_packet
    
    
    
    def _sendCmd(self, req_packet):
        """Send Request Packet
        """
        # Send Request Packet
        self.s.sendto( req_packet,                             #UDP packet
                           (self.UDP_IP, self.UDP_PORT) )
        
        
    def _rceiveAns(self):
        """Receive reply packet.
        """
        (Ans_packet, address) = self.s.recvfrom(512)

        return Ans_packet


    def ServoMH(self, state):
        """Servo ON/OFF
        - state(1) = ON
        - state(2) = OFF
        """
        reqSubHeader = {'Command_No': (0x83, 0x00),  #Command No.
                        'Instance': [2, 0],             #instance 1: HOLD, 2: Servo ON, 3: HLOCK
                        'Attribute': 1,                   #Fixed to “1”
                        'Service':  0x10,            #Get_Attribute_Single: 0x0E, Get_Attribute_All: 0x01
                        'Padding': (0, 0) }
        reqData = [state,0,0,0]

        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        Error = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        return Error
    
    def holdMH(self, state):
        """Hold ON/OFF
        - state(1) = ON
        - state(2) = OFF
        """
        reqSubHeader = {'Command_No': (0x83, 0x00),  #Command No.
                        'Instance': [1, 0],             #instance 1: HOLD, 2: Servo ON, 3: HLOCK
                        'Attribute': 1,                   #Fixed to “1”
                        'Service':  0x10,            #Get_Attribute_Single: 0x0E, Get_Attribute_All: 0x01
                        'Padding': (0, 0) }
        reqData = [state,0,0,0]

        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        Error = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        return Error
    
    def getstatusMH(self):
        """Get status INF.
        - Data 1 
            - bit0 Step 
            - bit1 1 cycle 
            - bit2 Automatic and continuous
            - bit3 Running 
            - bit4 In-guard safe operation
            - bit5 Teach 
            - bit6 Play 
            - bit7 Command remote

        - Data 2 
            - bit0
            - bit1 In hold status (by programming pendant)
            - bit2 In hold status (externally)
            - bit3 In hold status (by command)
            - bit4 Alarming
            - bit5 Error occurring
            - bit6 Servo ON
            - bit7
        - Return:
            data = [0~255, 0, 0, 0, 0~255, 0, 0, 0]
        """
        reqSubHeader= { 'Command_No': (0x72, 0x00),
                    'Instance': [1, 0],
                    'Attribute': 0,
                    'Service':  0x01,
                    'Padding': (0, 0) }
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        
        
        return data

    def getSysTime(self, Type=211):
        """Get DX200 system time
        - Args:
            - DX200控制箱總電源開啟時計算:
                - 1 :Control power ON time
            - 伺服電源啟動時開始計算:
                - 10 :Servo power ON time (TOTAL)
                - 11 to 18 :Servo power ON time (R1 to R8)
                - 21 to 44 :Servo power ON time (S1 to S24)
            - 程式開始執行時開始計算:
                - 110 :Play back time (TOTAL)
                - 111 to 118 :Play back time (R1 to R8)
                - 121 to 144 :Play back time (S1 to S24)
            - 手臂開始運動時開始計算:
                - 210 :Motion time (TOTAL)
                - 211 to 218 :Motion time (R1 to R8) >>> defult
                - 221 to 244 :Motion time (S1 to S24)
            - 應用之工作類別總時數(ex: Arc welding)
                - 301 to 308 :Operation time (application 1 to 8)
        - Return:
           - hours: 總小時數
           - minutes: 分鐘數
           - seconds: 秒數
           - totalSeconds: 總秒數(hour*3600 + minutes*60 + seconds)
        """
        # TODO 待測試
        Type = hex(Type)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Type = Type[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Type[:2], 16)
        low_byte = int(Type[2:], 16)

        
        reqSubHeader= { 'Command_No': (0x88, 0x00),
                    'Instance': [low_byte, high_byte],
                    'Attribute': 2,
                    'Service':  0x0E,
                    'Padding': (0, 0) }
        reqData = []

        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        
        result = self.list_to_char_string(data)
        # 將時間字串分割為總時數和分鐘秒數
        total_hour_str, minutes_seconds_str = result.split(':')

        # 總小時數
        hours = int(total_hour_str)
        # 分離出分鐘和秒數
        minutes, seconds = map(int, minutes_seconds_str.split("'"))
        # 計算總秒數
        totalSeconds = hours *3600 + minutes * 60 + seconds
       
        return hours, minutes, seconds, totalSeconds
    
    def list_to_char_string(self, lst):
        # 將列表中的數字轉換為對應的ASCII字元並組成字串
        char_string = ''.join([chr(num) for num in lst])
        return char_string
    
    def getcoordinateMH(self, Type:int):
        """Get coordniate or Motor Pulse
        - Args :
            - Type(1 or 101)
                - 1 :Motor Pulse(6 axis)
                - 101 : Cartesian coordinate
            
        - Return:
            - result:
                - Type = 1   ➔[dataType=1 , Form, Tool No, User coordinate No, Extended form, S pulse, L pulse, U pulse, R pulse, B pulse, T pulse, 0, 0]
                - Type = 101 ➔[dataType=16, Form, Tool No, User coordinate No, Extended form, x, y, z, Rx, Ry, Rz, 0, 0]
            - coordinate:
                - Type = 1   ➔[S degree, L degree, U degree, R degree, B degree, T degree]
                - Type = 101 ➔[x, y, z, Rx, Ry, Rz]
        """
        
        """
        - Instance: R1
            - Read Pulse data: 1
            - Read coordinate data: 101
        """
        reqSubHeader= { 'Command_No': (0x75, 0x00),
                    'Instance': [Type, 0],
                    'Attribute': 0,
                    'Service':  0x0E,
                    'Padding': (0, 0) }
        reqData = []
    
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        result = self.Cvt_SignInt(data)

        
        if Type == 101:
            data = {"dataType": result[0],
                    "Form": result[1],
                    "Toolnumber": result[3],
                    "UserCoordinate": result[4]}
            coordinate = [result[5], result[6], result[7], result[8], result[9], result[10]]

            return data, coordinate
        elif Type == 1:
            Pulse = [result[5], 
                          result[6], 
                          result[7], 
                          result[8], 
                          result[9], 
                          result[10]]
            
            JointAngle = [float(result[5]/self.S_pulse), 
                          float(result[6]/self.L_pulse), 
                          float(result[7]/self.U_pulse), 
                          float(result[8]/self.R_pulse), 
                          float(result[9]/self.B_pulse), 
                          float(result[10]/self.T_pulse)]
            return result, JointAngle, Pulse
        else:
            print("Your dataType is Error!!!")
    
    
    def getTorqueMH(self):
        """Get Torque
        """
        reqSubHeader= { 'Command_No': (0x77, 0x00),
                    'Instance': [1, 0],
                    'Attribute': 0,
                    'Service':  0x01,
                    'Padding': (0, 0) }
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        result = self.Cvt_SignInt(data)
        if result == []:
            Torque = [0, 0, 0, 0, 0, 0]
            return Torque
        else:
            Torque = [result[0], result[1], result[2], result[3], result[4], result[5]]
            return Torque
     
    def Cvt_SignInt(self, data):
        """將4Byte數據轉換成32bit有符整數 or 2Byte數據轉換成16bit有符整數
        Convert 32bit Signed Integer
        input type: list
        input len: 4
        """
        result = []
        # coordinate
        if len(data) == 52:
            for i in range(0, len(data), 4):
                databuffer = (data[i+3] << 24) | (data[i+2] << 16) | (data[i+1] << 8) | data[i]
                
                if databuffer & (1 << 31):
                    databuffer -= 1 << 32
                
                if i == 20:
                    databuffer = round(databuffer*0.001,3)
                elif i == 24:
                    databuffer = round(databuffer*0.001,3)
                elif i == 28:
                    databuffer = round(databuffer*0.001,3)
                elif i == 32:
                    databuffer = round(databuffer*0.0001,4)
                elif i == 36:
                    databuffer = round(databuffer*0.0001,4)
                elif i == 40:
                    databuffer = round(databuffer*0.0001,4)
                result.append(databuffer)

        # Pulse
        elif len(data) == 44:
            for i in range(0, len(data), 4):
                databuffer = (data[i+3] << 24) | (data[i+2] << 16) | (data[i+1] << 8) | data[i]
                
                if databuffer & (1 << 31):
                    databuffer -= 1 << 32
                
                # if i == 20:
                #     databuffer = round(databuffer*0.001,3)
                # elif i == 24:
                #     databuffer = round(databuffer*0.001,3)
                # elif i == 28:
                #     databuffer = round(databuffer*0.001,3)
                # elif i == 32:
                #     databuffer = round(databuffer*0.0001,4)
                # elif i == 36:
                #     databuffer = round(databuffer*0.0001,4)
                # elif i == 40:
                #     databuffer = round(databuffer*0.0001,4)
                result.append(databuffer)
        
        # Torque
        elif len(data) == 24:
            for i in range(0, len(data), 4):
                # Combine the four bytes into a 32-bit unsigned integer
                databuffer = (data[i+3] << 24) | (data[i+2] << 16) | (data[i+1] << 8) | data[i]

                if databuffer & (1 << 31):
                    databuffer -= 1 << 32
                
                result.append(databuffer)

        # single data(4Byte)
        elif len(data) == 4:
            databuffer = (data[3] << 24) | (data[2] << 16) | (data[1] << 8) | data[0]

            if databuffer & (1 << 31):
                databuffer -= 1 << 32
                
            result.append(databuffer)
        
        # single data(2Byte)
        elif len(data) == 2:
            databuffer = (data[1] << 8) | data[0]

            if databuffer & (1 << 15):
                databuffer -= 1 << 16
                
            result.append(databuffer)

        # multiple data(2Byte) multiple Integer
        elif len(data) == 22:
            # 首4Byte 是資料筆數
            databuffer = (data[3] << 24) | (data[2] << 16) | (data[1] << 8) | data[0]

            if databuffer & (1 << 31):
                databuffer -= 1 << 32
                
            result.append(databuffer)

            # 之後每2Byte是變數資料(Integer)
            for i in range(4, len(data), 2):
                databuffer = (data[i+1] << 8) | data[i]

                if databuffer & (1 << 15):
                    databuffer -= 1 << 16
                    
                result.append(databuffer)

        # multipleReadVar
        elif len(data) == 472:
            for i in range(0, len(data), 4):
                databuffer = (data[i+3] << 24) | (data[i+2] << 16) | (data[i+1] << 8) | data[i]

                if databuffer & (1 << 31):
                    databuffer -= 1 << 32
                    
                result.append(databuffer)

        return result
    
    def Cvt_UnsignedInt(self, data):
        """Convert 32-bit unsigned Integer
        - Args: type: list
        - Return :list
        """
        result = []
        if len(data) == 24:
            for i in range(0, len(data), 4):
                # Combine the four bytes into a 32-bit unsigned integer
                databuffer = (data[i+3] << 24) | (data[i+2] << 16) | (data[i+1] << 8) | data[i]
      
                result.append(databuffer)
        
        return result
    
    ################################################ I/O ################################################
    
    def ReadIO(self, Pin):
        """Read I/O Data
        * Arg:
            Pin number.

        * Return:
            Pin number Data.
        """
        Pin_hex = hex(Pin)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Pin_hex = Pin_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Pin_hex[:2], 16)
        low_byte = int(Pin_hex[2:], 16)
        
        reqSubHeader = { 'Command_No': (0x78, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 1,
                        'Service':  0x0E,
                        'Padding': (0, 0)}
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        return data
    
    def WriteIO(self, Pin, data):
        """Write I/O Data
        * Args:
            Pin number
            I/O Data

        * Return:
            UDP stute
        """

        Pin_hex = hex(Pin)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Pin_hex = Pin_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Pin_hex[:2], 16)
        low_byte = int(Pin_hex[2:], 16)
        
        reqSubHeader = {'Command_No': (0x78, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 1,
                        'Service':  0x10,
                        'Padding': (0, 0)}
        reqData = [data]
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)

        return data
    
    ################################################ Variable ################################################
    def ReadVar(self, varType:str, address:int):
        """Read variable
        - Args:
            - varType: Input str. ex: "Integer".
                - Byte
                - Integer
                - double
                - Real
            - address: Pin number.

        - Return:
            Variable data
        """
        # TODO Integer測試成功，其餘三個未測試

        command_No = 0x00

        if varType == "Byte":
            command_No = 0x7A
            
        elif varType == "Integer":
            command_No = 0x7B
        elif varType == "double":
            command_No = 0x7C
        elif varType == "Real":
            command_No = 0x7D
        else:
            print("varType error!!!")

        Address_hex = hex(address)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)


        reqSubHeader = {'Command_No': (command_No, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 1,
                        'Service':  0x0E,
                        'Padding': (0, 0)}
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        var = self.Cvt_SignInt(data)
        
        return var
    
    def WriteVar(self, varType, address, data):
        """Write Variable to address
         Args:
            - varType: Input str. ex: "Integer".
                - Byte
                - Integer: -32768 to 32767
                - double: -2147483648 to 2147483647
                - Real: 3.4E+38 to 3.4E38. E:10的次方數
            - address: Pin number.

        - Return:
            Variable data
        """
        # TODO 尚未測試

        command_No = 0x00

        if varType == "Byte":
            command_No = 0x7A
        elif varType == "Integer":
            command_No = 0x7B
            data = struct.pack('h', data)
        elif varType == "double":
            command_No = 0x7C
        elif varType == "Real":
            command_No = 0x7D
        else:
            print("varType error!!!")

        Address_hex = hex(address)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)

        reqSubHeader = {'Command_No': (command_No, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 1,
                        'Service':  0x10,
                        'Padding': (0, 0)}
        reqData = data
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        
        return data
        
    def multipleReadVar(self, firstAddress, Number):
        """Multiple Read Variable
        - Arg:
            - firstAddress: 多筆資料的起始變數編號.
            - Number: Number of data written (Maximum 9)
            
        - Return:
            - Variable data.
        """
        Address_hex = hex(firstAddress)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)


        # 要讀取的資料個數
        Number = struct.pack('I', Number)


        reqSubHeader = {'Command_No': (0x03, 0x03),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 0,
                        'Service':  0x33,
                        'Padding': (0, 0)}
        reqData = Number
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        var = self.Cvt_SignInt(data)

        return var
    
    def multipleWriteVar(self, firstAddress:int, Number:int, data:list):
        """Multiple Write Variable(Integer)
        - Arg:
            - firstAddress: 多筆資料的起始變數編號.
            - Number: Number of data written (Maximum 9)
            - data: [0, 1, 2, .....]
                
            
        - Return:
            - status: Command Ans. 
        """
    
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
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)

        return data
        

    def ReadRPVar(self, address):
        """Read single Robot Position Variable
        - Arg:
            address(0 ~ 127)
        
        - Return:
            - Variable data:
                - dataType:
                    - 0: Pulse value
                    - 16: Base coordinated value
                    - 17: Robot coordinated value
                    - 18: User coordinated value
                    - 19: Tool coordinated value
                - Form
                - Tool number
                - User coordinate number
                - Extended form
                - First coordinate data
                - Second coordinate data
                - Third coordinated data
                - Fourth coordinate data
                - Fifth coordinate data
                - Sixth coordinate data
                - Seventh coordinate data
                - Eighth coordinate data
        """
        # TODO 測試成功，函式需優化，讀回之資料還未分類

        Address_hex = hex(address)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)

        dataType = 1
        # dataType 轉換16進制
        dataType_hex = hex(dataType)
        dataType_hex = int(dataType_hex, 16)


        reqSubHeader = {'Command_No': (0x7F, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 0,
                        'Service':  0x01,
                        'Padding': (0, 0)}
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        var = self.Cvt_SignInt(data)

        return var

    def WriteRPVar(self, address, data:list):
        """Write single Robot Position Variable
            - address: 變數編號.
            - data:
                - Type: dict
                - format: [dataType, Form, Toolnumber, UserCoordinate, coordinate]

                - Note:
                    - dataType(default 17):
                        - 0 : Pulse
                        - 16: Base coordinated value.
                        - 17: Robot coordinated value. 
                        - 18: User coordinated value.
                        - 19: Tool coordinated value.
                    - Form: Arm pose(請看手冊定義)
                    - Toolnumber: Tool data number. (default 5)
                    - UserCoordinate: User coordinate system number. (default 0)
                    - Extended form: None(default 0).
                    - coordinate( 1st~6th data):
                        - type: list
                        - format: [x(first), y(second), z(third), Rx(fourth), Ry(Fifth), Rz(Sixth)]
                    - SeventhCoordinate: None(default 0).
                    - Eighthcoordinate: None(default 0).
        """

        dataType = struct.pack('I', data[0])
        Form = struct.pack('I', data[1])
        Toolnumber = struct.pack('I', data[2])
        UserCoordinate = struct.pack('I', data[3])
        ExtendedForm = struct.pack('I', 0)
        FirstCoordinate  = self.signDecide(data[4], 1000)
        SecondCoordinate = self.signDecide(data[5], 1000)
        ThirdCoordinated = self.signDecide(data[6], 1000)
        FourthCoordinate = self.signDecide(data[7], 1000)
        FifthCoordinate  = self.signDecide(data[8], 1000)
        SixthCoordinate  = self.signDecide(data[9], 1000)
        SeventhCoordinate = struct.pack('i', 0)
        EighthCoordinate = struct.pack('i', 0)

        Packet = dataType\
                + Form + Toolnumber + UserCoordinate + ExtendedForm + FirstCoordinate + SecondCoordinate + ThirdCoordinated + FourthCoordinate\
                + FifthCoordinate + SixthCoordinate + SeventhCoordinate + EighthCoordinate
                
        Address_hex = hex(address)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)
        
        reqSubHeader = {'Command_No': (0x7F, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 0,
                        'Service':  0x02,
                        'Padding': (0, 0)}
        reqData = Packet
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)

        return data
    

    def multipleReadRPVar(self, firstAddress, Number):
        """Multiple Read Robot Position Variable
        - Arg:
            - address(多筆資料的起始變數編號)
            - Number: Number of data read. (Maximum 9)
        
        - Return:
        """
        # TODO 已測試成功一次讀取9筆資料，函式輸出的資料需要優化處理

        Address_hex = hex(firstAddress)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Address_hex = Address_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Address_hex[:2], 16)
        low_byte = int(Address_hex[2:], 16)


        # 要讀取的資料個數
        Number = struct.pack('I', Number)


        reqSubHeader = {'Command_No': (0x07, 0x03),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 0,
                        'Service':  0x33,
                        'Padding': (0, 0)}
        reqData = Number
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        var = self.Cvt_SignInt(data)

        return var

    def multipleWriteRPVar(self, firstAddress:int, Number:int, data:dict):
        """Multiple Read Robot Position Variable
        - Arg:
            - firstAddress: 多筆資料的起始變數編號.
            - Number: Number of data written (Maximum 9)
            - data:
                - Type: dict
                - format: 'data number' : [dataType, Form, Toolnumber, UserCoordinate, coordinate]

                - Note:
                    - dataType:
                        - 0 : Pulse
                        - 16: Base coordinated value.
                        - 17: Robot coordinated value. (default)
                        - 18: User coordinated value.
                        - 19: Tool coordinated value.
                    - Form: Arm pose(請看手冊定義)
                    - Toolnumber: Tool data number. (default 5)
                    - UserCoordinate: User coordinate system number. (default 0)
                    - Extended form: None(default 0).
                    - coordinate( 1st~6th data):
                        - type: list
                        - format: [x(first), y(second), z(third), Rx(fourth), Ry(Fifth), Rz(Sixth)]
                    - SeventhCoordinate: None(default 0).
                    - Eighthcoordinate: None(default 0).
            
        - Return:
            - status: Command Ans. 
        """
    
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

            FirstCoordinate  = self.signDecide(data[f'{n}'][4], 1000)
            SecondCoordinate = self.signDecide(data[f'{n}'][5], 1000)
            ThirdCoordinate  = self.signDecide(data[f'{n}'][6], 1000)
            FourthCoordinate = self.signDecide(data[f'{n}'][7], 1000)
            FifthCoordinate  = self.signDecide(data[f'{n}'][8], 1000)
            SixthCoordinate  = self.signDecide(data[f'{n}'][9], 1000)

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
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)

        return data

        

    ################################################ Register ################################################
    
    def ReadRegister(self, number):
        """
        - number : 12bit
        """
        
        number_hex = hex(number)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        number_hex = number_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(number_hex[:2], 16)
        low_byte = int(number_hex[2:], 16)
        
        reqSubHeader = { 'Command_No': (0x79, 0x00),
                    'Instance': [low_byte, high_byte],
                    'Attribute': 1,
                    'Service':  0x0E,
                    'Padding': (0, 0)}
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        return data
    
    def WriteRegister(self, Pin, data):
        # TODO 559後無法讀取與寫入
        """
        559後無法讀取與寫入
        Service 嘗試 0x01
        """
        Pin_hex = hex(Pin)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        Pin_hex = Pin_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(Pin_hex[:2], 16)
        low_byte = int(Pin_hex[2:], 16)
        
        reqSubHeader = {'Command_No': (0x79, 0x00),
                        'Instance': [low_byte, high_byte],
                        'Attribute': 1,
                        'Service':  0x10,
                        'Padding': (0, 0)}
        if Pin >= 560:
            # M560 - M599 Register是以12bit資料格式表示，但封包型式則以16bit格式傳送
            data_ = data << 4
            packed_data = struct.pack('>H', data_)
            reqData = packed_data
            
        else:
            reqData = [data]
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        return data
    

################################################ Robot Move Cammand ################################################
    def MoveCMD_data(self, moveType, moveSpeedType, speed, coordinateType, coordinate, Type= 4, Expanded_type= 0, Tool_No=5, User_coordinate=0):

        """Move Joint Angle(Point to Point)
        - Args: data use  Pack_MoveCMD_Packet(fun.)!!!
        - moveType:
            - 1: Link absolute position operation() ➜ Joint space ➜ 走弧線
            - 2: Straight absolute position operation ➜ Catesian space ➜ 走直線
            - 3: Straight increment value operation ➜ Catesian space ➜ 走直線 ➜ 給位置誤差
        - moveSpeedType:
            - 0: Link operation(0.01%)
            - 1: V(Cartesian operation)(0.1 mm/s)
            - 2: VR(Cartesian operation)(0.1 degree/s) ➜ 此選項移動速度極快，請小心使用!!!
        - coordinateType:
            - 16: Base coordinate
            - 17: Robot coordinate
            - 18: User coordinate
            - 19: Tool coordinate
        - x  unit(μm) 
        - y  unit(μm)
        - z  unit(μm)
        - Rx unit(0.0001 degree)
        - Ry unit(0.0001 degree)
        - Rz unit(0.0001 degree)
        """
        # Example
        # Movedata ={"Robot": 1,
        #    "Station": 1,
        #    "speedType": 0,
        #    "speed": 5,
        #    "coordinateType": 19,
        #    "coordinate":[485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879],
        #    "Reservation1":0,
        #    "Reservation2":0,
        #    "Type": 0,
        #    "Expanded type": 0,
        #    "Tool No": 5,
        #    "User coordniate": 0,
        #    "Base axis": [0, 0, 0],
        #    "Station axis": [0, 0, 0, 0, 0, 0]}

        Movedata ={"Robot": 1,
           "Station": 0,
           "moveType": moveType,
           "moveSpeedType": moveSpeedType,
           "speed": speed,
           "coordinateType": coordinateType,
           "coordinate":[coordinate[0], coordinate[1], coordinate[2], coordinate[3], coordinate[4], coordinate[5]],
           "Reservation1":0,
           "Reservation2":0,
           "Type": Type,
           "Expanded type": Expanded_type,
           "Tool No": Tool_No,
           "User coordniate": User_coordinate,
           "Base axis": [0, 0, 0],
           "Station axis": [0, 0, 0, 0, 0, 0]}
        
        return Movedata

    def signDecide(self, number, rate):
        """判斷正負符號並編碼成Bytes型別
        """
        if number < 0:
            ans = struct.pack('i', int(number*rate))
        else:
            ans = struct.pack('I', int(number*rate))

        return ans

    def Pack_MoveCMD_Packet(self, Movedata):
        """Pack the MOVE command package
        """
        
        Robot = struct.pack('I', Movedata["Robot"])
        Station= struct.pack('I', Movedata["Station"])
        moveType= struct.pack('I', Movedata["moveSpeedType"])
        speed= struct.pack('I', Movedata["speed"])
        # speed= struct.pack('f', Movedata["speed"])
        coordinateType= struct.pack('I', Movedata["coordinateType"])
        coordinate_x= self.signDecide(Movedata["coordinate"][0], 1000)
        coordinate_y= self.signDecide(Movedata["coordinate"][1], 1000)
        coordinate_z= self.signDecide(Movedata["coordinate"][2], 1000)
        coordinate_Rx= self.signDecide(Movedata["coordinate"][3], 10000)
        coordinate_Ry= self.signDecide(Movedata["coordinate"][4], 10000)
        coordinate_Rz= self.signDecide(Movedata["coordinate"][5], 10000)
        Reservation1= struct.pack('I', Movedata["Reservation1"])
        Reservation2= struct.pack('I', Movedata["Reservation2"])
        Type= struct.pack('I', Movedata["Type"])
        Expanded_type= struct.pack('I', Movedata["Expanded type"])
        Tool_No= struct.pack('I', Movedata["Tool No"])
        User_coordniate= struct.pack('I', Movedata["User coordniate"])
        Base_axis_1= struct.pack('I', Movedata["Base axis"][0])
        Base_axis_2= struct.pack('I', Movedata["Base axis"][1])
        Base_axis_3= struct.pack('I', Movedata["Base axis"][2])
        Station_axis_1= struct.pack('I', Movedata["Station axis"][0])
        Station_axis_2= struct.pack('I', Movedata["Station axis"][1])
        Station_axis_3= struct.pack('I', Movedata["Station axis"][2])
        Station_axis_4= struct.pack('I', Movedata["Station axis"][3])
        Station_axis_5= struct.pack('I', Movedata["Station axis"][4])
        Station_axis_6= struct.pack('I', Movedata["Station axis"][5])
        # Move command data 
        MovePacket = Robot+Station+moveType+speed+coordinateType+coordinate_x+coordinate_y+coordinate_z\
                +coordinate_Rx+coordinate_Ry+coordinate_Rz+Reservation1+Reservation2+Type+Expanded_type\
                +Tool_No+User_coordniate+Base_axis_1+Base_axis_2+Base_axis_3+Station_axis_1+Station_axis_2\
                +Station_axis_3+Station_axis_4+Station_axis_5+Station_axis_6
        
        return MovePacket, Movedata["moveType"]

    def MoveCMD_req(self, moveType, data):

        if moveType < 1 and moveType > 3:
            print("moveType value Error!!!")

        reqSubHeader = { 'Command_No': (0x8A, 0x00),
                    'Instance': [moveType, 0],  
                    'Attribute': 1,
                    'Service':  0x02,
                    'Padding': (0, 0)}
        reqData = data

        
        Ans_packet = self.sendCmd(reqSubHeader, reqData)
        
        status = UDP_packet.Unpack_Ans_packet(self, Ans_packet)

        return status

    def moveCoordinateMH(self, moveType, moveSpeedType, speed, coordinateType, coordinate):
        """Move Command
        Use me!!! 
        - moveType:
            - 1: Link absolute position operation() ➜ Joint space ➜ 走弧線
            - 2: Straight absolute position operation ➜ Catesian space ➜ 走直線
            - 3: Straight increment value operation ➜ Catesian space ➜ 走直線 ➜ 給位置誤差
        - moveSpeedType :
            - 0: Link operation(0.01%)
            - 1: V(Cartesian operation)(0.1 mm/s)
            - 2: VR(Cartesian operation)(0.1 degree/s)➜ 此選項移動速度極快，請小心使用!!!
        - speed:
            - 0: unit (0.01%)
            - 1: unit (0.1 mm/s)
            - 2: unit (0.1 degree/s)
        - coordinateType:
            - 16: Base coordinate
            - 17: Robot coordinate
            - 18: User coordinate
            - 19: Tool coordinate
        - coordinate : [x, y, z, Rx, Ry, Rz] -list
            - x  unit(μm) 
            - y  unit(μm)
            - z  unit(μm)
            - Rx unit(0.0001 degree)
            - Ry unit(0.0001 degree)
            - Rz unit(0.0001 degree)
        - Type : Please read the manual!
        - Expanded type : Please read the manual!
        - Tool No.: 
            - 5: default
        - User_coordinate:
            - 0: default
        """
        # 參數
        # 填寫參數，並轉字典形式
        dict_data = self.MoveCMD_data(moveType, moveSpeedType, speed, coordinateType, coordinate)
        # 把字典打包封包
        Movedata_packet, moveType = self.Pack_MoveCMD_Packet(dict_data)
        # 加入標題、子標題並完成封包後寄出
        status = self.MoveCMD_req(moveType, Movedata_packet)

        return status

    def MoveJointAngleCMD_data(self, moveType, moveSpeedType, speed, JointAngle:list, Tool_No=5):
        """Move Joint Angle(Point to Point)
        - moveType:
            - 1: Link absolute position operation() ➜ Joint space ➜ 走弧線
            - 2: Straight absolute position operation ➜ Catesian space ➜ 走直線
        - moveSpeedType :
            - 0: Link operation(0.01%)
            - 1: V(Cartesian operation)(0.1 mm/s)
            - 2: VR(Cartesian operation)(0.1 degree/s)➜ 此選項移動速度極快，請小心使用!!!
        - speed:
            - 0: unit (0.01%)
            - 1: unit (0.1 mm/s)
            - 2: unit (0.1 degree/s)
        - coordinate : [S axis degree, L axis degree, U axis degree, R axis degree, B axis degree, T axis degree] -list
        - Type : Please read the manual!
        - Expanded type : Please read the manual!
        - Tool No.: 
            - 5: default
        - User_coordinate:
            - 0: default
        """

        Movedata ={"Robot": 1,
           "Station": 0,
           "moveType": moveType,
           "moveSpeedType": moveSpeedType,
           "speed": speed,
           "JointAngle":[JointAngle[0], JointAngle[1], JointAngle[2], JointAngle[3], JointAngle[4], JointAngle[5]],
           "Axis 78": [0, 0],
           "Tool No": Tool_No,
           "Base axis": [0, 0, 0],
           "Station axis": [0, 0, 0, 0, 0, 0]}
        
        return Movedata
    
    def Pack_MoveJointAngleCMD_Packet(self, Movedata):
        """Pack the MOVE command package
        """
        
        Robot = struct.pack('I', Movedata["Robot"])
        Station= struct.pack('I', Movedata["Station"])
        moveType= struct.pack('I', Movedata["moveSpeedType"])
        speed= struct.pack('I', Movedata["speed"])
        # 需經過轉換，先將degree to Pulse，再將Pulse轉換成Byte data
        SaxisPulse = self.signDecide(Movedata["JointAngle"][0]*self.S_pulse, 1)
        LaxisPulse = self.signDecide(Movedata["JointAngle"][1]*self.L_pulse, 1)
        UaxisPulse = self.signDecide(Movedata["JointAngle"][2]*self.U_pulse, 1)
        RaxisPulse = self.signDecide(Movedata["JointAngle"][3]*self.R_pulse, 1)
        BaxisPulse = self.signDecide(Movedata["JointAngle"][4]*self.B_pulse, 1)
        TaxisPulse = self.signDecide(Movedata["JointAngle"][5]*self.T_pulse, 1)
        axis7Pulse =  struct.pack('i', Movedata["Axis 78"][0])
        axis8Pulse =  struct.pack('i', Movedata["Axis 78"][1])
        Tool_No= struct.pack('I', Movedata["Tool No"])
        Base_axis_1= struct.pack('I', Movedata["Base axis"][0])
        Base_axis_2= struct.pack('I', Movedata["Base axis"][1])
        Base_axis_3= struct.pack('I', Movedata["Base axis"][2])
        Station_axis_1= struct.pack('I', Movedata["Station axis"][0])
        Station_axis_2= struct.pack('I', Movedata["Station axis"][1])
        Station_axis_3= struct.pack('I', Movedata["Station axis"][2])
        Station_axis_4= struct.pack('I', Movedata["Station axis"][3])
        Station_axis_5= struct.pack('I', Movedata["Station axis"][4])
        Station_axis_6= struct.pack('I', Movedata["Station axis"][5])
        # Move command data 
        MovePacket = Robot+Station+moveType+speed+SaxisPulse+LaxisPulse+UaxisPulse\
                +RaxisPulse+BaxisPulse+TaxisPulse+axis7Pulse+axis8Pulse+Tool_No+Base_axis_1+Base_axis_2\
                +Base_axis_3+Station_axis_1+Station_axis_2+Station_axis_3+Station_axis_4+Station_axis_5+Station_axis_6
        
        return MovePacket, Movedata["moveType"]
    
    def MoveJointAngleCMD_req(self, moveType, data):

        if moveType < 1 and moveType > 2:
            print("moveType value Error!!!")

        reqSubHeader = { 'Command_No': (0x8B, 0x00),
                    'Instance': [moveType, 0],  
                    'Attribute': 1,
                    'Service':  0x02,
                    'Padding': (0, 0)}
        reqData = data

        Ans_packet = self.sendCmd(reqSubHeader, reqData)
        
        status = UDP_packet.Unpack_Ans_packet(self, Ans_packet)

        return status
    
    def moveJointSapceMH(self, moveType, moveSpeedType, speed, JointAngle:list):
        """Move JointSapce Command
        Use me!!! 
        - moveType:
            - 1: Link absolute position operation() ➜ Joint space ➜ 走弧線
            - 2: Straight absolute position operation ➜ Catesian space ➜ 走直線
        - moveSpeedType :
            - 0: Link operation(0.01%)
            - 1: V(Cartesian operation)(0.1 mm/s)
            - 2: VR(Cartesian operation)(0.1 degree/s)➜ 此選項移動速度極快，請小心使用!!!
        - speed:
            - 0: unit (0.01%)
            - 1: unit (0.1 mm/s)
            - 2: unit (0.1 degree/s)
        - coordinate : [S axis degree, L axis degree, U axis degree, R axis degree, B axis degree, T axis degree] -list
        - Type : Please read the manual!
        - Expanded type : Please read the manual!
        - Tool No.: 
            - 5: default
        - User_coordinate:
            - 0: default
        """
        

        # 參數
        # 填寫參數，並轉字典形式
        dict_data = self.MoveJointAngleCMD_data(moveType, moveSpeedType, speed, JointAngle)
        # 把字典打包成封包
        Movedata_packet, moveType = self.Pack_MoveJointAngleCMD_Packet(dict_data)
        # 加入標題、子標題並完成封包後寄出
        status = self.MoveJointAngleCMD_req(moveType, Movedata_packet)

        return status

    def arconMH(self):
        """ARC ON
        Network input: #27012 and # 27013 ON.
        Ans = 8 + 4
        """
        udp.WriteIO(2701, 12)

    def arcoffMH(self):
        """ARC OFF
        - Network input: #2701X 賦歸 
        """
        udp.WriteIO(2701, 0)

    def wireout(self):
        """WIRE INCHING(送線)
        - Network input: #27010 ON.
        """
        udp.WriteIO(2701, 1)

    def wireback(self):
        """WIRE RETRACT(收線)
        - Network input: #27011 ON.
        """
        udp.WriteIO(2701, 2)

    def arcon_wireout(self):
        """ARC ON
        - Network input: 
            - ArcON : #27012 and # 27013 ON.
            - wireout : #27010 ON.
        Ans = 8 + 4 + 1
        """
        udp.WriteIO(2701, 13)

if __name__ == "__main__":
    # UDP test
    udp = MotomanUDP()
    Time = TimeTool()
    dB = dataBase()
    
    # 讀取DX200系統時間命令
    # 讀取DX200系統時間所花費的時間: 最慢11ms | 最快7ms | 平均9.56ms
    # hour, minutes, seconds, startTotal_seconds = udp.getSysTime(1)
    # print(startTotal_seconds)
    
    # 遠端起弧測試OK

    # 送線
    # udp.WriteIO(2701, 1)

    # 收線
    # udp.WriteIO(2701, 2)

    # 起弧
    # udp.WriteIO(2701, 12)

    # IO狀態賦歸
    # udp.WriteIO(2701, 0)

    # # Read IO
    # data = udp.ReadIO(2701)
    # print(data)

    # 位置讀取(Cartesian)
    # 命令時間(ms) :
    # 最大值: 24.0
    # 最小值: 11.0
    # 平均值: 15.61
    result, coordinate = udp.getcoordinateMH(101)
    print(result)
    print(coordinate)
    """
    矩形軌跡:
    Org = [485.126, -1.295, 234.296, 179.9772, 20.2428, 1.6694]

    PreGo:[1028.838, -100.512, -60.384, 153.7943, -12.9858, -137.0558]

    第一段起點:[1028.892, -100.126, -133.43, 153.7838, -12.9644, -137.0478]
    第一段姿態變換起點:[1028.898, 39.173, -133.479, 153.7858, -12.965, -137.0483]

    第二段起點:[1031.113, 46.448, -133.548, 153.794, -12.9626, -67.5844]
    第二段姿態變換前:[889.137, 46.416, -133.527, 153.7951, -12.9672, -67.5838]

    第三段起點:[883.23, 46.267, -136.13, 152.7504, 9.8314, 46.9511]
    第三段姿態變換前:[883.227, -94.75, -133.892, 152.7565, 9.824, 46.9406]

    第四段起點:[883.285, -103.725, -135.859, 166.9137, 9.1798, 131.1553]
    第四段終點:[1034.248, -103.696, -135.859, 166.9115, 9.179, 131.1576]

    PreBack:[1034.267, -103.681, -45.869, 166.9084, 9.181, 131.1607]
    
    Org = [485.126, -1.295, 234.296, 179.9772, 20.2428, 1.6694]
    """
    
    # 位置讀取(Joint)
    # result, JointAngle, pulse = udp.getcoordinateMH(1)
    # print(JointAngle)
    # print(pulse)

    # 單筆變數讀取(Robot Position)
    # 命令時間(ms) :
    # 最大值: 12.0
    # 最小值: 3.0
    # 平均值: 6.37
    # status = udp.ReadRPVar(21)
    # print(status)

    # 單筆變數寫入(Robot Position)
    # 命令時間(ms) :
    # 最大值: 31.0
    # 最小值: 15.0
    # 平均值: 21.15
    # coordinate = [958.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149]
    # status = udp.WriteRPVar(14, coordinate)
    # print(status)

    # 單筆變數讀取(Integer)
    # 命令時間(ms) :
    # 最大值: 11.0
    # 最小值: 5.0
    # 平均值: 7.31
    # varType = "Integer"
    # address = 0
    # status = udp.ReadVar(varType, address)
    # print(status)

    # 單筆變數寫入(Integer)
    # 命令時間(ms) :
    # 最大值: 30.0
    # 最小值: 15.0
    # 平均值: 21.65
    # varType = "Integer"
    # address = 2
    # data = 160
    # status = udp.WriteVar(varType, address, data)
    # print(status)

    # 多筆變數讀取(Integer)
    # firstAddress  = 0
    # Number = 9
    # status = udp.multipleReadVar(firstAddress, Number)
    # print(status)

    # 多筆變數寫入(Integer)
    # 命令時間(ms) :
    # 最大值: 149.0
    # 最小值: 126.0
    # 平均值: 134.39
    # firstAddress  = 0
    # Number = 9
    # data = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # status = udp.multipleWriteVar(firstAddress, Number, data)
    # print(status)

    # 多筆位置變數讀取(Robot Position)
    # 命令時間(ms) :
    # 最大值: 11.0
    # 最小值: 3.0
    # 平均值: 7.23
    # status = udp.multipleReadRPVar(6, 9)
    # print(status)
        
    # 多筆位置變數寫入(Robot Position)
    # 命令時間(ms) :
    # n = 9
    # 最大值: 149.0
    # 最小值: 125.0
    # 平均值: 133.63
    # n = 8
    # 最大值: 130.0
    # 最小值: 115.0
    # 平均值: 120.19
    # n = 7
    # 最大值: 110.0
    # 最小值: 97.0
    # 平均值: 105.66
    # n = 6
    # 最大值: 100.0
    # 最小值: 83.0
    # 平均值: 91.62
    # format : {'number' :[dataType, Form, Toolnumber, UserCoordinate, firstCoordinate, SecondCoordinate, ThirdCoordinate, FourthCoordinate, FifthCoordinate, SixthCoordinate]}
    # b = Time.ReadNowTime()
    # data = {'0':[17, 4, 5, 0, 958.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '1':[17, 4, 5, 0, 959.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '2':[17, 4, 5, 0, 960.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '3':[17, 4, 5, 0, 961.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '4':[17, 4, 5, 0, 962.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '5':[17, 4, 5, 0, 963.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '6':[17, 4, 5, 0, 964.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '7':[17, 4, 5, 0, 965.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #         '8':[17, 4, 5, 0, 966.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149]}
    # status = udp.multipleWriteRPVar(36, 9, data)
    # a = Time.ReadNowTime()
    # err = Time.TimeError(b,a)
    # err_ms = err["millisecond"]
    # print(f"花費時間: {err_ms}ms")

    # 伺服電源開啟
    # status = udp.ServoMH(1)

    # 伺服電源關閉
    # status = udp.ServoMH(2)
    # print(status)

    # 動作暫停ON
    # status = udp.holdMH(1)
    # print(status)

    # 動作暫停OFF
    # status = udp.holdMH(2)
    # print(status)

    # 系統狀態讀取
    # data = udp.getstatusMH()
    # print(data)

    # Read torque
    # data = udp.getTorqueMH()
    # print(data)

    # Read Register
    # data = udp.ReadRegister(561)
    # print(data)

    # Write Register
    # data = udp.WriteRegister(620, 0)
    # print(data)

    # Move指令

    # 設定座標
    # ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
    # weldstart = [955.41, -102.226, -166.726, -165.2919, -7.1991, 17.5642]
    # weldend = [955.404, 14.865, -166.749, -165.2902, -7.1958, 17.5569]
    # GoalEnd = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]
    # test = [958.52, -35.709, -164.944, -165.287, -7.172, 17.5178]

    # Cariten space
    # Real speed = speed * 0.1 mm/s
    # status = udp.ServoMH(1)
    # status = udp.moveCoordinateMH(2,1, 200, 17, test)
    # print(status)

    # Point to Point
    # Real speed = speed * 0.01%
    # status = udp.moveCoordinateMH(0, 500, 17, coord)
    # print(status)

    # pmov
    # udp.moveJointSapceMH( 1, 0, 100, JointAngle)

    # MOVJ
    # status = udp.ServoMH(1)
    # ORG = [-0.0020900097533788488, -38.81728698861888, -41.08704823512867, 0.003093102381688834, -76.45684554172618, 1.071035847811744]
    # ORG_pulse = [-3, -50478, -58434, 3, -74943, 487]
    # GoalEnd = [-13.775254284519994, 4.050292217779145, -45.61383771621431, -71.65996494483967, -32.04448071822077, 87.91071035847811]
    # GoalEnd_pulse = [-19773, 5267, -64872, -69503, -31410, 39973]
    # # status = udp.ServoMH(1)
    # udp.moveJointSapceMH(1, 1, 100, ORG)

    """
    cmdTime test
    """
    # cmdtimeData = np.zeros((100))
    # for i in range(100):
    #     b = Time.ReadNowTime()
        
        
    #     # result, coordinate = udp.getcoordinateMH(101)
    #     # # print(coordinate)

    #     # status = udp.ReadVar("Integer", 0)
    #     # # print(status)

    #     firstAddress  = 0
    #     Number = 9
    #     data = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    #     status = udp.multipleWriteVar(firstAddress, Number, data)

    #     data = {'0':[17, 4, 5, 0, 958.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '1':[17, 4, 5, 0, 959.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '2':[17, 4, 5, 0, 960.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '3':[17, 4, 5, 0, 961.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '4':[17, 4, 5, 0, 962.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '5':[17, 4, 5, 0, 963.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '6':[17, 4, 5, 0, 964.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '7':[17, 4, 5, 0, 965.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149],
    #             '8':[17, 4, 5, 0, 966.535, -37.777, -104.713, -165.2944, -7.1707, 17.5149]}
    #     status = udp.multipleWriteRPVar(36, 9, data)

    #     a = Time.ReadNowTime()
    #     cmdTime = Time.TimeError(b,a)
    #     print(cmdTime["millisecond"], "毫秒")
    #     dB.Save_time(cmdTime["millisecond"], "Experimental_data/cmdTime/multipleWriteVar/multipleWriteVar_cmdTime_n9.csv")
    #     cmdtimeData[i] = cmdTime["millisecond"]

    # # 计算最大值
    # max_val = np.max(cmdtimeData)

    # # 计算最小值
    # min_val = np.min(cmdtimeData)

    # # 计算平均值
    # mean_val = np.mean(cmdtimeData)

    # print("最大值:", max_val)
    # print("最小值:", min_val)
    # print("平均值:", mean_val)
    # print("End")


# test

# # 創建一個空視窗
# cv2.namedWindow('Empty Window')

# ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
# weldstart = [955.398, -87.132, -166.811, -165.2914, -7.1824, 17.5358]
# weldend = [955.421, -8.941, -166.768, -165.288, -7.1896, 17.5397]
# testGoal = [485.364+50, -1.213, 234.338+50, 179.984, 20.2111, 1.6879]

# # Servo ON
# Servo_status = udp.ServoMH(1)

# # 讀取是否Servo ON
# sys_status = udp.getstatusMH()
# print(sys_status)
# if sys_status[4] == 64:
#     print("Servo ON is success")
#     # 0: speed * 0.01 %
#     # 1: speed * 0.1 mm/s
#     # 2: speed * 0.1 deg/s
    
    
#     while True:
#         # 等待鍵盤事件，並取得按下的鍵
#         key = cv2.waitKey(1) & 0xFF
#         torque = udp.getTorqueMH()
#         print(torque)

#         # 離開
#         if key == 27:  # 27是'ESC'鍵的ASCII碼
#             print('You pressed "ESC". Exiting...')
#             status = udp.holdMH(2)
#             time.sleep(0.01)
#             status = udp.ServoMH(2)
#             udp.WriteIO(2701, 0)
#             break

#         elif key == ord('h'):
#             print('Hold on')
#             status = udp.holdMH(1)
        
#         elif key == ord('w'):
#             print('Send Position Error')
#             status = udp.holdMH(1)
#             time.sleep(0.01)
#             status = udp.holdMH(2)

#             # 增量型
#             dp = [10, 0, 0, 0, 0, 0]
#             status = udp.moveCoordinateMH(3, 1, 100, 17, dp)
#             print(status)

#             while True:
#                 print("讀取是否運轉中")
#                 sys_status = udp.getstatusMH()
#                 print(sys_status)

#                 if sys_status[0] == 194:
#                     # 回歸原本路徑
#                     status = udp.moveCoordinateMH(2,1, 100, 17, weldend)
#                     print(status)
#                     break
#                 else:
#                     print("Manipulator operating!!")
#                     time.sleep(0.01)
            
#         elif key == ord('r'):
#             print('Hold off and Servo off')
#             status = udp.holdMH(2)
#             time.sleep(0.01)
#             status = udp.ServoMH(2)

#         elif key == ord('s'):
#             print('Read Position')
#             pos_result, coordinate = udp.getcoordinateMH()
#             print(coordinate)
#             sys_result = udp.getstatusMH()
#             print(sys_result)
#             torque = udp.getTorqueMH()
#             print(torque)

#         # elif key == ord('n'):
#         #     print('Arc ON')
#         #     udp.WriteIO(2701, 12)
#         #     status = udp.moveCoordinateMH(2,1, 14, 17, weldend)
#         #     print(status)

#         # elif key == ord('f'):
#         #     print('Arc OFF')
#         #     udp.WriteIO(2701, 0)

#         elif key == ord('m'):
#             print('Move to Goal')
#             status = udp.moveCoordinateMH(2,1, 50, 17, ORG)
#             print(status)

#     # 釋放資源
#     cv2.destroyAllWindows()
# else:
#     print(Servo_status)

#%%
# result, coordinate = udp.getcoordinateMH()
# print(coordinate)


#　作業區
# TODO BMOV 電流值尚未得知
# 讀取IO
# while True:
#     data1 = udp.ReadIO(1001)
#     print("1001", data1)

#     data2 = udp.ReadIO(3003)
#     print("3003", data2)
#     time.sleep(1)

# 控制系統有待加強
# TODO 緊急開關IO應與收弧相連，可做到使用硬體緊急停止收弧
# TODO 找到udp如何讀取機器人狀態， 需要Running狀態
# TODO 判斷收弧的條件，若用座標+姿態，必須給予值range，防止因數值不同而無法收弧
# TODO 完善軟體端之EMS開關
# try:
#     weldstart = [955.410, -102.226, -166.726, -165.2919, -7.1991, 17.5642]
#     weldend = [955.404, 14.865, -166.749, -165.2902, -7.1958, 17.5569]

#     # 伺服電源開啟
#     status = udp.ServoMH(1)
#     print(status)
#     if status == []:
#         print("ON")

#     # Cariten space
#     # Real speed = speed * 0.1 mm/s
#     # status = udp.moveCoordinateMH(0,500, 17, weldend)
#     status = udp.moveCoordinateMH(1,13, 17,  weldend)
#     print(status)

#     if status == []:
#         print("起弧")
#         print("送料")
#         # 純起弧
#         # data = udp.WriteIO(2701, 12)

#         # 起弧+送料
#         status = udp.WriteIO(2701, 13)
#         print(status)

#     # 創建一個空視窗
#     cv2.namedWindow('Empty Window')

#     while True:
#         # 等待鍵盤事件，並取得按下的鍵
#         key = cv2.waitKey(1) & 0xFF

#         # 位置讀取
#         result, coordinate = udp.getcoordinateMH()
#         # print(coordinate)

#         if coordinate == weldend:
#             print("收弧+收料")
#             udp.WriteIO(2701, 0)
#             break

#         # 檢查按下的鍵
#         if key == 27:  # 27是'ESC'鍵的ASCII碼
#             print('You pressed "ESC". Exiting...')
#             udp.holdMH(1)
#             udp.WriteIO(2701, 0)
#             break

#         elif key == ord('q'):
#             print('You pressed "q"')
#             # 在這裡加入相應的動作
#         elif key == ord('r'):
#             print('You pressed "r"')


# except Exception as e:
#     # Handle any type of exception
#     print(f"程式終止!!!: {e}")
#     udp.holdMH(1)
#     udp.WriteIO(2701, 0)




"""
ORG = [16, 4, 5, 0, 0, 485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879, 0, 0]
start = [16, 4, 5, 0, 0, 958.58, -102.274, -164.748, -165.2922, -7.1994, 17.5635, 0, 0]
end = [16, 4, 5, 0, 0, 956.709, 23.919, -164.373, -165.2942, -7.2005, 17.5837, 0, 0]
"""





# Robot = struct.pack('I', Movedata["Robot"])
# Station= struct.pack('I', Movedata["Station"])
# speedType= struct.pack('I', Movedata["speedType"])
# speed= struct.pack('I', Movedata["speed"])
# coordinateType= struct.pack('I', Movedata["coordinateType"])
# coordinate_x= signDecide(Movedata["coordinate"][0], 1000)
# coordinate_y= signDecide(Movedata["coordinate"][1], 1000)
# coordinate_z= signDecide(Movedata["coordinate"][2], 1000)
# coordinate_Rx= signDecide(Movedata["coordinate"][3], 10000)
# coordinate_Ry= signDecide(Movedata["coordinate"][4], 10000)
# coordinate_Rz= signDecide(Movedata["coordinate"][5], 10000)
# Reservation1= struct.pack('I', Movedata["Reservation1"])
# Reservation2= struct.pack('I', Movedata["Reservation2"])
# Type= struct.pack('I', Movedata["Type"])
# Expanded_type= struct.pack('I', Movedata["Expanded type"])
# Tool_No= struct.pack('I', Movedata["Tool No"])
# User_coordniate= struct.pack('I', Movedata["User coordniate"])
# Base_axis_1= struct.pack('I', Movedata["Base axis"][0])
# Base_axis_2= struct.pack('I', Movedata["Base axis"][1])
# Base_axis_3= struct.pack('I', Movedata["Base axis"][2])
# Station_axis_1= struct.pack('I', Movedata["Station axis"][0])
# Station_axis_2= struct.pack('I', Movedata["Station axis"][1])
# Station_axis_3= struct.pack('I', Movedata["Station axis"][2])
# Station_axis_4= struct.pack('I', Movedata["Station axis"][3])
# Station_axis_5= struct.pack('I', Movedata["Station axis"][4])
# Station_axis_6= struct.pack('I', Movedata["Station axis"][5])
# data = Robot+Station+speedType+speed+coordinateType+coordinate_x+coordinate_y+coordinate_z\
#         +coordinate_Rx+coordinate_Ry+coordinate_Rz+Reservation1+Reservation2+Type+Expanded_type\
#         +Tool_No+User_coordniate+Base_axis_1+Base_axis_2+Base_axis_3+Station_axis_1+Station_axis_2\
#         +Station_axis_3+Station_axis_4+Station_axis_5+Station_axis_6
# print(data)



# Ans = b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# print(Ans[0:4].decode("utf-8"))




        
# Hex = 0x83
# Hex_1 = 0x12
# Hex_2 = 'YERC'
# Hex_3 = "99999999"
# dec = 1

# packed_data = struct.pack('B', Hex)
# packed_data1 = struct.pack('B', Hex_1)

# packed_data2 = Hex_2.encode('utf-8')

# packed_data3 = struct.pack('B', dec)
# packed_data4 = Hex_3.encode('utf-8')
# all = packed_data2 + packed_data + packed_data1 + packed_data3 +packed_data4
# print(all)
# print(packed_data4)
# print(packed_data3)