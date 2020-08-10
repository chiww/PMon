#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
proc(address, options) => stdout
parser(stdout) => report
reformat(report) => output

"""

from __future__ import print_function
from __future__ import absolute_import
import os
import time
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
from work.lib.masscan import MasscanProcess, MasscanParser
from .task import Task
from celery.utils.log import get_task_logger

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
MASSCAN_EXE_PATH = basedir + "/bin/masscan"


logger = get_task_logger("work")


class NmapTask(Task):

    def __init__(self):
        self.process = NmapProcess
        self.parser = NmapParser.parse
        self.report = dict()
        self.output = []

        super(Task, self)

    def reformat(self, report):
        """
        重新格式化输出统一样式
        :param report:
        :return:
        """

        output = list()

        for host in report.hosts:
            _open = list()
            _close = list()
            _services = list()

            for port in host._services:

                if port.state == 'open':
                    _open.append(str(port.port))
                elif port.state == 'close':
                    _close.append(str(port.port))

                __service = port.service_dict
                __service['banner'] = port.banner
                __service['port'] = str(port.port)
                _services.append(__service)

            host_end_time = int(host.endtime) if host.endtime else 0

            output.append({
                'address': host.address,
                'status': host.status,
                'open': _open,
                'close': _close,
                'service': _services,
                'timestamp': host_end_time
            })

        return output

    def __call__(self, task_obj, task_tag, address, options, result_backend):

        self.options = options
        proc = self.process(targets=str(address), options=options, event_callback=self.event(task_obj))
        proc.run()
        self.stdout = proc.stdout
        self.report = self.parser(self.stdout)
        self.output = self.reformat(self.report)
        return self.handle_output(task_obj, task_tag, self.output, result_backend)


class MasscanTask(Task):

    def __init__(self):
        self.process = MasscanProcess
        self.parser = MasscanParser.parse_from_string
        self.report = dict()
        self.output = []

        self.bin = MASSCAN_EXE_PATH

        super(Task, self)

    def reformat(self, report):
        """
        暂时不支持 --banner 参数解析
        :param report:
        :return:
        """

        output = list()
        for host in report:

            _open = [str(p['port']) for p in host['ports'] if p['status'] == 'open']
            _close = [str(p['port']) for p in host['ports'] if p['status'] == 'close']

            output.append({
                'address': host['address'],
                'open': _open,
                'close': _close,
                'timestamp': int(time.time()),
                'service': list(),
                'status': 'up'
            })
        return output

    def __call__(self, task_obj, task_tag, address, options, result_backend):

        self.options = options
        proc = MasscanProcess(targets=str(address), options=options, event_callback=self.event(task_obj), fqp=self.bin)
        proc.run()
        self.stdout = proc.stdout
        self.report = self.parser(self.stdout)
        self.output = self.reformat(self.report)
        return self.handle_output(task_obj, task_tag, self.output, result_backend)



