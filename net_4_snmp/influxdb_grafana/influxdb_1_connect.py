#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

from influxdb import InfluxDBClient

influx_host = '10.1.1.180'
router_ip = "10.1.1.253"
snmp_community = "tcpipro"

if __name__ == '__main__':
    client = InfluxDBClient(influx_host, 8086, 'admin', 'Cisc0123')

    # 查看数据库 
    print(client.get_list_database())
    # 创建数据库
    print(client.create_database('testdb'))
    print(client.get_list_database())
    # 删除数据库
    print(client.drop_database('testdb'))
    print(client.get_list_database())

    client = InfluxDBClient(influx_host, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')
    measurements_result = client.query('show measurements;')  # 显示数据库中的表
    print(f"Result: {format(measurements_result)}")

    retention_result = client.query('show retention policies on "qytdb";')  # 显示数据库中的表
    print(f"Result: {format(retention_result)}")


