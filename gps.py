import time
import serial
import os

def readString():
    while 1:
        while ser.read().decode("utf-8") != '$':
            pass
        return ser.readline().decode("utf-8")

def getTime(string, format, returnFormat):
    return time.strftime(returnFormat, time.strptime(string, format))

def getCoordinates(latInfo, lngInfo):
    latDecimal = float(latInfo[2:]) * 1.0 / 60.0
    lngDecimal = float(lngInfo[3:]) * 1.0 / 60.0
    latInt = float(latInfo[:2])
    lngInt = float(lngInfo[:3])
    lat = str(latInt + latDecimal)
    lng = str(lngInt + lngDecimal)
    return lat[:8], lng[:9]

def storeGPS(info):
    GPSfile = open("GPS_data.txt","a")
    GPSfile.write(getTime(info[1], "%H%M%S.%f", "%H:%M:%S"))
    GPSfile.write(",")
    latlng = getCoordinates(info[2], info[4])
    GPSfile.write(latlng[0])
    GPSfile.write(",")
    GPSfile.write(info[3])
    GPSfile.write(",")
    GPSfile.write(latlng[1])
    GPSfile.write(",")
    GPSfile.write(info[5])
    GPSfile.write(",")
    GPSfile.write(info[9])
    GPSfile.write("\n")
    GPSfile.close()
    return
    
def storeSystemInfo():
    systemFile = open("System_data.txt","a")
    systemFile.write(getTime(info[1], "%H%M%S.%f", "%H:%M:%S"))
    systemFile.write(",")
    temp = os.popen('vcgencmd measure_temp').readline()
    temp = temp.replace("temp=","").replace("'C\n","")
    systemFile.write(temp)
    systemFile.write(",")
    systemFile.write(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline()))
    systemFile.close()

def gpsInputCheck(serialInput):
    checkString = serialInput.partition("*")
    checksum = 0
    for c in checkString[0]:
        checksum ^= ord(c)
        
    inputChecksum = int(checkString[2].rstrip(), 16);
    
    if checksum == inputChecksum:
        return True
    else:
        return False

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    gpsFile = open("GPS_data.txt","w+")
    gpsFile.write("Time (UTC),Latitude,Hemisphere,Longitude,Hemisphere,Elevation (M)\n")
    gpsFile.close()
    systemFile = open("System_data.txt","w+")
    systemFile.write("Time (UTC),CPU Temp,CPU usage (%)\n")
    systemFile.close()
    x = 0
    while x < 480:
        serialInput = readString()
        info = serialInput.split(",")
        if gpsInputCheck(serialInput):
            if int(time.time() % 60) == 0 or int(time.time() % 60) == 15 or int(time.time() % 60) == 30 or int(time.time() % 60) == 45:
                if info[0] == "GPGGA":
                    storeGPS(info)
                    x = x + 1
            if int(time.time() % 60) == 0 or int(time.time() % 60) == 20 or int(time.time() % 60) == 30 or int(time.time() % 60) == 50:
                if info[0] == "GPGGA":
                    storeSystemInfo()

