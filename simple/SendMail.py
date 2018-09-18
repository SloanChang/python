#!/usr/bin/python
#-*- coding:utf8 -*-
import sys
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging.config

def getLogger(loggerName):
    logging.config.fileConfig('logging.config')
    return logging.getLogger(loggerName)
props=getProperties()
logger=getLogger('polling')
def sendEmail(mailText,subject):
    try:
        email_from_user = props.get('email.from.user')
        email_from_password = props.get('email.from.password')
        email_to_user = props.get('email.to.user')
        email_smtp = props.get('email.smtp')
        logger.info('发送邮件,发件人:%s，登录密码:%s,收件人:%s,服务地址：%s'%(email_from_user,email_from_password,email_to_user,email_smtp))
        msg = MIMEMultipart()
        msg['from'] = email_from_user
        msg['to'] = email_to_user
        msg['subject'] = unicode(subject, 'utf-8')

        txt = MIMEText(mailText, 'html', 'utf-8')
        msg.attach(txt)
        smtpObj = smtplib.SMTP(email_smtp, '25')
        state = smtpObj.login(email_from_user, email_from_password)
        if state[0] == 235:
            smtpObj.sendmail('', email_to_user.split(','), msg.as_string())
        smtpObj.quit()
        logger.error("邮件发送成功")
        return True
    except Exception, e:
        logger.error("邮件发送异常：%s" % e.message)
        return False

def makeHtml(results,title):
    logger.info('加工html格式表格')
    d = ''  # 表格内容
    i = 0
    for result in results:
        i = i + 1
        d = d + """
                <tr>
                    <td width="50" align="center"> """ + str(i) + """</td>
                    <td width="50" align="center">""" + result[0] + """</td>
                    <td width="50" align="center">""" + result[1] + """</td>
                    <td width="50" align="center">""" + result[2] + """</td>
                    <td width="50" align="center">""" + result[3] + """</td>
                    <td width="50" align="center">""" + str(result[4]) + """</td>
                    <td width="50" align="center">""" + result[5] + """</td>
                </tr>"""
    html = """
                 <head>
                  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                  <body>
                   <div id="container">
                    <p><strong>""" + title + """</strong></p>
                     <div id="content">
                       <table width="80%" border="2" bordercolor="black" cellspacing="0" cellpadding="0">
                        <tr>
                          <td width="50" align="center"><strong>任务序号</strong></td>
                          <td width="50" align="center"><strong>工程名称</strong></td>
                          <td width="50" align="center"><strong>任务名称</strong></td>
                          <td width="50" align="center"><strong>开始时间</strong></td>
                          <td width="50" align="center"><strong>结束时间</strong></td>
                          <td width="50" align="center"><strong>任务耗时</strong></td>
                          <td width="50" align="center"><strong>运行状态</strong></td>
                        </tr>""" + d + """
                       </table>
                      </div>
                      </div>
                      </div>
                      </body>
                  </html>
            """
    logger.info('html格式表格加工完成')
    return html

html = makeHtml([],'您好！生产作业运行出现异常，请尽快查看，详情如下:')
sendEmail(html, '生产作业告警')