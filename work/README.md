PMon - Work
--------------------------
异步任务执行Agent


## 1x 主要功能：
1. 执行Web Api下发扫描任务；
2. 支持以下扫描方式:
    - socket connect扫描
    - nmap扫描
    - masscan扫描
    - Web后台发现 
    - 基于Nmap的Banner识别
3. 可自定义扫描参数；
4. 可选择返回的字段，可指定结果发送到特定的节点服务器；

## 2x 组件实现
### 组件
- celery: 分布式任务调度
- flower: celery的监控、调度组件；

### 任务
现已实现`nmap` `masscan` `webcheck`个扫描器任务；

### 部署(以CentOS示例)
1. 下载代码
    ```shell script
    git clone https://github.com/chiww/PMon.git  
    ```
2. 下载pipenv，支持pipenv环境部署
    ```shell script
    cd PMon/work
    pip install pipenv
    ```
3. 部署pipenv环境
    ```shell script
    cd PMon/work
    pipenv install
    ```
4. 安装redis，并启动
    ```shell script
    yum install redis-server
    service redis start
    ```
5. celery分布式任务
    ```shell script
    celery -A work.celery worker -l INFO -P threads -E 
    ```
6. celery flower 监控
    ```shell script
    celery -A work.celery flower --port=5555
    ```

7. 编译安装masscan
    ```shell script
    yum install gcc make libpcap libpcap-devel
    git clone https://github.com/robertdavidgraham/masscan.git
    cd masscan
    make
    cp ./bin/masscan /YOU/DEPLOY/PATH/PMon/work/bin
    ```
8. 安装nmap
    ```shell script
    yum install nmap
    ```
   
9. 安装supervisor
    ```shell script
    pip3 install supervisor
    echo_supervisord_conf > /etc/supervisord.conf
    ```

    supervisord.conf配置参考：
```
[program:PMon-work-Worker]
command=pipenv run celery -A work.celery worker -l INFO -P threads -E              ; the program (relative uses PATH, can take args)
;process_name=%(program_name)s ; process_name expr (default %(program_name)s)
numprocs=1                    ; number of processes copies to start (def 1)
directory=/YOU/DEPLOY/PATH/PMon/work                ; directory to cwd to before exec (def no cwd)
;umask=022                     ; umask for process (default None)
;priority=999                  ; the relative start priority (default 999)
autostart=true                ; start at supervisord start (default: true)
;startsecs=1                   ; # of secs prog must stay up to be running (def. 1)
;startretries=3                ; max # of serial start failures when starting (default 3)
;autorestart=unexpected        ; when to restart if exited after running (def: unexpected)
;exitcodes=0                   ; 'expected' exit codes used with autorestart (default 0)
;stopsignal=QUIT               ; signal used to kill process (default TERM)
;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
;stopasgroup=false             ; send stop signal to the UNIX process group (default false)
;killasgroup=false             ; SIGKILL the UNIX process group (def false)
;user=chrism                   ; setuid to this UNIX account to run the program
;redirect_stderr=true          ; redirect proc stderr to stdout (default false)
;stdout_logfile=/a/path        ; stdout log path, NONE for none; default AUTO
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

[program:PMon-work-Flower]
command=pipenv run celery -A work.celery flower --port=5555              ; the program (relative uses PATH, can take args)
;process_name=%(program_name)s ; process_name expr (default %(program_name)s)
numprocs=1                    ; number of processes copies to start (def 1)
directory=/YOU/DEPLOY/PATH/PMon/work                  ; directory to cwd to before exec (def no cwd)
;umask=022                     ; umask for process (default None)
;priority=999                  ; the relative start priority (default 999)
autostart=true                ; start at supervisord start (default: true)
;startsecs=1                   ; # of secs prog must stay up to be running (def. 1)
;startretries=3                ; max # of serial start failures when starting (default 3)
;autorestart=unexpected        ; when to restart if exited after running (def: unexpected)
;exitcodes=0                   ; 'expected' exit codes used with autorestart (default 0)
;stopsignal=QUIT               ; signal used to kill process (default TERM)
;stopwaitsecs=10               ; max num secs to wait b4 SIGKILL (default 10)
;stopasgroup=false             ; send stop signal to the UNIX process group (default false)
;killasgroup=false             ; SIGKILL the UNIX process group (def false)
;user=chrism                   ; setuid to this UNIX account to run the program
;redirect_stderr=true          ; redirect proc stderr to stdout (default false)
;stdout_logfile=/a/path        ; stdout log path, NONE for none; default AUTO
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


### 任务下发
下发样例：
```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
扫描测试，模拟客户端发送扫描任务
"""

from __future__ import print_function
from __future__ import absolute_import
import pprint
import requests
import json

api = "http://localhost:5555/api"
func = 'work.celery.nmap'
uri = '/task/async-apply/'

data = {'args': ['HOST_DISC', '10.0.0.1', '-p22,80', 'http://localhost:5001/admin/taskend']}
pprint.pprint(requests.post(url=api + uri + func, data=json.dumps(data)).json())
```
响应：
```
{u'state': u'PENDING', u'task-id': u'7d05bfb9-b2aa-4cdd-83f2-e558db10caaf'}
```
关于API使用，参见`flower`官方文档: https://flower.readthedocs.io/en/latest/api.html

注意：也可是使用`flower`的api查看任务执行状态，直接在浏览器中输入"http://FLOWER_IP:5555"即可。



### 任务状态

任务状态通过`flower`api实现:
```
(work) ➜  work curl "http://localhost:5555/api/task/info/7d05bfb9-b2aa-4cdd-83f2-e558db10caaf"
{"root_id": "7d05bfb9-b2aa-4cdd-83f2-e558db10caaf", "result": "{'timestamp': 1582288939, 'tag': 'HOST_DISC', 'result': [{'status': 'up', 'service': [...], 'timestamp': 1582288939, 'address': '10.0.0.1', 'close': [...], 'open': [...]}], 'task_id': '7d05bfb9-b2aa-4cdd-83f2-e558db10caaf'}", "children": [], "uuid": "7d05bfb9-b2aa-4cdd-83f2-e558db10caaf", "clock": 905, "exchange": null, "routing_key": null, "failed": null, "state": "SUCCESS", "client": null, "parent_id": null, "kwargs": "{}", "sent": null, "expires": null, "parent": null, "retries": 0, "started": 1582288939.690995, "timestamp": 1582288939.776921, "args": "['HOST_DISC', '10.0.0.1', '-p22,80', 'http://localhost:5001/monitor-admin/taskend']", "worker": "celery@chiweiweis-Mini", "rejected": null, "name": "work.celery.nmap", "received": 1582288939.689871, "exception": null, "revoked": null, "succeeded": 1582288939.776921, "traceback": null, "eta": null, "retried": null, "runtime": 0.08524997299537063, "root": "7d05bfb9-b2aa-4cdd-83f2-e558db10caaf"}%   
```
关于API使用，参见`flower`官方文档: https://flower.readthedocs.io/en/latest/api.html

详细状态:

|状态   |说明    | 备注   |
|:-----|:-------|:------|
|PENDING|The task is waiting for execution.|
|STARTED|The task has been started.|Celery|
|RETRY|The task is to be retried, possibly because of failure.|Celery|
|FAILURE|The task raised an exception, or has exceeded the retry limit. The result attribute then contains the exception raised by the task.|Celery|
|SUCCESS|The task executed successfully. The result attribute then contains the tasks return value.|Celery|
|PROGRESS|任务进行中,显示任务进度,进度保存在`data.result.percent`字段中|自定义状态，该功能已实现，但未读取|

### 任务结果
任务结果通过`flower`api实现：
```
(work) ➜  work curl "http://localhost:5555/api/task/result/7d05bfb9-b2aa-4cdd-83f2-e558db10caaf"
{"task-id": "7d05bfb9-b2aa-4cdd-83f2-e558db10caaf", "state": "SUCCESS", "result": {"timestamp": 1582288939, "tag": "HOST_DISC", "result": [{"status": "up", "service": [{"name": "ssh", "method": "table", "cpelist": [], "conf": "3", "banner": "", "port": "22"}, {"name": "http", "method": "table", "cpelist": [], "conf": "3", "banner": "", "port": "80"}], "timestamp": 1582288939, "address": "10.0.0.1", "close": [], "open": ["80"]}], "task_id": "7d05bfb9-b2aa-4cdd-83f2-e558db10caaf"}}% 
```


任务执行结果会首先通过`backend_url`将结果POST回目标服务器，其次，也会在本地保留一天;

```
{u'date_done': u'2020-02-06T13:37:53.271201',
 u'result': [{u'address': u'10.0.0.102',
              u'close': [],
              u'open': [u'22'],
              u'service': {},
              u'status': u'up',
              u'timestamp': 1580996273},
             {u'address': u'10.0.0.97',
              u'close': [],
              u'open': [u'80', u'22'],
              u'service': {},
              u'status': u'up',
              u'timestamp': 1580996273},
             {u'address': u'10.0.0.1',
              u'close': [],
              u'open': [u'80'],
              u'service': {},
              u'status': u'up',
              u'timestamp': 1580996273},
             {u'address': u'10.0.0.55',
              u'close': [],
              u'open': [u'80'],
              u'service': {},
              u'status': u'up',
              u'timestamp': 1580996273}],
 u'status': u'SUCCESS',
 u'tag': u'PORT_SCAN',
 u'task_id': u'f556c66d-6c89-42db-9f6f-6320cd49a841'}
```
扫描结果可以通过POST方式推送backend中的URL;



### Socket Connect 扫描
使用python标准库中的socket实现的简单的TCP连接，为了能够快速检测端口是否开放；

#### 参数(options)
    -p 指定扫描端口


### Nmap扫描
使用`python-libnmap`包实现的nmap扫描；该包是nmap的封装，底层仍是nmap；

#### 参数(options)
与nmap参数兼容(详见Nmap官方文档)，但部分设置输出的参数会被屏蔽;

### Masscan扫描
注意：需要自编译Masscan，并放置`work/bin`路径下；
参考`python-libnmap`，重新封装了masscan调用，基本使用方法与Nmap扫描一直，扫描参数同样参考官方文档;

#### 参数(options)
与nmap参数兼容(详见Nmap官方文档)，但部分设置输出的参数会被屏蔽;


