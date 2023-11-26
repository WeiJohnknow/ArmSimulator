from motoman_robotraconteur_driver.motoplus_rr_driver_feedback_client \
    import MotoPlusRRDriverFeedbackSyncClient
import sys, copy, socket, os, time, struct, traceback, threading, select
import numpy as np
from contextlib import suppress
import pickle,base64

#######################ROBOT STATE FLAG#################################
STATUS_STEP=0x01
STATUS_1_CYCLE=0x02
STATUS_AUTO=0x04
STATUS_RUNNING=0x08
STATUS_HOLD=0x10
STATUS_SAFETY_SPEED_OPERATION=0x20
STATUS_TEACH=0x40
STATUS_PLAY=0x80
STATUS_COMMAND_REMOTE=0x100
STATUS_ALARM=0x200
STATUS_ERROR=0x400
STATUS_SERVO_POWER=0x800
STATUS_API_ERROR_ROBOT=0x4000
STATUS_API_ERROR_STATUS=0x8000

# Disable print
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore print
def enablePrint():
    sys.stdout = sys.__stdout__

def DirExists(folder):
    """Returns true if the folder exists"""
    return os.path.isdir(folder)

def getFileDir(filepath):
    """Returns the directory of a file path"""
    return os.path.dirname(filepath)
def getBaseName(filepath):
    """Returns the file name and extension of a file path"""
    return os.path.basename(filepath)
def RemoveFileFTP(ftp, filepath):
    """Delete a file on a remote server."""
    import ftplib
    try:
        ftp.delete(filepath)
    except ftplib.all_errors as e:
        import sys
        print('POPUP: Could not remove file {0}: {1}'.format(filepath, e))
        sys.stdout.flush()
def UploadFileFTP(file_path_name, server_ip, remote_path, username, password):
    """Upload a file to a robot through FTP"""
    filepath = getFileDir(file_path_name)
    filename = getBaseName(file_path_name)
    import ftplib
    import os
    import sys
    print("POPUP: <p>Connecting to <strong>%s</strong> using user name <strong>%s</strong> and password ****</p><p>Please wait...</p>" % (server_ip, username))
    sys.stdout.flush()
    try:
        myFTP = ftplib.FTP(server_ip, username, password)
    except:
        error_str = sys.exc_info()[1]
        print("POPUP: <font color=\"red\">Connection to %s failed: <p>%s</p></font>" % (server_ip, error_str))
        sys.stdout.flush()
        time.sleep(4)
        return False

    remote_path_prog = remote_path + '/' + filename
    print("POPUP: Connected. Deleting remote file %s..." % remote_path_prog)
    sys.stdout.flush()
    RemoveFileFTP(myFTP, remote_path_prog)
    print("POPUP: Connected. Uploading program to %s..." % server_ip)
    sys.stdout.flush()
    try:
        myFTP.cwd(remote_path)
    except:
        error_str = sys.exc_info()[1]
        print("POPUP: <font color=\"red\">Remote path not found or can't be created: %s</font>" % (remote_path))
        sys.stdout.flush()
        time.sleep(4)
        #contin = mbox("Remote path\n%s\nnot found or can't create folder.\n\nChange path and permissions and retry." % remote_path)
        return False

    def uploadThis(localfile, filename):
        print('  Sending file: %s' % localfile)
        print("POPUP: Sending file: %s" % filename)
        sys.stdout.flush()
        fh = open(localfile, 'rb')
        myFTP.storbinary('STOR %s' % filename, fh)
        fh.close()

    uploadThis(file_path_name, filename)
    myFTP.close()
    print("POPUP: File trasfer completed: <font color=\"blue\">%s</font>" % remote_path_prog)
    sys.stdout.flush()
    return True

def UploadFTP(program, robot_ip, remote_path, ftp_user, ftp_pass, pause_sec=2):
    if os.path.isfile(program):
        print('Sending program file %s...' % program)
        UploadFileFTP(program, robot_ip, remote_path, ftp_user, ftp_pass)
    else:
        print('Sending program folder %s...' % program)
        UploadDirFTP(program, robot_ip, remote_path, ftp_user, ftp_pass)

    time.sleep(pause_sec)
    print("POPUP: Done")
    sys.stdout.flush()

class MotionProgram:
    """Robot post object defined for Motoman robots"""
    MAX_LINES_X_PROG = 2000      # maximum number of lines per program. It will then generate multiple "pages (files)". This can be overriden by RoboDK settings.    
                
    def __init__(self, pulse2deg,ROBOT_CHOICE ,ROBOT_CHOICE2=None,ROBOT_CHOICE3=None, tool_num = 12, pulse2deg_2=None,pulse2deg_3=None):
        self.ACTIVE_TOOL = tool_num
        self._primitives={'movel':self.MoveL,'movej':self.MoveJ}
        #hardcoded p2d for all robots in series
        # self.reading_conversion=10000*np.ones(14)
        # self.reading_conversion[1::2]=-self.reading_conversion[1::2]

        self.reading_conversion=np.array([1341.380023,1907.674052,1592.888923,1022.862207,980.2392898,454.754161,1435.350459,1300.317471,1422.222174,969.9555508,980.2392898,454.754161,1994.296925,1376.711214])

        self.ROBOT_CHOICE = ROBOT_CHOICE
        self.PULSES_X_DEG = pulse2deg
        self.PULSES_X_DEG_2 = pulse2deg_2
        self.PULSES_X_DEG_3 = pulse2deg_3
        self.ROBOT_CHOICE2=ROBOT_CHOICE2
        self.ROBOT_CHOICE3=ROBOT_CHOICE3
        self.ProgStart()

    def ProgStart(self):
        self.PROG=[]
        self.PROG_TARGETS=[]
        self.PROG_TARGETS2=[]
        # PROG specific variables:
        self.LINE_COUNT = 0      # Count the number of instructions (limited by MAX_LINES_X_PROG)
        self.C_COUNT = 0         # Count the number of P targets in one file
        self.EC_COUNT = 0
        self.tool_CONF_set=False
        self.pulse_CONF_set=False

    def ProgEnd(self):
        self.ProgFinish(r"""AAA""")
        self.progsave(".","AAA")
        
    def ProgFinish(self, progname):

        header = ''
        header += '/JOB' + '\n'
        header += '//NAME %s' % progname + '\n'
        header += '//POS' + '\n'
        header += '///NPOS %i,0,%i,0,0,0' % (self.C_COUNT, self.EC_COUNT)
        
        # Targets are added at this point       
        
        import time        
        datestr = time.strftime("%Y/%m/%d %H:%M")
        
        header_ins = ''
        header_ins += '//INST' + '\n'
        header_ins += '///DATE %s' % datestr + '\n'

        if self.ROBOT_CHOICE3:
            header_ins += '///ATTR SC,RW' + '\n'

            header_ins += '///GROUP1 '+self.ROBOT_CHOICE +','+self.ROBOT_CHOICE2 + '\n'
            header_ins += '///GROUP2 '+self.ROBOT_CHOICE3 + '\n'

        elif self.ROBOT_CHOICE2:
            header_ins += '///ATTR SC,RW' + '\n'

            header_ins += '///GROUP1 '+self.ROBOT_CHOICE + '\n'
            header_ins += '///GROUP2 '+self.ROBOT_CHOICE2 + '\n'
        else:
            header_ins += '///ATTR SC,RW' + '\n'
            header_ins += '///GROUP1 '+self.ROBOT_CHOICE + '\n'

        header_ins += 'NOP'

        self.PROG.insert(0, header_ins)
        self.PROG.append('END')
        
        self.PROG_TARGETS.insert(0, header)
        
        self.PROG = self.PROG_TARGETS + self.PROG_TARGETS2 + self.PROG        
        
        
    def progsave(self, folder, progname):
        if not folder.endswith('/'):
            folder = folder + '/'
        progname = progname + '.JBI'
        filesave = folder + progname
        fid = open(filesave, "w")
        #fid.write(self.PROG)
        for line in self.PROG:
            fid.write(line)
            fid.write('\n')
        fid.close()        
    
    ##############################################MOTION COMMAND################################################################################    
    def MoveJ(self, joints, speed, zone=None, target2=None, target3=None):
        ###target2: [primitive,q,v]
        """Add a joint movement"""
        speed=max(speed,0.1)                ###speed=0 will raise error in INFORM
        
        if zone is not None:
            zone_args=' PL=%i' % round(min(zone, 8))
        else:
            zone_args=''

        if 'ST' in self.ROBOT_CHOICE:
            target_id = self.add_target_joints2(joints,self.PULSES_X_DEG)
            self.addline("MOVJ EC%05d %s" % (target_id, "VJ=%.1f" % speed))
        else:
            target_id = self.add_target_joints(joints)
            if target3:
                target_id_2 = self.add_target_joints2(target2[1],self.PULSES_X_DEG_2)
                target_id_3 = self.add_target_joints(target3[1],self.PULSES_X_DEG_3)
                if target3[2]: #speed args given
                    if 'J' in target3[0]:
                        self.addline("MOVJ C%05d EC%05d %s%s" % (target_id,target_id_2, "VJ=%.1f" % speed, zone_args)+ ' +' + target3[0]+" C%05d" % (target_id_3)+ " VJ=%.1f" % target3[2])  
                    else:
                        self.addline("MOVJ C%05d EC%05d %s%s" % (target_id,target_id_2, "VJ=%.1f" % speed, zone_args)+ ' +' + target3[0]+" C%05d" % (target_id_3)+ " V=%.1f" % target3[2]) 
                else:
                    self.addline("MOVJ C%05d EC%05d %s%s" % (target_id,target_id_2, "VJ=%.1f" % speed, zone_args)+ ' +' + target3[0]+" C%05d" % (target_id_3))
            elif target2:
                if 'RB' in self.ROBOT_CHOICE2:   ###if second robot is a robot
                    target_id_2 = self.add_target_joints(target2[1],self.PULSES_X_DEG_2)
                    if target2[2]: #speed args given
                        if 'J' in target2[0]:
                            self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args)+ ' +' + target2[0]+" C%05d" % (target_id_2)+ " VJ=%.1f" % target2[2])
                        else:
                            self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args)+ ' +' + target2[0]+" C%05d" % (target_id_2)+ " V=%.1f" % target2[2]) 
                    else:
                        self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args)+ ' +' + target2[0]+" C%05d" % (target_id_2))
                else:                           ###if second robot is a positioner
                    target_id_2 = self.add_target_joints2(target2[1],self.PULSES_X_DEG_2)
                    if target2[2]: #speed args given
                        if 'J' in target2[0]:
                            self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2)+ " VJ=%.1f" % target2[2]) 
                        else:
                            self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2)+ " V=%.1f" % target2[2])  
                    else:
                        self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2))

            else:
                self.addline("MOVJ C%05d %s%s" % (target_id, "VJ=%.1f" % speed, zone_args))                  
            
    def MoveL(self, joints, speed, zone=None, target2=None, target3=None):
        ###target2: [primitive,q,v]
        ###joints: degrees
        """Add a linear movement"""        
        target_id = self.add_target_joints(joints)
        speed=max(speed,0.1)                ###speed=0 will raise error in INFORM

        if zone is not None:
            zone_args=' PL=%i' % round(min(zone, 8))
        else:
            zone_args=''

        if target3:
                
                target_id_2 = self.add_target_joints2(target2[1],self.PULSES_X_DEG_2)
                target_id_3 = self.add_target_joints(target3[1],self.PULSES_X_DEG_3)
                if target3[2]: #speed args given
                    speed3=max(target3[2],0.1)      ###speed=0 will raise error in INFORM
                    if 'J' in target3[0]:
                        self.addline("MOVL C%05d EC%05d %s%s" % (target_id, target_id_2, "V=%.1f" % speed, zone_args)+ ' +' + target3[0]+" C%05d" % (target_id_3) + " VJ=%.1f" % speed3)                    
                    else:
                        self.addline("MOVL C%05d EC%05d %s%s" % (target_id, target_id_2, "V=%.1f" % speed, zone_args)+ ' +' + target3[0]+" C%05d" % (target_id_3) + " V=%.1f" % speed3)
                else:
                    self.addline("MOVL C%05d EC%05d %s%s" % (target_id, target_id_2, "V=%.1f" % speed, zone_args)+ ' +' + target3[0]+" C%05d" % (target_id_3))

        elif target2:
            if 'RB' in self.ROBOT_CHOICE2:   ###if second robot is a robot
                target_id_2 = self.add_target_joints(target2[1],self.PULSES_X_DEG_2)
                if target2[2]: #speed args given
                    speed2=max(target2[2],0.1)      ###speed=0 will raise error in INFORM
                    if 'J' in target2[0]:
                        self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" C%05d" % (target_id_2) + " VJ=%.1f" % speed2)                        
                    
                    else:
                        self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" C%05d" % (target_id_2) + " V=%.1f" % speed2) 
                else:
                    self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" C%05d" % (target_id_2))       
            else:                           ###if second robot is a positioner
                target_id_2 = self.add_target_joints2(target2[1],self.PULSES_X_DEG_2)
                if 'J' in target2[0]:
                    if target2[2]: #speed args given
                        self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2) + " VJ=%.1f" % target2[2])       
                    else:
                        self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2))                 
                else:
                    if target2[2]: #speed args given
                        self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2) + " V=%.1f" % target2[2])        
                    else:
                        self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args)+ ' +' + target2[0]+" EC%05d" % (target_id_2))
        else:
            self.addline("MOVL C%05d %s%s" % (target_id, "V=%.1f" % speed, zone_args))        
        
    def MoveC(self, joints1, joints2, joints3, speed, zone, target2=None):
        ###target2: MOVC,j1,j2,j3,speed,zone
        """Add a circular movement"""
        
        speed=max(speed,0.1)                ###speed=0 will raise error in INFORM
        if zone is not None:
            zone_args=' PL=%i' % round(min(zone, 8))
        else:
            zone_args=''

        target_id1 = self.add_target_joints(joints1)
        target_id2 = self.add_target_joints(joints2)
        target_id3 = self.add_target_joints(joints3)
        
        if target2:
            if 'RB' in self.ROBOT_CHOICE2:   ###if second robot is a robot
                target_id1_2 = self.add_target_joints(target2[1],self.PULSES_X_DEG_2)
                target_id2_2 = self.add_target_joints(target2[2],self.PULSES_X_DEG_2)
                target_id3_2 = self.add_target_joints(target2[3],self.PULSES_X_DEG_2)

                if 'J' in target2[0]:
                    self.addline("MOVC C%05d %s%s" % (target_id1, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" C%05d" % (target_id1_2))
                    self.addline("MOVC C%05d %s%s" % (target_id2, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" C%05d" % (target_id2_2))
                    self.addline("MOVC C%05d %s%s" % (target_id3, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" C%05d" % (target_id3_2))

                else:
                    
                    self.addline("MOVC C%05d %s%s" % (target_id1, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" C%05d" % (target_id1_2))
                    self.addline("MOVC C%05d %s%s" % (target_id2, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" C%05d" % (target_id2_2))
                    self.addline("MOVC C%05d %s%s" % (target_id3, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" C%05d" % (target_id3_2))

            else:
                target_id1_2 = self.add_target_joints2(target2[1],self.PULSES_X_DEG_2)
                target_id2_2 = self.add_target_joints2(target2[2],self.PULSES_X_DEG_2)
                target_id3_2 = self.add_target_joints2(target2[3],self.PULSES_X_DEG_2)

                if 'J' in target2[0]:
                    self.addline("MOVC C%05d %s%s" % (target_id1, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" EC%05d" % (target_id1_2))
                    self.addline("MOVC C%05d %s%s" % (target_id2, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" EC%05d" % (target_id2_2))
                    self.addline("MOVC C%05d %s%s" % (target_id3, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" EC%05d" % (target_id3_2))

                else:
                    
                    self.addline("MOVC C%05d %s%s" % (target_id1, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" EC%05d" % (target_id1_2))
                    self.addline("MOVC C%05d %s%s" % (target_id2, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" EC%05d" % (target_id2_2))
                    self.addline("MOVC C%05d %s%s" % (target_id3, "V=%.1f" % speed, zone_args) + ' +' + target2[0]+" EC%05d" % (target_id3_2))

        else:
                
            self.addline("MOVC C%05d %s%s" % (target_id1, "V=%.1f" % speed, zone_args))
            self.addline("MOVC C%05d %s%s" % (target_id2, "V=%.1f" % speed, zone_args))
            self.addline("MOVC C%05d %s%s" % (target_id3, "V=%.1f" % speed, zone_args+' FPT'))

    def setArc(self,on,cond_num=None):
        if cond_num:
            if on:
                self.addline('ARCON '+'ASF#('+str(cond_num)+')')
            else:
                self.addline('ARCOF')
        else:
            if on:
                self.addline('ARCON')
            else:
                self.addline('ARCOF')

    def changeArc(self,cond_num):
        self.addline('ARCSET '+'ASF#('+str(cond_num)+')')
        

    def touchsense(self,joints, speed ,distance):

        target_id = self.add_target_joints(joints)
        self.addline("MOVL C%05d V=%.1f SRCH RIN#(3)=ON DIS=%.1f" % (target_id, speed, distance))

    def setTool(self, tool_id):
        self.addline("// TOOL#(%i)" % tool_id)

    def setWaitTime(self,t):
        self.addline('TIMER T=%.2f' % t)

    def setDOPulse(self,io_var,duration):        
        self.addline('PULSE OT#(%s) T=%.2f' % (io_var, duration))

    def setDO(self, io_var, io_value):  ###Universal Output
        ###OT 11:   WireCut
        ###OT 21:   SOLENOID (spray cooler)
        ###OT 4092: Gas Purge
        ###OT 4095: Wire Inch
        ###OT 4096: Wire Retract
        
        """Sets a variable (output) to a given value"""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = 'OT#(%s)' % str(io_var)        
        if type(io_value) != str: # set default variable value if io_value is a number            
            if io_value > 0:
                io_value = 'ON'
            else:
                io_value = 'OFF'
        
        self.addline('DOUT %s %s' % (io_var, io_value))
        
    def waitDI(self, io_var, io_value, timeout_ms=-1):
        """Waits for an input io_var to attain a given value io_value. Optionally, a timeout can be provided."""
        if type(io_var) != str:  # set default variable name if io_var is a number
            io_var = 'IN#(%s)' % str(io_var)        
        if type(io_value) != str: # set default variable value if io_value is a number            
            if io_value > 0:
                io_value = 'ON'
            else:
                io_value = 'OFF'
        
        # at this point, io_var and io_value must be string values
        if timeout_ms < 0:
            #WAIT IN#(12)=ON
            self.addline('WAIT %s=%s' % (io_var, io_value))
        else:
            self.addline('WAIT %s=%s T=%.2f' % (io_var, io_value, timeout_ms*0.001))

# ------------------ private ----------------------
    def addline(self, newline, movetype = ' '):
        """Add a program line"""
        
        self.LINE_COUNT = self.LINE_COUNT + 1
        self.PROG.append(newline)

    def setPulses(self):
        if not self.tool_CONF_set:
            self.PROG_TARGETS.append("///TOOL %i" % self.ACTIVE_TOOL)
            self.tool_CONF_set=True
        if not self.pulse_CONF_set:
            self.PROG_TARGETS.append("///POSTYPE PULSE")
            self.PROG_TARGETS.append("///PULSE")
            self.pulse_CONF_set=True


    def add_target_joints(self, joints, pulse2deg=None):    

        self.setPulses()            
        cid = self.C_COUNT
        self.C_COUNT = self.C_COUNT + 1        
                
        str_pulses=[]

        if pulse2deg is None:
            pulse2deg = self.PULSES_X_DEG
        for i in range(len(joints)):
            str_pulses.append('%i' % round(joints[i] * pulse2deg[i]))

        self.PROG_TARGETS.append('C%05i=' % cid + ','.join(str_pulses))         
        return cid

    def add_target_joints2(self, joints,pulse2deg): 

        self.setPulses()            
        ecid = self.EC_COUNT
        self.EC_COUNT = self.EC_COUNT + 1        
                
        str_pulses=[]        
        for i in range(len(joints)):
            str_pulses.append('%i' % round(joints[i] * pulse2deg[i]))

        self.PROG_TARGETS2.append('EC%05i=' % ecid + ','.join(str_pulses))         
        return ecid
    
    def primitive_call(self, primitive,q,v):
        return self._primitives[primitive](q,v)

    def primitive_call_dual(self, primitive,q,v,target2):
        return self._primitives[primitive](q,v,target2=target2)

    def primitive_call_tri(self, primitive,q,v,target2,target3):
        return self._primitives[primitive](q,v,target2=target2,target3=target3)


# Object class that handles the robot instructions/syntax
class MotionProgramExecClient(object):
    
    def __init__(self, IP='192.168.1.31', PORT=80):
        self.s_MP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #motoplus socket connection
        self.s_MP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s_MP.bind(('0.0.0.0',11000))
        self._lock=threading.Lock()
        self._recording=False

        #hardcoded p2d for all robots in series
        # self.reading_conversion=10000*np.ones(14)
        # self.reading_conversion[1::2]=-self.reading_conversion[1::2]

        self.reading_conversion=np.array([1341.380023,1907.674052,1592.888923,1022.862207,980.2392898,454.754161,1435.350459,1300.317471,1422.222174,969.9555508,980.2392898,454.754161,1994.296925,1376.711214])

        self.IP=IP
        self.PORT=PORT

        self.buf_struct = struct.Struct("<34i")
        self.recording=[]
        self._streaming=False
        self.state_flag=0        
                
        ##################RR driver part for new reading############################
        s='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'
        self.controller_info=pickle.loads(base64.b64decode(s))
        self.fb = MotoPlusRRDriverFeedbackSyncClient()
        self.fb.start(IP)
    
    ##################ADVANCED ETHERNET FUNCTION############################

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
        self.s = socket.socket()        #ethernet function socket connection
        self.connectMH()
        try:

            self.s.send(bytes(f"HOSTCTRL_REQUEST {command} {len(payload)}\r\n","utf-8"))
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
        finally:
            with suppress(Exception):
                self.disconnectMH()


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

    def getJointAnglesMH(self,PULSES_X_DEG): #Read Encoder pulses and convert them to Joint Angles
        """Read the Joint Angles

        Returns:
            list: list of the six joint angles
        """
        d1, d2 = self.__sendCMD("RPOSJ","")

        data2_str = d2.decode("utf-8").replace("\r","").split(",")

        data2_arr = [int(data2_str[0])/PULSES_X_DEG[0],int(data2_str[1])/PULSES_X_DEG[1],int(data2_str[2])/PULSES_X_DEG[2],int(data2_str[3])/PULSES_X_DEG[3],int(data2_str[4])/PULSES_X_DEG[4],int(data2_str[5])/PULSES_X_DEG[5]]
        return np.radians(data2_arr)

    def getJointAnglesDB(self,PULSES_X_DEG): #Read Encoder pulses and convert them to Joint Angles
        """Read the Joint Angles

        Returns:
            list: list of the six joint angles
        """
        d1, d2 = self.__sendCMD("RPOSJ","")

        data2_str = d2.decode("utf-8").replace("\r","").split(",")

        data2_arr = [int(data2_str[6])/PULSES_X_DEG[0],int(data2_str[7])/PULSES_X_DEG[1]]
        return np.radians(data2_arr)

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
        cmd = f"{speed},{int(S*self.PULSES_X_DEG[0])},{int(L*self.PULSES_X_DEG[1])},{int(U*self.PULSES_X_DEG[2])},{int(R*self.PULSES_X_DEG[3])},{int(B*self.PULSES_X_DEG[4])},{int(T*self.PULSES_X_DEG[5])},0,0,0,0,0,0,0\r" #Convert encoder pulses
        self.__sendCMD("PMOVJ",cmd)

    def statusMH(self):
        """Read the Status bytes from the Robot

        Returns:
            list: list containing the two status bytes
        """
        d1,d2 = self.__sendCMD("RSTATS","")
        status = d2.decode("utf-8").replace("\r","").split(",")
        return status
    
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

    # def threadfunc(self):
    #     while(self._streaming):
    #         try:                
    #             res, data = self.receive_from_robot(0.01)
    #             # print(res)
    #             if res:
    #                 with self._lock:
    #                     self.joint_angle=np.radians(np.divide(np.array(data[20:34]),self.reading_conversion))
    #                     self.state_flag=data[16]
    #                     # print(self.joint_angle)
    #                     timestamp=data[0]+data[1]*1e-9
    #                     if self._recording:
    #                         self.recording.append(np.array([timestamp]+self.joint_angle.tolist()+[data[18],data[19]]))
    #                     else:
    #                         self.recording=[]
    #         except:
    #             traceback.print_exc()


    def threadfunc(self):
        while(self._streaming):
            try:                
                res, fb_data = self.fb.try_receive_state_sync(self.controller_info, 0.001)
                if res:
                    with self._lock:
                        self.joint_angle=np.hstack((fb_data.group_state[0].feedback_position,fb_data.group_state[1].feedback_position,fb_data.group_state[2].feedback_position))
                        self.state_flag=fb_data.controller_flags
                        # print(self.joint_angle)
                        timestamp=fb_data.time
                        if self._recording:
                            self.recording.append(np.array([timestamp]+self.joint_angle.tolist()+[fb_data.job_state[0][1],fb_data.job_state[0][2]]))
                        else:
                            self.recording=[]
            except:
                traceback.print_exc()

    def receive_from_robot(self, timeout=0):
        """
        Receive feedback from the robot. Specify an optional timeout. Returns a tuple with success and the current
        robot state.
        :param timeout: Timeout in seconds. May be zero to immediately return if there is no new data.
        :return: Success and robot state as a tuple
        """
        s=self.s_MP
        s_list=[s]
        try:
            res=select.select(s_list, [], s_list, timeout)
        except select.error as err:
            if err.args[0] == errno.EINTR:
                return False, None
            else:
                raise

        if len(res[0]) == 0 and len(res[2])==0:
            return False, None
        try:
            (buf, addr)=s.recvfrom(65536)
        except:
            return False, None

        data = self.buf_struct.unpack(buf)
        return True, data


    def StartStreaming(self):
        if self._streaming:     ###if already streaming
            return
        self._streaming=True
        t=threading.Thread(target=self.threadfunc)
        t.daemon=True
        t.start()
    def StopStreaming(self):
        self._streaming=False


    ##############################EXECUTION############################################
    def execute_motion_program_nonblocking(self, motion_program: MotionProgram):
        motion_program.ProgEnd()
        UploadFTP('AAA.JBI', self.IP, 'JOB', "ftp", "")
        ###TODO: figure out return time
        self.servoMH() #Turn Servo on
        self.startJobMH('AAA')
        motion_program.ProgStart()

    def execute_motion_program(self, motion_program: MotionProgram):
        motion_program.ProgEnd()
        self.StartStreaming()
        try:            
            UploadFTP('AAA.JBI', self.IP, 'JOB', "ftp", "")
            ###TODO: figure out return time
            self.servoMH() #Turn Servo on

            self.startJobMH('AAA')
            self._recording=True
            ###block printing
            # blockPrint()
            last_reading=np.zeros(14)
            start_time=time.time()
            while True:
                time.sleep(0.001)
                # print(self.state_flag)
                if self.state_flag & STATUS_RUNNING == 0 and time.time()-start_time>1.:
                    break       ###quit running loop if servo motor off
                    
                # if len(self.joint_recording)>10:
                #     if np.array_equal(self.joint_recording[-1][1:],self.joint_recording[-7][1:]):
                #         with self._lock:
                #             [d1,d2]=self.statusMH()
                #             d1 = [int(i) for i in bin(int(d1))[2:]]
                #             if not d1[4]:       #if robot not running
                #                 break


            ###enable printing
            # enablePrint()
            recording=np.array(copy.deepcopy(self.recording))
            self._recording=False
            self.servoMH(False) #Turn the Servos of

            return recording[:,0]-recording[0,0], recording[:,1:-2], recording[:,-2], recording[:,-1]
        finally:
            self.StopStreaming()
            ###clean INFORM code
            motion_program.ProgStart()
    
    def execute_motion_program_file(self, filename):
        self.StartStreaming()
        try:            
            UploadFTP(filename, self.IP, 'JOB', "ftp", "")
            ###TODO: figure out return time
            self.servoMH() #Turn Servo on

            self.startJobMH(filename[:-4])
            self._recording=True
            ###block printing
            # blockPrint()
            last_reading=np.zeros(14)
            start_time=time.time()
            while True:
                time.sleep(0.001)
                # print(self.state_flag)
                if self.state_flag & STATUS_RUNNING == 0 and time.time()-start_time>1.:
                    break       ###quit running loop if servo motor off
                    
                # if len(self.joint_recording)>10:
                #     if np.array_equal(self.joint_recording[-1][1:],self.joint_recording[-7][1:]):
                #         with self._lock:
                #             [d1,d2]=self.statusMH()
                #             d1 = [int(i) for i in bin(int(d1))[2:]]
                #             if not d1[4]:       #if robot not running
                #                 break


            ###enable printing
            # enablePrint()
            recording=np.array(copy.deepcopy(self.recording))
            self._recording=False
            self.servoMH(False) #Turn the Servos of

            return recording[:,0]-recording[0,0], recording[:,1:-2], recording[:,-2], recording[:,-1]
        finally:
            self.StopStreaming()

            
            

def main():
    mp=MotionProgram(ROBOT_CHOICE='RB1',pulse2deg=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02])
    client=MotionProgramExecClient()

    mp.setWaitTime(1)
    mp.MoveJ([0,0,0,0,0,0],10,0)
    mp.setWaitTime(1)
    mp.MoveJ([0,-1.23097,-15.1604,0,13.9294,0],10,0)
    mp.MoveJ([0,-27.1205,-36.7057,0,9.58517,0],10,0)

    timestamp,joint_recording,job_line,job_step=client.execute_motion_program(mp)
    print('job_line ', job_line)
    print('job_step ',job_step)



def movec_test():
    mp=MotionProgram(ROBOT_CHOICE='RB1',pulse2deg=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02])
    client=MotionProgramExecClient()

    q1=np.array([-29.3578,31.3077,10.7948,7.6804,-45.9367,-18.5858])
    q2=np.array([-3.7461,37.3931,19.2775,18.7904,-53.9888,-48.712])
    q3=np.array([29.3548,5.8107,-20.41,27.3331,-58.956,-86.4])
    mp.MoveJ(q1,1,0)
    mp.MoveC(q1, q2, q3, 10,0)

    client.execute_motion_program(mp)

def multimove_positioner():           ###multimove with robot+ positioner
    mp=MotionProgram(ROBOT_CHOICE='RB2',ROBOT_CHOICE2='ST1',pulse2deg=[1.435355447016790322e+03,1.300329111270902331e+03,1.422225409601069941e+03,9.699560942607320158e+02,9.802408285708806943e+02,4.547552630640436178e+02],pulse2deg_2=[1994.3054,1376.714])
    client=MotionProgramExecClient()

    q1=np.array([43.5893,72.1362,45.2749,-84.0966,24.3644,94.2091])
    q2=np.array([34.6291,55.5756,15.4033,-28.8363,24.0298,3.6855])
    q3=np.array([27.3821,51.3582,-19.8428,-21.2525,71.6314,-62.8669])

    target2=['MOVJ',[-15,180],[-15,160],[-15,140],1,0]
    target2J_1=['MOVJ',[-15,180],1,0]
    target2J_2=['MOVJ',[-15,140],1,0]
    target2J_3=['MOVJ',[-15,100],1,0]

    mp.MoveJ(q1, 1,0,target2=target2J_1)
    mp.MoveL(q2, 10,0,target2=target2J_2)
    mp.MoveL(q3, 10,0,target2=target2J_3)
    
    client.execute_motion_program(mp)

def multimove_robots():  ####multimove with 2 robots
    mp=MotionProgram(ROBOT_CHOICE='RB1',ROBOT_CHOICE2='RB2',pulse2deg=[1.435355447016790322e+03,1.300329111270902331e+03,1.422225409601069941e+03,9.699560942607320158e+02,9.802408285708806943e+02,4.547552630640436178e+02],pulse2deg_2=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02])
    client=MotionProgramExecClient()

    q1=np.array([43.5893,72.1362,45.2749,-84.0966,24.3644,94.2091])
    q2=np.array([34.6291,55.5756,15.4033,-28.8363,24.0298,3.6855])
    q3=np.array([27.3821,51.3582,-19.8428,-21.2525,71.6314,-62.8669])

    target2J_1=['MOVJ',q1,1,0]
    target2J_2=['MOVJ',q2,1,0]
    target2J_3=['MOVJ',q3,1,0]

    mp.MoveJ(q1, 1,None,target2=target2J_1)
    mp.MoveL(q2, 10,None,target2=target2J_2)
    mp.MoveL(q3, 10,None,target2=target2J_3)

    
    client.execute_motion_program(mp)


def DO_test():
    mp=MotionProgram(ROBOT_CHOICE='RB1',pulse2deg=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02])
    client=MotionProgramExecClient()
    mp.setDO(4092,1)
    mp.setDOPulse(11,2)
    mp.setDO(4092,0)
    client.execute_motion_program(mp)  

def Touch_test():
    mp=MotionProgram(ROBOT_CHOICE='RB1',pulse2deg=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02])
    client=MotionProgramExecClient()
    q1=np.array([-32.3278,34.4634,11.3912,-14.2208,-50.0826,39.8111])
    q2=np.array([-32.3264,36.432,9.0947,-15.1946,-46.0499,41.2464])
    mp.MoveJ(q1,1,0)
    mp.touchsense(q2, 10 ,20)
    client.execute_motion_program(mp) 

def read_joint():
    client=MotionProgramExecClient()
    print(client.getJointAnglesDB([1994.296925,1376.711214]))

def read_joint2():
    mp=MotionProgram(ROBOT_CHOICE='RB1',pulse2deg=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02])
    client=MotionProgramExecClient()
    q1=np.zeros(6)
    mp.MoveJ(q1,1,0)
    ts,js,job_line,job_step=client.execute_motion_program(mp) 
    print(ts,js,job_line,job_step)

def move_3robots():
    mp=MotionProgram(ROBOT_CHOICE='RB1',pulse2deg=[1.341416193724337745e+03,1.907685083229250267e+03,1.592916090846681982e+03,1.022871664227330484e+03,9.802549195016306385e+02,4.547554799861444508e+02],
                     ROBOT_CHOICE2='ST1',pulse2deg_2=[1994.296925,1376.711214],
                     ROBOT_CHOICE3='RB2',pulse2deg_3=[1435.350459,1300.317471,1422.222174,969.9555508,980.2392898,454.754161])
    q1_1=np.zeros(6)
    q2_1=np.array([np.radians(-15),np.pi])
    q3_1=np.array([np.pi/2,0,0,0,0,0])
    q1_2=-0.5*np.ones(6)
    q2_2=np.array([np.radians(15),np.pi])
    q3_2=np.array([np.pi/2,np.pi/6,0,0,0,0])

    target2_1=['MOVJ',np.degrees(q2_1),None]
    target3_1=['MOVJ',np.degrees(q3_1),None]
    target2_2=['MOVJ',np.degrees(q2_2),None]
    target3_2=['MOVJ',np.degrees(q3_2),None]

    mp.MoveJ(np.degrees(q1_1), 10,None,target2=target2_1,target3=target3_1)
    mp.MoveJ(np.degrees(q1_2), 10,None,target2=target2_2,target3=target3_2)


    client=MotionProgramExecClient()
    client.execute_motion_program(mp) 


if __name__ == "__main__":
    # main()
    # DO_test()
    # multimove_positioner()
    # movec_test()
    # multimove_robots()
    read_joint2()
    # move_3robots()

    
