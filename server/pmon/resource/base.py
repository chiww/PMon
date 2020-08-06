#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Resource基类
"""

from __future__ import print_function
from __future__ import absolute_import
from flask import jsonify
from flask_restful import Resource, reqparse


class BaseResource(Resource):

    def __init__(self):
        self.collection = None
        self.limit = 20
        self.skip = 0
        self.action = None
        self.parser_default_args()

    def parser_default_args(self):
        # 默认的参数解析 [page=1&limit=20&sort=%2Btask_id]
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('limit', type=int, location='args')
        parser.add_argument('sort', type=str, location='args')
        parser.add_argument('action', type=str, location='args')

        args = parser.parse_args()

        if args['limit']:
            self.limit = args['limit']
        if args['page']:
            self.skip = args['limit'] * (args['page'] - 1)
        self.action = args['action']

        # TODO: parse sort

    def options(self, agg_body, default_data):
        """
        获取页面中过滤项中的可选择的选择项列表
        :return:
        """

        try:
            try:
                dataset = list(self.collection.aggregate(agg_body))[0]
            except IndexError:
                # 如果为空,则返回默认的空值;
                dataset = default_data
            code = 20000
            data = dataset
        except Exception as e:
            code = 40000
            data = {'message': 'failed: [%s]' % str(e)}

        return self.create_response(code, data)

    @staticmethod
    def create_response(code, data):
        return jsonify({'code': code, 'data': data})

