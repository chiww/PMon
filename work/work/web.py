#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
高危Web应用检测
"""

from __future__ import print_function
from __future__ import absolute_import
from work.lib.webcheck import WebCheckProcess
from celery.utils.log import get_task_logger
from .task import Task

logger = get_task_logger("work")


class WebCheckTask(Task):

    def __init__(self):
        self.process = WebCheckProcess
        self.output = []
        super(Task, self)

    def __call__(self, task_obj, task_tag, address, options, result_backend):

        self.options = options
        proc = self.process(targets=str(address), options=options)
        proc.run()
        self.stdout = proc.stdout
        return self.handle_output(task_obj, task_tag, self.stdout, result_backend)
