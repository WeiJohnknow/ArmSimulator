from MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one

mh = MotomanConnector() #Create connector
mh.connectMH()  #Connect
'''
cmd 
format_1 = {D1}{D2}{D3}
Data1 = 0:位元型, 1:整數型, 2:倍精度型, 3:實數型, 7:字串型
Data2 = 變數編號
Data3 = 變數值

format_2 = {D1}{D2}{D3}{D4}{D5}{D6}{D7}{D8}{D9}{D10}{D11}{D12}
Data1 = 4:Robot coordinate, 5:Base coordinate, 6:Station axis
Data2 = Vatiable No.
Data3 = 0:pluse, 1:Cartesian coordinate

if Data3 is 0:
Data4 = S pluse
Data5 = L pluse
Data6 = U pluse
Data7 = R pluse
Data8 = B pluse
Data9 = T pluse
Data10 = Tool No.

if Data3 is 1:
Data4 = 0:Base, 1:Robot, 2:User1, 3:User2 ... , 65:User64, 66:Tool , 67: Master Tool
Data5 = X
Data6 = Y
Data7 = Z
Data8 = Rx
Data9 = Ry
Data10 = Rz
Data11 = Type
Dara12 = Tool No.
'''
# format1 (Data1 ~ Data3)
cmd = [1,0,1]
# format2 (data1 ~ data12)
cmd_P1 = [4, 1, 1, 1, 485.364, -1.213, 234.338, 179.9840, 20.2111, 1.6879, 0, 5]
cmd_P2 = [4, 2, 1, 1, 955.326, -312.783, -154.686, -168.3765, -2.9339, 7.0523, 0, 5]
cmd_P3 = [4, 3, 1, 1, 955.326, -178.005, -154.700, -168.3718, -2.9293, 7.0363, 0, 5]
cmd_P4 = [4, 4, 1, 1, 485.364, -1.213, 234.338, 179.9840, 20.2111, 1.6879, 0, 5]
# cmd_P4 = [4, 4, 1, 1, 485.335, -1.1218, 234.330, 179.9841, 20.2141, 1.6879, 0, 5]
# cmd_P5 = [4, 5, 1, 1, 485.335, -1.1218, 234.330, 179.9841, 20.2141, 1.6879, 0, 5]
# mh.WriteVariableMH(4,4,1) #Write integer 200 to I004 on the controller
mh.WriteVariableMH(cmd_P4)
mh.disconnectMH() #Disconnect