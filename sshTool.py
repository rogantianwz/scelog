#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,time,sys,string
# this script is used to ssh to the sce server more conviniently
appKeys = {}
homedir = os.path.expanduser('~')
configDir = homedir + "/.sceapp"
def readApps():
    f = open("%s/apps.conf"%configDir,"r")
    for line in f.readlines():
        line = line.strip()
        appKeys[line.split(",")[0]] = line.split(",")[1]
    f.close()
def getIps(user):
    if appKeys.has_key(user) == False:
        print "pls modify this file,add appId:secretKey into appKeys"
        sys.exit(-1)
    secret = appKeys[user];
    ips = os.popen("groovy -cp .:./scelib/* ./getSceInstances.groovy %s %s" % (user,secret))
    ipsArr=ips.read().split(",");
    return ipsArr

def connect(user,ip):
    cmd = "ssh %s@%s -i ./gitKeyRsa" % (user,ip)
    print "ready to login to %s@%s" % (user,ip)
    print cmd
    os.system(cmd)


readApps()
argLen = len(sys.argv)
if argLen == 1:
    for key in appKeys.keys():
        print key
if argLen == 2:
    appId = sys.argv[1]
    ips = getIps(appId)
    for ip in ips:
        print ip    
if argLen == 3:
    appId = sys.argv[1]
    ipOrNumberStr = sys.argv[2]
    if len(ipOrNumberStr)<=2:
        number = string.atoi(ipOrNumberStr)
        ips = getIps(appId)
        if len(ips)>=number and number>0:
            ip = ips[number-1]
            connect(appId,ip)
        else:
            print "number is wrong, this app only have %d instances, pls input the number in [1,%d]" %(len(ips),len(ips))
    else:
        connect(appId,ipOrNumberStr)

