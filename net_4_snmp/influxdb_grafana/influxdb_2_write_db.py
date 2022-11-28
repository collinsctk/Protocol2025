#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


import datetime
from influxdb import InfluxDBClient
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host

client = InfluxDBClient(influx_host, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')

current_time = datetime.datetime.utcnow().isoformat("T")
body = [
    {
        "measurement": "router_monitor_insert",
        "time": current_time,
        "tags": {
            "device_ip": "10.1.1.1",
            "device_type": "IOS-XE"
        },
        "fields": {
            "cpu_usage": 43,
            "mem_usage": 30000,
            "mem_free": 60000,
        },
    }
]
res = client.write_points(body)
measurements_result = client.query('show measurements;')  # 显示数据库中的表
for x in measurements_result.get_points():
    print(x)
print('-' * 100)
router_monitor_result = client.query('select * from router_monitor_insert;')
print(router_monitor_result)
for x in router_monitor_result.get_points('router_monitor_insert'):
    print(x)

