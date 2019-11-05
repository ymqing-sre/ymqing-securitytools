#!/usr/bin/env python
# -*- coding: utf-8 -*-
# cython: language_level=3
import smtplib
import os
from email.mime.text import MIMEText
from email.header import Header
from SecurityTools.tamper_defender import tamper_config
import time
import socket


def mail_sender(msg, sub_msg):
    log_root = tamper_config.log_root
    mail_host = tamper_config.mail_host
    mail_user = tamper_config.mail_user
    mail_pass = tamper_config.mail_pass
    sender = tamper_config.sender
    receivers = tamper_config.receivers
    localtime = time.asctime(time.localtime(time.time()))

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header('防篡改监控', 'utf-8')
    message['To'] = Header('尊敬的运维工程师', 'utf-8')

    subject = sub_msg
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        os.system("echo '%s--------邮件发送成功' >> %s/mail.log" % (localtime, log_root))
    except (smtplib.SMTPException, smtplib.SMTPConnectError, socket.gaierror):
        os.system("echo '%s--------Error:无法发送邮件' >> %s/mail.log" % (localtime, log_root))
