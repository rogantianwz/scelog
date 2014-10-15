#!/bin/sh

appId=$1
echo "check...$1====>"
for ip in `./sshTool.py $appId`; do echo $ip:;curl http://$ip/health/check;echo ""; done
