#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

import asyncio
from pathlib import Path
import sys

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

sys.path.insert(1, str(current_file_path.parent))
from snmp_v3_1_get import snmpv3_get
from snmp_v3_3_getbulk import snmpv3_getbulk

# ~~~~~~~~~~~~~~~~注意版本~~~~~~~~~~~~~
# pyasn1==0.6.1    # ~~~更新时间2025/2/23
# pysnmp==7.1.16   # ~~~更新时间2025/2/23


# SNMP v3 获取信息汇总
def snmpv3_get_all(ip_address, username, auth_key, priv_key):
    # 主机名
    sys_name = asyncio.run(snmpv3_get(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.1.5.0", port=161))[1]

    # cpmCPUTotal5sec
    cpu_usage = int(asyncio.run(snmpv3_get(ip_address,
                                           username,
                                           auth_key,
                                           priv_key,
                                           "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7",
                                           port=161))[1])

    # cpmCPUMemoryUsed
    mem_used = int(asyncio.run(snmpv3_get(ip_address,
                                          username,
                                          auth_key,
                                          priv_key,
                                          "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7",
                                          port=161))[1])

    # cpmCPUMemoryFree
    mem_free = int(asyncio.run(snmpv3_get(ip_address,
                                          username,
                                          auth_key,
                                          priv_key,
                                          "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7",
                                          port=161))[1])

    mem_percent = (round(mem_used / (mem_used + mem_free), 4)) * 100

    # -----------------------------------------------------
    # 接口名称
    raw_name_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.2", port=161))
    if_name_list = [raw_if_name[1] for raw_if_name in raw_name_list]

    # 接口速率
    raw_speed_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.5", port=161))
    if_speed_list = [raw_speed[1] for raw_speed in raw_speed_list]

    # 接口速率
    raw_status_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.7", port=161))
    if_status_list = [raw_status[1] for raw_status in raw_status_list]

    # 进接口字节数
    raw_in_bytes_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.10", port=161))
    if_in_bytes_list = [raw_in_bytes[1] for raw_in_bytes in raw_in_bytes_list]

    # 出接口字节数
    raw_out_bytes_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.16", port=161))
    if_out_bytes_list = [raw_out_bytes[1] for raw_out_bytes in raw_out_bytes_list]

    interface_list = []
    for name, speed, status, in_bytes, out_bytes in zip(if_name_list, if_speed_list, if_status_list, if_in_bytes_list, if_out_bytes_list):
        if int(in_bytes) and int(out_bytes):
            interface_list.append({
                'interface_name': name,
                'interface_speed': int(speed),
                'interface_status': True if status == '1' else False,
                'in_bytes': int(in_bytes),
                'out_bytes': int(out_bytes)
            })

    return {'device_ip': ip_address,
            'hostname': sys_name,
            'cpu_usage_percent': cpu_usage,
            'mem_usage_percent': mem_percent,
            'interface_list': interface_list
            }


if __name__ == "__main__":
    # ip地址与snmpv3用户名、认证密钥和加密密钥
    from pprint import pprint
    ip_address = "196.21.5.211"
    username = "qytanguser"
    auth_key = 'Cisc0123'
    priv_key = 'Cisc0123'
    pprint(snmpv3_get_all(ip_address, username, auth_key, priv_key))
