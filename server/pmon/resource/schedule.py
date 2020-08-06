#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
任务调度 接口

"""

from __future__ import print_function
from __future__ import absolute_import
import json
import uuid
from flask_restful import reqparse
from .base import BaseResource
from pmon.mongo import mongo

parser = reqparse.RequestParser()

parser.add_argument('uuid', type=str, location=['args', 'json'])
parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('trigger', choices=('date', 'interval', 'cron'), location=['args', 'json'],
                    help='Bad choice: {error_msg}')
parser.add_argument('remark', type=str, location=['args', 'json'])

# trigger
# :param int misfire_grace_time: seconds after the designated runtime that the job is still allowed to be run
parser.add_argument('misfire_grace_time', type=int, location=['args', 'json'])
# :param bool coalesce: run once instead of many times if the scheduler determines that the
# job should be run more than once in succession
parser.add_argument('coalesce', type=bool, location=['args', 'json'])
# :param int max_instances: maximum number of concurrently running instances allowed for this job
parser.add_argument('max_instances', type=int, location=['args', 'json'])
# :param datetime next_run_time: when to first run the job, regardless of the trigger (pass
# ``None`` to add the job as paused)
parser.add_argument('next_run_time', type=str, location=['args', 'json'])
# :param bool replace_existing: ``True`` to replace an existing job with the same ``id``
#  (but retain the number of runs from the existing one)
parser.add_argument('replace_existing', type=bool, location=['args', 'json'])

parser.add_argument('start_end', type=int, action='append', dest='start_end', location=['args', 'json'])

# date
parser.add_argument('run_date', type=int, location=['args', 'json'])
parser.add_argument('timezone', type=str, location=['args', 'json'])

# interval
parser.add_argument('weeks', type=int, location=['args', 'json'])
parser.add_argument('days', type=int, location=['args', 'json'])
parser.add_argument('hours', type=int, location=['args', 'json'])
parser.add_argument('minutes', type=int, location=['args', 'json'])
parser.add_argument('seconds', type=int, location=['args', 'json'])
parser.add_argument('start_date', type=str, location=['args', 'json'])
parser.add_argument('end_date', type=str, location=['args', 'json'])
# parser.add_argument('timezone', type=str, location=['args', 'json'])

# cron
parser.add_argument('year', type=str, location=['args', 'json'])
parser.add_argument('month', type=str, location=['args', 'json'])
parser.add_argument('day', type=str, location=['args', 'json'])
parser.add_argument('week', type=str, location=['args', 'json'])
parser.add_argument('day_of_week', type=str, location=['args', 'json'])
parser.add_argument('hour', type=str, location=['args', 'json'])
parser.add_argument('minute', type=str, location=['args', 'json'])
parser.add_argument('second', type=str, location=['args', 'json'])
# parser.add_argument('start_date', type=int, location=['args'])
# parser.add_argument('end_date', type=str, location=['args'])
# parser.add_argument('timezone', type=str, location=['args', 'json'])

# Job
# parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('module', type=str, location=['args', 'json'])
parser.add_argument('func', type=str, location=['args', 'json'])
parser.add_argument('args', type=str, action='append', location=['args', 'json'])
parser.add_argument('kwargs', type=str, location=['args', 'json'])

# Task
# parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('tag', type=str, location=['args', 'json'])
parser.add_argument('backend', type=str, location=['args', 'json'])
parser.add_argument('options', type=str, location=['args', 'json'])
parser.add_argument('tool', type=str, location=['args', 'json'])
parser.add_argument('target', type=str, location=['args', 'json'])
parser.add_argument('node', type=str, location=['args', 'json'])

# Schedule
# parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('trigger_name', type=str, location=['args', 'json'])
parser.add_argument('job_name', type=str, location=['args', 'json'])
parser.add_argument('name', type=str, location=['args', 'json'])
parser.add_argument('status', type=str, location=['args', 'json'])


def modify_collection(collection, uid, doc):
    if uid:
        if doc['type'] == 'trigger':
            recreate_collection(collection, uid, doc)
        collection.update_one({'uuid': uid}, {'$set': doc})
    else:
        doc['uuid'] = str(uuid.uuid1())
        collection.insert(doc)


def recreate_collection(collection, uid, doc):
    collection.delete_one({'uuid': uid})
    collection.insert(doc)


def delete_collection(collection, args):
    uid = args.get('uuid')
    if not uid:
        code = 40000
        data = {'message': 'Error: Miss UUID!'}
        return code, data

    try:
        collection.delete_one({'uuid': uid})
        code = 20000
        data = {'message': 'success'}
    except Exception as e:
        code = 40000
        data = {'message': str(e)}
    return code, data


# /schedule/trigger
class Trigger(BaseResource):

    def get(self):
        collection = mongo.db.schedule
        try:
            dataset = list(collection.find({'type': 'trigger'}, {'_id': 0, 'type': 0}))
            datalen = len(dataset)
            data = {'total': datalen, 'items': dataset}
            code = 20000
        except Exception as e:
            data = {'message': str(e)}
            code = 40000
        return self.create_response(code, data)

    def post(self):
        collection = mongo.db.schedule

        try:
            args = parser.parse_args()
            fields = {
                'cron': ['year', 'month', 'week', 'day_of_week', 'day', 'hour', 'minute', 'second', 'start_date', 'end_date', 'start_end'],
                'interval': ['weeks', 'days', 'hours', 'minutes', 'seconds', 'start_date', 'end_date', 'start_end'],
                'date': ['run_date'],
            }[args['trigger']]
            base_fields = ['uuid', 'name', 'remark', 'trigger']
            setting_fields = ['misfire_grace_time', 'coalesce', 'max_instances', 'replace_existing', 'next_run_time']
            fields.extend(base_fields)
            fields.extend(setting_fields)

            _doc = dict()
            for _key, _value in args.items():
                if _value and _key in fields:
                    if _key == 'start_end':
                        _doc['start_date'] = _value[0] / 1000
                        _doc['end_date'] = _value[1] / 1000
                        continue
                    if _key == 'run_date':
                        _doc['run_date'] = _value / 1000
                        continue
                    _doc[_key] = _value
            _doc['type'] = 'trigger'

        except Exception as e:
            code = 40000
            data = {'message': 'parser args error: [%s];' % (str(e))}
            return self.create_response(code, data)

        try:
            modify_collection(collection, _doc.get('uuid'), _doc)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}
        return self.create_response(code, data)

    def delete(self):
        collection = mongo.db.schedule
        args = parser.parse_args()
        code, data = delete_collection(collection, args)
        return self.create_response(code, data)


# /schedule/job
class Job(BaseResource):

    def get(self):
        collection = mongo.db.schedule
        try:
            dataset = list(collection.find({'type': 'job'}, {'_id': 0, 'type': 0}))
            datalen = len(dataset)
            data = {'total': datalen, 'items': dataset}
            code = 20000
        except Exception as e:
            data = {'message': str(e)}
            code = 40000
        return self.create_response(code, data)

    def post(self):
        collection = mongo.db.schedule

        try:
            args = parser.parse_args()
            _doc = dict()
            _doc['args'] = list()
            _doc['kwargs'] = dict()
            for _key, _value in args.items():
                if _value:
                    if _key == 'kwargs':
                        _doc[_key] = json.loads(_value)
                    else:
                        _doc[_key] = _value
            _doc['type'] = 'job'
        except Exception as e:
            code = 40000
            data = {'message': 'parser args error: [%s]' % (str(e))}
            return self.create_response(code, data)

        try:
            modify_collection(collection, _doc.get('uuid'), _doc)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}
        return self.create_response(code, data)

    def delete(self):
        collection = mongo.db.schedule
        args = parser.parse_args()
        code, data = delete_collection(collection, args)
        return self.create_response(code, data)


# /schedule/task
class Task(BaseResource):

    def get(self):
        self.collection = mongo.db.schedule

        if self.action == 'options':
            return self.options([
                {'$match': {'type': 'node', 'status': 'enable'}},
                {'$group': {'_id': 'options', 'node': {'$addToSet': '$name'}}}
            ], {'node': []})

        try:
            dataset = list(self.collection.find({'type': 'task'}, {'_id': 0, 'type': 0}))
            datalen = len(dataset)
            data = {'total': datalen, 'items': dataset}
            code = 20000
        except Exception as e:
            data = {'message': str(e)}
            code = 40000
        return self.create_response(code, data)

    def post(self):
        collection = mongo.db.schedule

        try:
            args = parser.parse_args()
            _doc = dict()
            for _key, _value in args.items():
                if _value:
                    _doc[_key] = _value
            _doc['type'] = 'task'
        except Exception as e:
            code = 40000
            data = {'message': 'parser args error: [%s]' % (str(e))}
            return self.create_response(code, data)

        try:
            modify_collection(collection, _doc.get('uuid'), _doc)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}
        return self.create_response(code, data)

    def delete(self):
        collection = mongo.db.schedule
        args = parser.parse_args()
        code, data = delete_collection(collection, args)
        return self.create_response(code, data)


# /schedule/schedule
class Schedule(BaseResource):

    def get(self):
        collection = mongo.db.schedule

        if self.action == 'options':
            data = dict()
            try:
                for item in collection.aggregate([{'$group': {'_id': '$type', 'name': {'$push': '$name'}}}]):
                    data[item['_id']] = item['name']
                data['_id'] = 'options'
                code = 20000
            except Exception as e:
                code = 40000
                data['message'] = str(e)
            return self.create_response(code, data)

        try:
            dataset = list(collection.find({'type': 'schedule'}, {'_id': 0, 'type': 0}))
            datalen = len(dataset)
            data = {'total': datalen, 'items': dataset}
            code = 20000
        except Exception as e:
            data = {'message': str(e)}
            code = 40000
        return self.create_response(code, data)

    def post(self):
        collection = mongo.db.schedule

        try:
            args = parser.parse_args()
            _doc = dict()
            for _key, _value in args.items():
                if _value:
                    _doc[_key] = _value
            _doc['type'] = 'schedule'
            _doc['name'] = "%s[%s]" % (_doc['job_name'], _doc['trigger_name'])
        except Exception as e:
            code = 40000
            data = {'message': 'parser args error: [%s]' % (str(e))}
            return self.create_response(code, data)

        try:
            modify_collection(collection, _doc.get('uuid'), _doc)
            code = 20000
            data = {'message': 'success'}
        except Exception as e:
            code = 40000
            data = {'message': str(e)}
        return self.create_response(code, data)

    def delete(self):
        collection = mongo.db.schedule
        args = parser.parse_args()
        code, data = delete_collection(collection, args)
        return self.create_response(code, data)



