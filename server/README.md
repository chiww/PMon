
# PMon - server 后台管理

## 0x 概述
PMon的后台管理


## 1x 主要功能：
1. 通过Web Api下给任务节点下发扫描任务；
2. 接收节点任务完成后的结果，并进行处理，按要求入库；
3. 为前端(PMon - admin)提供数据Api；
4. 提供定时任务执行模块，需要自行实现代码逻辑；


## 2x 部署
### .flaskenv
在`server`目录下创建flask环境变量文件
```
FLASK_ENV="development"
FLASK_APP="PMon"
MONGODB_HOST="127.0.0.1"
MONGODB_PORT="27017"
MONGODB_DATABASE="PMon"
```
如果是生产环境，将`FLASK_ENV`设置为`production`.
详细配置可查看`./pmon/settings`文件;


### 组件安装

#### 基础组件
```shell script
#yum install git python3-pip nginx
```

#### python 依赖
安装全局的管理依赖:
```shell script
#pip3 install supervisord pipenv gunicorn
```
使用pipenv管理python组件依赖
```shell script
#pip3 install pipenv
#pipenv install 
```

#### mongodb

1. 添加软件源
`/etc/yum.repos.d/mongodb-org-4.2.repo`

```
[mongodb-org-4.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
```
2. 安装
`#yum install mongodb-org`

### 下载代码
```shell script
git clone https://github.com/chiww/PMon.git
cd PMon/server
pipenv install
```

### 配置环境 
**以下配置参数仅供参考，请根据实际情况配置！！**

1. 配置supervisord进程守护:
```shell script
echo-supervisord-conf >> /etc/supervisord.conf
vim /etc/supervisord.conf
```
将以下配置写入配置文件：
**配置仅做参考。请修改成实际部署路径!! 注意路径"/YOU/DEPLOY/PATH/"**
```
[program:PMon-server]
command=pipenv run gunicorn -w 1 -b :8001 wsgi:app              ; the program (relative uses PATH, can take args)
;process_name=%(program_name)s ; process_name expr (default %(program_name)s)
numprocs=1                    ; number of processes copies to start (def 1)
directory=/YOU/DEPLOY/PATH/PMon/server                ; directory to cwd to before exec (def no cwd)
;umask=022                     ; umask for process (default None)
;priority=999                  ; the relative start priority (default 999)
autostart=true                ; start at supervisord start (default: true)
startsecs=1                   ; # of secs prog must stay up to be running (def. 1)
startretries=3                ; max # of serial start failures when starting (default 3)
autorestart=unexpected        ; when to restart if exited after running (def: unexpected)
exitcodes=0                   ; 'expected' exit codes used with autorestart (default 0)
stopsignal=QUIT               ; signal used to kill process (default TERM)
stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
stopasgroup=false             ; send stop signal to the UNIX process group (default false)
killasgroup=false             ; SIGKILL the UNIX process group (def false)
;user=chrism                   ; setuid to this UNIX account to run the program
redirect_stderr=true          ; redirect proc stderr to stdout (default false)
;stdout_logfile=/YOU/DEPLOY/PATH/PMon/server/log/gunicorn.log        ; stdout log path, NONE for none; default AUTO
;stdout_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stdout_logfile_backups=10     ; # of stdout logfile backups (0 means none, default 10)
;stdout_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stdout_events_enabled=false   ; emit events on stdout writes (default false)
;stdout_syslog=false           ; send stdout to syslog with process name (default false)
;stderr_logfile=/a/path        ; stderr log path, NONE for none; default AUTO
;stderr_logfile_maxbytes=1MB   ; max # logfile bytes b4 rotation (default 50MB)
;stderr_logfile_backups=10     ; # of stderr logfile backups (0 means none, default 10)
;stderr_capture_maxbytes=1MB   ; number of bytes in 'capturemode' (default 0)
;stderr_events_enabled=false   ; emit events on stderr writes (default false)
;stderr_syslog=false           ; send stderr to syslog with process name (default false)
;environment=A="1",B="2"       ; process environment additions (def no adds)
;serverurl=AUTO                ; override serverurl computation (childutils)
```
注意： 请使用"-w 1"单进程启动，否则sheduler的api会概率报404；原因是flask的上下文机制未处理好。


2. 使用nginx
参考配置如下：


## 使用注意事项！！

1. 部署完成后，请优先查看"pmon/initialize.py"文件。

该文件是初始化配置脚本，默认的配置会在此脚本配置并写入mongodb。理解里面每个参数的含义可以让你加快理解整个系统的组成及运行方式。

在使用之前一定要执行一遍脚本。

**请一定要看一遍！！里面已尽可能做好注释的了。**

2. 使用该系统需要使用者有一定python脚本知识，并且了解scheduler和celery相关组件的调用方法。

## 系统启动关键流程

1. supervisor启动，加载配置，通过gunicorn启动flask;
2. flask启动后，通过`register_extensions`方法注册插件，包括`server`端api(flask_restful); (详见`pmon/__init__.py`)
3. `scheduler_init`方法会启用scheduler服务，启动后默认无任务；需要在"任务面板 >> 任务配置 >> 调度器"中加载调度任务，只有加载后才能在"任务面板 >> 后台任务"中找到待执行的任务；
4. scheduler中的任务会通过`pmon/jobs/task.py`下发具体任务参数到`work`端；
5. `work`端api接收到任务后，启动任务，完成后将任务结果返回给`server`， `server`对数据进行处理并入库；


## 自定义扫描任务

当前整个系统都是默认的

## 附录
### Apscheduler触发器

interval
```
weeks (int) – 间隔几周 
days (int) – 间隔几天 
hours (int) – 间隔几小时 
minutes (int) – 间隔几分钟 
seconds (int) – 间隔多少秒 
start_date (datetime|str) – 开始日期 
end_date (datetime|str) – 结束日期 
timezone (datetime.tzinfo|str) – 时区 
```

crontab
``` 
year (int|str) – 年，4位数字 
month (int|str) – 月 (范围1-12) 
day (int|str) – 日 (范围1-31) 
week (int|str) – 周 (范围1-53) 
day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun) 
hour (int|str) – 时 (范围0-23) 
minute (int|str) – 分 (范围0-59) 
second (int|str) – 秒 (范围0-59) 
start_date (datetime|str) – 最早开始日期(包含) 
end_date (datetime|str) – 最晚结束时间(包含) 
timezone (datetime.tzinfo|str) – 指定时区 
```