#!/usr/bin/python
# -*- coding: utf-8 -*-

import sshTool
import string,sys,commands,time,os

"""
为了在线上出问题时，能快速的，全局的看到各个实例中，有哪些异常或错误，以及每种异常错误的发生次数，写了这个脚本。
它有2种模式：
1）一种是根据某个appid，每个实例的最近xx行（比如500）的日志(/opt/logs/stdout_$appId.log)，去分析其中各种exception或error的出错次数
2）另外一种模式，是看最近x分钟（比如5分钟）的日志中，分析各种exception和error的出错次数
2种模式使用的命令分别如下，请谨慎使用行数，和分钟数，不要太大，以免对线上服务器的io造成较大影响

./errorQuickOverview.py 10237 line 500
./errorQuickOverview.py 10237 min 5
"""

def printAllLog(appId,mode,number):
    ips = sshTool.getIps(appId)
    count = 0
    
    filename = "/tmp/%s.%s.%d.%d.log"%(appId,mode,number,int(time.time()))
    fh = open(filename,'w')
    for ip in ips:
        count = count+1
        cmd = "scp logScanner.py %s@%s:/tmp/;ssh %s@%s /tmp/logScanner.py /opt/logs/stdout_%s.log %s %d" % (appId,ip,appId,ip,appId,mode,number)
        out = commands.getoutput(cmd)
        outAll = "%d. ip:%s, error infos:\n===============================\n%s===============================\n" % (count,ip,out)
        fh.write(outAll)
    print "log has written to %s" %(filename,)
    fh.close()

if __name__=='__main__':
    appId = sys.argv[1]
    mode = sys.argv[2]
    number = string.atoi(sys.argv[3])
    printAllLog(appId,mode,number)    
