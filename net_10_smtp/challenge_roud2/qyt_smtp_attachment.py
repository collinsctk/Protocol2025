#!/usr/bin/env python3
# -*- coding=utf-8 -*-
import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, files=None):
    tos = to_mail.split(';')
    date = email.utils.formatdate()
    msg = MIMEMultipart()
    msg["Subject"] = subj
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg["Date"] = date

    part = MIMEText(main_body)
    msg.attach(part)

    if files:
        for file in files:
            part = MIMEApplication(open(file, 'rb').read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            msg.attach(part)

    server = smtplib.SMTP_SSL(mailserver, 465)
    server.login(username, password)
    failed = server.sendmail(from_mail, tos, msg.as_string())
    server.quit()
    if failed:
        print('Falied recipients:', failed)
    else:
        print('send email success!')


if __name__ == '__main__':
    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'anchwprpwxfbdbif',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        'test',
                        'test\r\nline 1\r\nline 2')

