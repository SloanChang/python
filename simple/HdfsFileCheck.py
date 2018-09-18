#!/usr/bin/python
#-*- coding:utf8 -*-
'''稽核hdfs下文件数量'''
import sys
import commands

#根据路径获取下一级目录
def getSubFilePath(path):
    status, results = commands.getstatusoutput("hdfs dfs -ls -R %s |grep .db|grep -v '\.hive'" % path)
    if status==0:
        return results.split("\n")
    else:
        sys.exit(status)


def reduceFile(checkResult):
    for cr in checkResult.keys():
        if checkResult.get(cr) <= 2000:
            checkResult.pop(cr)
    return checkResult

#根据路径获取该目录下文件数
def check():
    results=getSubFilePath("/")
    checkResult={}
    for result in results:
        if result.startswith("d"):
            checkResult[result.split(" ")[-1]] = 0
        elif result.startswith("-"):
            result = result.split(" ")[-1]
            dire = result.replace("/" + result.split("/")[-1], "")
            if checkResult.has_key(dire):
                checkResult[dire] = checkResult.get(dire) + 1
            else:
                checkResult[dire] = 1
    checkResult = reduceFile(checkResult)
    if len(checkResult)>0:
        checkResult=sorted(checkResult.items(), key=lambda x: x[1], reverse=True)
        print checkResult
