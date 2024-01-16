#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


import time
from net_4_snmp.snmp_v2.snmpv2_get import snmpv2_get
from sqlalchemy.orm import sessionmaker
from orm_1_create_table import RouterMonitor, db_filename
from sqlalchemy import create_engine


engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False',
                       # echo=True
                       )

Session = sessionmaker(bind=engine)
session = Session()


def get_info_writedb(ip, rocommunity, seconds):
    while seconds > 0:
        # cpmCPUTotal5sec
        cpu_info = snmpv2_get(ip, rocommunity, "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)[1]
        # cpmCPUMemoryUsed
        memu_info = snmpv2_get(ip, rocommunity, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)[1]
        # cpmCPUMemoryFree
        memf_info = snmpv2_get(ip, rocommunity, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)[1]
        router_monitor_record = RouterMonitor(
            device_ip=ip,
            cpu_useage_percent=cpu_info,
            mem_use=memu_info,
            mem_free=memf_info
        )
        session.add(router_monitor_record)
        session.commit()
        # 每五秒采集一次数据
        time.sleep(5)
        seconds -= 5


if __name__ == '__main__':
    # ip地址与snmp community字符串
    ip_address = "10.10.1.1"
    community = "tcpipro"

    get_info_writedb(ip_address, community, 60)
    for i in session.query(RouterMonitor).all():
        print(i)
