#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
工单报备

"""

from __future__ import print_function
from __future__ import absolute_import
from flask_restful import reqparse, inputs
from pmon.mongo import mongo

from .base import BaseResource

parser = reqparse.RequestParser()
parser.add_argument('ip', type=inputs.regex(r'[\d.\\]{7,18}'), location=['args', 'json'])
parser.add_argument('port', type=str, location=['args', 'json'])
parser.add_argument('url', type=str, location=['args', 'json'])

# ticket
parser.add_argument('ticket_id', type=str, location=['args', 'json'])
parser.add_argument('source', type=str, location=['args', 'json'])
parser.add_argument('remark', type=str, location=['args', 'json'])
parser.add_argument('owner', type=str, location=['args', 'json'])
parser.add_argument('status', type=str, location=['args', 'json'])
parser.add_argument('create_time', type=int, location=['args', 'json'])


class Ticket(BaseResource):

    def post(self):

        args = parser.parse_args()

        _doc = dict()
        for _key, _value in args.items():
            if _value:
                _doc[_key] = _value

        if 'ip' and 'port' in _doc.keys():
            query = {'ip': _doc['ip'], 'port': _doc['port']}
            self.collection = mongo.db.port
        elif 'url' in _doc.keys():
            query = {'url': _doc['url']}
            self.collection = mongo.db.webcheck
        else:
            return self.create_response(40000, {'message': 'Can not parser ip:port or url.'})

        self.collection.update_one(query, {
            '$set': {
                'ticket_info.owner': _doc['owner'],
                'ticket_info.ticket_id': _doc['ticket_id'],
                'ticket_info.status': _doc['status'],
                'ticket_info.source': _doc['source'],
                'ticket_info.remark': _doc['remark'],
                'ticket_info.create_time': _doc['create_time']
            }})

        return self.create_response(20000, {'message': 'Update success: %s' % str(query)})
