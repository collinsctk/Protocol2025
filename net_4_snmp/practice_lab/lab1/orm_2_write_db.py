#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


import sys
import os
from pathlib import Path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()
# 当前目录的路径
current_dir = current_file_path.parent.parent
sys.path.insert(1, current_dir)
# 上一级目录的路径
parent_dir = current_file_path.parent.parent.parent
sys.path.insert(1, str(parent_dir))

from python_script.snmp_v3_4_get_all import snmpv3_get_all
from orm_1_create_table import RouterMonitor, db_filename



engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False',
                       # echo=True
                       )

Session = sessionmaker(bind=engine)
session = Session()


def get_info_writedb(ip_address, username, auth_key, priv_key):
    get_all_dict = snmpv3_get_all(ip_address, username, auth_key, priv_key)

    get_all_dict.pop('hostname')
    get_all_dict.pop('interface_list')
    router_monitor_record = RouterMonitor(**get_all_dict)
    session.add(router_monitor_record)
    session.commit()


if __name__ == '__main__':
    # ip地址与snmp community字符串
    ip_address = "196.21.5.211"
    username = "qytanguser"
    auth_key = 'Cisc0123'
    priv_key = 'Cisc0123'

    get_info_writedb(ip_address, username, auth_key, priv_key)


