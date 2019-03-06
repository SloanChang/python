#!/bin/python
# -*- coding: UTF-8 -*-
import argparse
import pandas as pd
import logging
from sqlalchemy import create_engine
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from sqlalchemy import Float,VARCHAR,Integer
import os

# 声明参数解析器
parse = argparse.ArgumentParser(description="load  excel data to database table")
# -P参数 在scan类型时，指定文件所在家目录
parse.add_argument('-P', '--path',default=None, help='excel file home path')
# -f 文件名，scan时指定文件名的不变化部分，在single时指定文件全路径
parse.add_argument('-f', '--file', required=True, help='excel file name')
# -s ecxcel文件需加载的sheetname
parse.add_argument('-s', '--sheetname', required=True, help='excel sheetname')
# -sr 读取excel开始行数，默认数为0
parse.add_argument('-sr', '--start_row', default=0, type=int, help='read excel start row number,default is 0,this row will become to columns name')
# -sf 从尾行开始指定忽略行数，默认数为0
parse.add_argument('-sf', '--skip_footer', default=0, type=int, help='skip row number from footer,defalut is 0')
# -c 指定列区间或列名
parse.add_argument('-c', '--cols',default=None, help='columns name list or columns range')
# -ac 指定列区间或列名
parse.add_argument('-ac', '--add_column',default=None, help='add column (column name and values)')
# -U oracle连接的url
parse.add_argument('-U', '--url', required=True, help='database URL')
# -u oracle连接的用户名
parse.add_argument('-u', '--user', required=True, help='database user')
# -p oracle连接的密码
parse.add_argument('-p', '--password', required=True, help='database password')
# -t 目标表名
parse.add_argument('-t', '--tablename', default=None, help='target tablename,defalut use sheetname')
# -i 写入类型 在表存在时 fail不做任何动作，replace 删表重建后写入，append追加写入，若不存在会创建
parse.add_argument('-i', '--insert', default='fail', choices=["fail", "replace", "append"],
               help="insert type,default 'fail',- fail: If table exists, do nothing.- replace: If table exists, drop it, recreate it, and insert data.- append: If table exists, insert data.Create if does not exist.")
# -v 详细日志 DEBUG级别
parse.add_argument('-v', '--version', action="store_true", help='DEBUG level log message')
args = parse.parse_args()
level="INFO"
if args.version:
    level = "DEBUG"
pd.set_option('display.width',2000)
path=os.path.dirname(os.path.abspath(__file__))+"/"
format='[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d][%(funcName)s][%(name)s][%(message)s]'
trfh = TimedRotatingFileHandler(path + 'Dtransport.log', when='d', interval=1, backupCount=5)
trfh.setFormatter(logging.Formatter(format))
logger = logging.getLogger('Dtransport')
logger.setLevel(level)
logger.addHandler(trfh)

'''
加载excel文件至oracle
'''
def mapping_df_types(df):
    '''映射dataframe的数据类型
    :param df: dataframe
    :return: 映射dict
    '''
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        if "object" in str(j):
            dtypedict.update({i: VARCHAR(length=255)})
        if "float64" in str(j):
            dtypedict.update({i: Float()})
        if "int" in str(j):
            dtypedict.update({i: Integer()})
    return dtypedict

def transport(file,sheetname,url,user,password,tablename,insert,start,skip,cols,add_column):
    '''
    读取文件 写入数据库
    :param file:文件路径
     :param sheetname:sheet页名
    :param url:数据库连接
    :param user:用户名
    :param password:密码
    :param tablename:表名
    :param insert:写入类型
    :param start:开始行数
    :param skip:跳转行数
    :return:
    '''
    logger.info("加载文件：%s" % file)
    df = pd.read_excel(file, sheetname=sheetname,header=start,skip_footer=skip,parse_cols=cols)
    colus=[x for i,x in enumerate(df.columns) if ('Unnamed') in x]
    df.drop(colus,axis=1,inplace=True)
    if add_column:
        columns=add_column.split(',')
        for column in columns:
            if (":") in column and len(column.split(":"))==2:
                kv=column.split(":")
                df[kv[0]]=kv[1]
    dtypedict = mapping_df_types(df)
    engine = create_engine('oracle://{}:{}@{}'.format(user, password,url))
    if tablename is None:
        tablename=sheetname
    logger.info("写入数据库")
    # df.to_sql(tablename, con=engine, chunksize=1, if_exists=insert,index=False,dtype=dtypedict)

def scan(path,filename,sheetname, url, user, password, tablename, insert, start, skip,cols,add_column):
    '''
    扫描路径下所有符合条件的文件，匹配文件名
    :param path:文件夹路径
    :param filename:被匹配文件名
    :param sheetname:sheet页名
    :param url:数据库连接
    :param user:用户名
    :param password:密码
    :param tablename:表名
    :param insert:写入类型
    :param start:开始行数
    :param skip:跳转行数
    :return:
    '''
    logger.info("扫描目录：%s" % path)
    for path,dirs,files in os.walk(path):
        for file in files:
            if filename in file:
                file=os.path.join(path,file)
                transport(file, sheetname, url, user, password, tablename, insert, start, skip,cols,add_column)
    logger.info("文件加载入库完成")
def main():
    '''
    主函数
    解析参数，并分类处理
    :return:
    '''
    logger.info("加载参数信息...")
    # operation=args.operation
    # logger.debug("作业类型：{}模式".format(operation))
    file = args.file
    # if operation == "scan":
    path=args.path
    logger.debug("文件家目录:{}".format(path))
    logger.info("文件名:{}".format(file))
    # else:
    #     logger.debug("文件路径：{}".format(file))
    sheetname=args.sheetname
    logger.debug("文件读取sheetname:{}".format(sheetname))
    start_row=args.start_row
    logger.debug("文件读取开始行数：{}".format(start_row))
    skip_footer=args.skip_footer
    logger.debug("文件读取尾部省略行数：{}".format(skip_footer))
    cols=args.cols
    if cols:
        logger.debug("文件读取列区间：{}".format(cols))
    add_column=args.add_column
    if add_column:
        logger.debug("添加列信息：{}".format(add_column))
    url=args.url
    user=args.user
    password=args.password
    logger.info("目标数据库：url={}，user={}".format(url,user))
    tablename=args.tablename
    if tablename:
        logger.info("目标表名：{}".format(tablename))
    insert=args.insert
    logger.info("写入类型：{}".format(insert))

    scan(path,file,sheetname,url,user,password,tablename,insert,start_row,skip_footer,cols,add_column)

if __name__ == "__main__":
    main()