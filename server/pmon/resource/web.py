#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
风险web

"""

from __future__ import print_function
from __future__ import absolute_import
from flask_restful import reqparse
from pmon.mongo import mongo

from .base import BaseResource

parser = reqparse.RequestParser()
parser.add_argument('url', type=str, location=['args', 'json'])
parser.add_argument('code', type=int, location=['args', 'json'])
parser.add_argument('tag', type=str, location=['args', 'json'])
parser.add_argument('status', type=str, location=['args', 'json'])
parser.add_argument('create_range[]', type=int, action='append', location=['args'])


class Web(BaseResource):

    def get(self):
        """"
        :return:
        """

        self.collection = mongo.db.webcheck

        if self.action == 'options':
            return self.options([{
                '$group': {
                    '_id': 'options',
                    'code': {'$addToSet': '$code'},
                    'tag': {'$addToSet': '$tag'},
                    'status': {'$addToSet': '$status'},
                }}], {'code': [], 'tag': [], 'status': []})

        args = parser.parse_args()

        query_body = dict()

        for _key, _value in args.items():
            if _key == 'create_range[]' and _value:
                query_body['create_time'] = {'$gte': int(_value[0] / 1000), '$lte': int(_value[1] / 1000)}
            elif _value:
                query_body[_key] = _value
            else:
                continue

        try:
            dataset = list(
                self.collection.find(
                    query_body, {'_id': 0}).sort([('timestamp', -1)]).skip(self.skip).limit(self.limit))
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
