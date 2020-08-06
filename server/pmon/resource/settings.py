#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
系统配置管理

"""

from __future__ import print_function
from __future__ import absolute_import

from flask_restful import reqparse
from pmon.mongo import mongo
from .base import BaseResource


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('value', type=str, action='append', location=['arg', 'json'])


class Settings(BaseResource):

    def get(self):
        """
        :return:
        """

        self.collection = mongo.db.settings

        try:
            __data = list(self.collection.find({}, {'_id': 0}))
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
        # args = json.loads(request.data)

        self.collection = mongo.db.settings
        args = parser.parse_args()

        print(args)

        try:
            self.collection.update_one({'name': args['name']}, {'$set': args})
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
        # args = json.loads(request.data)

        self.collection = mongo.db.node
        args = parser.parse_args()

        try:
            self.collection.delete_one({'name': args['name']})
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}

        return self.create_response(code, data)

    @classmethod
    def get_info(cls, name, field=None):

        _data = mongo.db.node.find_one({'name': name}, {'_id': 0})
        if field:
            return _data.get(field, None)
        else:
            return _data


