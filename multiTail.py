#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,time,sys
appKeys = {}
homedir = os.path.expanduser('~')
configDir = homedir + "/.sceapp"
def readApps():
    f = open("%s/apps.conf"%configDir,"r")
    for line in f.readlines():
        line = line.strip()
        appKeys[line.split(",")[0]] = line.split(",")[1]
    f.close()

readApps();
sleepTime=0.5
showLastNLines=10


argLen = len(sys.argv)
if argLen!=3:
    print "python multiTail.py $appId $logFileName"
    print "e.g."
    print "python multiTail.py 10457 /opt/logs/access_10457.log"
    sys.exit(-1)

user=sys.argv[1]
if appKeys.has_key(user) == False:
    print "pls modify the file apps.conf,add \"appId,secretKey\" into it"
    sys.exit(-1)
secret = appKeys[user];
ips = os.popen("groovy -cp .:./scelib/* ./getSceInstances.groovy %s %s" % (user,secret))
ipsArr=ips.read().split(",");

filePath=sys.argv[2]

lastMTime={}
while True:
	for ip in ipsArr:
		header = "\r\n\r\n\r\n"+filePath+":::"+ip+"============================================\r\n\r\n\r\n"
		cmd="ssh %s@%s -i ./gitKeyRsa \"stat %s|grep Modify\"" % (user,ip,filePath)
		x = os.popen(cmd)
                newLastTime = x.read() 
                if lastMTime.has_key(ip):
			lastTime = lastMTime[ip]
			if lastTime != newLastTime:
                                print header
                                tailCmd = "ssh %s@%s -i ./gitKeyRsa \"tail -%s %s\"" % (user,ip,showLastNLines,filePath)
				os.system(tailCmd)
				lastMTime[ip] = newLastTime
		else:
			lastMTime[ip] = newLastTime
	time.sleep(sleepTime)		

