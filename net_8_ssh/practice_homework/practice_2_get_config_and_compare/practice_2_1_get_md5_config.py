#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from net_12_ssh.ssh_sftp.ssh_client_netmiko import netmiko_show_cred
import re
import hashlib
from datetime import datetime


def get_md5_config(host, username, password):
    try:
        # 获取完整的running-configuration
        device_config_raw = netmiko_show_cred(host, username, password, 'show run')
        print(device_config_raw)
        split_result = re.split(r'\nhostname \S+\n', device_config_raw)
        run_config = device_config_raw.replace(split_result[0], '').strip()
        # 计算MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 获取配置的MD5值
        # md5 = netmiko_show_cred(host, username, password, 'verify /md5 system:running-config')

        # 返回ip, 时间, 配置, md5值
        return host, datetime.now(), run_config, md5_value
    except Exception as e:
        print('%stErrorn %s' % (host, e))


if __name__ == '__main__':
    # print(get_md5_config('10.1.1.253', 'admin', 'Cisc0123'))
    import os
    import sqlite3
    db_path = './db_file/config_db.sqlite'
    # ========================= 创建数据库表 =========================
    # if os.path.exists(db_path):
    #     os.remove(db_path)
    # # 连接数据库
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # # 创建数据库
    # cursor.execute(r"create table router_config_md5(id INTEGER PRIMARY KEY AUTOINCREMENT, ip varchar(40), record_time timestamp, config varchar(99999), md5 varchar(1000))")

    # =========================== 插入数据 ==========================
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    r = get_md5_config('10.1.1.253', 'admin', 'Cisc0123')
    if r:
        cursor.execute("insert into router_config_md5(ip, record_time, config, md5) values(?, ?, ?, ?)", (r[0], r[1], r[2], r[3]))
        conn.commit()

