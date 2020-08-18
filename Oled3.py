import os
import glob
import time
import serial
import serial.tools.list_ports
from threading import Thread
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess


alert = 0
C = 0
T = 0
##############################################################################

#Temperature
 
def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
    
def Temp_check():
    while True:
        global alert
        global C
        global T
        alert = 0
        C = 0
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
 
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        
        lines = read_temp_raw(device_file)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw(device_file)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            T = float(temp_string) / 1000.0
        
        
        while(T>45):
            time.sleep(1)
            C+=1
            
            lines = read_temp_raw(device_file)
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw(device_file)
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                T = float(temp_string) / 1000.0
            
            if(C>60):
                break
        if(C>60):
            alert = 1        
    
	
#############################################################################
            


#GSM Connectivity
            
def Gsm_Connectivity():
    out = subprocess.Popen(['sudo','qmicli','-d','/dev/cdc-wdm0','--nas-get-signal-strength'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    a = int(unicode(stdout,'UTF-8')[152:156].strip())
    if(a>-85):
        return "Good"
    elif(a<-85 and a>-100):
        return "Average"
    elif(a<-100):
        return "Poor"
    else:
        return "Error"
    
#############################################################################

    
#Check Data_Connectivity
    
def Data_Check():
    #RS232
    A = []
    try:
        ser1 = serial.Serial(
                   port="/dev/ttySC1",
                   baudrate = 9600,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   bytesize=serial.EIGHTBITS,
                   timeout=3
                   )
        
        myports = [p.device for p in serial.tools.list_ports.comports()]
        if "/dev/ttySC1" not in myports:
            A.append(1)
        else:
            A.append(0)
            
    
        
        
    except serial.serialutil.SerialException:
        print('Exception')
        A.append(0)
        
    #RS485
        
    try:
        ser2 = serial.Serial(
                   port="/dev/ttySC0",
                   baudrate = 9600,
                   parity=serial.PARITY_NONE,
                   stopbits=serial.STOPBITS_ONE,
                   bytesize=serial.EIGHTBITS,
                   timeout=3
                   )
        
        myports = [p.device for p in serial.tools.list_ports.comports()]
        if "/dev/ttySC0" not in myports:
            A.append(1)
        else:
            A.append(0)
            
    
            
    
        
        
    except serial.serialutil.SerialException:
        print('Exception')
        A.append(0)
        
    #Ethernet        
    out = subprocess.Popen(['ethtool','eth0'],stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout,stderr = out.communicate()
    x = unicode(stdout,'UTF-8')[-3:].strip()
    if(x=='no'):
        A.append(0)
    else:
        A.append(1)
    
    return A



    
background_thread = Thread(target=Temp_check)
background_thread.start()
try:
    gsm = Gsm_Connectivity()
except:
    gsm = "ERROR"
Data = Data_Check()

Send = str(T)+'°C'+" "+gsm+" "+("RS232:Connected" if(Data[0]) else "RS232:Disconnected" )+" "+("RS485:Connected" if(Data[1]) else "RS485:Disconnected" )+" "+("Ethernet:Connected" if(Data[2]) else "Ethernet:Disconnected" )
print(Send)
        




    
    
    
        