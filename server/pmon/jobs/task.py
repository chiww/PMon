#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
task相关定时执行任务

"""

from __future__ import print_function
from __future__ import absolute_import
import logging
import time
from datetime import datetime
from collections import defaultdict
from pmon.mongo import mongo
from pmon.nodes import Nodes
from pmon.work import Work

from pymongo import MongoClient

logger = logging.getLogger('apscheduler')


def status():

    update_field_state = ['started', 'succeeded', 'received', 'succeeded', 'revoked', 'retried']
    update_field_other = ['state', 'args', 'kwargs', 'timestamp', 'worker', 'name', 'traceback', 'runtime', 'exception']

    task_dataset = defaultdict(list)
    for _task in mongo.db.task.find({
        'state': {'$not': {'$in': ['SUCCESS', 'FAILURE']}}
    }):
        task_dataset[_task['node']['name']].append(_task['task-id'])

    for _node_name, _task_ids in task_dataset.items():
        node = Nodes().get_node(_node_name)
        task_ag = Work(node['api'])
        response = task_ag.fetch_info(_task_ids)

        msg = ''
        if response['success']:
            for _data in response['data']:
                up_item = dict()
                if _data['state'] in ['SUCCESS']:
                    msg = 'succeeded time: %s  runtime %s' % (str(_data['succeeded']), str(_data['runtime']))

                    res = task_ag.task_result(_data['uuid'])
                    if not res['success']:
                        continue
                    else:
                        up_item['result'] = res['data']

                elif _data['state'] in ['FAILURE']:
                    msg = _data['traceback']

                up_item['message'] = msg
                for field in update_field_state:
                    if _data.get(field):
                        up_item[field] = int(_data[field])
                for field in update_field_other:
                    if _data.get(field):
                        up_item[field] = _data[field]

                mongo.db.task.update_one({'task-id': _data['uuid']}, {'$set': up_item})

        else:
            logger.error("Get node[%s] task status failed!" % _node_name)


def issue(name, tag, tool, target, options, node_name, backend, sleep=3):
    """
    任务下发

    tag: 任务标签
    tool: 执行扫描工具; nmap|masscan|web
    target: 扫描任务目标，即IP地址段或IP地址；
    options: 扫描工具的参数，例如nmap、masscan参数；
    node_name: 扫描任务的节点名；此节点名要已经在数据库中的；
    backend: 任务完成后返回结果的API

    ！！！注意！！！
    tag参数与 pmon/backend 强绑定，只能是以下四种：
        PORT_CHEK：端口更新，指已经发现的端口，对已知端口的状态更新
        PORT_DISC：端口扫描，发现未知端口；
        PORT_INFO：端口指纹识别，通过nmap实现；
        HOST_DISC：主机存活探测；
        PORT_RISK：高危端口探测
        WEB_CHECK: 高危后台页面检测
    几种类型在处理结果不太相同；


    也可以自定义tag，设置是backend，不过需要自己实现相关处理方法；

    """

    nodes = Nodes()

    param = dict()
    param['name'] = name + "-" + datetime.strftime(datetime.now(), '%Y%m%d%H%M')
    param['tag'] = tag
    param['backend'] = backend
    param['tool'] = tool

    collection = mongo.db.task

    func = 'work.celery.' + tool

    def get_node():
        if node_name == 'AUTO':
            _node = nodes.select_best_node()
        else:
            _node = nodes.get_node(node_name)
        if _node:
            return _node
        else:
            raise Exception("Can not find node[%s] in db, please check!" % node_name)

    def is_task_running(tl, addr, opt):

        if collection.find_one({'param.address': addr,
                                'param.tool': tl,
                                'param.options': opt,
                                'state': {'$not': {'$in': ['SUCCESS', 'FAILURE']}}}):
            return True
        else:
            return False

    try:
        node = get_node()
        client = Work(node['api'])
    except Exception as e:
        raise Exception("Init client error %s" % str(e))

    for item in generate_address_options(target, options):

        param['address'] = item['address']
        param['options'] = item['options']
        try:
            if is_task_running(tool, item['address'], item['options']):
                continue
            res = client.async_apply(func, tag, item['address'], item['options'], backend)
        except Exception as e:
            raise Exception("issue > %s" % str(e))
        res['data']['param'] = param
        res['data']['node'] = node
        if res['success']:
            collection.update_one({'task-id': res['data']['task-id']}, {'$set': res['data']}, upsert=True)
        else:
            logger.error('task_issue error node: %s  param: %s' % (str(node['name']), str(param)))

        time.sleep(sleep)


def generate_address_options(target, options):

    def target_ip_assets(q, opt):
        collection = database.ipassets
        _data = list()
        for item in collection.find(q):
            _data.append({'address': item['address'], 'options': opt})
        return _data

    def target_ip_set(q, opt):
        collection = database.ipset
        _data = list()
        for item in collection.find(q):
            _data.append({'address': item['ip'], 'options': opt})
        return _data

    def target_port_state(q, opt):
        collection = database.port
        _data = list()
        for item in collection.aggregate(
                [{'$match': q}, {'$group': {'_id': '$ip', 'ports': {'$push': '$port'}}}]):
            if '{ports}' in opt:
                _opt = opt.format(ports=",".join(item['ports']))
            else:
                _opt = opt
            _data.append({'address': item['_id'], 'options': _opt})
        return _data

    database = mongo.db

    try:
        query = {
            'IP_ASSETS': {},
            'IP_ONLINE': {'status': 'UP'},
            'IP_OFFLINE': {'status': 'DOWN'},
            'PORT_OPEN': {'status': 'OPEN'},
            'PORT_DOWN': {'status': 'CLOSE'}
        }[target]

        func = {
            'IP_ASSETS': target_ip_assets,
            'IP_ONLINE': target_ip_set,
            'IP_OFFLINE': target_ip_set,
            'PORT_OPEN': target_port_state,
            'PORT_DOWN': target_port_state
        }[target]

        return func(query, options)

    except KeyError as e:
        logger.info("target: [%s] is not define by system." % str(e))
        return [{'address': target, 'options': options}]
