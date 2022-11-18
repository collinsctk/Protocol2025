from net_4_snmp.snmp_v2.snmpv2_get import snmpv2_get
from net_4_snmp.snmp_v2.snmpv2_getbulk import snmpv2_getbulk
import time
import datetime
from influxdb import InfluxDBClient
from net_4_snmp.influxdb_grafana.influxdb_1_connect import influx_host, router_ip, snmp_community

client = InfluxDBClient(influx_host, 8086, 'qytdbuser', 'Cisc0123', 'qytdb')
# client.query("drop measurement router_monitor")  # 删除表
# client.query("drop measurement if_monitor")  # 删除表


while True:
    # ----------------------写入CPU 内存数据------------------------
    # cpmCPUTotal5sec
    cpu_usage = snmpv2_get(router_ip, snmp_community, "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)

    # cpmCPUMemoryUsed
    mem_usage = snmpv2_get(router_ip, snmp_community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)

    # cpmCPUMemoryFree
    mem_free = snmpv2_get(router_ip, snmp_community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)

    current_time = datetime.datetime.utcnow().isoformat("T")
    cpu_mem_body = [
        {
            "measurement": "router_monitor",
            "time": current_time,
            "tags": {
                "device_ip": router_ip,
                "device_type": "IOS-XE"
            },
            "fields": {
                "cpu_usage": int(cpu_usage[1]),
                "mem_usage": int(mem_usage[1]),
                "mem_free": int(mem_free[1]),
            },
        }
    ]
    client.write_points(cpu_mem_body)
    # ----------------------写入接口进出数据------------------------
    # 进接口字节数
    in_bytes = snmpv2_getbulk(router_ip, snmp_community, "1.3.6.1.2.1.2.2.1.10", port=161)

    # 出接口字节数
    out_bytes = snmpv2_getbulk(router_ip, snmp_community, "1.3.6.1.2.1.2.2.1.16", port=161)

    gi1_in_bytes = in_bytes[0][1]
    gi1_out_bytes = out_bytes[0][1]

    current_time = datetime.datetime.utcnow().isoformat("T")
    if_bytes_body = [
        {
            "measurement": "if_monitor",
            "time": current_time,
            "tags": {
                "device_ip": router_ip,
                "device_type": "IOS-XE",
                "interface_name": "Gi1"
            },
            "fields": {
                "in_bytes": int(gi1_in_bytes),
                "out_bytes": int(gi1_out_bytes),
            },
        }
    ]
    client.write_points(if_bytes_body)
    time.sleep(5)
