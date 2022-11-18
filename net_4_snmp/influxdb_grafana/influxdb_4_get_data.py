from dateutil import parser
from influxdb import InfluxDBClient
from datetime import timedelta, timezone
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host, router_ip

tzutc_8 = timezone(timedelta(hours=8))

client = InfluxDBClient(influx_host, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')

router_monitor_result = client.query('select * from router_monitor;')
for x in router_monitor_result.get_points('router_monitor',  # 表measurement
                                          {
                                              'device_ip': router_ip,  # tag
                                              'device_type': 'IOS-XE'   # tag
                                          }):
    print(x)
    # 转换为时间对象, 并且切换时区
    print(parser.parse(x.get('time')).astimezone(tzutc_8))


print('-' * 80)

if_monitor_result = client.query('select * from if_monitor;')
# print(if_monitor_result)
for x in if_monitor_result.get_points('if_monitor',
                                      {
                                          'device_ip': router_ip,
                                          'device_type': 'IOS-XE',
                                          "interface_name": "Gi1"
                                      }):
    print(x)
