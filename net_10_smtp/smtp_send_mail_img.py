#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import re
import smtplib, email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import os


def qyt_smtp_attachment(mailserver, username, password, from_mail, to_mail, subj, main_body, images=None):
    # 使用SSL加密SMTP发送邮件, 此函数发送的邮件有主题,有正文,还可以发送附件
    tos = to_mail.split(';')  # 把多个邮件接受者通过';'分开
    date = email.utils.formatdate()  # 格式化邮件时间
    msg = MIMEMultipart()  # 产生MIME多部分的邮件信息
    msg["Subject"] = subj  # 主题
    msg["From"] = from_mail  # 发件人
    msg["To"] = to_mail  # 收件人
    msg["Date"] = date  # 发件日期

    # # 邮件正文为Text类型, 使用MIMEText添加, 参数描述了文本类型为HTML, 编码为utf-8
    # MIME类型介绍 https://docs.python.org/2/library/email.mime.html
    part = MIMEText(main_body, 'html', 'utf-8')
    msg.attach(part)  # 添加正文
    if images:
        for img in images:
            fp = open(img, 'rb')
            # MIMEXXX决定了什么类型 MIMEImage为图片文件
            # 添加图片
            images_mime_part = MIMEImage(fp.read())
            fp.close()
            # 添加头部! Content-ID的名字会在HTML中调用!
            images_mime_part.add_header('Content-ID', os.path.basename(img).split('.')[0])  # 这个部分就是cid: xxx的名字!
            # 把这个部分内容添加到MIMEMultipart()中
            msg.attach(images_mime_part)

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
    # 注意cid:Logo 对应头部里边的Content-ID的名称
    # ---------------------------- 案例一: 简单的图文 ----------------------------
    main_body_txt = """
    <h3>图片测试</h3>
    <p>这是乾颐堂公司LOGO图片。</p>
    <p>
    <br><img src="cid:Logo"></br>
    </p>
    <p>
    """
    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'anchwprpwxfbdbif',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        '图片测试',
                        main_body_txt,
                        ['./attachment_dir/Logo.jpg'])

    # ---------------------------- 案例二: 更加负载的HTML ----------------------------
    # 产生饼状图，后续嵌入到网页
    from net_10_smtp.modules.syslog_bing import syslog_bing
    syslog_result = syslog_bing('syslog.png')

    # 导入jinja2模块，并且定义模块所在目录
    from jinja2 import Template
    tem_path = './templates/'

    # x为级别名字(例如:ALERT), y为数量
    total = sum([y for x, y in syslog_result])
    # 产生替换模板的数据severity_list
    severity_list = [{'severity': x, 'count': y, 'percent': f"{(y/total)*100:.1f}"} for x, y in syslog_result]
    # 模板替换产生email的html
    with open(tem_path + 'email.jinja2', encoding='utf-8') as f:
        email_template = Template(f.read())
    email_html = email_template.render(severity_list=severity_list)

    # 发送邮件
    qyt_smtp_attachment('smtp.qq.com',
                        '3348326959@qq.com',
                        'anchwprpwxfbdbif',
                        '3348326959@qq.com',
                        '3348326959@qq.com;collinsctk@qytang.com',
                        '乾颐堂Python强化班Syslog分析',
                        email_html,
                        ['./word_pdf/src_img/logo.png', 'syslog.png'])
    # 删除没有用的图片
    import os
    os.remove('syslog.png')

