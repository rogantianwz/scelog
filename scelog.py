#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,time,sys,datetime

def printHelp():
    print "python scelog.py tail $appid  -- 实时查看log"
    print "python scelog.py help  -- 查看帮助"
    print "python scelog.py cp $appid  -- 把stdout_$ppid.log文件下载到当前目录下scelog_tmp文件夹中"
    print "python scelog.py cpy $appid  -- 把把实例上昨天的stdout日志文件下载到当前目录下scelog_tmp文件夹中"
    print "python scelog.py cpa $appid  -- 把把各实例上的access.log文件下载到当前目录下的scelog_access_tmp文件夹中"
    print "python scelog.py cpperf4j $appid  -- 将sce上的perfStats.log文件下载到当前目录下的scelog_tmp文件夹中"
    print "python scelog.py ip $appid  -- 查看各实例ip"
    print "python scelog.py login $appid  -- 登录到实例上"
    
argLen = len(sys.argv)
if argLen != 3:
    printHelp()
    sys.exit(-1)

appid=sys.argv[2]
action =sys.argv[1]

def copyLog():
    '''
    将sce上的stout_$appid.log文件下载到当前目录下的scelog_tmp文件夹中, 多个实例的文件用序号区分：0.log,1.log
    '''
    tmpDir = os.path.abspath(os.curdir) + "/scelog_tmp"
    logfile = "stdout_%s.log" % (appid)
    os.popen("mkdir scelog_tmp")
    #os.popen("touch %s/%s" % (tmpDir, logfile));
    for idx, ip in enumerate(ipsArr):
        localLog = "%s/%s.log" % (tmpDir, idx)
        os.popen("scp %s@%s:/opt/logs/stdout_%s.log %s" % (appid, ip, appid, localLog))
        #os.popen("cat %s >> %s" % (localLog, logfile))
        #os.popen("rm %s" % localLog)

def copyAccess():
    '''
    将sce上的stout_$appid.log文件下载到当前目录下的scelog_tmp文件夹中, 多个实例的文件用序号区分：0.log,1.log
    '''
    tmpDir = os.path.abspath(os.curdir) + "/scelog_access_tmp"
    logfile = "access_%s.log" % (appid)
    os.popen("mkdir scelog_access_tmp")
    #os.popen("touch %s/%s" % (tmpDir, logfile));
    for idx, ip in enumerate(ipsArr):
        localLog = "%s/%s.log" % (tmpDir, idx)
        os.popen("scp %s@%s:/opt/logs/access_%s.log %s" % (appid, ip, appid, localLog))
        #os.popen("cat %s >> %s" % (localLog, logfile))
        #os.popen("rm %s" % localLog)

def copyYesterdayLog():
    '''
    将sce上的stout_$appid.log文件下载到当前目录下的scelog_tmp文件夹中, 多个实例的文件用序号区分：0.log,1.log
    '''
    today = datetime.date.today();
    yesterday = "%s-%0.2d-%0.2d" % (today.year, today.month, today.day - 1)
    tmpDir = os.path.abspath(os.curdir) + "/scelog_tmp_%s" % yesterday
    os.popen("mkdir scelog_tmp_%s" % yesterday)
    for idx, ip in enumerate(ipsArr):
        localLog = "%s/%s.log" % (tmpDir, idx)
        os.popen("scp %s@%s:/opt/logs/stdout_%s.log.%s %s" % (appid, ip, appid, yesterday, localLog))

def tailLog():
    '''
    通过tail命令实时查看日志
    '''
    sessionName = "sce%s" % appid
    print 'sname', sessionName
    #while True:
    sessionCmd = "tmux new-session -s %s -n appwin -d" % sessionName
    splitWinCmd = "tmux splitw -h -t %s" % sessionName
    layoutCmd = "tmux select-layout -t %s even-horizontal" % sessionName
    os.popen(sessionCmd)
    print ipsArr
    for idx, ip in enumerate(ipsArr):
        if idx > 0:
            os.popen(splitWinCmd)
        cmd = "tail -f -n 100 /opt/logs/stdout_%s.log" % appid
        os.popen("tmux send-keys -t %s:appwin.%s 'ssh %s@%s %s' C-m" % (sessionName, idx, appid, ip, cmd))
    os.popen(layoutCmd)
    os.popen("tmux attach -t %s" % sessionName)

def login():
    '''
    登录到实例上
    '''
    sessionName = "sce%s" % appid
    print 'sname', sessionName
    #while True:
    sessionCmd = "tmux new-session -s %s -n appwin -d" % sessionName
    splitWinCmd = "tmux splitw -h -t %s" % sessionName
    layoutCmd = "tmux select-layout -t %s even-horizontal" % sessionName
    os.popen(sessionCmd)
    print ipsArr
    for idx, ip in enumerate(ipsArr):
        if idx > 0:
            os.popen(splitWinCmd)
        os.popen("tmux send-keys -t %s:0.%s 'ssh %s@%s ' C-m" % (sessionName, idx, appid, ip))
    os.popen(layoutCmd)
    os.popen("tmux attach -t %s" % sessionName)

def cdlog():
    '''
    登录到实例上
    '''
    sessionName = "sce%s" % appid
    print 'sname', sessionName
    #while True:
    sessionCmd = "tmux new-session -s %s -n appwin -d" % sessionName
    splitWinCmd = "tmux splitw -h -t %s" % sessionName
    layoutCmd = "tmux select-layout -t %s even-horizontal" % sessionName
    cmd = "cd /opt/logs"
    os.popen(sessionCmd)
    print ipsArr
    for idx, ip in enumerate(ipsArr):
        if idx > 0:
            os.popen(splitWinCmd)
        #cmd = "cd /opt/logs"
        os.popen("tmux send-keys -t %s:appwin.%s 'ssh %s@%s %s' C-m" % (sessionName, idx, appid, ip, cmd))
        #os.popen("tmux send-keys -t %s:0.%s '%s' C-m" % (sessionName, idx, cmd))
    os.popen(layoutCmd)
    os.popen("tmux attach -t %s" % sessionName)

def cpperf4j():
    '''
    将sce上的perfStats.log文件下载到当前目录下的scelog_tmp文件夹中
    '''
    tmpDir = os.path.abspath(os.curdir) + "/scelog_tmp"
    logfile = "stdout_%s.log" % (appid)
    os.popen("mkdir scelog_tmp")
    #os.popen("touch %s/%s" % (tmpDir, logfile));
    for idx, ip in enumerate(ipsArr):
        localLog = "%s/perfStats_%s.log" % (tmpDir, idx)
        os.popen("scp %s@%s:/opt/logs/perfStats.log %s" % (appid, ip, localLog))
        #os.popen("cat %s >> %s" % (localLog, logfile))
        #os.popen("rm %s" % localLog)

def ip():
    print '------------------------------------'
    for ip in ipsArr:
        print ip
    print '------------------------------------'

pwd = os.path.realpath(__file__)
pwd = os.path.dirname(pwd)
homedir = os.path.expanduser('~')
configDir = homedir + "/.sceapp"
appKeys = {}
def readApps():
    f = open(configDir + "/apps.conf","r")
    for line in f.readlines():
        line = line.strip()
        appKeys[line.split(",")[0]] = line.split(",")[1]
    f.close()

readApps();
sleepTime=0.5
showLastNLines=10

if appKeys.has_key(appid) == False:
    print "pls modify the file apps.conf,add \"appId,secretKey\" into it"
    sys.exit(-1)
secret = appKeys[appid];
ips = os.popen("groovy -cp .:%s/scelib/* %s/getSceInstances.groovy %s %s" % (pwd, pwd, appid,secret))
ipsArr=ips.read().split(",");

if action == 'cp':
    copyLog()
elif action == 'tail':
    tailLog()
elif action == 'cpy':
    copyYesterdayLog()
elif action == 'login':
    login()
elif action == 'cdlog':
    cdlog()
elif action =='ip':
    ip()
elif action == 'cpperf4j':
    cpperf4j()
elif action == 'cpa':
    copyAccess()
else:
    printHelp()
