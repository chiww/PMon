#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
登录管理

"""

from __future__ import print_function
from __future__ import absolute_import

import json
from flask import request
from flask_restful import Resource, reqparse


tokens = {
    'admin': {'token': 'admin-token'},
    'editor': {'token': 'editor-token'}
}


class Login(Resource):

    def post(self):
        request_body = json.loads(request.data)

        token = tokens.get(request_body['username'])
        if token:
            return {'code': 20000, 'data': token}


users = {
  'admin-token': {
    'roles': ['admin'],
    'introduction': 'I am a super administrator',
    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    'name': 'Super Admin'
  },
  'editor-token': {
    'roles': ['editor'],
    'introduction': 'I am an editor',
    'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    'name': 'Normal Editor'
  }
}


class User(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='args')
        args = parser.parse_args()

        user = users.get(args['token'])
        if user:
            return {'code': 20000, 'data': user}