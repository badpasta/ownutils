#!/usr/bin/env python
# -*- coding: utf-8 -*-
# # Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# Python by version 2.7.
# request = ['redis']

from redis import ConnectionPool,Redis
from contextlib import contextmanager


class NonAsyncRedis(object):
    def __init__(self, server='127.0.0.1', port=6379,db=0): 
        pool = ConnectionPool(host=server, port=port,db=db)
        self.redis = Redis(connection_pool=pool)
        self.pipe = self.redis.pipeline()

    def push(self, param, key, *args):
        message = str()
        if not self.redis.llen(key):
            p = eval('self.pipe.'+param)
            message = p(key, *args)
            self.pipe.execute()
        return message

    def get(self, param, key, *args):
        message = str()
        if self.redis.llen(key):
            p = eval('self.redis.'+param)
            message = p(key, *args)
        return message

    def parseData(self, key, *args): pass

