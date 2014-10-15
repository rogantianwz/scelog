#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,time,sys
import sshTool
# this script is used to curl a url(get/post) in all instances of one sce app

def help():
    print "readonlyMode:"
    print "./batchCurl.py 10258 path1/controller1?para1=v1&para2=v2 get/post"
    print "doitMode:"
    print "./batchCurl.py 10258 path1/controller1?para1=v1&para2=v2 get/post doit"
    sys.exit(0)
cmd="curl %s http://%s/%s"
argLen=len(sys.argv)
if argLen<3 or argLen>4:
    help()
appId=sys.argv[1]
url=sys.argv[2]
getPost=sys.argv[3]
mode="readonly"
if argLen==5 and sys.argv[4]=="doit":
    mode="doit"
if getPost!="get" and getPost!="post":
    help()
if getPost=="get":
   getPost = ""
if getPost=="post":
   getPost = "-d \"1=1\""
ips=sshTool.getIps(appId)
for ip in ips:
    curlCmd= cmd % (getPost,ip,url)
    print curlCmd
    if mode=="doit":
        os.system(curlCmd)

print "done!"






