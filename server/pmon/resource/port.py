#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
风险端口

"""

from __future__ import print_function
from __future__ import absolute_import
from flask_restful import reqparse, inputs
from pmon.mongo import mongo
from pmon.jobs.count import risk_port_list, risk_serv_list
from .base import BaseResource

parser = reqparse.RequestParser()
parser.add_argument('ip', type=inputs.regex(r'[\d.\\]{7,18}'), location=['args', 'json'])
parser.add_argument('host', type=str, location=['args', 'json'])
parser.add_argument('owner', type=str, location=['args', 'json'])
parser.add_argument('sys_code', type=str, location=['args', 'json'])
parser.add_argument('ticket_status', type=str, location=['args', 'json'])
parser.add_argument('port', type=str, location=['args', 'json'])
parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('product', type=str, location=['args', 'json'])
parser.add_argument('discover_range[]', type=int, action='append', location=['args'])
parser.add_argument('isGroup', type=str, location=['args'])
parser.add_argument('isHigh', type=str, location=['args'])


class Ports(BaseResource):

    def get(self):
        """"
        :return:
        """

        self.collection = mongo.db.port

        if self.action == 'options':
            return self.options([{
                '$group': {
                    '_id': 'options',
                    'owner': {'$addToSet': '$assets.owner'},
                    'business': {'$addToSet': '$assets.business'},
                    'sys_code': {'$addToSet': '$assets.sys_code'},
                    'service_name': {'$addToSet': '$detail.name'},
                    'service_product': {'$addToSet': '$detail.product'}
                }}], {'owner': [], 'business': [], 'sys_code': [], 'service_name': [], 'service_product': []})

        args = parser.parse_args()

        __isGroup = args.pop('isGroup')
        __isHigh = args.pop('isHigh')

        query_body = dict()
        query_body['status'] = 'OPEN'
        for _key, _value in args.items():
            if _key == 'discover_range[]' and _value:
                query_body['discover_time'] = {'$gte': int(_value[0] / 1000), '$lte': int(_value[1] / 1000)}
            elif _key == 'ticket_status' and _value:
                query_body['ticket_info.status'] = _value
            elif _key == 'name' and _value:
                query_body['detail.name'] = _value
            elif _key == 'product' and _value:
                query_body['detail.product'] = _value
            elif _value:
                query_body[_key] = _value
            else:
                continue

        # 如果选择高危过滤，检索语句中加入端口过滤；TODO：1. 支持高危服务过滤；2. 高危服务支持正则过滤
        if __isHigh == 'true':
            query_body['port'] = {'$in': risk_port_list()}
            query_body['detail.name'] = {'$in': risk_serv_list()}

        try:
            # 聚合，使用聚合的语句检索
            if __isGroup == 'true':
                group_body = {'_id': {'ip': '$ip', 'assets': '$assets'}, 'ports': {'$push': '$port'}}
                project_body = {'ip': '$_id.ip', 'assets': '$_id.assets', 'ports': '$ports',
                                '_id': 0, 'ticket_info.status': 'UNREPORTED'}
                dataset = list(self.collection.aggregate([
                    {'$match': query_body},
                    {'$group': group_body},
                    {'$project': project_body},
                    {'$skip': self.skip},
                    {'$limit': self.limit}]))
                datalen = len(list(self.collection.aggregate([{'$match': query_body}, {'$group': group_body}])))
            # 非聚合，使用普通的find语句检索
            else:
                dataset = list(
                    self.collection.find(
                        query_body, {'_id': 0}).sort([('discover_time', -1)]).skip(self.skip).limit(self.limit))
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
