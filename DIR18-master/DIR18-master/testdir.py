from DxPackage.dx_fast_eth_server import DxFastEthServer

from paralelno_izvajanje import obdelaj_sliko



dx = DxFastEthServer("192.168.255.1")
#dx = DxFastEthServer("169.254.236.154")

# dx.getStatusInfo()
# for i, item in enumerate(dx.status.viewkeys()):
#     print item, ": ", dx.status[item]

type=1         #0-B, 1-I, 2-D
nr=0            #index
value = 119
#value=120       #value
#text_file = open("C:/Users/Gaja/Desktop/DIR2017/Locevanje_odpadkov-master/Rezultati.txt", "r")
#rezultat = text_file.read()
#text_file.close()

#rezultat = obdelaj_sliko()
#print rezultat

#if rezultat == "konzerva":
#    value = 115
#elif rezultat == "plastenka":
#    value = 116
#elif rezultat == "aluminij":
#    value = 117
#elif rezultat == "tetrapak":
#    value = 118
#elif rezultat == "steklo":
#    value = 119

#dx.writeVar(type, nr, value)

#dx.putServoOff()

type = 0
nr = 2

print "---------------Write/Read  variables"
#type=0              #0-B, 1-I, 2-D
#nr=0                #index
# value=255    #value
# dx.writeVar(type, nr, value)

dx.readVar(type, nr)
print dx.readVar(type, nr)