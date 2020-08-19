import subprocess as s
import time
ip="www.google.com"
time_check = 0
freq = 0 
while(time_check < 7200):
    if(freq == 300):
        try:
            #print("trying")
            s.check_output(["ping","-c","5",ip])
            time_check=0
            freq = 0
        except:
            #print("Error")
            time_check += 313
            freq = 0
    else:
        time.sleep(1)
        freq+=1 
#print('rebooting')
out = s.Popen(['sudo','reboot'],stdout = s.PIPE,stderr=s.STDOUT)
stdout,stderr = out.communicate()



   
