#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
任务结果处理

"""

from __future__ import print_function
from __future__ import absolute_import
from flask import request, jsonify, current_app
from flask_restful import Resource

import json
from pmon.mongo import mongo
from .port import PortParser
from .web import WebParser


class TaskBackend(Resource):
    """
    接收任务结果
    """

    def post(self):
        """
        :return:
        """

        _report = json.loads(request.data)

        try:
            _task = mongo.db.task.find_one({'task-id': _report['task_id']})

            TaskParse(_report, _task['param']).run()
            code = 200
            data = {'message': 'success'}
        except Exception as e:
            _task_detail = dict()
            code = 400
            data = {'message': "Update task_id:[%s] failed:[%s]" % (_report['task_id'], str(e))}
            current_app.logger.error("Update task_id:[%s] failed:[%s]" % (_report['task_id'], str(e)))

        return jsonify({'code': code, 'data': data})


class TaskParse(object):

    def __init__(self, report, param):

        if param['tag'] in ['PORT_CHEK', 'PORT_DISC', 'PORT_INFO', 'HOST_DISC', 'PORT_RISK']:
            self.parse = PortParser(param['tag'])
        elif param['tag'] in ['WEB_CHECK']:
            self.parse = WebParser(param['tag'])

        self.report = report
        self.param = param

    def run(self):
        try:
            self.parse(self.report, self.param)
        except Exception as e:
            raise Exception("Task parse error: %s" % str(e))