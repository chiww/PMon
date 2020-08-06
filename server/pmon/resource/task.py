#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
任务管理

"""

from __future__ import print_function
from __future__ import absolute_import
import json
from flask import request
from flask_restful import reqparse
from pmon.mongo import mongo

from pmon.work import Work
from .base import BaseResource


parser = reqparse.RequestParser()
parser.add_argument('task_name', type=str, location=['args', 'json'])
parser.add_argument('address', type=str, location=['args', 'json'])
parser.add_argument('task_id', type=str, location=['args', 'json'])
parser.add_argument('tag', type=str, location=['args', 'json'])
parser.add_argument('node', type=str, location=['args', 'json'])
parser.add_argument('state', type=str, location=['args', 'json'])
parser.add_argument('sort', type=str, location=['json'])
parser.add_argument('start_range[]', type=int, action='append', location=['args'])


class TaskIssue(BaseResource):
    """
    下发任务

    将下发的任务保存到数据库中
    """

    def post(self):

        # 注意，这里获取的请求的数据与其他不同
        args = json.loads(request.data)

        self.collection = mongo.db.task
        try:
            assert args.get('node', None), "Can not find [node name] in request!"
            node_name = args.pop('node')
            node = self.get_node(node_name)
            assert node, "Can not find [%s] in mongodb collection [node]!" % node_name
        except Exception as e:
            code = 40000
            data = {'message': str(e)}
            return self.create_response(code, data)

        try:
            task = Work(node)
            func = 'work.celery.' + args['tool']
            res = task.async_apply(func, args['tag'], args['address'], args['options'], args['backend_url'])

            res['data']['node'] = node_name
            res['data']['param'] = args
            if res['success']:
                code = 20000
                data = {'message': 'success'}
                self.collection.update_one({'task-id': res['data']['task-id']}, {'$set': res['data']}, upsert=True)
            else:
                code = 40000
                data = {'message': res['message']}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}

        return self.create_response(code, data)

    def get_node(self, name):

        return mongo.db.schedule.find_one({'type': 'node', 'name': name}, {'type': 0, '_id': 0})


class Tasks(BaseResource):
    """
    任务列表

    从数据库中获取各任务状态
    """

    def get(self):

        self.collection = mongo.db.task

        if self.action == 'options':
            return self.options([{
                '$group': {
                    '_id': 'options',
                    'tag': {'$addToSet': '$param.tag'},
                    'state': {'$addToSet': '$state'},
                    'node': {'$addToSet': '$node'},
                }}], {'tag': [], 'state': [], 'node': []})

        args = parser.parse_args()

        query_body = dict()
        for _key, _value in args.items():
            if _key == 'start_range[]' and _value:
                query_body['date_start'] = {'$gte': int(_value[0] / 1000), '$lte': int(_value[1] / 1000)}
            elif _key == 'tag' and _value:
                query_body['param.tag'] = _value
            elif _key == 'address' and _value:
                query_body['param.address'] = _value
            elif _value:
                query_body[_key] = _value
            else:
                continue

        try:
            dataset = list(self.collection.find(query_body, {'_id': 0}).sort([('date_start', -1)]).skip(self.skip).limit(self.limit))
            datalen = len(list(self.collection.find(query_body, {'_id': 0})))
            code = 20000
            data = {
                'total': datalen,
                'items': dataset
            }
        except Exception as e:
            code = 40000
            data = {'message': 'failed: [%s]' % str(e)}

        return self.create_response(code, data)


