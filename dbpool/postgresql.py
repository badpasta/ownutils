#!/usr/bin/env python
#
# Author: Jingyu Wang <badpasta@gmail.com>
# 
# Environment:
# -*- coding: utf-8 -*-
# Python by version 2.7.
# momoko

from smalltools.Other import singleton
from smalltools.parseConfig import Options

from psycopg2 import connect
from tornado import gen
from tornado.gen import Return, coroutine
from tornado.ioloop import IOLoop
from contextlib import contextmanager

import momoko
import sys
import os
import datetime
import time
import psycopg2 


class Momoko(object):
    def connect(self, ioloop, host, 
                dbname, user, passwd, port=5432):
        
        dsn = (("dbname=%s user=%s password=%s \
                host=%s port=%d" %(dbname, user, passwd, host, port)))

        self.db = momoko.Pool(dsn=dsn, 
                              size=5,
                              ioloop=ioloop)
        future = self.db.connect()
        ioloop.add_future(future, lambda x: ioloop.stop())
        ioloop.start()
        try:
            future.result()
        except momoko.exceptions.PartiallyConnectedError, e:
            print "DB connection failed!! %s" %e
            sys.exit(0)

    @coroutine
    def insert(self, sql, **data):
        yield self.db.execute(sql, data)

    @coroutine
    def select(self, sql, **data):
        cursor = yield self.db.execute(sql, data)
        raise Return(cursor.fetchall())


@singleton
class Module(object):
    '''Used as a Single Object
    '''
    def __init__(self):
        pass

    @property
    def dsn(self):
        """
        Data Source Name
        """
        if not hasattr(self, '_dsn'):
            self._dsn = 'dbname=%s user=%s password=%s host=%s port=%d' % (
                Options.DBNAME, Options.DBUSER,
                Options.DBPASS, Options.DBSERVER, Options.DBPORT)
            return self._dsn

    @property
    def pg_db(self):
        if not hasattr(self, '_pg_db'):
            self._pg_db = momoko.Pool(
                    dsn = self.dsn,
                    size = 5,
                    ioloop = IOLoop.instance(),
                    setsession=(),
                    )

        return self._pg_db

    db = pg_db


class SyncPG(object):
    def __init__(self, **config):
        self.config_dict =  dict(
            database = config['database'],
            user = config['user'],
            password = config['password'],
            host = config['host'],
            port = config['port']
            )

    @contextmanager
    def execute_base(self):
        try:
            self.conn = connect(**self.config_dict)
            self.cursor = self.conn.cursor()
            yield self.cursor
        except psycopg2.DataError, e:
            print e
            self.cursor.close()
        except:
            self.cursor.close()
        finally:
            self.conn.commit()
            self.conn.close()

    def execute_query(self, sql_context, **data):
        with self.execute_base() as cur:
            cur.execute(sql_context, **data)
            result = cur.fetchall()
            return result

    def execute_push(self, sql_context, **data):
        with self.execute_base() as cur:
            cur.execute(sql_context, data)
