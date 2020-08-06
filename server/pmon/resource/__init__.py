#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
插件配置

"""

from __future__ import print_function
from __future__ import absolute_import

from flask_restful import Api

from .login import Login, User
from .task import TaskIssue, Tasks
from ..backend.task import TaskBackend
from .port import Ports
from .ticket import Ticket
from .web import Web
from .ipassets import IPAssets
from .ipset import IPSset
from .dashboard import Dashboard, PanelCount, HisLine, RiskBar, ReportPie, UnreportedPie
from .base import BaseResource
from .settings import Settings
from .schedule import Trigger, Job, Task, Schedule
from .node import Node

base_url = '/admin'

api = Api()
api.add_resource(Login, base_url + '/user/login')
api.add_resource(User, base_url + '/user/info')
api.add_resource(Node, base_url + '/node')

api.add_resource(Dashboard, base_url + '/dashboard')
api.add_resource(PanelCount, base_url + '/panel_count')
api.add_resource(HisLine, base_url + '/his_line')
api.add_resource(RiskBar, base_url + '/risk_bar')
api.add_resource(ReportPie, base_url + '/report_pie')
api.add_resource(UnreportedPie, base_url + '/unreported_pie')

api.add_resource(TaskIssue, base_url + '/task/issue')
api.add_resource(Tasks, base_url + '/tasks')

api.add_resource(TaskBackend, base_url + '/taskend')

api.add_resource(Ports, base_url + '/ports')
api.add_resource(Ticket, base_url + '/ticket')
api.add_resource(Web, base_url + '/web')

api.add_resource(IPAssets, base_url + '/ipassets')
api.add_resource(IPSset, base_url + '/ipset')
api.add_resource(Settings, base_url + '/settings')
api.add_resource(BaseResource, '/base')

api.add_resource(Trigger, base_url + '/schedule/trigger')
api.add_resource(Job, base_url + '/schedule/job')
api.add_resource(Task, base_url + '/schedule/task')
api.add_resource(Schedule, base_url + '/schedule/schedule')

