#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
节点管理

"""

from __future__ import print_function
from __future__ import absolute_import
from flask_restful import reqparse
from .base import BaseResource
from pmon.mongo import mongo
from pmon.resource.schedule import delete_collection, modify_collection
parser = reqparse.RequestParser()

parser.add_argument('uuid', type=str, location=['args', 'json'])
parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('remark', type=str, location=['args', 'json'])
parser.add_argument('api', type=str, location=['args', 'json'])
parser.add_argument('scope', type=str, action='append', location=['args', 'json'])
parser.add_argument('status', type=str, location=['args', 'json'])


class Node(BaseResource):

    def get(self):
        """
        :return:
        """
        self.collection = mongo.db.node

        try:
            __data = list(self.collection.find({}, {'_id': 0}).sort([('_id', 1)]))
            code = 20000
            data = {
                'total': len(__data),
                'items': __data
            }
        except Exception as e:
            code = 40000
            data = {'message': str(e)}

        return self.create_response(code, data)

    def post(self):
        """
        新建、更新 节点
        :return:
        """
        collection = mongo.db.node

        args = parser.parse_args()

        try:
            _doc = dict()
            for _key, _value in args.items():
                if _value:
                    _doc[_key] = _value
            _doc['type'] = 'node'
            modify_collection(collection, _doc.get('uuid'), _doc)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}
        return self.create_response(code, data)

    def delete(self):
        """
        删除节点
        :return:
        """
        collection = mongo.db.node
        args = parser.parse_args()
        code, data = delete_collection(collection, args)
        return self.create_response(code, data)






