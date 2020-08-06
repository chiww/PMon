#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Mongodb常量初始化

默认配置初始化
"""

from __future__ import print_function
from __future__ import absolute_import
import sys
import uuid
from pymongo import MongoClient

# 高危端口列表:    FROM: https://blog.csdn.net/duanchuanttao/article/details/91957105
RISK_PORT = ['20', '21', '22', '23', '25', '111', '2049', '135', '137', '139', '445', '161', '389', '512', '513', '514',
             '873', '1194', '1352', '1433', '1521', '2181', '3128', '2601', '2604', '3306', '3389', '3690', '4848',
             '5000', '5432', '5900', '5901', '5902', '5984', '6379', '7001', '7002', '8069', '8080', '8081', '8082',
             '8083', '8084', '8085', '8086', '8087', '8088', '8089', '9080', '9081', '9090', '9200', '9300', '11211',
             '27017', '27018', '50070', '50030']

# 高危服务
RISK_SERV = ['ssh', 'mysql', 'redis', 'mongodb', 'vnc']

# 默认识别主机存活的探测端口(适用Nmap)
DEFAULT_HOST_DISC_PORTS = ['21', '22', '23', '80', '135', '137', '139', '445', '3389', '8080', '6379', '27017', '2222']

# 默认全端口范围
DEFAULT_FULL_PORT = ['1-65535']

# 特别关注的高危端口
DEFAULT_RISK_PORT = ['21', '22', '23', '3306', '3389', '6379', '27017']


# 工具默认参数
TOOL_OPTIONS_TEMPLATE = {
    'nmap': {
        'HOST_DISC': '-sn -n --disable-arp-ping -PS{ports}',
        'PORT_DISC': '-Pn -n -p{ports}',
        'PORT_CHEK': '-Pn -n -p{ports}',
        'PORT_INFO': '-sV -n -p{ports}',
        'PORT_RISK': '-Pn -n -p{ports}'
    },
    'masscan': {
        # --rate Int:  扫描速率
        # --wait Int:  扫描完成后停止时间；默认10
        'PORT_DISC': '-Pn -n -p{ports}',
        'PORT_CHEK': '-Pn -n -p{ports}',
        'PORT_RISK': '-Pn -n -p{ports}'
    },
    'webcheck': {
        'WEB_CHECK': '-p{ports}'
    }
}


# 添加节点，"api"参数是指调用下发任务的api，指work的celery中的flower提供的下发api, "scope"指该节点扫描范围；
DEFAULT_NODE = [
    {'name': 'Local-01', 'status': 'enable', 'api': 'http://127.0.0.1:5555/api', 'scope': ['0.0.0.0/0']}
]

# 默认处理结果的后端，任务结束后，会通过这个接口将结果返回；
DEFAULT_BACKEND_URL = 'http://127.0.0.1:8001/admin/taskend'

# 默认执行的任务；指具体的任务内容及相关参数；
DEFAULT_JOBS = [
    {'name': 'COUNT_SNAPSHOT', 'func': 'pmon.jobs.count:snapshot', 'args': [], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'TASK_STATUS',    'func': 'pmon.jobs.task:status',    'args': [], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'NMAP_HOST_DISC', 'func': 'pmon.jobs.task:issue',     'args': ['NMAP_HOST_DISC', 'HOST_DISC', 'nmap', 'IP_ASSETS', TOOL_OPTIONS_TEMPLATE['nmap']['HOST_DISC'].format(ports=",".join(DEFAULT_HOST_DISC_PORTS)), 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'NMAP_PORT_DISC', 'func': 'pmon.jobs.task:issue',     'args': ['NMAP_PORT_DISC', 'PORT_DISC', 'nmap', 'IP_ONLINE', TOOL_OPTIONS_TEMPLATE['nmap']['PORT_DISC'].format(ports=",".join(DEFAULT_FULL_PORT)), 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'NMAP_PORT_CHEK', 'func': 'pmon.jobs.task:issue',     'args': ['NMAP_PORT_CHEK', 'PORT_CHEK', 'nmap', 'PORT_OPEN', TOOL_OPTIONS_TEMPLATE['nmap']['PORT_CHEK'], 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'NMAP_PORT_INFO', 'func': 'pmon.jobs.task:issue',     'args': ['NMAP_PORT_INFO', 'PORT_INFO', 'nmap', 'PORT_OPEN', TOOL_OPTIONS_TEMPLATE['nmap']['PORT_INFO'], 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'NMAP_PORT_RISK', 'func': 'pmon.jobs.task:issue',     'args': ['NMAP_PORT_RISK', 'PORT_RISK', 'nmap', 'IP_ONLINE', TOOL_OPTIONS_TEMPLATE['nmap']['PORT_RISK'].format(ports=",".join(DEFAULT_RISK_PORT)), 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'WEB_CHECK_FIND', 'func': 'pmon.jobs.task:issue',     'args': ['WEB_CHECK_FIND', 'WEB_CHECK', 'webcheck', 'PORT_OPEN', TOOL_OPTIONS_TEMPLATE['webcheck']['WEB_CHECK'], 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'MASSCAN_PORT_DISC', 'func': 'pmon.jobs.task:issue',     'args': ['MASSCAN_PORT_DISC', 'PORT_DISC', 'masscan', 'IP_ONLINE', TOOL_OPTIONS_TEMPLATE['masscan']['PORT_DISC'], 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'MASSCAN_PORT_CHEK', 'func': 'pmon.jobs.task:issue',     'args': ['MASSCAN_PORT_CHEK', 'PORT_CHEK', 'masscan', 'PORT_OPEN', TOOL_OPTIONS_TEMPLATE['masscan']['PORT_CHEK'], 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
    {'name': 'MASSCAN_PORT_RISK', 'func': 'pmon.jobs.task:issue',     'args': ['MASSCAN_PORT_RISK', 'PORT_RISK', 'masscan', 'IP_ONLINE', TOOL_OPTIONS_TEMPLATE['masscan']['PORT_RISK'], 'Local-01', DEFAULT_BACKEND_URL], 'kwargs': {}, 'remark': 'Default Job'},
]
# 说明：
# 此配置是由Scheduler后台调用使用的配置，就是说Scheduler后台在到底指定执行的时间时，会调用配置的"func"执行对应的操作，例如下发任务、统计计数。
# 参数说明：
# name: 任务名称，可自定义，一般是"执行任务函数(例如：nmap)" + "任务标签tag(例如：HOST_DISC)"
# func: 任务具体方法函数, 需要指定路径及函数; 例如："pmon.jobs.task:issue"，指的是 "pmon/jobs/task.py"下的"issue"方法函数；
# args: 是一个数组，是上述任务方法函数的参数，各字段含义如下，具体含义可到对应的方法函数下查看；"issue"方法函数很重要，请务必到该函数下查看具体说明！！
# kwargs: 同args
# mark: 备注
#
# 也可以自行添加func方法函数，只要路径相同即可；


# 默认触发器；就是定义任务的执行周期；
DEFAULT_TRIGGER_PARAM = [
    {'name': 'EVERY_10S', 'seconds': 10, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_30S', 'seconds': 30, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_10M', 'minutes': 10, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_30M', 'minutes': 30, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_60M', 'minutes': 60, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_2H', 'hours': 2, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_4H', 'hours': 4, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_8H', 'hours': 8, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_12H', 'hours': 12, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'},
    {'name': 'EVERY_24H', 'hours': 24, 'max_instances': 1, 'trigger': 'interval', 'remark': 'Default Trigger'}
]


# 默认调度器；就是定义任务的执行周期，其中"trigger_name"与"DEFAULT_TRIGGER_PARAM"对应，"job_name"与"DEFAULT_JOBS"对应；
# "status"指加载状态，默认是不加载，在页面"加载"会更改数据库对应字段的状态，在"LOADED"状态下，才会真正加载到调度器中；
# 简单理解，调度器 = 触发器 + 任务； "触发器"负责任务执行时间，"任务"负责在触发器到底预定时间后执行的具体任务；
DEFAULT_SCHEDULER = [
    {'trigger_name': 'EVERY_30M', 'job_name': 'COUNT_SNAPSHOT', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_30S', 'job_name': 'TASK_STATUS', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_2H', 'job_name': 'NMAP_HOST_DISC', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_2H', 'job_name': 'NMAP_PORT_DISC', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_30M', 'job_name': 'NMAP_PORT_CHEK', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_2H', 'job_name': 'NMAP_PORT_INFO', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_10M', 'job_name': 'NMAP_PORT_RISK', 'remark': 'Default Job', 'status': 'UNLOADED'},
    {'trigger_name': 'EVERY_2H', 'job_name': 'WEB_CHECK_FIND', 'remark': 'Default Job', 'status': 'UNLOADED'},
]


# --------------
#  写入方法
# --------------


def init_settings():
    collection = database['settings']
    collection.update_one({'name': 'risk_port'}, {'$set': {'value': RISK_PORT}}, upsert=True)
    print("Insert settings.risk_port success!")

    collection = database['settings']
    collection.update_one({'name': 'risk_serv'}, {'$set': {'value': RISK_SERV}}, upsert=True)
    print("Insert settings.risk_serv success!")


def init_schedule():

    collection = database['schedule']

    for item in DEFAULT_JOBS:
        collection.update_one({'type': 'job', 'name': item['name']}, {
            '$set': item,
            '$setOnInsert': {'uuid': str(uuid.uuid1())}
        }, upsert=True)
        print("Insert schedule.job [%s] success!" % item['name'])

    for item in DEFAULT_TRIGGER_PARAM:
        collection.update_one({'type': 'trigger', 'name': item['name']}, {
            '$set': item,
            '$setOnInsert': {'uuid': str(uuid.uuid1())}
        }, upsert=True)
        print("Insert schedule.trigger [%s] success!" % item['name'])

    for item in DEFAULT_SCHEDULER:
        item['name'] = "{job}[{trigger}]".format(job=item['job_name'], trigger=item['trigger_name'])
        collection.update_one({'type': 'schedule', 'name': item['name']}, {
            '$set': item,
            '$setOnInsert': {'uuid': str(uuid.uuid1())}
        }, upsert=True)
        print("Insert schedule.scheduler [%s] success!" % item['name'])


def init_node():

    collection = database['node']
    for item in DEFAULT_NODE:
        collection.update_one({'name': item['name']}, {
            '$set': item,
            '$setOnInsert': {'uuid': str(uuid.uuid1())}
        }, upsert=True)
        print("Insert node [%s] success!" % item['name'])


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Error! Please input mongodb URI! \n"
              "> python initialize.py mongodb://127.0.0.1:27017")
        sys.exit()
        
    mongodb_uri = sys.argv[1]
    client = MongoClient(mongodb_uri)
    database = client['pmon']

    init_settings()
    init_schedule()
    init_node()

    print("Done!")

