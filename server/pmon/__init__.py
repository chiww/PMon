#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
task相关定时执行任务

"""

from __future__ import print_function
from __future__ import absolute_import
import os
import fcntl
import atexit
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, has_request_context, request
from apscheduler.jobstores.mongodb import MongoDBJobStore
from pmon.settings import config
from pmon.mongo import mongo

from pymongo import MongoClient

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(os.getenv('FLASK_APP'))

    app.config.from_object(config[config_name])

    register_logging(app)

    with app.app_context():
        register_extensions(app)

    return app


def register_extensions(app):

    mongo.init_app(app)

    from pmon.resource import api

    api.init_app(app)
    scheduler_init(app)


def scheduler_init(app):
    """
    调度器初始化

    :param app:
    :return:
    """

    from pmon.apscheduler import Scheduler

    # 添加Jobstores
    mongodb_uri = app.config['MONGO_URI']
    app.config['SCHEDULER_JOBSTORES'] = {
        'default': MongoDBJobStore(database='PMon', client=MongoClient(mongodb_uri))
    }
    scheduler = Scheduler()
    # 通过文件锁限制gunicorn重复执行，详细参见：doc/how_to_make_APScheduler_single.md
    f = open("scheduler.lock", "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scheduler.init_app(app)
        scheduler.start()
    except IOError as e:
        pass

    def unlock():
        fcntl.flock(f, fcntl.LOCK_UN)
        f.close()

        try:
            os.remove('scheduler.lock')
        except OSError as e:
            pass

    atexit.register(unlock)

    # 初始化logger
    logger = logging.getLogger('apscheduler')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s|%(funcName)s - %(message)s')
    handler = RotatingFileHandler(os.path.join(basedir, 'log/scheduler.log'), maxBytes=10 * 1024 * 1024,
                                  backupCount=10)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)


def register_logging(app):

    class RequestFormatter(logging.Formatter):
        def format(self, record):
            if has_request_context():
                record.url = request.url
                record.remote_addr = request.remote_addr
            else:
                record.url = None
                record.remote_addr = None

            return super(RequestFormatter, self).format(record)

    if not os.path.exists(basedir + '/log'):
        os.makedirs(basedir + '/log')

    task_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s|%(funcName)s - %(message)s')
    task_handler = RotatingFileHandler(os.path.join(basedir, 'log/pmon.log'), maxBytes=10 * 1024 * 1024, backupCount=10)
    task_handler.setFormatter(task_formatter)
    task_handler.setLevel(logging.INFO)
    app.logger.addHandler(task_handler)

    # if not app.debug:
    #     app.logger.addHandler(task_handler)




