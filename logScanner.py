#!/usr/bin/python
# -*- coding: utf-8 -*-


import re,time,string,datetime
import commands,sys

javaExceptionLineReg = r"\s+at\s+(\w+\.)+.+\("
timeReg = r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"
errorExceptionFirstLineReg = timeReg + r".+(error|exception)"
lineMax = 6
averageLinesPerMinute = 500

def isRegTrue(reg,src):
    m = re.compile(reg,re.I).search(src)
    if m:
        return True
    else:
        return False

def find1st(reg,src):
    m = re.compile(reg,re.I).findall(src)
    if len(m)>0:
        return m[0]
    return None
def getTailLines2List(filename,linesNum):
    return commands.getoutput("tail -%d %s" %(linesNum,filename)).split("\n")
def getTailMinutes2List(filename,minutes):
    lines = commands.getoutput("tail -%d %s|grep 201[4,5]-" %(averageLinesPerMinute,filename)).split("\n")
    times = get2TimestampFromList(lines)
    deltaMinutes = (int)((times[1]-times[0])/60)
    if deltaMinutes==0:
        deltaMinutes = 1
    expectLines = (int)(averageLinesPerMinute * minutes * 1.5/ deltaMinutes)
    expectTime = datetime.datetime.fromtimestamp(times[1])-datetime.timedelta(seconds=minutes*60)
    expectTimestamp = time.mktime(expectTime.timetuple())
    while 1:
        lines = commands.getoutput("tail -%d %s|grep 201[4,5]-" %(expectLines,filename)).split("\n")
        times = get2TimestampFromList(lines)
        if times[0]<=expectTimestamp:
            break
        expectLines = expectLines*2
    lines = getTailLines2List(filename,expectLines)
    newlines = []
    isNewlineBegin = False
    for line in lines:
        timestr = find1st(timeReg,line)
        #可能有问题，强行认为[framework]开头的才算是符合要求的line
        if not line.startswith("[framework]"):
            timestr = None
        if not isNewlineBegin and timestr!=None and getFloatTimeFromStr(timestr) >= expectTimestamp:
            isNewlineBegin = True
        if isNewlineBegin:
            newlines.append(line)
    return newlines;
    
def get2TimestampFromList(lines):
    if len(lines)==0:
        return None
    ll = []
    lastLine = lines[len(lines)-1]
    firstLine = lines[0]
    ll.append(getFloatTimeFromStr(find1st(timeReg,firstLine)))
    ll.append(getFloatTimeFromStr(find1st(timeReg,lastLine)))
    return ll
def getFloatTimeFromStr(timeStr):
    return time.mktime(time.strptime(timeStr,"%Y-%m-%d %H:%M:%S"))

def md5(str):
    str = str.replace("\n",",")
    cmd = "echo -n \"%s\"|md5sum|cut -d ' ' -f1" % (str,)
    return commands.getoutput(cmd)

def trimNumbers(str):
    if str==None:
        return str
    for i in range(0,10):
        str = str.replace("%d"%i,"")
    return str
def getLineStatus(line):
    if line==None or len(line)==0:
        return "other"
    if isRegTrue(errorExceptionFirstLineReg,line):
        return "errorExceptionBegin"
    if isRegTrue(javaExceptionLineReg,line):
        return "javaException"
    return "other"


def stats(lines):
    statsRe = {}
    sampleRe = {}
    if lines==None or len(lines)==0:
        return statsRe
    lineCollect = ""
    lineCount = 0
    for line in lines:
        lineStatus = getLineStatus(line)
        if lineStatus=="errorExceptionBegin":
            if lineCount>0:
                digestKey = md5(trimNumbers(lineCollect))
                if statsRe.has_key(digestKey):
                    statsRe[digestKey] = statsRe[digestKey]+1
                else:
                    statsRe[digestKey] = 1
                    sampleRe[digestKey] = lineCollect
                lineCollect = ""
                lineCount = 0
            lineCount = lineCount+1
            lineCollect = lineCollect+"\n"+line
        else:
            if lineCount>0:
                if line.startswith("[framework]"):
                    continue;
                lineCount = lineCount+1
                lineCollect =  lineCollect+"\n"+line
                if lineCount>=lineMax:
                    digestKey = md5(trimNumbers(lineCollect))
                    if statsRe.has_key(digestKey):
                        statsRe[digestKey] = statsRe[digestKey]+1
                    else:
                        statsRe[digestKey] = 1
                        sampleRe[digestKey] = lineCollect
                    lineCollect = ""
                    lineCount = 0
    return (statsRe,sampleRe)

def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]


def printStatsRe(reTuple):
    statsRe = reTuple[0]
    sampleRe = reTuple[1]
    statsReList = sort_by_value(statsRe)
    count = 1
    for k in statsReList:
        print "%d. occur times:%d\t\tsample lines:\n{{{{{{{{{{{{{{{%s\n}}}}}}}}}}}}}}}\n\n" % (count,statsRe[k],sampleRe[k])
        count = count + 1


if __name__=='__main__':
    filename = sys.argv[1]
    mode = sys.argv[2]
    number = string.atoi(sys.argv[3])
    lines = None
    if mode=="line":
        lines = getTailLines2List(filename,number)
    if mode=="min":
        lines = getTailMinutes2List(filename,number)
    printStatsRe(stats(lines))

