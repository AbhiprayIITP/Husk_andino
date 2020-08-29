import os
import glob
import time

alert = 0
C = 0
T = 0

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
    
def Temp_check():
    while True:
        print("Hi")
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
           #print('The temperature is : ',T,' degree celsius')
            print(T)
        
        while(T>45):
            #print("Inside While")
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
    
print("Hello")
Temp_check()
