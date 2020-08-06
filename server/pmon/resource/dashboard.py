#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
首页面板

"""

from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime, timedelta
from copy import deepcopy
from time import mktime
from pmon.mongo import mongo
from pmon.jobs.count import count_summary, risk_port_list, risk_serv_list
from .base import BaseResource


class Dashboard(BaseResource):

    def get(self):

        self.collection = mongo.db.snapshot

        code = 20000
        data = dict()
        data['count'] = count_summary()
        data['history'] = summary_history(self.collection)
        data['risk'] = risk_bar(mongo.db.port)
        data['report_pie'] = report_pie(mongo.db.port),
        data['unreported_pie'] = unreported_pie(mongo.db.port, 10)

        return self.create_response(code, data)


class PanelCount(BaseResource):

    def get(self):
        code = 20000
        data = dict()
        data['count'] = count_summary()
        return self.create_response(code, data)


class HisLine(BaseResource):

    def get(self):

        self.collection = mongo.db.history
        code = 20000
        data = dict()
        data['history'] = summary_history(self.collection)
        return self.create_response(code, data)


class RiskBar(BaseResource):

    def get(self):

        self.collection = mongo.db.port
        code = 20000
        data = dict()
        data['risk'] = risk_bar(self.collection)
        return self.create_response(code, data)


class ReportPie(BaseResource):

    def get(self):

        self.collection = mongo.db.port
        code = 20000
        data = dict()
        data['report_pie'] = report_pie(self.collection)
        return self.create_response(code, data)


class UnreportedPie(BaseResource):

    def get(self):

        self.collection = mongo.db.port
        code = 20000
        data = dict()
        data['unreported_pie'] = unreported_pie(self.collection, 10)
        return self.create_response(code, data)


def summary_history(collection):
    # 获取历史数据
    __fields = ['ipassets', 'ipset', 'open_port', 'risk_port', 'risk_serv', 'unreported', 'timestamp',
                'task_total', 'task_success', 'task_failure']
    __history = {key: list() for key in __fields}

    for _h_item in collection.find({}, {'_id': 0}).sort([('timestamp', -1)]).limit(500):
        for key, value in _h_item.items():
            if key == 'timestamp':
                value = datetime.strftime(datetime.fromtimestamp(value), '%m-%d %H:%M')
            __history[key].append(value)

    return __history


def risk_bar(collection):
    n = 7
    # begin_before_7day_time = datetime.utcnow() - timedelta(days=7)
    begin_before_7day_time = datetime(2020, 3, 6, 0, 0) - timedelta(days=n)
    _data = dict()
    _data['date'] = [(datetime(2020, 3, 6, 0, 0) - timedelta(days=i)).strftime('%m-%d') for i in range(n)]

    agg_body = [
        {'$project': {
            'discover_date': {
                '$dateToString': {
                    'format': "%m-%d",
                    'date': {"$add": [datetime(1970, 1, 1, 0, 0), {"$multiply": ["$discover_time", 1000]}]}}},
            '_id': 0,
            'port': 1,
            'status': 1,
        }},
        {'$group': {'_id': '$discover_date', 'count': {'$sum': 1}}}
    ]

    open_port_match_body = {
        '$match': {
            'discover_time': {'$gt': int(mktime(begin_before_7day_time.utctimetuple()))},
            'status': 'OPEN'
        }}

    risk_port_match_body = {
        '$match': {
            'discover_time': {'$gt': int(mktime(begin_before_7day_time.utctimetuple()))},
            'status': 'OPEN',
            'port': {'$in': risk_port_list()}
        }}

    risk_serv_match_body = {
        '$match': {
            'discover_time': {'$gt': int(mktime(begin_before_7day_time.utctimetuple()))},
            'status': 'OPEN',
            'detail.name': {'$in': risk_serv_list()}
        }}

    for category, match_body in zip(
            ['open_port', 'risk_port', 'risk_serv'],
            [open_port_match_body, risk_port_match_body, risk_serv_match_body]):
        _agg_body = deepcopy(agg_body)
        _agg_body.insert(0, match_body)
        _data[category] = list()

        _d = dict()
        for item in collection.aggregate(_agg_body):
            _d[item['_id']] = item['count']

        for e in _data['date']:
            _data[category].append(_d.get(e, 0))

    return _data


def report_pie(collection):

    _d = dict()
    for item in collection.aggregate([{'$match': {'status': 'OPEN'}},
                                      {'$group': {'_id': '$ticket_info.status', 'count': {'$sum': 1}}}]):
        _d[item['_id']] = item['count']

    _data = dict()
    _data['legend'] = list()
    _data['data'] = list()
    for k, v in _d.items():
        _data['legend'].append(k.title())
        _data['data'].append({'value': v, 'name': k.title()})

    return _data


def unreported_pie(collection, display_count):
    _d = dict()
    for item in collection.aggregate([{'$match': {'ticket_info.status': 'UNREPORTED', 'status': 'OPEN'}},
                                      {'$group': {'_id': '$port', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}]):
        _d[item['_id']] = item['count']

    _data = dict()
    _data['legend'] = list()
    _data['data'] = list()

    _other = 0
    for k, v in _d.items():
        if len(_data['legend']) < display_count:
            _data['legend'].append(k)
            _data['data'].append({'value': v, 'name': k})
        else:
            _other += v
    if _other != 0:
        _data['data'].append({'value': _other, 'name': 'other'})
        _data['legend'].append('other')

    return _data