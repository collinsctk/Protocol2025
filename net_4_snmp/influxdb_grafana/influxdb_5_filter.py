from dateutil import parser
from influxdb import InfluxDBClient
from datetime import timedelta, timezone
import pytz
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host, router_ip

tzutc_8 = timezone(timedelta(hours=8))
utc = timezone(timedelta(hours=0))

client = InfluxDBClient(influx_host, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')


# 基于时间增量进行过滤
router_monitor_result = client.query('select cpu_usage from router_monitor where time > now() - 1d group by "device_ip", "device_type"')
# print(router_monitor_result)
# {'('router_monitor', {'device_ip': '192.168.1.2', 'device_type': 'IOS-XE'})': [{'time': '2020-09-02T01:20:08.590070Z', 'cpu_usage': 14}, ...
for x in router_monitor_result.get_points(tags={'device_ip': router_ip, 'device_type': 'IOS-XE'}):
    print(x)

print('-' * 100)
# 基于具体时间范围进行过滤
start_datetime = parser.parse('2020-11-21 14:00:00').astimezone(pytz.utc).isoformat("T")
# start_datetime = parser.parse('2020-09-02T09:21:00+08:00').astimezone(pytz.utc).isoformat("T")
end_datetime = parser.parse('2020-11-21 14:08:00').astimezone(pytz.utc).isoformat("T")
# end_datetime = parser.parse('2020-09-02T09:25:00+08:00').astimezone(pytz.utc).isoformat("T")

router_monitor_result = client.query(f"select cpu_usage from router_monitor where time > '{start_datetime}' and time < '{end_datetime}' group by \"device_ip\", \"device_type\"")
for x in router_monitor_result.get_points(tags={'device_ip': router_ip, 'device_type': 'IOS-XE'}):
    print(x)
