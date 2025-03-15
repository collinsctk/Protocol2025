#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


import time
from snmp_v3_3_get_all import snmpv3_get_all
from sqlalchemy.orm import sessionmaker
from orm_1_create_table import RouterMonitor, engine
from datetime import timezone, timedelta, datetime

Session = sessionmaker(bind=engine)
session = Session()

ip_address = "196.21.5.211"
username = "qytanguser"
auth_key = 'Cisc0123'
priv_key = 'Cisc0123'

gmt_8 = timezone(timedelta(hours=8))


def get_info_writedb(ip_address, username, auth_key, priv_key):
    get_all_dict = snmpv3_get_all(ip_address, username, auth_key, priv_key)
    get_all_dict.pop('hostname')
    get_all_dict.pop('interface_list')
    update_record_time = datetime.now().astimezone(gmt_8)
    get_all_dict['record_datetime'] = update_record_time
    router_monitor_record = RouterMonitor(**get_all_dict)
    session.add(router_monitor_record)
    session.commit()


