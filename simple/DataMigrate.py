# #!/bin/python
# # -*- coding: utf-8-*-
'''oracle同步数据至mysql
查询oracle的数据插入mysql'''
import cx_Oracle
import MySQLdb

try:
    pros = config.getProperties()
    connection = cx_Oracle.Connection(pros.get("oracle.user"),config.getplaintext(pros.get("oracle.passwd")),pros.get("oracle.host"), events = True)
    cu=connection.cursor()
    cu.execute("select * from %s"% pros.get("oracle.table"))
    results=cu.fetchall()
    mqconn = MySQLdb.connect(host=pros.get("mysql.host"), port=3306, user=pros.get("mysql.user"), passwd=config.getplaintext(pros.get("mysql.passwd")), db=pros.get("mysql.db"), charset="utf8")
    cursor = mqconn.cursor()
    sql="replace into {} values ({}%s)".format(pros.get("mysql.table"),"%s," *(len(results[0])-1))
    print results
    cursor.executemany(sql,results)
    mqconn.commit()
    del results
    cu.close()
    connection.close()
    cursor.close()
    mqconn.close()
except Exception,e:
    print e
