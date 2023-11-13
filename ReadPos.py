from MotomanEthernet import MotomanConnector # ..MotomanEthernet - .. because the file is one folder above the current one
buffer = []
mh = MotomanConnector() #Create Connector
mh.connectMH() #Connect
# buffer = mh.getJointAnglesMH()
buffer = mh.getCoordinatesMH()
print(buffer) #Get the Joint angles and print them
mh.disconnectMH()