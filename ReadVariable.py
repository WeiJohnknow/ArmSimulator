from MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one

mh = MotomanConnector() #Create Connector
mh.connectMH() #Connect
print(mh.ReadVariableMH(4,1)) #Read I004 and print the result
mh.disconnectMH() #Disconnect