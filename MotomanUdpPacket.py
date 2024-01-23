import struct
import socket
import pandas as pd
from Toolbox import TimeTool
import time
import keyboard
import cv2
from dataBase import dataBase

class UDP_packet:
    def __init__(self, Sub_header, data=[]) -> None:
        # Request Packet

        # main format
        # 4 Byte
        self.identifier  = 'YERC'
        # 2 Byte
        self.Header_part_size = [0x20, 0x00]
        # 2 Byte
        self.Data_part_size   = [0x20, 0x00]
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

        self.Data_part_size[0] = len(data)
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
            for i in range(self.Data_part_size[0]):
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
        
        
        size = 4 * dataSize[1] * 256 + dataSize[0]
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
                Error = ['Error code: E4A7','Packet format error!!']
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
            else:
                return add_status
        

            

          
class MotomanUDP:
    def __init__(self,ip="192.168.255.200",S_pulse = 1435.4, L_pulse = 1300.4, U_pulse = 1422.2, R_pulse = 969.9, B_pulse = 980.2, T_pulse = 454.7) -> None:
        # MA1440 deg/pulse
        self.S_pulse = S_pulse
        self.L_pulse = L_pulse
        self.U_pulse = U_pulse
        self.R_pulse = R_pulse
        self.B_pulse = B_pulse
        self.T_pulse = T_pulse

        # socket UDP setting
        self.s = socket.socket(socket.AF_INET,          #Internet socket type
                               socket.SOCK_DGRAM)
        self.s.settimeout(2)

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
    
    def getcoordinateMH(self):
        """Get coordniate
        - result:
            [dataType, Form, Tool No, User coordinate No, Extended form, x, y, z, Rx, Ry, Rz, 0, 0]
        - coordinate:
            [x, y, z, Rx, Ry, Rz]
        """
        reqSubHeader= { 'Command_No': (0x75, 0x00),
                    'Instance': [101, 0],
                    'Attribute': 0,
                    'Service':  0x0E,
                    'Padding': (0, 0) }
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        result = self.Cvt_SignInt( data)
        # print(result)
        coordinate = [result[5], result[6], result[7], result[8], result[9], result[10]]

        return result, coordinate
    
    
    
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
        """Convert 32bit Signed Integer
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
        
        # Torque
        if len(data) == 24:
            for i in range(0, len(data), 4):
                # Combine the four bytes into a 32-bit unsigned integer
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
    
    def ReadIO(self, number):
        # TODO Instance高、低位元輸入還未完成
        number_hex = hex(number)

        # 移除 '0x' 前綴並填充零，確保至少有兩個字元
        number_hex = number_hex[2:].zfill(4)

        # 將十六進位表示法分為高位元和低位元
        high_byte = int(number_hex[:2], 16)
        low_byte = int(number_hex[2:], 16)
        
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
        # TODO Instance高、低位元輸入還未完成
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
        # TODO Instance高、低位元輸入還未完成
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
        reqData = [data]
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        return data
#------------------------------------------------------------------------------ Robot Move Cammand-----------------------------------------------------------------------------------------
    def MoveCMD_data(self, moveType, moveSpeedType, speed, coordinateType, coordinate, Type= 4, Expanded_type= 0, Tool_No=5, User_coordinate=0):

        # TODO : 參數已完成，待測驗。
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

    def moveMH(self, moveType, moveSpeedType, speed, coordinateType, coordinate):
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
    
    def arconMH(self):
        """ARC ON
        - Network input: #27012 and # 27013 ON.
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

# UDP test
udp = MotomanUDP()
Time = TimeTool()
dB = dataBase()


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

# 位置讀取
# result, coordinate = udp.getcoordinateMH()
# print(coordinate)
GoalEnd = [955.386, -19.8, -75.117, -165.2853, -7.1884, 17.5443]
count = 0
Servo_status = udp.ServoMH(1)
while count<=100:
    b = Time.ReadNowTime()
    udp.moveMH(2,1, 14, 17, GoalEnd)
    a = Time.ReadNowTime()
    err = Time.TimeError(b, a)
    dB.Save_time(err["millisecond"], "dataBase/moveCMDtime_3.csv")
    count+=1
Servo_status = udp.ServoMH(2)
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
# data = udp.ReadRegister(560)
# print(data)

# Write Register
# data = udp.WriteRegister(548, 0)
# print(data)

# Move指令

# 設定座標
# ORG = [485.364, -1.213, 234.338, 179.984, 20.2111, 1.6879]
# weldstart = [955.41, -102.226, -166.726, -165.2919, -7.1991, 17.5642]
# weldend = [955.404, 14.865, -166.749, -165.2902, -7.1958, 17.5569]

# Cariten space
# Real speed = speed * 0.1 mm/s
# status = udp.moveMH(1,13, 17, weldstart)
# print(status)

# Joint space
# Real speed = speed * 0.01%
# status = udp.moveMH(0,500, 17, coord)
# print(status)

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
#             status = udp.moveMH(3, 1, 100, 17, dp)
#             print(status)

#             while True:
#                 print("讀取是否運轉中")
#                 sys_status = udp.getstatusMH()
#                 print(sys_status)

#                 if sys_status[0] == 194:
#                     # 回歸原本路徑
#                     status = udp.moveMH(2,1, 100, 17, weldend)
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
#         #     status = udp.moveMH(2,1, 14, 17, weldend)
#         #     print(status)

#         # elif key == ord('f'):
#         #     print('Arc OFF')
#         #     udp.WriteIO(2701, 0)

#         elif key == ord('m'):
#             print('Move to Goal')
#             status = udp.moveMH(2,1, 50, 17, ORG)
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
#     # status = udp.moveMH(0,500, 17, weldend)
#     status = udp.moveMH(1,13, 17,  weldend)
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