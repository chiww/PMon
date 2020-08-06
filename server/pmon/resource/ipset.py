#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
存活IP

"""

from __future__ import print_function
from __future__ import absolute_import
from flask_restful import reqparse, inputs
from pmon.mongo import mongo

from .base import BaseResource

parser = reqparse.RequestParser()
parser.add_argument('ip', type=inputs.regex(r'[\d.\\]{7,18}'), location=['args', 'json'])
parser.add_argument('owner', type=str, location=['args', 'json'])
parser.add_argument('host', type=str, location=['args', 'json'])
parser.add_argument('sys_code', type=str, location=['args', 'json'])
parser.add_argument('business', type=str, location=['args', 'json'])
parser.add_argument('status', type=str, location=['args', 'json'])
parser.add_argument('range', type=str, location=['args', 'json'])
parser.add_argument('discover_range[]', type=int, action='append', location=['args'])


class IPSset(BaseResource):

    def get(self):
        """"
        :return:
        """

        self.collection = mongo.db.ipset

        if self.action == 'options':
            return self.options([{
                '$group': {
                    '_id': 'options',
                    'ip': {'$addToSet': '$source'},
                    'range': {'$addToSet': '$range'},
                    'owner': {'$addToSet': '$assets.owner'},
                    'host': {'$addToSet': '$assets.host'},
                    'sys_code': {'$addToSet': '$assets.sys_code'},
                    'business': {'$addToSet': '$assets.business'},
                    'status': {'$addToSet': '$status'}
                }}], {'ip': [], 'range': [], 'owner': [], 'host': [], 'sys_code': [], 'business': [], 'status': []})

        args = parser.parse_args()

        query_body = dict()
        for _key, _value in args.items():
            if _key == 'discover_range[]' and _value:
                query_body['discover_time'] = {'$gte': int(_value[0] / 1000), '$lte': int(_value[1] / 1000)}
            elif _key in ['owner', 'host', 'sys_code', 'business'] and _value:
                query_body['assets.' + _key] = _value
            elif _value:
                query_body[_key] = _value
            else:
                continue

        try:
            dataset = list(self.collection.find(query_body, {'_id': 0}).sort([('discover_time', -1)]).skip(self.skip).limit(self.limit))
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

    def post(self):
        """
        新建、更新 IP资产
        :return:
        """
        # args = json.loads(request.data)
        self.collection = mongo.db.ipset
        args = parser.parse_args()
        try:
            self.collection.update_one({'ip': args['ip']}, {'$set': args}, upsert=True)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}

        return self.create_response(code, data)
