#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
端口扫描任务结果处理

"""

from __future__ import print_function
from __future__ import absolute_import
import time
from pmon.mongo import mongo


class PortParser(object):

    def __init__(self, tag):
        __mapper = {
            'PORT_CHEK': self.port_scan,
            'PORT_DISC': self.port_scan,
            'PORT_INFO': self.port_serv,
            'HOST_DISC': self.host_disc,
            'PORT_RISK': self.port_scan
        }
        self.func = __mapper[tag]

    def __call__(self, report, param):

        try:
            self.func(report, param)
        except Exception as e:
            raise Exception("port: [%s] report: %s  param: %s" % (str(e), str(report), str(param)))

    def port_scan(self, report, param):
        """
        处理普通端口扫描返回的结果
        :param report: 扫描结果
        :param param: 扫描参数
        :return:
        """

        # 更新端口状态
        for res in report['result']:
            # 处理开放的端口
            for port in res['open']:
                mongo.db.port.update_one({'ip': res['address'], 'port': port}, {
                    '$set': {
                        'update_time': res['timestamp'],
                        'status': 'OPEN',
                        'failed_times': 0
                    },
                    '$setOnInsert': self._default_on_insert(res['timestamp'])
                }, upsert=True)

            # 处理关闭的端口
            for port in res['close']:
                mongo.db.port.update_one({'ip': res['address'], 'port': port}, {
                    '$set': {'update_time': res['timestamp']},
                    '$inc': {'failed_times': 1}
                })
                # 如果失败次数超过3次，认为该端口是关闭的
                _port_status = mongo.db.port.find_one({'ip': res['address'], 'port': port})
                if _port_status and _port_status['failed_times'] >= 3:
                    mongo.db.port.update_one({'ip': res['address'], 'port': port}, {
                        '$set': {'status': 'CLOSE'}
                    })

    def port_serv(self, report, param):
        """
        处理详细端口扫描返回的结果, 指nmap -sV
        :param report: 扫描结果
        :param param: 扫描参数
        :return:
        """
        for host in report['result']:
            for _service in host['service']:
                _service['update_time'] = host['timestamp']
                _port_on_insert = self._default_on_insert(host['timestamp'])
                _port_on_insert.pop('detail')
                mongo.db.port.update_one({'ip': host['address'], 'port': _service.pop('port')}, {
                    '$set': {
                        'detail': _service,
                        'update_time': host['timestamp']
                    },
                    '$setOnInsert': _port_on_insert
                    }, upsert=True)

    def host_disc(self, report, param):
        """
        处理主机发现返回的结果
        :param report: 扫描结果
        :param param: 扫描参数
        :return:
        """

        _up = [i['address'] for i in report['result'] if i['status'] == 'up']
        _down = [i['address'] for i in report['result'] if i['status'] == 'down']
        __now = int(time.time())
        _disc_on_insert = self._default_on_insert(__now)
        _disc_on_insert.pop('detail')
        _disc_on_insert.pop('ticket_info')

        for res in report['result']:
            _range = get_address_range(res['address'], param['address'])
            if res['status'] == 'up':
                mongo.db.ipset.update_many({'ip': res['address']}, {
                    '$set': {
                        'status': 'UP',
                        'failed_times': 0,
                        'update_time': __now,
                        'range': _range
                    },
                    '$setOnInsert': _disc_on_insert}, upsert=True)
            else:
                mongo.db.ipset.update_many({'ip': res['address']}, {
                    '$set': {
                        'status': 'DOWN',
                        'update_time': __now,
                        'range': _range
                    },
                    '$inc': {'failed_times': 1},
                    '$setOnInsert': _disc_on_insert})

        _ip_status = mongo.db.ipset.delete_many({'failed_times': {'$gt': 3}})

    @staticmethod
    def _default_on_insert(timestamp):
        """
        新增记录，默认补充的字段;
        :param timestamp:
        :return:
        """
        return {
            'discover_time': timestamp,
            'assets': {
                'host': 'NA',
                'owner': 'NA',
                'sys_code': 'NA',
                'business': 'NA',
            },
            'ticket_info': {
                'status': 'UNREPORTED',
                'ticket_id': 'NA',
                'owner': 'NA',
                'remark': 'NA',
                'create_time': 0,
                'source': 'NA'
            },
            'detail': {
                'service': '',
                'banner': '',
                'update_time': ''
            }
        }


def get_address_range(addr, target_address):
    """
    从扫描参数的address字段中提取出与某个IP的网段
    :param addr: 需要查找的地址
    :param target_address: 参数中的address值
    :return:
    """

    import ipaddress
    targets = target_address.replace(' ', '').split(',')
    for target in targets:
        if not isinstance(target, str):
            target = target.decode('utf-8')
        if addr in [str(i) for i in ipaddress.IPv4Network(target, strict=False).hosts()]:
            return target
    return addr
