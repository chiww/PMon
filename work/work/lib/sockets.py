#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from threading import Thread
import socket
import ipaddress
import time

"""
sockets -sT -v4 -p 80,2200 10.0.0.1/24 
"""

__version__ = 'v1.0.0'


class SocketsTask(object):

    """
    SocketsTask是记录扫描进程中各任务的，现在只实现了"TCP Connect"
    """

    def __init__(self, name, starttime=0, extrainfo=''):
        self.name = name
        self.etc = 0
        self.progress = 0
        self.percent = 0
        self.remaining = 0
        self.status = 'started'
        self.starttime = starttime
        self.endtime = 0
        self.extrainfo = extrainfo
        self.updated = 0


class SocketsProcess(Thread):

    def __init__(self, targets="127.0.0.1", options="-sT", event_callback=None, timeout=1):
        """
        Constructor of SocketsProcess class.

        :param targets: hosts to be scanned. Could be a string of hosts \
        separated with a coma or a python list of hosts/ip.
        :type targets: string or list

        :param options: list of nmap options to be applied to scan. \
        These options are all documented in nmap's man pages.

        :param event_callback: callable function which will be ran \
        each time nmap process outputs data. This function will receive \
        two parameters:

            1. the nmap process object
            2. the data produced by nmap process. See readme for examples.

        :return: SocketsProcess object

        """
        Thread.__init__(self)

        self.__nmap_targets = targets
        self.__nmap_options = options

        if event_callback and callable(event_callback):
            self.__nmap_event_callback = event_callback
        else:
            self.__nmap_event_callback = None
        (self.DONE, self.READY, self.RUNNING,
         self.CANCELLED, self.FAILED) = range(5)

        self.timeout = timeout

        # API usable in callback function
        self.__state = self.RUNNING
        self.__starttime = 0
        self.__endtime = 0
        self.__version = ''
        self.__elapsed = ''
        self.__summary = ''
        self.__stdout = list()
        self.__stderr = ''
        self.__current_task = ''
        self.__nmap_tasks = {}

        # ---------------------------
        self.__options_conn_type = "TCP"
        self.__options_conn_ports = ""

        self.parse_options()

        # 目标总连接数
        self.__target_conn_count = len(self.__addresses) * len(self.__ports)
        # 已经完成连接数
        self.__done_connect_count = 0

    def run(self):

        self.__starttime = int(time.time())

        self.__process_event({'status': 'socketsrun', 'start': self.__starttime, 'version': __version__})

        for event in self.__tcp_conn():
            if event['status'] == 'taskprogress':
                self.__stdout.append(event['stdout'])
            self.__process_event(event)

        self.__endtime = int(time.time())
        self.__process_event({
            'status': 'finish', 'time': self.__endtime, 'elapsed': self.__endtime - self.__starttime,
            'summary': {'address_count': len(self.__addresses), 'port_count': len(self.__ports),
                        'conn_count': self.__target_conn_count}})

    def is_running(self):
        """
        Checks if nmap is still running.

        :return: True if nmap is still running
        """
        return self.state == self.RUNNING

    def has_terminated(self):
        """
        Checks if nmap has terminated. Could have failed or succeeded

        :return: True if nmap process is not running anymore.
        """
        return (self.state == self.DONE or self.state == self.FAILED or
                self.state == self.CANCELLED)

    def has_failed(self):
        """
        Checks if nmap has failed.

        :return: True if nmap process errored.
        """
        return self.state == self.FAILED

    def is_successful(self):
        """
        Checks if nmap terminated successfully.

        :return: True if nmap terminated successfully.
        """
        return self.state == self.DONE

    def stop(self):
        """
        Send KILL -15 to the nmap subprocess and gently ask the threads to
        stop.
        """
        pass

    def __process_event(self, eventdata):
        """
        处理扫描期间产生的事件，并生成SocketsTask对象的值，用于跟踪扫描任务状态

        :return: True is event is known.

        :todo: handle parsing directly via NmapParser.parse()
        """
        rval = False

        try:
            if eventdata['status'] == 'taskbegin':
                taskname = eventdata['task']
                starttime = eventdata['time']
                xinfo = eventdata['extrainfo'] if eventdata.get('extrainfo') else ''
                newtask = SocketsTask(taskname, starttime, xinfo)
                self.__nmap_tasks[newtask.name] = newtask
                self.__current_task = newtask.name
                rval = True
            elif eventdata['status'] == 'taskend':
                taskname = eventdata['task']
                self.__nmap_tasks[taskname].endtime = eventdata['time']
                if eventdata.get('extrainfo'):
                    self.__nmap_tasks[taskname].extrainfo = eventdata['extrainfo']
                self.__nmap_tasks[taskname].status = "ended"
                rval = True
            elif eventdata['status'] == 'taskprogress':
                taskname = eventdata['task']
                self.__nmap_tasks[taskname].percent = eventdata['percent']
                self.__nmap_tasks[taskname].progress = eventdata['percent']
                self.__nmap_tasks[taskname].etc = eventdata['etc']
                self.__nmap_tasks[taskname].remaining = eventdata['remaining']
                self.__nmap_tasks[taskname].updated = eventdata['updated']
                rval = True
            elif eventdata['status'] == 'taskerror':
                taskname = eventdata['task']
                self.__nmap_tasks[taskname].endtime = eventdata['time']
                if eventdata.get('extrainfo'):
                    self.__nmap_tasks[taskname].extrainfo = eventdata['extrainfo']
                    self.__stderr = eventdata['extrainfo']
                self.__nmap_tasks[taskname].status = "ended"
                rval = True
            elif eventdata['status'] == 'socketsrun':
                self.__starttime = eventdata['start']
                self.__version = eventdata['version']
            elif eventdata['status'] == 'finished':
                self.__endtime = eventdata['time']
                self.__elapsed = eventdata['elapsed']
                self.__summary = eventdata['summary']
                rval = True
        except Exception as e:
            pass

        if self.__nmap_event_callback:
            self.__nmap_event_callback(self)

        return rval

    @property
    def targets(self):
        """
        Provides the list of targets to scan

        :return: list of string
        """
        return self.__nmap_targets

    @property
    def options(self):
        """
        Provides the list of options for that scan

        :return: list of string (nmap options)
        """
        return self.__nmap_options

    @property
    def state(self):
        """
        Accessor for nmap execution state. Possible states are:

        - self.READY
        - self.RUNNING
        - self.FAILED
        - self.CANCELLED
        - self.DONE

        :return: integer (from above documented enum)
        """
        return self.__state

    @property
    def starttime(self):
        """
        Accessor for time when scan started

        :return: string. Unix timestamp
        """
        return self.__starttime

    @property
    def endtime(self):
        """
        Accessor for time when scan ended

        :return: string. Unix timestamp
        """
        # warnings.warn("data collected from finished events are deprecated."
        #               "Use NmapParser.parse()", DeprecationWarning)
        return self.__endtime

    @property
    def elapsed(self):
        """
        Accessor returning for how long the scan ran (in seconds)

        :return: string
        """
        # warnings.warn("data collected from finished events are deprecated."
        #               "Use NmapParser.parse()", DeprecationWarning)
        return self.__elapsed

    @property
    def summary(self):
        """
        Accessor returning a short summary of the scan's results

        :return: string
        """
        # warnings.warn("data collected from finished events are deprecated."
        #               "Use NmapParser.parse()", DeprecationWarning)
        return self.__summary

    @property
    def tasks(self):
        """
        Accessor returning for the list of tasks ran during nmap scan

        :return: dict of NmapTask object
        """
        return self.__nmap_tasks

    @property
    def version(self):
        """
        Accessor for nmap binary version number

        :return: version number of nmap binary
        :rtype: string
        """
        return self.__version

    @property
    def current_task(self):
        """
        Accessor for the current NmapTask beeing run

        :return: NmapTask or None if no task started yet
        """
        rval = None
        if len(self.__current_task):
            rval = self.tasks[self.__current_task]
        return rval

    @property
    def etc(self):
        """
        Accessor for estimated time to completion

        :return:  estimated time to completion
        """
        rval = 0
        if self.current_task:
            rval = self.current_task.etc
        return rval

    @property
    def progress(self):
        """
        Accessor for progress status in percentage

        :return: percentage of job processed.
        """
        rval = 0
        if self.current_task:
            rval = self.current_task.progress
        return rval

    @property
    def stdout(self):
        """
        Accessor for nmap standart output

        :return: output from nmap scan in XML
        :rtype: string
        """
        return self.__stdout

    @property
    def stderr(self):
        """
        Accessor for nmap standart error

        :return: output from nmap when errors occured.
        :rtype: string
        """
        return self.__stderr

    # ---------------------------------------------
    @property
    def __addresses(self):

        addr = list()
        for target in self.targets.split(','):
            if "/" in target and "/32" not in target:
                try:
                    network = ipaddress.ip_network(unicode(target))
                    addr = [i.__str__() for i in network.hosts()]
                except Exception as e:
                    raise Exception(e)
            elif "/32" in target:
                addr.append(target.replace('/32', ''))
            else:
                addr.append(target)
        return addr

    @property
    def __ports(self):

        if not self.__options_conn_ports:
            raise Exception

        _ports = list()

        for _port in self.__options_conn_ports.split(','):
            if '-' not in _port:
                _ports.append(int(_port))
            else:
                _ports.extend(range(int(_port.split('-')[0]), int(_port.split('-')[1])))

        return _ports

    def __tcp_conn(self):

        start_time = int(time.time())
        task_name = 'TCP Connect'

        # 开始事件
        yield {'status': 'taskbegin', 'time': start_time, 'task': task_name}

        failed_count = 0
        try:

            for addr in self.__addresses:
                _op = list()    # 开放的端口
                _cl = list()    # 关闭的端口

                for port in self.__ports:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(self.timeout)

                        if s.connect_ex((addr, port)) == 0:
                            status = 'open'
                            _op.append(str(port))
                        else:
                            status = 'close'
                            _cl.append(str(port))
                        s.close()
                    except Exception as e:
                        failed_count += 1
                    self.__done_connect_count += 1

                percent = '{:.2f}'.format(float(self.__done_connect_count) / float(self.__target_conn_count) * 100)
                _stdout = {'address': addr, 'open': _op, 'close': _cl, 'status': 'unknown',
                           'service': {}, 'timestamp': int(time.time())}
                # 扫描过程中的事件
                yield {'status': 'taskprogress', 'task': task_name, 'stdout': _stdout, 'percent': percent,
                       'pregress': percent, 'remaining': self.__target_conn_count - self.__done_connect_count,
                        'etc': int(time.time()), 'updated': int(time.time())}
        except Exception as e:
            yield {'status': 'taskerror', 'time': int(time.time()), 'task': task_name, 'extrainfo': str(e)}

        # 扫描结束事件
        yield {'status': 'taskend', 'time': int(time.time()), 'task': task_name, 'extrainfo': 'failed:%d' % failed_count}

    def parse_options(self):

        # TODO：补充其他参数的解析
        for _opt in self.options.split(' '):
            if '-p' in _opt:
                self.__options_conn_ports = _opt.replace('-p', '')
                self.__options_conn_type = 'TCP Connect'


def mycallback(event_obj):
    # print(self.target, self.options, self.multi_process)
    try:
        current = event_obj.current_task
        task = event_obj.tasks[current.name]
        print(task.name, task.percent, task.status, task.remaining, task.progress)
    except (KeyError, AttributeError) as e:
        print(str(e))


if __name__ == '__main__':
    sp = SocketsProcess(targets='10.0.0.1/32,10.0.0.2', options='-sT -p22,80,443', event_callback=mycallback)
    sp.start()
    sp.join()

    import pprint
    pprint.pprint(sp.stdout)




