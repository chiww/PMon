#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
统计计数

"""
from __future__ import print_function
from __future__ import absolute_import

import logging
import time
from datetime import datetime, timedelta
import ipaddress
from pmon.mongo import mongo
from bson.objectid import ObjectId

logger = logging.getLogger('apscheduler')


def snapshot():
    """
    定时快照数值
    :return:
    """
    data = count_summary()
    mongo.db.snapshot.insert(data)


def count_summary():

    begin_before_24hours_time = datetime.utcnow() - timedelta(hours=24)

    data = {
        'ipassets': count_ip_assets(),
        'ipset': count_ip_set(),
        'open_port': count_open_port(),
        'risk_port': count_risk_port(),
        'risk_serv': count_risk_serv(),
        'unreported': count_unreported_port(),
        'timestamp': int(time.time())
    }

    data.update(count_task_state(begin_before_24hours_time))

    return data


def risk_port_list():
    risk_port_settings = mongo.db.settings.find_one({'name': 'risk_port'})
    if risk_port_settings:
        risk_port = risk_port_settings['value']
    else:
        risk_port = list()
    return risk_port


def risk_serv_list():
    risk_serv_settings = mongo.db.settings.find_one({'name': 'risk_serv'})
    if risk_serv_settings:
        risk_serv = risk_serv_settings['value']
    else:
        risk_serv = list()
    return risk_serv


def count_ip_assets():

    count = 0
    try:
        __address = list(mongo.db.ipassets.aggregate([{
            '$group': {'_id': 'address', 'address': {'$addToSet': '$address'}}}]))[0]['address']
    except Exception as e:
        __address = []

    for addr in __address:
        if not isinstance(addr, str):
            addr = addr.decode('utf-8')
        ct = len(list(ipaddress.IPv4Network(addr, strict=False).hosts()))
        if ct != 0:
            count += ct
        else:
            count += 1
    return count


def count_ip_set():
    count = mongo.db.ipset.count({'status': 'UP'})
    return count


def count_open_port():
    count = mongo.db.port.count({'status': 'OPEN'})
    return count


def count_risk_port():
    count = mongo.db.port.count({'status': 'OPEN', 'port': {'$in': risk_port_list()}})
    return count


def count_risk_serv():
    count = mongo.db.port.count({'status': 'OPEN', 'detail.name': {'$in': risk_serv_list()}})
    return count


def count_unreported_port():
    count = mongo.db.port.count({'status': 'OPEN', 'ticket_info.status': 'UNREPORTED'})
    return count


def count_task_state(begin_time, end_time=None):
    query_body = dict()
    query_body['_id'] = dict()
    query_body['_id']['$gte'] = ObjectId.from_datetime(begin_time)
    if end_time:
        query_body['_id']['$lte'] = ObjectId.from_datetime(end_time)

    _data = dict()
    _data['task_failure'] = 0
    _data['task_success'] = 0
    _data['task_total'] = 0
    for item in mongo.db.task.aggregate([{'$group': {'_id': '$state', 'count': {'$sum': 1}}}]):
        if item['_id'] == 'FAILURE':
            _data['task_failure'] = item['count']
        if item['_id'] == 'SUCCESS':
            _data['task_success'] = item['count']

    _data['task_total'] = _data.get('task_failure', 0) + _data.get('task_success', 0)

    return _data





