#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from threading import Thread
import time
import pprint
from lxml import html
import json
import requests
import urllib3
import logging

urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MAX_CONTENT_LENGTH = 200

DEFAULT_PAGE_TITLE = [
    'Welcome to OpenResty!',
    'Welcome to nginx!',
    'IIS Windows Server',
    'Welcome to tengine!',
    'Test Page for the Nginx HTTP Server on Fedora',
    'Test Page for the Nginx HTTP Server on EPEL'
]

logger = logging.getLogger()


class WebCheckProcess(Thread):

    def __init__(self, targets="127.0.0.1", options="-p80", event_callback=None):
        Thread.__init__(self)
        self.address = targets
        self.event_callback = event_callback
        self.stdout = list()
        self.ports = list()
        self.parse_options(options)

    def run(self):

        for port in self.ports:
            res = self._request(self.address, port)
            if self.event_callback:
                self.event_callback(res)
            self.stdout.append(res)

        return self.stdout

    def _request(self, address, port):

        if int(port) == 443:
            url = "https://%s" % address
        else:
            url = "http://%s:%s" % (address, str(port))

        title = ""
        headers = {'Content-Type': '*'}
        try:
            res = requests.get(url, headers=headers, verify=False, timeout=5)
            res_content = res.text
            res_code = res.status_code
            res_headers = dict(res.headers)

            if res.encoding:
                res_content = res_content.encode(res.encoding)

            title, tag, res_content = self.parse_content(res_content)
            message = 'Success'
            status = 'ACCESSIBLE'

        except Exception as e:
            tag = 'Failure'
            res_code = 1
            res_headers = dict()
            res_content = ''
            message = e.__class__.__name__
            status = 'INACCESSIBLE'

        report = {
            'url': url,
            'code': res_code,
            'headers': res_headers,
            'title': title,
            'tag': tag,
            'content': str(res_content),
            'message': message,
            'status': status,
            'timestamp': int(time.time())
        }

        return report

    def parse_options(self, options):
        """

        :param options:
        :return:
        """

        for opt in options.split(' '):
            if '-p' in opt:
                self._opt_p(opt)

    def _opt_p(self, opt):
        """
        解析 -p 配置
        :param opt:
                -p80,443
                -p80-88,443,90
        :return:
        """

        for op in opt.replace('-p', '').split(','):
            if "-" in op:
                _s, _e = op.split('-')
                self.ports.extend([str(p) for p in range(int(_s), int(_e) + 1)])
            else:
                self.ports.append(op)

    def parse_content(self, content):

        def _try_json(con):

            return json.dumps(json.loads(con))

        def _try_html(con):

            _title = ''
            tree = html.fromstring(con)
            try:
                if tree is not None:
                    _title = tree.xpath('//title/text()')[0]

            except IndexError as e:
                _title = ''

            return _title

        content.rstrip()

        try:
            content = _try_json(content)
            title = ''
            tag = 'Api'
        except ValueError as e:
            title = _try_html(content)
            if not title:
                tag = self.pickup_tag(title, content)
            else:
                tag = 'Web'
            content = content[:MAX_CONTENT_LENGTH]

        return title, tag, content

    @staticmethod
    def pickup_tag(title, content):

        if title in DEFAULT_PAGE_TITLE:
            return 'DefaultPage'
        else:
            return 'Unknown'


def print_item(report):
    pprint.pprint(report)


if __name__ == '__main__':

    w = WebCheckProcess(targets='127.0.0.1', options='-p5555,80', event_callback=print_item)
    w.run()
    print(w.report)