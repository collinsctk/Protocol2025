#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# pip install python-docx
# pip install docx2pdf

import os
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import platform
import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
project_root = current_file.parent.parent
current_dir = current_file.parent
sys.path.append(str(project_root))
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
    # 获取环境变量
    smtp_user = os.environ.get('SMTPUSER')
    smtp_password = os.environ.get('SMTPPASS')
    smtp_from = os.environ.get('SMTPFROM')
    qyt_smtp_attachment("smtp.qq.com",
                        smtp_user,
                        smtp_password,
                        smtp_from,
                        '3348326959@qq.com;collinsctk@qytang.com',
                        '附件测试_主题',
                        '附件测试_正文\r\n行1\r\n行2',
                        [f'{current_dir}{os.sep}word_pdf{os.sep}src_img{os.sep}logo.png'])

    # 下面代码由于涉及到MS Office所以需要在Windows下运行
    from net_10_smtp.word_pdf.create_word_for_syslog import create_word_for_syslog

    create_word_for_syslog(f'{current_dir}{os.sep}word_pdf{os.sep}src_img{os.sep}logo.png',
                           f'{current_dir}{os.sep}word_pdf{os.sep}saved_word{os.sep}syslog.docx')

    if platform.system() == "Linux":
        """
        -------------Linux操作记录----------------
        # 安装LibreOffice：
        yum install libreoffice
        
        # 下载并安装Noto Sans CJK字体
        cd /usr/share/fonts
        sudo wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKsc-hinted.zip
        sudo unzip NotoSansCJKsc-hinted.zip -d noto
        sudo fc-cache -fv
        
        """
        print('System is Linux')
        import os
        os.popen(f"libreoffice --headless "
                 f"--convert-to pdf "
                 f"--outdir {current_dir}{os.sep}word_pdf{os.sep}saved_pdf {current_dir}{os.sep}word_pdf{os.sep}saved_word{os.sep}syslog.docx")
    elif platform.system() == "Windows":
        print('System is Windows')
        from docx2pdf import convert
        convert(f'{current_dir}{os.sep}word_pdf{os.sep}saved_word{os.sep}syslog.docx',
                f'{current_dir}{os.sep}word_pdf{os.sep}saved_pdf{os.sep}syslog.pdf')
    qyt_smtp_attachment("smtp.qq.com",
                        smtp_user,
                        smtp_password,
                        smtp_from,
                        '3348326959@qq.com;collinsctk@qytang.com',
                        'Syslog分析报告',
                        '详情请看附件',
                        [f'{current_dir}{os.sep}word_pdf{os.sep}saved_word{os.sep}syslog.docx', 
                         f'{current_dir}{os.sep}word_pdf{os.sep}saved_pdf{os.sep}syslog.pdf'])
