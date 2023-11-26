# coding=utf-8
__author__ = 'kromau'

# Echo client program
import array
import logging
import socket
import time

from udpPacket import UdpPacket, UdpPacket_Req, UdpPacket_Ans

#sws

class DxFastEthServer():

    #def __init__(self, ip="192.168.255.1"):
    def __init__(self, ip="192.168.99.100"):
        """
        constructor method for DxFastEthServer class
        :param ip:  ip number of dx controller-server
        :return:    None
        """

        #create socket
        self.s = socket.socket(socket.AF_INET,          #Internet socket type
                               socket.SOCK_DGRAM)       #UDP socket !!!
        self.s.settimeout(2)                            #timeout 1 sec

        #set connection data
        self.UDP_IP = ip                #default IP ("192.168.99.100")
        self.UDP_PORT = 10040          #port (fixed to 10040)


        self.status={}

    def setHostIp(self, ip ):
        self.UDP_IP = ip

    def sendCmd(self, reqSubHeader, reqData, procDiv=1):
        """
        Send Command (request packet) to Dx server ang get response (answer packet)
        :param reqSubHeader:    request sub header part of packet ( depend on each command )
        :param reqdata:         data part of the packet ( optional, depend of the command )
        :param procDiv :        Processing division (1-robot control, 2-file control)
        :return: ansPacket      answer packet
        """

        req_packet = UdpPacket_Req(reqSubHeader, reqData, procDiv)       #prepare packet
        req_packet.reqID=0
        req_str = str(req_packet)                               #string representation of the packet

        ans_str = self.socketSndRcv(req_str)


        if ans_str == None:
            return None


        a = array.array('B', req_str)
        b = array.array('B', ans_str)

        ansPacket = UdpPacket_Ans(ans_str, procDiv)                  #create answer packet from answer string
        return ansPacket

    def socketSndRcv(self, req_str):

        #TODO: sending and receiving in spawned thread !!! (doesn't block in case of sockets errors)


        try:
            #send request packet (string) to dx server, get response (string) from dx server
            #send request
            self.s.sendto( req_str,                             #UDP packet
                           (self.UDP_IP, self.UDP_PORT) )       #A pair (host, port) is used for the AF_INET address family
            #get answer from the server
            (ans_str, address) = self.s.recvfrom(512)

        except socket.timeout as e:
            print 'socket timeout: ' + str(e)
            logging.exception(str(e))
            return None

        except socket.gaierror as e:
            print 'socket address error'
            logging.exception(str(e))
            return None

        except socket.error as e:
            print 'socket related error'
            logging.exception(str(e))
            return None

        else:
            return ans_str

    #---------- Dx server functions --------------------
    #Status Information Reading Command
    def getStatusInfo(self):
        """
        """
        reqSubHeader = {    'cmdNo': (0x72, 0x00),       #Command No. 0x72
                            'inst': (1, 0),              #Fixed to 1
                            'attr': 0,                   #1: Data 1, 2: Data 2
                            'service':  0x01,            #Get_Attribute_Single: 0x0E, Get_Attribute_All: 0x01
                            'padding': (0, 0) }

        reqData = []


        ansPacket = self.sendCmd(reqSubHeader, reqData)

        if( ansPacket == None or ansPacket.status != 0):
            return False

        #parse answer data
        byte1=ansPacket.data[0]
        byte2=ansPacket.data[4]

        def testBit(int_type, offset):
            mask = 1 << offset
            if (int_type & mask) == mask:
                return True
            else:
                return False

        self.status['Step'] = testBit(byte1,0)
        self.status['Cycle'] = testBit(byte1,1)
        self.status['Auto'] = testBit(byte1,2)
        self.status['Running'] = testBit(byte1,3)
        self.status['InGuard'] = testBit(byte1,4)
        self.status['Teach'] = testBit(byte1,5)
        self.status['Play'] = testBit(byte1,6)
        self.status['Remote'] = testBit(byte1,7)

        self.status['Hold_PP'] = testBit(byte2,1)
        self.status['Hold_Ext'] = testBit(byte2,2)
        self.status['Hold_Cmd'] = testBit(byte2,3)
        self.status['Alarm'] = testBit(byte2,4)
        self.status['Error'] = testBit(byte2,5)
        self.status['ServoOn'] = testBit(byte2,6)

        return True

    #Hold/Servo control
    def holdServoOnOff(self,a1, a2):
        """
        Sub header part:
        Command No. 0x83
        Instance Specify one out of followings  Specify the type of OFF/ON command
            1: HOLD
            2: Servo ON
            3: HLOCK
        Attribute Fixed to “1”. Specify “1”.
        Service • Set_Attribute_Single: 0x10 Specify the accessing method to the data.
                    0x10 : Execute the specified request

        Data part:
        32bit integer Byte 0 Byte 1 Byte 2 Byte3 <Details>
                1 1:ON
                2:OFF

        """
        reqSubHeader = { 'cmdNo': (0x83, 0x00),  #Command No.
                    'inst': [a1, 0],             #instance 1: HOLD, 2: Servo ON, 3: HLOCK
                    'attr': 1,                   #Fixed to “1”
                    'service':  0x10,            #Get_Attribute_Single: 0x0E, Get_Attribute_All: 0x01
                    'padding': (0, 0) }

        reqData = [a2,0,0,0]

        ansPacket = self.sendCmd(reqSubHeader, reqData)

        return ( ansPacket != None and ansPacket.status == 0)

    def putServoOn(self):
        return self.holdServoOnOff(2,1)
    def putServoOff(self):
        return self.holdServoOnOff(2,2)
    def putHoldOn(self):
        return self.holdServoOnOff(1,1)
    def putHoldOff(self):
        return self.holdServoOnOff(1,2)

    #Start-up (Job Start) Command
    def startUp(self):
        """
        Command No. 0x86
        Instance Fixed to “1”. Specify “1”.
        Attribute Fixed to “1”. Specify “1”.
        Service • Set_Attribute_Single: 0x10 Specify the accessing method to the data.
                0x10 : Execute the specified request

        Data part:
        32bit integer Byte 0 Byte 1 Byte 2 Byte3 <Details>
        """
        reqSubHeader = { 'cmdNo': (0x86, 0x00),
                    'inst': [1, 0],
                    'attr': 1,
                    'service':  0x10,
                    'padding': (0, 0) }

        reqData = [1,0,0,0]

        ansPacket = self.sendCmd(reqSubHeader, reqData)

        return ( ansPacket != None and ansPacket.status == 0)


    #Read/Write vars (B, I, D)
    def writeVar(self, type, index, value):

        #Command No.
        commNo = [0x7A,   #Bvar
                    0x7B,   #Ivar
                    0x7C,   #Dvar
                    0x7D]   #Rvar
        """
        Instance (Specify the variable number.) 0-99
        Attribute Fixed to “1”. Specify “1”.
        Service • Get_Attribute_Single: 0x0E
                • Get_Attribute_All: 0x01
                • Set_Attribute_Single: 0x10
                • Set_Attribute_All: 0x02

        Data part:
        32bit integer Byte 0 Byte 1 Byte 2 Byte3 <Details>
        """

        reqSubHeader = { 'cmdNo': (commNo[type], 0x00),
                    'inst': [index, 0],
                    'attr': 1,
                    'service':  0x10,       #writing
                    'padding': (0, 0) }


        if (type == 0):
            reqData = [value]
        elif (type == 1):
            tc = two_comp(value, 16)            #two's complement
            bytes = divmod(tc, 0x100)           #vrne [celi_del, ostanek]   --->   [bytes / 2^8, bytes % 2^8]
            reqData = [bytes[1], bytes[0]]
        elif (type == 2):
            tc = two_comp(value, 32)            #two's complement
            bytes = divmod(tc, 0x10000)         #vrne [celi_del, ostanek]   --->   [bytes / 2^16, bytes % 2^16]
            bytesLow = divmod(bytes[1], 0x100)
            bytesHigh = divmod(bytes[0], 0x100)
            reqData = [bytesLow[1], bytesLow[0], bytesHigh[1], bytesHigh[0] ]


        ansPacket = self.sendCmd(reqSubHeader, reqData)

        return ( ansPacket != None and ansPacket.status == 0)

    def readVar(self, type, index):
        #Command No.
        commNo = [0x7A,   #Bvar
                    0x7B,   #Ivar
                    0x7C,   #Dvar
                    0x7D]   #Rvar
        """
        Instance (Specify the variable number.) 10
        Attribute Fixed to “1”. Specify “1”.
        Service • Get_Attribute_Single: 0x0E
                • Get_Attribute_All: 0x01
                • Set_Attribute_Single: 0x10
                • Set_Attribute_All: 0x02

        Data part:
        32bit integer Byte 0 Byte 1 Byte 2 Byte3 <Details>
        """
        reqSubHeader = { 'cmdNo': (commNo[type], 0x00), #cmd Nr
                    'inst': [index, 0],       #index of var
                    'attr': 1,
                    'service':  0x0E,           #reading variable
                    'padding': (0, 0) }

        reqData = []

        ansPacket = self.sendCmd(reqSubHeader, reqData)

        if( ansPacket == None or ansPacket.status != 0):
            return False

        if (type == 0):     #B var
            #B var - unsigned data
            return ( ansPacket.data[0] )
        elif (type == 1):   #I var
            #convert received data (2 bytes) to signed integer
            return toSint(ansPacket.data[1]*(1<<8) + ansPacket.data[0], 16)
        elif (type == 2):   #D var
            #convert received data (4 bytes) to signed integer
            wordLow=ansPacket.data[1]*(1<<8) + ansPacket.data[0]
            wordHigh=ansPacket.data[3]*(1<<8) + ansPacket.data[2]
            return toSint(wordHigh*(1<<16) + wordLow, 32)

    #Get File list
    def FileList(self):
        reqSubHeader = { 'cmdNo': (0x00, 0x00),
                    'inst': [0, 0],
                    'attr': 0,
                    'service':  0x32,
                    'padding': (0, 0) }

        reqData = "*.lst"

        ansPacket = self.sendCmd(reqSubHeader, reqData, 2)

        status = {'status': hex(ansPacket.status), 'errcode': [hex(ansPacket.add_status[0]),hex(ansPacket.add_status[1])] }

        return status
        #return ( ansPacket != None and ansPacket.status == 0)

    #Delete File
    def FileDelete(self):
        reqSubHeader = { 'cmdNo': (0x00, 0x00),
                    'inst': [0, 0],
                    'attr': 0,
                    'service':  0x09,
                    'padding': (0, 0) }

        reqData = "TEST.JBI"

        ansPacket = self.sendCmd(reqSubHeader, reqData, procDiv=2)

        return ( ansPacket != None and ansPacket.status == 0)


    #Save File
    def FileSave(self, file):
        reqSubHeader = { 'cmdNo': (0x00, 0x00),
                    'inst': [0, 0],
                    'attr': 0,
                    'service':  0x16,
                    'padding': (0, 0) }

        reqData = file

        ansPacket = self.sendCmd(reqSubHeader, reqData, 2)

        return ( ansPacket != None and ansPacket.status == 0)


#HELPER functions
#two's complement of the signed integer number
def two_comp(val, nbits):
    return (val + (1 << nbits)) % (1 << nbits)

#convert number to signed integer
def toSint (val, nbits):
    if ( val >= (1 << nbits-1) ):
        val =  val - (1 << 16)
    return val



#Testing...
if __name__ == '__main__':

    dx = DxFastEthServer("192.168.255.1")

    # dx.getStatusInfo()
    # for i, item in enumerate(dx.status.viewkeys()):
    #     print item, ": ", dx.status[item]



    type=1          #0-B, 1-I, 2-D
    nr=0            #index
    value=120       #value
    dx.writeVar(type, nr, value)



    print "---------------Write/Read  variables"
    type=0              #0-B, 1-I, 2-D
    nr=0                #index
    # value=255    #value
    # dx.writeVar(type, nr, value)
    print dx.readVar(type, nr)


    #-----------Servo, Hold On/Off
    dx.putServoOn()
    time.sleep(2)
    dx.putServoOff()
    #
    # dx.putHoldOn()
    # time.sleep(1)
    # dx.putHoldOff()














