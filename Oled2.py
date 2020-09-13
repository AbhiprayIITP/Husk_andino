
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
        #print("In temp")
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
    try:
        #subprocess.check_output(['sudo','qmicli','-d','/dev/cdc-wdm0','--nas-get-signal-strength'],stderr = subprocess.STDOUT,timeout = 3)
        out = subprocess.Popen(['sudo','qmicli','-d','/dev/cdc-wdm0','--nas-get-signal-strength'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        a = str(stdout,'UTF-8')
        a = a[a.find('RSSI'):a.find('RSSI')+35]
        b = [i for i in a if i.isdigit()]
        if (len(b) == 0):
            return "Error"
        a =-1*int("".join(b))
        # print("A",a)
          

        if(a>-85):
            return "Good"
        elif(a<-85 and a>-100):
            return "Average"
        elif(a<-100):
            return "Poor"
        else:
            return "Error 2"
 
    except:
        return "Error3"
    
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
    x = str(stdout,'UTF-8')[-3:].strip()
    if(x=='no'):
        A.append(0)
    else:
        A.append(1)
    

    #Wifi
    ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        output = subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
        A.append(1)
    except subprocess.CalledProcessError:
        A.append(0)
    return A


    
def SaveFile():
    try:
        gsm = Gsm_Connectivity()
    except:
        gsm = "ERROR"
    #gsm = "Good"
    data = Data_Check()
    #data = [1,1,1]
    
    L = [""" "Values" :\n""" , "{\n" , """ "Temperature": \""""+str(T)+"\" \n" , """ "GSM" : \"""" + gsm + "\" \n", """ "Data Connectivity" : \"""" +"RS232 "+("OK\"  \n" if data[0] else "FAIL\"  \n"),""" "Data Connectivity" : \""""+"RS485 "+("OK\"  \n" if data[1] else "FAIL\"  \n"),""" "Data Connectivity" : \""""+"Ethernet "+("OK\" \n" if data[2] else "FAIL\" \n") , "}" ]
    File = open("Test.txt",'w')
    File.writelines(L)
    File.close()
    


    

###############################################################################

# OLED

# #Initialization
RST = None

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

image1 = Image.new('1', (width, height))

draw = ImageDraw.Draw(image1)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding

bottom = height-padding
x = 0
#font = ImageFont.load_default()
font  = ImageFont.truetype('DejaVuSans.ttf',15)
background_thread = Thread(target=Temp_check)
background_thread.start()



while True:
    draw.rectangle((0,0,width,height),outline=0,fill=0)
    #time.sleep(20)
    i = 0
    while(i<=5):
        #disp.clear()
        #disp.display()
        
        draw.rectangle((0,0,width,height),outline = 0,fill = 0)
        draw.text((x, top+16),    "GSM: " + Gsm_Connectivity() ,  font=font, fill=255)
        draw.text((x,top+40),"Temp: "+ str(int(T))+chr(223)+"C",font = font, fill = 255) 
        disp.image(image1)
        disp.display()
        time.sleep(1)
        print("GSM "+ Gsm_Connectivity(), "Temp "+str(int(T)))
           # SaveFile()
        i+=1
          
    i = 0
    B = []
    B = Data_Check()    
    while(i<=5):
       
        
        #disp.clear()
        #disp.display()
        draw.rectangle((0,0,width,height),outline = 0,fill = 0)
        print(B)
        draw.text((x, top+16),    "RS232: " + ("OK" if B[0] else "NOT OK"),  font=font, fill=255)
        draw.text((x, top+40),    "RS485: " + ("OK" if B[1] else "NOT OK"),  font=font, fill=255)
        disp.image(image1)
        disp.display()
        time.sleep(1)
       # SaveFile()
        i+=1
        
    i = 0
    while(i<=5):
       
        
        #disp.clear()
        #disp.display()
        draw.rectangle((0,0,width,height),outline = 0,fill = 0)
        print(B)
        draw.text((x, top+16),    "LAN: " + ("OK" if B[2] else "NOT OK"),  font=font, fill=255)
        draw.text((x, top+40),    "Wi-fi: " + ("OK" if B[3] else "NOT OK"),  font=font, fill=255)
        disp.image(image1)
        disp.display()
        time.sleep(1)
       # SaveFile()
        i+=1

    i = 0
    while(i<=5):
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        #IP = subprocess.check_output(['hostname','--all-ip-addresses'])
        #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        #CPU = subprocess.check_output(cmd, shell = True )
        draw.rectangle((0,0,width,height),outline= 0 ,fill = 0)
        draw.text((x, top+16),  str(IP.decode('utf-8')),  font=font, fill=255)
        #draw.text((x, top+40),     str(CPU), font=font, fill=255)        
        disp.image(image1)
        disp.display()
        print("IP",str(IP.decode('utf-8')))
        #print(str(CPU))     
        time.sleep(1)
        i+=1
   
    i = 0
    while(i<=5):
        draw.rectangle((0,0,width,height),outline = 0,fill = 0)
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        font1  = ImageFont.truetype('DejaVuSans.ttf',10)
        draw.text((x, top+16),    str(MemUsage.decode('utf-8')),  font=font1, fill=255)
        draw.text((x, top+40),    str(Disk.decode('utf-8')),  font=font1, fill=255)
        disp.image(image1)
        disp.display()
        mem = list(map(int,str(MemUsage.decode('utf-8'))[5:12].split("/")))
        print(str(int((mem[0]/mem[1])*100))+" %")
        dis = list(map(int,str(Disk.decode('utf-8'))[6:10].split("/")))
        print(str(int((dis[0]/dis[1])*100))+ " %")
        time.sleep(1)
       # SaveFile()
        i+=1  
        


