#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
proc(address, options) => stdout
parser(stdout) => report
reformat(report) => output

"""

from __future__ import print_function
from __future__ import absolute_import
import time
import requests
from celery.utils.log import get_task_logger

logger = get_task_logger("work")


class Task(object):

    @staticmethod
    def handle_output(task_obj, task_tag, output, result_backend):

        data = dict()
        data['timestamp'] = int(time.time())
        data['result'] = output
        data['task_id'] = task_obj.request.id
        data['tag'] = task_tag

        try:
            response = requests.post(url=result_backend, json=data)

            # 将结果推送到目标web api
            if response.status_code != 200:
                logger.error("Error! Response code [%s]; [%s]" % (str(response.status_code), data['task_id']))
            else:
                logger.info("Backend Request success! [%s]" % data['task_id'])
        except Exception as e:
            logger.error("Error! [%s] Post to [%s] [%s]!" % (data['task_id'], result_backend, str(e)))

        return output

    @staticmethod
    def event(task_obj):

        def _event(scan_obj):
            cur_task = scan_obj.current_task
            if cur_task:
                _task = scan_obj.tasks[cur_task.name]
                task_obj.update_state(state='PROGRESS', meta={'percent': _task.progress})

        return _event

