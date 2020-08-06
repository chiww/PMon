#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""

"""

from __future__ import print_function
from __future__ import absolute_import

import os
import logging
from celery import Celery, chain
from celery.signals import after_setup_logger
from .port import NmapTask, MasscanTask
from .web import WebCheckTask

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
brokers = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'

app = Celery('work', broker=brokers, backend=backend)

nmap_task = NmapTask()
masscan_task = MasscanTask()
webcheck_task = WebCheckTask()


@app.task(bind=True)
def nmap(self, *args, **kwargs):
    return nmap_task(self, *args)


@app.task(bind=True)
def masscan(self, *args, **kwargs):
    return masscan_task(self, *args)


@app.task(bind=True)
def webcheck(self, *args, **kwargs):
    return webcheck_task(self, *args)


@after_setup_logger.connect
def setup_loggers(*args, **kwargs):

    logger = logging.getLogger("work")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # StreamHandler
    # sh = logging.StreamHandler()
    # sh.setFormatter(formatter)
    # logger.addHandler(sh)

    # FileHandler
    fh = logging.FileHandler('./log/worker.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)