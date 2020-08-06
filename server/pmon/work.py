#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
任务节点 客户端
用于下发任务和获取任务结果

"""
import os
import json
import logging
from logging.handlers import RotatingFileHandler
import requests


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logger = logging.getLogger('work')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s|%(funcName)s - %(message)s')
handler = RotatingFileHandler(os.path.join(basedir, 'log/work.log'), maxBytes=10 * 1024 * 1024, backupCount=10)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class Work(object):
    """
    任务节点
    """

    def __init__(self, api):
        """
        初始化
        :param api: flower api, like: 'http://127.0.0.1:5555/api'
        """
        self._headers = {'Content-Type': 'application/json; charset=utf8'}
        self.api = api

    def fetch_info(self, task_ids):
        """
        获取任务状态
        :param task_ids:
        :return:
        """

        data = list()
        try:

            for _id in task_ids:
                res = self.task_info(_id)
                if res['success']:
                    data.append(res['data'])
            success = True
            message = ""
        except Exception as e:
            success = False
            message = "Error: %s" % str(e)

        return {'success': success, 'data': data, 'message': message}

    def fetch_result(self, task_ids):
        """
        获取任务结果
        :param task_ids:
        :return:
        """

        data = list()
        try:

            for _id in task_ids:
                res = self.task_result(_id)
                if res['success']:
                    data.append(res['data'])
            success = True
            message = ""
        except Exception as e:
            success = False
            message = "Error: %s" % str(e)

        return {'success': success, 'data': data, 'message': message}

    def task_result(self, task_id):
        url = self.api + '/task/result/' + task_id
        res = requests.get(url=url)

        if not res.status_code == 200:
            success = False
            message = 'Error, response_code: %s' % str(res.status_code)
            data = ''
        else:
            success = True
            message = ''
            data = res.json()['result']

        return {'success': success, 'data': data, 'message': message}

    def task_info(self, task_id):
        url = self.api + '/task/info/' + task_id
        res = requests.get(url=url)

        if not res.status_code == 200:
            success = False
            message = 'Error, response_code: %s' % str(res.status_code)
            data = dict()
        else:
            success = True
            message = ''
            data = res.json()

        return {'success': success, 'data': data, 'message': message}

    def async_apply(self, func, *args, **kwargs):
        """
        异步下发任务

        下发的目标是对应节点的 celery worker
        """

        try:
            url = self.api + '/task/async-apply/' + func
            res = requests.post(url=url, headers=self._headers, data=json.dumps({'args': args, 'kwargs': kwargs}))

            if not res.status_code == 200:
                success = False
                message = 'async-apply failure: code[%s]' % str(res.status_code)
                data = dict()
            else:
                success = True
                message = ''
                data = res.json()
        except Exception as e:
            raise Exception("work.async_apply error: %s" % str(e))

        return {'success': success, 'message': message, 'data': data}

