#!/bin/python
# -*- coding:utf-8 -*-

from sqlalchemy import create_engine


def getEngine(database, user, password, port, db, host='localhost'):
    return create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(database, user, password, host, port, db))