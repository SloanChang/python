#!/bin/python
# -*- coding:utf-8 -*-
import logging
import os
from logging.handlers import TimedRotatingFileHandler

class log:
    def __init__(self,name,level):
        self.path=os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))+"/"
        self.name = name
        self.level = level
        self.file_name=self.name+'.log'
        self.format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d][%(funcName)s][%(name)s][%(message)s]'
    def get(self):
        trfh=TimedRotatingFileHandler(self.path+"logs/"+self.file_name, when='d', interval=1, backupCount=5)
        trfh.setFormatter(logging.Formatter(self.format))
        logger=logging.getLogger(self.name)
        logger.setLevel(self.level)
        logger.addHandler(trfh)
        return logger

def getLogger(name,leavel=logging.INFO):
    return log(name,leavel).get()
