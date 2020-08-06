#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
风险web任务结果处理

"""

from __future__ import print_function
from __future__ import absolute_import
from pmon.mongo import mongo


class WebParser(object):

    def __init__(self, tag):
        __mapper = {
            'WEB_CHECK': self.webcheck,
        }
        self.func = __mapper[tag]

    def __call__(self, report, param):
        self.func(report, param)

    def webcheck(self, report, param):

        collection = mongo.db.webcheck

        try:
            for res in report['result']:
                collection.update_one({'url': res['url']}, {
                    '$set': res,
                    '$setOnInsert': {
                        'create_time': report['timestamp'],
                        'assets': {
                            'host': 'NA',
                            'owner': 'NA',
                            'sys_code': 'NA',
                            'business': 'NA',
                        },
                        'ticket_info': {
                            'status': 'UNREPORTED',
                            'ticket_id': 'NA',
                            'owner': 'NA',
                            'remark': 'NA',
                            'create_time': 0,
                            'source': 'NA'
                        }
                    }}, upsert=True)
        except Exception as e:
            raise Exception("webcheck: [%s] report: %s  param: %s" % (str(e), str(report), str(param)))




