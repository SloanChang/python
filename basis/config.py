#!/bin/python
# -*- coding: UTF-8 -*-
import logging.config
import ConfigParser
import os
from Crypto.Cipher import AES
import base64

PADDING = '\0'
HOME_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))+"/"
conf= ConfigParser.ConfigParser()
conf.read(HOME_PATH+"config/config.ini")

key = conf.get("CRYPT","password")
aiv = conf.get("CRYPT","ivparame")


def getConfig():
    return  conf

def getSubConfig(section):
    '''获取子配置项
    :param section:子配置项标签
    :return: 子配置信息
    '''
    return dict(conf.items(section))


def getPlainText(ciphertext):
    '''密文解析
    :param ciphertext: 密文文本
    :return: 明文文本
    '''
    generator = AES.new(key, AES.MODE_CBC, aiv)
    cryptedStr = base64.b64decode(ciphertext)
    recovery = generator.decrypt(cryptedStr)
    decryptedStr = recovery.rstrip(PADDING)
    return decryptedStr
