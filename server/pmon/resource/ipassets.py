#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
IP资产管理

"""

from __future__ import print_function
from __future__ import absolute_import
from flask_restful import reqparse, inputs
from pmon.mongo import mongo
from .base import BaseResource


parser = reqparse.RequestParser()
parser.add_argument('address', type=inputs.regex(r'[\d.\\]{7,18}'), location=['args', 'json'])
parser.add_argument('region', type=str, location=['args', 'json'])
parser.add_argument('source', type=str, location=['args', 'json'])
parser.add_argument('remark', type=str, location=['args', 'json'])
parser.add_argument('status', type=str, location=['args', 'json'])
parser.add_argument('timestamp', type=int, location=['json'])


class IPAssets(BaseResource):

    def get(self):
        """"
        :return:
        """

        self.collection = mongo.db.ipassets

        if self.action == 'options':
            return self.options([{
                '$group': {
                    '_id': 'options',
                    'source': {'$addToSet': '$source'},
                    'region': {'$addToSet': '$source'},
                    'status': {'$addToSet': '$source'}
                }}], {'source': [], 'region': [], 'status': []})

        parser.add_argument('time_range[]', type=int, action='append', location=['args'])
        args = parser.parse_args()

        query_body = dict()
        for _key, _value in args.items():
            if _key == 'time_range[]' and _value:
                query_body['timestamp'] = {'$gte': int(_value[0] / 1000), '$lte': int(_value[1] / 1000)}
            elif _value:
                query_body[_key] = _value
            else:
                continue

        try:
            dataset = list(self.collection.find(query_body, {'_id': 0}).sort([('timestamp', -1)]).skip(self.skip).limit(self.limit))
            datalen = len(list(self.collection.find(query_body)))
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
        self.collection = mongo.db.ipassets

        args = parser.parse_args()

        try:
            self.collection.update_one({'address': args['address']}, {'$set': args}, upsert=True)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}

        return self.create_response(code, data)

    def delete(self):
        """
        删除
        :return:
        """
        self.collection = mongo.db.ipassets

        args = parser.parse_args()

        try:
            self.collection.delete_one({'address': args['address']})
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}

        return self.create_response(code, data)
