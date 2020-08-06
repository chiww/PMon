#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
重写原flask_apscheduler请求Api，主要是因为状态码；并附加几个新的Api

"""

from __future__ import print_function
from __future__ import absolute_import
from collections import OrderedDict
from flask import current_app, request, Response
from flask_apscheduler.json import jsonify
from apscheduler.jobstores.base import ConflictingIdError, JobLookupError


# ------------------------------
# From flask_apscheduler.api change response status code 
# ------------------------------

def get_scheduler_info():
    """Gets the scheduler info."""

    scheduler = current_app.apscheduler

    d = OrderedDict([
        ('current_host', scheduler.host_name),
        ('allowed_hosts', scheduler.allowed_hosts),
        ('running', scheduler.running)
    ])

    return jsonify(d)


def add_job():
    """Adds a new job."""

    data = request.get_json(force=True)

    try:
        job = current_app.apscheduler.add_job(**data)
        return jsonify(job)
    except ConflictingIdError:
        return jsonify(dict(message='Job %s already exists.' % data.get('id')), status=202)
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def delete_job(job_id):
    """Deletes a job."""

    try:
        current_app.apscheduler.remove_job(job_id)
        return Response(status=200)
    except JobLookupError:
        return jsonify(dict(message='Job %s not found' % job_id), status=202)
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def get_job(job_id):
    """Gets a job."""

    job = current_app.apscheduler.get_job(job_id)

    if not job:
        return jsonify(dict(message='Job %s not found' % job_id), status=202)

    return jsonify(job)


def get_jobs():
    """Gets all scheduled jobs."""

    jobs = current_app.apscheduler.get_jobs()

    job_states = []

    for job in jobs:
        job_states.append(job)

    return jsonify(job_states)


def update_job(job_id):
    """Updates a job."""

    data = request.get_json(force=True)

    try:
        current_app.apscheduler.modify_job(job_id, **data)
        job = current_app.apscheduler.get_job(job_id)
        return jsonify(job)
    except JobLookupError:
        return jsonify(dict(message='Job %s not found' % job_id), status=202)
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def pause_job(job_id):
    """Pauses a job."""

    try:
        current_app.apscheduler.pause_job(job_id)
        job = current_app.apscheduler.get_job(job_id)
        return jsonify(job)
    except JobLookupError:
        return jsonify(dict(message='Job %s not found' % job_id), status=202)
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def resume_job(job_id):
    """Resumes a job."""

    try:
        current_app.apscheduler.resume_job(job_id)
        job = current_app.apscheduler.get_job(job_id)
        return jsonify(job)
    except JobLookupError:
        return jsonify(dict(message='Job %s not found' % job_id), status=202)
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def run_job(job_id):
    """Executes a job."""

    try:
        current_app.apscheduler.run_job(job_id)
        job = current_app.apscheduler.get_job(job_id)
        return jsonify(job)
    except JobLookupError:
        return jsonify(dict(message='Job %s not found' % job_id), status=202)
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


# ------------------------
# For PMon server new api
# -------------------------

def load_job(job_id):
    """
    :return:
    """
    data = request.get_json(force=True)
    name = data['name']
    trigger_name = data['trigger_name']
    job_name = data['job_name']

    try:
        job = current_app.apscheduler.load_job(job_id, name, trigger_name, job_name)
        return jsonify(dict(
            message='Job: %s load success!' % job_id,
            title='Success',
            type='success'
        ), status=200)
        # return jsonify(job)
    except ConflictingIdError:
        return jsonify(dict(
            message='Job: %s already exists.' % job_id,
            title='Warning',
            type='warning'
        ), status=200)
    except Exception as e:
        return jsonify(
            dict(message=str(e), title='Error', type='error'), status=202)


def unload_job(job_id):
    """
    :return:
    """
    data = request.get_json(force=True)

    try:
        job = current_app.apscheduler.unload_job(job_id)
        return jsonify(dict(
            message='Job: %s unload success!' % job_id,
            title='Success',
            type='success'
        ), status=200)
    except ConflictingIdError:
        return jsonify(dict(
            message='Job: %s already exists.' % job_id,
            title='Warning',
            type='warning'
        ), status=200)
    except Exception as e:
        return jsonify(
            dict(message=str(e), title='Error', type='error'), status=202)


def load_jobs():

    try:
        jobs = current_app.apscheduler.load_jobs()
        return jsonify(dict(message='success', status=200))
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def remove_jobs():

    try:
        jobs = current_app.apscheduler.remove_all_jobs()
        return jsonify(dict(message='success', status=200))
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def shutdown():
    try:
        current_app.apscheduler.shutdown()
        return jsonify(dict(message='success', status=200))
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)


def start():
    try:
        current_app.apscheduler.start()
        return jsonify(dict(message='success', status=200))
    except Exception as e:
        return jsonify(dict(message=str(e)), status=202)

