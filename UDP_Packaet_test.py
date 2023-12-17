
"""
ASCII（American Standard Code for Information Interchange）:

    ASCII 是一種最早的字符編碼標準，僅使用7位二進制數（後來擴展為8位，稱為Extended ASCII）。
    ASCII 主要定義了英文字母、數字、標點符號和一些控制字符的二進制表示。
    ASCII 編碼是單字節編碼，每個字符使用一個字節。

Unicode:

    Unicode 是一種字符集，它為世界上大多數字符提供了唯一的數字標識。
    Unicode 包括了許多不同的編碼方案，其中最常見的是UTF-8、UTF-16和UTF-32。
    Unicode 編碼可以表示世界上的大多數字符，包括不同語言、符號和表情符號。

UTF-8（Unicode Transformation Format-8）:

    UTF-8 是 Unicode 編碼的一種實現方式，它使用不同數目的字節表示字符。
    UTF-8 是一種變長編碼，基本上可以表示任何Unicode字符，同時保持了對ASCII的向後兼容性。
    UTF-8 中的英文字母和ASCII字符使用一個字節表示，其他字符可能使用多個字節。

註:
字符（Character）:

    1.一個字符通常指的是文本中的一個單一字符，如字母、數字、標點符號等。
    2.在計算機中，字符通常使用編碼方式（如ASCII、UTF-8等）表示，每個字符被映射到一個或多個位元（bits）。
    3.一個常見的字符在ASCII編碼下使用7或8位表示，而在UTF-8等多字節編碼下可能使用更多位。

字節（Byte）:
    1.一個字節是計算機存儲的基本單位，通常由8個位元組成。
    2.字節是計算機中數據的基本單位，存儲二進制數據。
    3.字節可用於存儲字符數據，但它也可以表示其他數據，如圖像、音頻、二進制文件等。

字串（string）是由字符構成的
字節串（bytes）是由字節構成的

"""
# packet format
identifier = 'YERC'        
headSize = [0x20, 0x00]    
dataSize = [0x10, 0x20]    
reserve1 = 3               
procDiv = 1          
ACK = 0                    
reqID = 0                                                                                                
blockNo = [0, 0, 0, 0]    
reserve2 = '99999999'      

# Hold / Servo On/off Command 
cmdNo = [0x83, 0x00]
inst = [2, 0]
attr = 1
service = 0x10
padding = [0, 0]

Data_part = [1,0,0,0]
Data_partSize = len(Data_part)


req_UDP_packet = (identifier 
            +chr(headSize[0]) 
            +chr(headSize[1])
            +chr(dataSize[0]) 
            +chr(dataSize[1]) 
            +chr(reserve1)
            +chr(procDiv) 
            +chr(ACK) 
            +chr(reqID)
            +chr(blockNo[0]) 
            +chr(blockNo[1]) 
            +chr(blockNo[2]) 
            +chr(blockNo[3])
            +reserve2 
            +chr( cmdNo[0] ) 
            +chr( cmdNo[1] )
            +chr( inst[0] ) 
            +chr( inst[1] ) 
            +chr( attr ) 
            +chr( service ) 
            +chr( padding[0] ) 
            +chr( padding[1] ))
for i in range(Data_partSize):
    All_req_UDP_packet = req_UDP_packet + chr(Data_part[i])

print(All_req_UDP_packet)
# packet_str = str(UDP_packet)
packet_encode = All_req_UDP_packet.encode("utf-8")
print(packet_encode)
packet_decode = packet_encode.decode("utf-8")
print(packet_decode)

# Ans Packet
# ans_UDP_packet = (packet_decode[0:4] 
#             +ord(packet_decode[4]) 
#             +ord(packet_decode[5])
#             +ord(packet_decode[6]) 
#             +ord(packet_decode[7]) 
#             +ord(packet_decode[8])
#             +ord(packet_decode[9]) 
#             +ord(packet_decode[10]) 
#             +ord(packet_decode[11])
#             +ord(packet_decode[12]) 
#             +ord(packet_decode[13]) 
#             +ord(packet_decode[14]) 
#             +ord(packet_decode[15])
#             +packet_decode[16:24] 
#             +ord( packet_decode[24] ) 
#             +ord( packet_decode[25] )
#             +ord( packet_decode[26] ) 
#             +ord( packet_decode[27] ) 
#             +ord( packet_decode[28] ) 
#             +ord( packet_decode[29] ) 
#             +ord( packet_decode[30] ) 
#             +ord( packet_decode[31] ))
# print(ans_UDP_packet)

Ans_identifier = packet_decode[0:4]
Ans_headSize0 = ord(packet_decode[4])
Ans_headSize1 = ord(packet_decode[5])
Ans_dataSize0 =  ord(packet_decode[6])
Ans_dataSize1 =  ord(packet_decode[7])
Ans_reserve1=  ord(packet_decode[8])
Ans_procDiv =  ord(packet_decode[9])
Ans_ACK =  ord(packet_decode[10])
Ans_reqID =  ord(packet_decode[11])
Ans_blockNo=  ord(packet_decode[12])
Ans_blockNo=  ord(packet_decode[13])
Ans_blockNo=  ord(packet_decode[14])
Ans_blockNo=  ord(packet_decode[15])
Ans_reserve2=  packet_decode[16:24]
Ans_service =  ord( packet_decode[24] ) 
Ans_status =  ord( packet_decode[25] ) 
Ans_add_status_size =  ord( packet_decode[26] ) 
Ans_padding1 =  ord( packet_decode[27] ) 

Ans_add_status0=  ord( packet_decode[28] ) 
Ans_add_status1=  ord( packet_decode[29] )  

Ans_padding0=  ord( packet_decode[30] ) 
Ans_padding1=  ord( packet_decode[31] ) 
print('')

# 有符整數實驗 8bit 
DEC_2 = 160
BIN_2 = bin(DEC_2)
HEX_2 = hex(DEC_2)
#　16 轉 10 進制
HEX_2ToDEC_2 = int(HEX_2, 16)
print(BIN_2)
print(HEX_2)
print(HEX_2ToDEC_2)
print(format(DEC_2, '08b'))
print(format(DEC_2, '08X'))


int_list = [55, 251, 255, 255]

# 32bit 有符整數換算 
result = (int_list[3] << 24) | (int_list[2] << 16) | (int_list[1] << 8) | int_list[0]

# 判斷是否為負數
if result & (1 << 31):
    result -= 1 << 32

print(result*0.01)


'''
1.     16, 0, 0, 0,      
2.     4, 0, 0, 0, 
3.     5, 0, 0, 0, 
4.     0, 0, 0, 0, 
5.     0, 0, 0, 0, 
6.     147, 103, 7, 0, 
7.     55, 251, 255, 255, 
8.     82, 147, 3, 0, 
9.     160, 118, 27, 0, 
10.    3, 22, 3, 0, 
11.    246, 65, 0, 0, 
12.    0, 0, 0, 0, 
13.    0, 0, 0, 0
'''













