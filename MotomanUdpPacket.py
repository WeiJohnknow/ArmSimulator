
# for i in range(256):
#     high = i >> 8
#     Low = i - (high << 8)

#     # 有號 無號 映射
#     if Low > 127:
#         Low = -(255 - (Low-1))
#     print(i, Low)




# 'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\xc2\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'


# b'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x83\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'



# Hex = 'YERC \x00\x04\x00\x03\x01\x00\x00\x00\x00\x00\x0099999999\x83\x00\x02\x00\x01\x10\x00\x00\x01\x00\x00\x00'
# byte_data = bytes.fromhex(Hex)
# print(Hex.encode("ascii"))
# print(Hex)


import struct
import socket
import time

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
        for i in range(self.Data_part_size[0]):
            packet += struct.pack('B', self.Data[i])

        return packet
    
    def Unpack_Ans_packet(self, Ans_packet):


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
            print('udp ok!!')
            return data
        
        elif status == "0x1f":
            add_status[0] = hex(Ans_packet[28])
            add_status[1] = hex(Ans_packet[29])

            if add_status[0] == '0xa7' and  add_status[1] == '0xe4':
                Error = ['E4A7','Packet format error!!']
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
    
    def ReadPos(self):
        reqSubHeader = { 'Command_No': (0x75, 0x00),
                    'Instance': [101, 0],
                    'Attribute': 0,
                    'Service':  0x0E,
                    'Padding': (0, 0) }
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        result = self.Cvt_SignInt( data)
        print(result)

    def Cvt_SignInt(self, data):
        """Convert 32bit Signed Integer
        input type: list
        input len: 4
        """
        result = []
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

        return result
    
    def ReadIO(self, number):
        number = hex(number)
        
        reqSubHeader = { 'Command_No': (0x78, 0x00),
                    'Instance': [0xcf, 0x9],
                    'Attribute': 1,
                    'Service':  0x0E,
                    'Padding': (0, 0)}
        reqData = []
        
        Ans_packet = self.sendCmd( reqSubHeader, reqData)
        data = UDP_packet.Unpack_Ans_packet(self, Ans_packet)
        print(data)

    

# UDP test
udp = MotomanUDP()
# udp.ServoMH(0)
# time.sleep(5)
# Error = udp.ServoMH(2)
# udp.ReadPos()
while True:
    udp.ReadIO(255) 
# print(Error)


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