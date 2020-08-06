#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
节点相关

"""

from __future__ import print_function
from __future__ import absolute_import

from pmon.mongo import mongo


class Nodes(object):

    def __init__(self):
        self.collection = mongo.db.node
        self.nodes = [i for i in self.collection.find({'status': 'enable'}, {'_id': 0})]

    def get_node(self, name):

        _node = dict()
        for n in self.nodes:
            if n['name'] == name:
                _node = n
        if not _node:
            raise Exception("Can not find node name:[%s] in [%s]." % (name, self.collection))

        return _node

    def select_best_node(self):
        """
        选择最优节点

        TODO: 后期完成
        """
        return dict()
