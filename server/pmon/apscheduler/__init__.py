#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
调度器，根据需要重构flask-apscheduler 及其 api

"""

from __future__ import print_function
from __future__ import absolute_import
from datetime import datetime
from apscheduler.jobstores.base import ConflictingIdError
from pmon.mongo import mongo
from flask_apscheduler import APScheduler
from pmon.apscheduler import api


class Scheduler(APScheduler):

    def __init__(self):
        super(Scheduler, self).__init__()
        self.schedule_collection = mongo.db.schedule

    def load_jobs(self):

        jobs = list()
        for schedule in self.schedule_collection.find({'type': 'schedule', 'status': 'LOADED'}):
            try:
                self.load_job(schedule['uuid'], schedule['name'], schedule['trigger_name'], schedule['job_name'])
            except ConflictingIdError as e:
                continue
            jobs.append(schedule)
        return jobs

    def load_job(self, uid, name, trigger_name, job_name):
        job_def = dict()
        job_def.update(self.parse_trigger(trigger_name))
        func, args, kwargs = self.parse_job(job_name)
        job_def['args'] = args
        job_def['kwargs'] = kwargs
        job_def['name'] = name

        job = self.add_job(uid, func, **job_def)
        self.schedule_collection.update_one({'uuid': uid}, {'$set': {'status': 'LOADED'}})
        return job

    def unload_job(self, job_id):
        self.remove_job(job_id)
        self.schedule_collection.update_one({'uuid': job_id}, {'$set': {'status': 'UNLOADED'}})

    def reload_jobs(self):
        self.remove_all_jobs()
        self.load_jobs()

    def parse_trigger(self, name):

        _trigger = self.schedule_collection.find_one(
            {'type': 'trigger', 'name': name},
            {'name': 0, 'type': 0, 'remark': 0, '_id': 0, 'uuid': 0}
        )
        if not _trigger:
            raise Exception("parse_trigger error: Can not find [%s] in %s" % (name, self.schedule_collection))

        for _date_field in ['run_date', 'start_date', 'end_date']:
            if _date_field in _trigger.keys():
                _trigger[_date_field] = datetime.fromtimestamp(_trigger[_date_field])

        _trigger['timezone'] = 'Asia/Shanghai'

        return _trigger

    def parse_job(self, name):

        param = self.schedule_collection.find_one({'type': 'job', 'name': name})

        if not param:
            raise Exception("parse_job error: Can not find job name:[%s] in collection:[%s]" % (name, self.schedule_collection))

        try:
            return param['func'], param['args'], param['kwargs']
        except Exception as e:
            raise Exception("parse_job error: [%s],  param:[%s] " % (str(e), str(param)))

    def _load_api(self):
        """
        Add the routes for the scheduler API.
        """
        self._add_url_route('get_scheduler_info', '', api.get_scheduler_info, 'GET')
        self._add_url_route('add_job', '/jobs', api.add_job, 'POST')
        self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
        self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')
        self._add_url_route('delete_job', '/jobs/<job_id>', api.delete_job, 'DELETE')
        self._add_url_route('update_job', '/jobs/<job_id>', api.update_job, 'PATCH')
        self._add_url_route('pause_job', '/jobs/<job_id>/pause', api.pause_job, 'POST')
        self._add_url_route('resume_job', '/jobs/<job_id>/resume', api.resume_job, 'POST')
        self._add_url_route('run_job', '/jobs/<job_id>/run', api.run_job, 'POST')

        self._add_url_route('load_job', '/jobs/<job_id>/load', api.load_job, 'POST')
        self._add_url_route('unload_job', '/jobs/<job_id>/unload', api.unload_job, 'POST')
        self._add_url_route('load_jobs', '/jobs/loads', api.load_jobs, 'GET')
        self._add_url_route('remove_jobs', '/jobs/remove', api.remove_jobs, 'GET')
        self._add_url_route('shutdown', '/shutdown', api.shutdown, 'GET')
        self._add_url_route('start', '/start', api.start, 'GET')
