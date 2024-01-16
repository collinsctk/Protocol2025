#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

from net_4_snmp.snmp_v2.snmpv2_getall import snmpv2_getall

import time
import datetime
from influxdb import InfluxDBClient
from net_4_snmp.influxdb_grafana.influxdb_1_connect import (influx_host,
                                                            router_ip,
                                                            snmp_community,
                                                            influx_db,
                                                            influx_port,
                                                            influx_user,
                                                            influx_password,
                                                            )

client = InfluxDBClient(influx_host, influx_port, influx_user, influx_password, influx_db)
# client.query("drop measurement router_monitor")  # 删除表
# client.query("drop measurement if_monitor")  # 删除表


while True:
    # ----------------------写入CPU 内存数据------------------------
    getall_result = snmpv2_getall(router_ip, snmp_community)

    current_time = datetime.datetime.utcnow().isoformat("T")
    cpu_mem_body = [
        {
            "measurement": "router_monitor",
            "time": current_time,
            "tags": {
                "device_ip": getall_result.get('ip'),
                "device_type": "IOS-XE"
            },
            "fields": {
                "cpu_usage": getall_result.get('cpu_usage'),
                "mem_usage": getall_result.get('mem_usage'),
                "mem_free": getall_result.get('mem_free'),
            },
        }
    ]
    # print(cpu_mem_body)
    client.write_points(cpu_mem_body)
    # ----------------------写入接口进出数据------------------------
    current_time = datetime.datetime.utcnow().isoformat("T")
    if_bytes_body = []

    for if_info in getall_result.get('if_list'):
        if if_info.get('in_bytes') and if_info.get('out_bytes'):
            if_info_dict = {
                                "measurement": "if_monitor",
                                "time": current_time,
                                "tags": {
                                    "device_ip": getall_result.get('ip'),
                                    "device_type": "IOS-XE",
                                    "interface_name": if_info.get('name')
                                },
                                "fields": {
                                    "in_bytes": if_info.get('in_bytes'),
                                    "out_bytes": if_info.get('out_bytes'),
                                },
                            }
            if_bytes_body.append(if_info_dict)
    # print(if_bytes_body)
    client.write_points(if_bytes_body)
    time.sleep(5)
