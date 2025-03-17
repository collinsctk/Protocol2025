#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

from pathlib import Path
import sys
# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 上一级目录的路径
parent_dir = current_file_path.parent.parent.parent

# 添加上一级目录到 Python 路径
sys.path.insert(0, str(parent_dir))

from python_script.snmp_v2_4_get_all import snmpv2_get_all

import time
import datetime
from influxdb import InfluxDBClient

influx_host = '196.21.5.218'
router_ip = "196.21.5.211"
snmp_community = "qytangro"
influx_db = "qytdb"
influx_port = 8086
influx_measurement = "router_monitor"
influx_admin = "admin"
influx_user = "qytdbuser"
influx_password = "Cisc0123"


client = InfluxDBClient(influx_host, influx_port, influx_user, influx_password, influx_db)
# client.query("drop measurement router_monitor")  # 删除表
# client.query("drop measurement if_monitor")  # 删除表



# ----------------------写入CPU 内存数据------------------------
getall_result = snmpv2_get_all(router_ip, snmp_community)

current_time = datetime.datetime.now(datetime.UTC).isoformat("T")
cpu_mem_body = [
    {
        "measurement": "router_monitor",   # 可以认为是表名
        "time": current_time,     # 时间戳，时序数据库的核心
        "tags": {                 # 标签，用于过滤
            "device_ip": getall_result.get('ip'),
            "device_type": "IOS-XE"
        },
        "fields": {               # 字段，用于存储数据
            "cpu_usage": getall_result.get('cpu_usage'),
            "mem_usage": getall_result.get('mem_usage'),
            "mem_free": getall_result.get('mem_free'),
        },
    }
]
# print(cpu_mem_body)
client.write_points(cpu_mem_body)  # 写入数据库
# ----------------------写入接口进出数据------------------------
current_time = datetime.datetime.now(datetime.UTC).isoformat("T")

if_bytes_body = []  # 用于存储多个接口的字典

for if_info in getall_result.get('interface_list'):
    if if_info.get('in_bytes') and if_info.get('out_bytes'):
        if_info_dict = {
                            "measurement": "if_monitor",   # 可以认为是表名
                            "time": current_time,          # 时间戳，时序数据库的核心
                            "tags": {                      # 标签，用于过滤
                                "device_ip": getall_result.get('device_ip'),
                                "device_type": "IOS-XE",
                                "interface_name": if_info.get('interface_name')
                            },
                            "fields": {                    # 字段，用于存储数据
                                "in_bytes": if_info.get('in_bytes'),
                                "out_bytes": if_info.get('out_bytes'),
                            },
                        }
        if_bytes_body.append(if_info_dict)
# print(if_bytes_body)
client.write_points(if_bytes_body)  # 写入数据库
