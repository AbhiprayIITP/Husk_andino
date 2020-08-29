import subprocess
def Gsm_Connectivity():
	out =  subprocess.Popen([ 'sudo','qmicli','-d','/dev/cdc-wdm0','--nas-get-signal-strength'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = out.communicate()
        print("Stdout",stdout)
        print("Stderr: ",stderr)	
	a =int(unicode(stdout,'UTF-8')[152:156].strip())
        print(a)
	if(a>-85):
		return "Good"
	elif(a<-85 and a>-100):
		return "Average"
	elif(a<-100):
		return "Poor"
	else:
		return "ERROR"

print(Gsm_Connectivity())

