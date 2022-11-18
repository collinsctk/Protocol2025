#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tools.decorator_time import print_run_time


@print_run_time()
def qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, files=None):
    # 使用SSL加密SMTP发送邮件, 此函数发送的邮件有主题,有正文,还可以发送附件
    tos = to_mail.split(';')  # 把多个邮件接受者通过';'分开
    date = email.utils.formatdate()  # 格式化邮件时间
    msg = MIMEMultipart()  # 产生MIME多部分的邮件信息
    msg["Subject"] = subj  # 主题
    msg["From"] = from_mail  # 发件人
    msg["To"] = to_mail  # 收件人
    msg["Date"] = date  # 发件日期

    # 邮件正文为Text类型, 使用MIMEText添加
    # MIME类型介绍 https://docs.python.org/2/library/email.mime.html
    part = MIMEText(main_body)
    msg.attach(part)  # 添加正文

    if files:  # 如果存在附件文件
        for file in files:  # 逐个读取文件,并添加到附件
            # MIMEXXX决定了什么类型 MIMEApplication为二进制文件
            # 添加二进制文件
            part = MIMEApplication(open(file, 'rb').read())
            # 添加头部信息, 说明此文件为附件,并且添加文件名
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            # 把这个部分内容添加到MIMEMultipart()中
            msg.attach(part)

    server = smtplib.SMTP_SSL(mailserver, 465)  # 连接邮件服务器
    server.login(username, password)  # 通过用户名和密码登录邮件服务器
    failed = server.sendmail(from_mail, tos, msg.as_string())  # 发送邮件
    server.quit()  # 退出会话
    if failed:
        print('Falied recipients:', failed)  # 如果出现故障，打印故障原因！
    else:
        print('邮件已经成功发出！')  # 如果没有故障发生，打印'邮件已经成功发出！'！


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'dmyymagcazklcjie',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        '附件测试_主题',
                        '附件测试_正文\r\n行1\r\n行2',
                        ['./attachment_dir/Logo.jpg'])

    # 下面代码由于涉及到MS Office所以需要在Windows下运行
    from net_10_smtp.word_pdf.create_word_for_syslog import create_word_for_syslog
    from docx2pdf import convert
    create_word_for_syslog('./word_pdf/src_img/logo.png',
                           './word_pdf/saved_word/syslog-docx.docx')
    convert('./word_pdf/saved_word/syslog-docx.docx', './word_pdf/saved_pdf/syslog-pdf.pdf')
    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'dmyymagcazklcjie',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        'Syslog分析报告',
                        '详情请看附件',
                        ['./word_pdf/saved_word/syslog-docx.docx', './word_pdf/saved_pdf/syslog-pdf.pdf'])

