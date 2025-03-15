#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import re
import hashlib
from datetime import datetime
import os
from pathlib import Path
import sys
from sqlalchemy.orm import sessionmaker
from config_diff_1_create_table import RouterConfig
from config_diff_2_dff_conf import html_diff_snippet
from qyt_send_mail import qyt_smtp_attachment_html
from jinja2 import Template
from sqlalchemy import create_engine
from config_diff_0_ai import ai_diff
# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
current_dir = current_file_path.parent

# 插入tools路径到搜索路径
parent_dir = current_file_path.parent.parent
tools_dir = f'{parent_dir}{os.sep}tools'
sys.path.insert(1, tools_dir)
sys.path.insert(1, current_dir)
from config_diff_0_netmiko_show import netmiko_show_cred


def get_md5_config(host, username, password):
    try:
        # 获取完整的running-configuration
        device_config_raw = netmiko_show_cred(host,
                                              username,
                                              password,
                                              'show run',
                                              device_type='cisco_ios')
        # print(device_config_raw)
        split_result = re.split(r'\nhostname \S+\n', device_config_raw)
        run_config = device_config_raw.replace(split_result[0], '').strip()
        # 计算MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 返回ip, 时间, 配置, md5值
        return host, datetime.now(), run_config, md5_value
    except Exception as e:
        print('%stErrorn %s' % (host, e))


def config_diff_and_notification():
    engine = create_engine('postgresql+psycopg2://qytangdbuser:Cisc0123@196.21.5.218/qytangdb',
                           connect_args={"options": "-c timezone=Asia/Chongqing"})
    Session = sessionmaker(bind=engine)
    session = Session()

    host = "196.21.5.211"
    username = "admin"
    password = "Cisc0123"

    r = get_md5_config(host, username, password)

    if r:
        # 查询数据库中此设备最后一次记录
        last_record = session.query(RouterConfig).filter(RouterConfig.device_ip == host).\
            order_by(RouterConfig.record_time.desc()).first()

        current_md5 = r[3]
        current_config = r[2]

        # 如果有历史记录并且MD5不同
        if last_record and last_record.md5 != current_md5:
            # ---------------------- 产生diff片段 -------------------------------
            diff_snippet = html_diff_snippet(last_record.config, current_config)

            # -----------------------AI对变更进行分析------------------------------
            ai_diff_content = ai_diff(diff_snippet)
            print(ai_diff_content)
            # -----------------------AI对变更进行分析------------------------------

            # 使用Jinja2模板产生最终HTML
            # 这里假设notify_template.jinja2中包含{{ diff_content }}作为占位符
            template_path = f"{current_dir}{os.sep}html_template{os.sep}notify_template.jinja2"
            with open(template_path, 'r', encoding='utf-8') as f:
                template = Template(f.read())
                mail_html = template.render(diff_content=diff_snippet,
                                            ai_diff_content=ai_diff_content)

            # 发送邮件通知
            qyt_smtp_attachment_html('smtp.qq.com',
                                     '3348326959@qq.com',
                                     'anchwprpwxfbdbif',  # QQ SMTP授权码
                                     '3348326959@qq.com',
                                     '3348326959@qq.com;collinsctk@qytang.com',
                                     '配置发生改变通知',
                                     mail_html)

        # 无论有没有变化，都插入当前配置到数据库
        router_config = RouterConfig(
            device_ip=r[0],
            record_time=r[1],
            config=r[2],
            md5=r[3]
        )
        session.add(router_config)
        session.commit()


if __name__ == '__main__':
    config_diff_and_notification()

