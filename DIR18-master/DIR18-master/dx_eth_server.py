# coding=utf-8
__author__ = 'kromau'

# Echo client program
import socket


class DxEthServer():
    def __init__(self ):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keepAlive = -1        # default: keep alive - executes infinite number of commands


    def connect(self, host="192.168.255.1", port=80, keepAlive = 2 ):
        """
        connect to dx server
        arg1: host          host name string (default = "192.168.255.1")
        arg2: port          port number (default=80)
        arg3: keepAlive      2 ... n      stay connected for this no. of commands then close socket
                            -1            stay connected for infinite no. of commands
        """
        self.keepAlive = keepAlive         # default: keep alive - executes infinite number of commands

        #Connect
        print 'Connecting to DX server...'
        self.s.connect((host, port))
        print 'OK'

        #Send connection command
        #cmd = 'CONNECT Robot_access'
        #cmd = 'CONNECT Robot_access Keep-Alive:2'
        cmd = 'CONNECT Robot_access Keep-Alive:'+str(self.keepAlive)
        print 'Send: ' + cmd
        self.s.sendall(cmd + '\r\n')
        print 'OK'

        #Get response
        data = self.s.recv(1024)
        print 'Received', repr(data)

    def disconnect(self):
        """
        disconnect from dx server
        """
        print '\r\nDisconnecting...'
        self.s.close()
        print 'OK'

    def sendCmd(self, cmdName, cmdData=""):
        """
        send command to server
        """
        if ( len(cmdData) != 0 ):
             size = len(cmdData) + 1
        else:
            size = 0

        #send command
        cmd = 'HOSTCTRL_REQUEST ' + cmdName + ' ' + str(size)
        print 'Send: ' + cmd
        self.s.sendall(cmd + '\r\n')
        print 'OK'

        #Get response (to command)
        data = self.s.recv(1024)
        print 'Received', repr(data)

        #send command data
        if ( len(cmdData) != 0 ):
            print 'Send: ' + cmdData
            self.s.sendall(cmdData + '\r')

        #Get response (data)
        data = self.s.recv(1024)
        print 'Received', repr(data)

    #Read variables
    def readVarB(self, ind):
        self. readVar(0, ind)
    def readVarI(self, ind):
        self. readVar(1, ind)
    def readVarD(self, ind):
        self. readVar(2, ind)
    def readVarR(self, ind):
        self. readVar(3, ind)
    def readVarRobot(self, ind):
        self. readVar(4, ind)
    def readVar(self, type, ind):
        """
        Reads variable data.
        Command format: SAVEV
        Command data: Data-1, Data-2
        Data-1 = Type of variables
        0: Byte type variables
        1: Integer type variables
        2: Double precision type variables
        3: Real number type variables
        4: Robot axis position type variables
        5: Base axis position type variables
        6: Station axis position type variables (only pulse type)
        7:String variable
        Data-2 = Variable No.
        Answer format 1 (When the type of variables specified with the command
        data is 0, 1, 2, 3, or 7)
        Answer: Data-1
        Data-1 = Byte value / Integer value / Double precision integer value / Real
        number value / String
        The value corresponding to the type of variables that is specified
        with the command data is read out.
        Answer format 2 (When the type of variables specified with the command
        data is 4, 5, or 6)
        Answer: Data-1, Data-2, , Data-10 (When all the robots controlled by
        DX200 have 6 axes or less)
        Data-1 = Position data type (0: Pulse type, 1: Cartesian type)
        (When the position data type is "0")
        Data-2 = Number of robot S-axis pulses / Number of base 1st axis pulses / Number
        of station 1st axis pulses
        Data-3 = Number of robot L-axis pulses / Number of base 2nd axis pulses / Number of
        station 2nd axis pulses
        Data-4 = Number of robot U-axis pulses / Number of base 3rd axis pulses / Number of
        station 3rd axis pulses
        Data-5 = Number of robot R-axis pulses / Number of base 4th axis pulses / Number of
        station 4th axis pulses
        Data-6 = Number of robot B-axis pulses / Number of base 5th axis pulses / Number of
        station 5th axis pulses
        """
        name="SAVEV"
        data = str(type) + "," + str(ind)
        self. sendCmd(name, data)

    #Write variables
    def writeVarB(self, ind, value):
        self.writeVar(0, ind, value)
    def writeVarI(self, ind, value):
        self.writeVar(1, ind, value)
    def writeVarD(self, ind, value):
        self.writeVar(2, ind, value)
    def writeVarR(self, ind, value):
        self.writeVar(3, ind, value)
    def writeVar(self, type, ind, value):
        """
        LOADV
        Receives variable data from a host computer and writes it in a specified
        variable.
        Command format: LOADV
        Command data format 1: (When the type of variables specified with the
        command data is 0, 1, 2, 3, or 7)
        Command data: Data-1, Data-2, Data-3
        Data-1 = Type of variables
        0: Byte type variables
        1: Integer type variables
        2: Double precision type variables
        3: Real number type variables
        7: String variable
        Data-2 = Variable No.
        Data-3 = Byte value / Integer value / Double precision type integer value /
        Real number value / String
        The value corresponding to the type of variables that is specified
        in Data-1 is written in.
        Command data format 2: (When the type of variables specified with the
        command data is 4, 5, or 6)
        Command data: Data-1, Data-2, , Data-12 (When all the robots
        controlled by DX200 have 6 axes or less)
        Data-1 = Type of variables
        4: Robot axis position type variables
        5: Base axis position type variables
        6: Station axis position type variables (only pulse type)
        Data-2 = Variable No.
        Data-3 = Position data type (0: Pulse type, 1: Cartesian type)
        (When the position data type is 0)
        Data-4 = Number of S-axis pulses / Number of base 1st axis pulses / Number of
        station 1st axis pulses
        Data-5 = Number of L-axis pulses / Number of base 2nd axis pulses / Number of
        station 2nd axis pulses
        Data-6 = Number of U-axis pulses / Number of base 3rd axis pulses / Number of
        station 3rd axis pulses
        Data-7 = Number of R-axis pulses / Number of base 4th axis pulses / Number of
        station 4th axis pulses
        Data-8 = Number of B-axis pulses / Number of base 5th axis pulses / Number of
        station 5th axis pulses
        46/60
        3 Transmission Procedure
        3.2 Command Details
        3-35
        HW1481823
        HW1481823
        Data-9 = Number of T-axis pulses / Number of base 6th axis pulses / Number of
        station 6th axis pulses
        Data-10 = Tool No.(0 to 63)
        Data-11 = Not exist
        Data-12 = Not exist
        • When the robots controlled by DX200 include a 7-axis robot, the
        number of pulses of robot's E-axis is inserted between Data-9
        (Number of T-axis pulses ) and Data-10 (Tool No.). Therefore, the tool
        number is Data-11.
        (When the position data type is 1: Only robot axis position type variables /
        base axis position type variables exist.)
        Data-4 = Coordinate data
        0: Base coordinate
        1: Robot coordinate
        2: User coordinate 1
        3: User coordinate 2
        
        
        
        65: User coordinate 64
        66: Tool coordinate
        67: Master tool coordinate
        Data-5 = X coordinate value / Base 1st axis Cartesian value (unit: mm,
        significant 3 decimal points)
        Data-6 = Y coordinate value / Base 2nd axis Cartesian value (unit: mm,
        significant 3 decimal points)
        Data-7 = Z coordinate value / Base 3rd axis Cartesian value (unit: mm,
        significant 3 decimal points)
        Data-8 = Wrist angle Rx coordinate value (unit: degree (°), significant 4
        decimal points)
        Data-9 = Wrist angle Ry coordinate value (unit: degree (°), significant 4
        decimal points)
        Data-10 = Wrist angle Rz coordinate value (unit: degree (°), significant 4
        decimal points)
        Data-11 = Type
        • Data of the type are represented by the following bit data coded into
        a decimal number.
        47/60
        3 Transmission Procedure
        3.2 Command Details
        3-36
        HW1481823
        HW1481823
        Data-12 = Tool No. (0 to 63)
        • When the robots controlled by DX200 include a 7-axis robot, the
        elbow angle posture Re is inserted between Data-10 (Wrist angle Rz
        coordinate value) and Data-11 (Type). Therefore, the numbers of
        Data-11 and later are increased by 1 and the final data is Data-13.
        Answer format: 0000 at normal answer
        """

        name="LOADV"
        data = str(type) + "," + str(ind) + "," + str(value)
        self. sendCmd(name, data)

    #Read current position
    def robPosJoint(self):
        """
        Reads the current position in joint coordinate system.
        Command format: RPOSJ
        Command data: None
        Answer format: Data-1, Data-2, Data-3, Data-4, , Data-12 (For robots
        with 6 axes or less)
        Data-1 = Number of S-axis pulses
        Data-2 = Number of L-axis pulses
        Data-3 = Number of U-axis pulses
        Data-4 = Number of R-axis pulses
        Data-5 = Number of B-axis pulses
        Data-6 = Number of T-axis pulses
        Data-7 = Number of 7th axis pulses
        Data-8 = Number of 8th axis pulses
        Data-9 = Number of 9th axis pulses
        Data-10 = Number of 10th axis pulses
        Data-11 = Number of 11th axis pulses
        Data-12 = Number of 12th axis pulses
        • For 7-axis robots, Data-7 (number of pulses of the 7th axis) is the
        number of pulses of the E-axis and Data-13 (number of pulses of the
        13th axis) is added.
        """
        self.sendCmd("RPOSJ")

    #Read current job name, line No. and step No.
    def robJobSeq(self):
        """
        RJSEQ
        Reads the current job name, line No. and step No.
        Command format: RJSEQ
        Command data: None
        Answer format: Data-1, Data-2, Data-3
        Data-1 = Read job name
        Data-2 = Read line No. (0 to 9999)
        Data-3 = Read step No. (1 to 9998)
        """
        self.sendCmd("RJSEQ")

    #Read Univ IO
    def readUnivIn(self, ind, noG):
        contact = 10 + ((1 / 8) * 10) * (ind - 1)
        self.readIO(contact, noG)
    def readUnivOut(self, ind, noG):
        contact = 10010 + ((1 / 8) * 10) * (ind - 1)
        self.readIO(contact, noG)
    def readIO(self, contactNo, noG):
        """
        Command format: IOREAD
        Command data: Data-1, Data-2
        Data-1 = Contact point No. to start read-out
        Data-2 = The number of contact points to be read out
        • I/O data are output every eight contact points. Specify the number of
        contact points to be read out, in multiples of eight.
        Answer format: Data-1, Data-2, , Data-N
        Data-1 = Read-out data for the first eight contact points
        Data-2 = Read-out data for the next eight contact points
        """
        self.sendCmd("IOREAD", str(contactNo) + "," + str(noG))

    #Write network Inp
    def writeNetworkIn(self, contact, value):
        """
        Writes in I/O signals.
        Command format: IOWRITE
        Command data: Data-1, Data-2, , Data-N
        Data-1 = Contact point No. to start write-in
        Data-2 = The number of contact points to be written in
        Data-3 = Write-in data for the first eight contact points
        Data-4 = Write-in data for the next eight contact points
        
        
        
        Data-N = Write-in data for the last eight contact points
        N = (Command data Data-2)/8+2. The command data Data-2 should be
        multiples of eight.
        • I/O data are processed every eight contact points. Specify the number
        of contact points to be written-in, in multiples of eight.
        • The IO signals can only be written to the network inputs (#27010 to
        #29567).
        Answer format: 0000 at normal answer
        """
        data = str(contact) + ",8," + str(value)
        self.sendCmd("IOWRITE", data )

    #Set master job
    def setMaster(self, name):
        """
        SETMJ
        Sets a specified job as a master job.
        At the same time, the specified job is set as an execution job.
        Command format: SETMJ
        Command data: Job-Name
        Job-Name = Job name to be set
        Answer format: 0000 at normal answer
        """
        self.sendCmd("SETMJ", name)

    #Sevo On/Off
    def servoOn(self):
        """
        SVON
        Turns servo power supply ON/OFF.
        To turn ON/OFF the servo power supply by this command, connect the
        external servo ON (EXSVON) signal 29 of the input terminal block (MTX)
        for the manipulator, to 30.
        Command format: SVON
        Command data: Data
        Data = Specification of servo power supply ON/OFF status
        0: OFF
        1: ON
        Answer format: 0000 at normal answer
        """
        self.sendCmd("SVON", "1")
    def servoOff(self):
        self.sendCmd("SVON", "0")

    #Start job
    def start(self, job = ""):
        """
        START
        Starts a job.
        If a job name is specified for an operand, the execution is started from the
        beginning of the job. If no job name is specified, the execution is started
        from the current line number of the set execution job.
        Command format: START
        Command data: Job-Name (Can be omitted.)
        Job-Name = Starting job name
        Answer format: 0000 at normal answer
        """
        self.sendCmd("START", job)



if __name__ == '__main__':

    dx = DxEthServer()
    dx.connect("192.168.2.3", 80)


    #dx.servoOn()
    #dx.servoOff()

    #dx.robJobSeq()
    #
    #dx.readVarB(1)
    #dx.readVarI(2)
    # dx.readVarD(1)
    # dx.readVarR(1)
    # dx.readVarRobot(2)
    #
    # dx.robPosJoint()
    #
    #dx.readUnivIn(12,1)
    dx.readUnivOut(1,8)
    #
    #dx.setMaster("EEE")
    #
    #
    # dx.servoOff()
    #
    # dx.start()
    #
    #dx.writeVarB(3, 25)
    # dx.writeVarI(1,2121)
    # dx.writeVarD(1,2323232)
    # dx.writeVarR(1,1.23235)


    dx.disconnect()