#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from influxdb import InfluxDBClient
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host

client = InfluxDBClient(influx_host, 8086, 'admin', 'Cisc0123', 'qytdb')

# https://help.aliyun.com/document_detail/113126.html
# COUNT()
# DISTINCT()
# INTEGRAL()
# MEAN()
# MEDIAN()
# MODE()
# SPREAD()
# STDDEV()
# SUM()

# 可以计算采集次数
# ResultSet({'('router_monitor', {'device_ip': '192.168.1.1', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'count': 187}],
# '('router_monitor', {'device_type': 'IOS-XE', 'device_ip': '192.168.1.2'})': [{'time': '1970-01-01T00:00:00Z', 'count': 220}]})
count_result = client.query('select COUNT("cpu_usage") from router_monitor group by \"device_ip\", \"device_type\";')
print(count_result)
for x in count_result.get_points():
    print(x)

# 计算平均值
# ResultSet({'('router_monitor', {'device_ip': '192.168.1.1', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'mean': 14.031818181818181}], '('router_monitor', {'device_ip': '192.168.1.2', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'mean': 13.49090909090909}]})
mean_result = client.query('select MEAN("cpu_usage") from router_monitor group by \"device_ip\", \"device_type\";')
print(mean_result)
for x in mean_result.get_points():
    print(x)

# 计算中位数
# ResultSet({'('router_monitor', {'device_ip': '192.168.1.1', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'median': 13.0}], '('router_monitor', {'device_ip': '192.168.1.2', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'median': 13.0}]})
median_result = client.query('select MEDIAN("cpu_usage") from router_monitor group by \"device_ip\", \"device_type\";')
print(median_result)
for x in median_result.get_points():
    print(x)

# 出现频率最高的值
# ResultSet({'('router_monitor', {'device_ip': '192.168.1.1', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'mode': 13}], '('router_monitor', {'device_ip': '192.168.1.2', 'device_type': 'IOS-XE'})': [{'time': '1970-01-01T00:00:00Z', 'mode': 13}]})
mode_result = client.query('select MODE("cpu_usage") from router_monitor group by \"device_ip\", \"device_type\";')
print(mode_result)
for x in mode_result.get_points():
    print(x)


# SPREAD() 最大值和最小值之差
# STDDEV() 标准差
# SUM() 总和

# 最小的N个field value
# ResultSet({'('router_monitor', {'device_ip': '192.168.1.1', 'device_type': 'IOS-XE'})': [{'time': '2020-09-02T01:53:09.995514Z', 'bottom': 11}, {'time': '2020-09-02T02:05:45.686996Z', 'bottom': 10}, {'time': '2020-09-02T02:15:24.835640Z', 'bottom': 10}], '('router_monitor', {'device_type': 'IOS-XE', 'device_ip': '192.168.1.2'})': [{'time': '2020-09-02T01:20:25.788793Z', 'bottom': 10}, {'time': '2020-09-02T01:23:08.103539Z', 'bottom': 10}, {'time': '2020-09-02T01:24:02.128114Z', 'bottom': 9}]})
bottom_result = client.query('select BOTTOM("cpu_usage", 3) from router_monitor group by \"device_ip\", \"device_type\";')
print(bottom_result)
for x in bottom_result.get_points():
    print(x)

# FIRST() 返回具有最早时间戳的field value。
# LAST() 返回具有最新时间戳的field value。
# MAX() 返回field value的最大值。
# MIN() 返回field value的最小值。
# SAMPLE() 返回包含N个field value的随机样本
# TOP() 返回最大的N个field value。

