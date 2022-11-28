#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from influxdb import InfluxDBClient
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host

client = InfluxDBClient(influx_host, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')

series_result = client.query('show series from router_monitor;')

# 其实就是查询表中有几种tag的组合
# ResultSet({'('results', None)': [{'key': 'router_monitor,device_ip=192.168.1.1,device_type=IOS-XE'}, {'key': 'router_monitor,device_ip=192.168.1.2,device_type=IOS-XE'}]})

for x in series_result.get_points('results'):
    print(x)
