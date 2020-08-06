#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/%s' % (basedir, 'db.sqlite3')

    SCHEDULER_API_ENABLED = True


class DevelopmentConfig(BaseConfig):

    MONGO_URI = "mongodb://127.0.0.1:27017/PMon"


class ProductionConfig(BaseConfig):
    MONGO_URI = "mongodb://127.0.0.1:27017/PMon"


class TestingConfig(BaseConfig):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
