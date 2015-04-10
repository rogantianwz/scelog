需要在home目录下添加发下文件.sceapp/apps.conf，内容格式如下，每一行对应一个应用配置：   
$app_id,$app_sceret


## 使用
```sh
python scelog.py tail $appid  -- 实时查看log
python scelog.py help  -- 查看帮助
python scelog.py cp $appid  -- 把stdout_$ppid.log文件下载到当前目录下scelog_tmp文件夹中
python scelog.py cpy $appid  -- 把把实例上昨天的stdout日志文件下载到当前目录下scelog_tmp文件夹中
python scelog.py cpa $appid  -- 把把各实例上的access.log文件下载到当前目录下的scelog_access_tmp文件夹中
python scelog.py cpperf4j $appid  -- 将sce上的perfStats.log文件下载到当前目录下的scelog_tmp文件夹中
python scelog.py ip $appid  -- 查看各实例ip
python scelog.py login $appid  -- 登录到实例上
```


可以设置alias scelog = "/path/to/scelog/scelog.py"后直接使用:`scelog tail $appid`的方式更简单