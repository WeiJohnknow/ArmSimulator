import socket, time

#######################
# Communication Interface to Motoman Controllers
# Tested on MH24 with DX200
# Tested on 6VX7 with YRC1000
# 
# Philipp Triebold
######################


#MH24 Conversion Values
#S 1341,4 Pulse per °
#L 1341,4 Pulse per °
#U 1341,4 Pulse per °
#R 90° 90000 -> 1000 Pulse per °
#B 90° 90000 -> 1000 Pulse per °
#T 90° 56462 -> 622 Pulse per °

class MotomanConnector:
    def __init__(self,IP = "192.168.255.200", PORT=80, S_pulse = 1435.4, L_pulse = 1300.4, U_pulse = 1422.2, R_pulse = 969.9, B_pulse = 980.2, T_pulse = 454.7):
        """Interface for the Ethernet Server Function of various Yaskawa Motoman Controllers

        Args:
            IP (str, optional): IP of the Controller. Defaults to "192.168.255.200".
            PORT (int, optional): Port of the Controller. Defaults to 80.
            S_pulse (float, optional): S-Axis encoder pulses per degree. Defaults to 1341.4.
            L_pulse (float, optional): L-Axis encoder pulses per degree. Defaults to 1341.4.
            U_pulse (float, optional): U-Axis encoder pulses per degree. Defaults to 1341.4.
            R_pulse (float, optional): R-Axis encoder pulses per degree. Defaults to 1000.
            B_pulse (float, optional): B-Axis encoder pulses per degree. Defaults to 1000.
            T_pulse (float, optional): T-Axis encoder pulses per degree. Defaults to 622.
        """

        self.s = socket.socket()
        self.IP = IP
        self.PORT = PORT
        self.S_pulse = S_pulse
        self.L_pulse = L_pulse
        self.U_pulse = U_pulse
        self.R_pulse = R_pulse
        self.B_pulse = B_pulse
        self.T_pulse = T_pulse

    def __sendCMD(self,command,payload):
        """INTERNAL - Internal send Function.

        Args:
            command (string): Command - See Yaskawa documentation
            payload (string): Command payload - empty string if no data should be send. If not empty, remember the <CR> at the end!

        Raises:
            Exception: If the Command does not return an ok, an error is raised

        Returns:
            string data: returned data from command transaction
            string data2: returned data from command payload transaction
        """

        print(command,payload)

        # 送數據 命令:HOSTCTRL_REQUEST 
        self.s.send(bytes(f"HOSTCTRL_REQUEST {command} {len(payload)}\r\n","utf-8"))
        # 收數據
        data = self.s.recv(1024)
        print(f'Received: {repr(data)}')

        if data[:2] != b"OK":
            print(f"COMMAND ({command}) ERROR")
            raise Exception("Yaskawa Error!")

        elif len(payload) > 0:
            self.s.send(bytes(f"{payload}","utf-8"))
        
        data2 = self.s.recv(1024)
        print(f'Received: {repr(data2)}')
        
        return data, data2


    def connectMH(self):
        """Connect to the Motoman controller

        Raises:
            Exception: If the connection does not return OK
        """
        self.s.connect((self.IP,self.PORT))
        self.s.send(b"CONNECT Robot_access Keep-Alive:-1\r\n")
        data = self.s.recv(1024)
        print(f'Received: {repr(data)}')
        if data[:2] != b"OK":
            print("Connection Faulty!")
            raise Exception("Yaskawa Connection Error!")

    def disconnectMH(self): #Disconnect
        """Disconnect from the Controller
        """
        self.s.close()

    def getJointAnglesMH(self): #Read Encoder pulses and convert them to Joint Angles
        """Read the Joint Angles

        Returns:
            list: list of the six joint angles
        """
        d1, d2 = self.__sendCMD("RPOSJ","")

        data2_str = d2.decode("utf-8").replace("\r","").split(",")

        data2_arr = [float(data2_str[0])/self.S_pulse,float(data2_str[1])/self.L_pulse,float(data2_str[2])/self.U_pulse,float(data2_str[3])/self.R_pulse,float(data2_str[4])/self.B_pulse,float(data2_str[5])/self.T_pulse]
        return data2_arr

    def getCoordinatesMH(self,coordinateSystem = 1): #Somehow our controller raises an internal error
        """Read the current Position in reference to a selectable coordinate system, currently Broken on DX Controllers!

        Args:
            coordinateSystem (int, optional): The refereced coordinate System. 0 = Base, 1 = Robot, 2-64 = User. Defaults to 0.

        Returns:
            list: List with the current Positional Values
        """
        # d1, d2 = self.__sendCMD("RPOSC","0,0\r")
        d1, d2 = self.__sendCMD("RPOSC",f"{coordinateSystem},{0}\r")
        
        return d2.decode("utf-8").replace("\r","").split(",")

    def servoMH(self, state = True): #Enable/Disable Servos
        """Turn on/off the Servo motors

        Args:
            state (bool, optional): Powerstate to set the servos to. Defaults to True.
        """
        time.sleep(0.1)
        self.__sendCMD("SVON",f"{1 if state else 0}\r")


    def moveAngleMH(self, speed,S,L,U,R,B,T):
        """Move the Robot in joint coordinates

        Args:
            speed (float): Speed value - 0% - 100% - It's not recomended to use more than 50%!
            S (float): S angle
            L (float): L angle
            U (float): U angle
            R (float): R angle
            B (float): B angle
            T (float): T angle
        """
        cmd = f"{speed},{int(S*self.S_pulse)},{int(L*self.L_pulse)},{int(U*self.U_pulse)},{int(R*self.R_pulse)},{int(B*self.B_pulse)},{int(T*self.T_pulse)},0,0,0,0,0,0,0\r" #Convert encoder pulses
        self.__sendCMD("PMOVJ",cmd)
    

    def WriteVariableMH(self, cmd):
        """Write a Variable on the controller

        Args:
            type (int): Type of the Variable | 0 = Byte, 1 = Integer, 2 = Double, 3 = Real, 7 = String. Other Values raise an exception
            number (int): variable numer
            value (byte/int/float/string): Variable Value

        Raises:
            Exception: Exception if the type is not allowed
        """
        cmdfmt1 = f"{cmd[0]},{cmd[1]},{cmd[2]}\r"
        cmdfmt2 = f"{cmd[0]},{cmd[1]},{cmd[2]},{cmd[3]},{cmd[4]},{cmd[5]},{cmd[6]},{cmd[7]},{cmd[8]},{cmd[9]},{cmd[10]},{cmd[11]}\r"
        if len(cmd) == 3: 
            # cmdfmt1 = cmd
            self.__sendCMD("LOADV",cmdfmt1) #Check if Variable Type is allowed
        elif len(cmd) == 12:
            # cmdfmt2 = cmd
            self.__sendCMD("LOADV",cmdfmt2)
        else: 
            raise Exception("Variable Type not supported!")
        

    def ReadVariableMH(self,type,number):
        """Read a variable from the controller

        Args:
            type (int): Type of the Variable
            number (int): Variable Number

        Returns:
            string: Variable Value
        """
        d1,d2 = self.__sendCMD("SAVEV",f"{type},{number}\r")
        return d2.decode("utf-8").replace("\r","")

    def statusMH(self):
        """Read the Status bytes from the Robot

        Returns:
            list: list containing the two status bytes
        """
        d1,d2 = self.__sendCMD("RSTATS","")
        status = d2.decode("utf-8").replace("\r","").split(",")
        return status

    def readCurrJobMH(self):
        """Read the current Job Name

        Returns:
            string: Current Job Name
        """
        d1,d2 = self.__sendCMD("RJSEQ","")
        return d2
    
    def startJobMH(self,job):
        """Start a Job by its name

        Args:
            job (string): Job Name which to start

        Returns:
            string d1: return of command transaction
            string d2: return of the Payload Transaction
        """
        d1,d2 = self.__sendCMD("START",f"{job}\r")
        return d1, d2
    
    def MOVJ(self, cmd):
        """Move Joint Angle with Posture Matrix

        Args:
            cmd = f"{Speed(%)},{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}\r"

            coordinate: 
            Base: 0
            Robot : 1
            User1 : 2
            ...
            User64 : 65
        """
        cmd_ = f"{cmd[0]},{cmd[1]},{cmd[2]},{cmd[3]},{cmd[4]},{cmd[5]},{cmd[6]},{cmd[7]},{cmd[8]},{cmd[9]},{cmd[10]},{cmd[11]},{cmd[12]},{cmd[13]},{cmd[14]},{cmd[15]}\r"
        self.__sendCMD("MOVJ",cmd_)

    def MOVL(self, cmd):
        """Move Line with Posture Matrix

        Args:
            cmd = f"{Speed(0 or 1)},{speed(mm/s or deg/s)}{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}\r"

            coordinate: 
                Base: 0
                Robot : 1
                User1 : 2
                ...
                User64 : 65
            
            Type : 0
        """
        # MOVL cmd = f"{Speed(0 or 1)},{speed(mm/s or deg/s)}{coordinate},{X},{Y},{Z},{Rx},{Ry},{Rz},{Type},{Tool No.},{0},{0},{0},{0},{0},{0}"
        cmd_ = f"{cmd[0]},{cmd[1]},{cmd[2]},{cmd[3]},{cmd[4]},{cmd[5]},{cmd[6]},{cmd[7]},{cmd[8]},{cmd[9]},{cmd[10]},{cmd[11]},{cmd[12]},{cmd[13]},{cmd[14]},{cmd[15]},{cmd[16]}\r"
        self.__sendCMD("MOVL",cmd_)

    def Servo_ON_OFF(self, State):
        ''' Servo Power ON/OFF

        ON:1
        OFF:0
        '''
        OFF = f"{0}\r"
        ON = f"{1}\r"
        if State == 'ON':
            self.__sendCMD("SVON",ON)
        else:
            self.__sendCMD("SVON",OFF)


