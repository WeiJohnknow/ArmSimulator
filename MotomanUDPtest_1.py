
identifier = 'YERC'    
headSize = [0x20, 0x00]
dataSize = [0x00, 0x00]
reserve1 = 3           
procDiv = 1     
ACK = 0                
reqID = 0              
blockNo = [0, 0, 0, 0]
reserve2 = '99999999'

cmdNo = [0x83,0]
inst = [2, 0]
attr = 1
service = 0x10
padding = [0, 0]

l_str = str(identifier 
            + chr(headSize[0])
            + chr(headSize[1])
            + chr(dataSize[0])
            + chr(dataSize[1])
            + chr(reserve1)
            + chr(procDiv)
            + chr(ACK)
            + chr(reqID)
            + chr(blockNo[0])
            + chr(blockNo[1])
            + chr(blockNo[2])
            + chr(blockNo[3])
            + reserve2
            + chr(cmdNo[0])
            # + chr(cmdNo[1])
            # + chr(inst[0] )
            # + chr(inst[1] )
            )
lstr = l_str.encode('utf-8')
print(lstr)

a = 0x7F
b = 0x83
c= b-a
print(hex(c))