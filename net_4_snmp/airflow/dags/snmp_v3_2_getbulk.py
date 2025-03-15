#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

# ~~~~~~~~~~~~~~~~注意版本~~~~~~~~~~~~~
# pyasn1==0.6.1    # ~~~更新时间2025/2/23
# pysnmp==7.1.16   # ~~~更新时间2025/2/23

import asyncio
from pysnmp.hlapi.v3arch.asyncio import *


# 异步 SNMPv3 GETBULK 请求
async def snmpv3_getbulk(ip, username, auth_key, priv_key, oid, count=25, auth_protocol=usmHMACSHAAuthProtocol,
                         priv_protocol=usmAesCfb128Protocol, port=161):
    # 使用 bulk_cmd 执行 SNMPv3 GETBULK 操作
    iterator = bulk_cmd(
        SnmpEngine(),
        UsmUserData(
            username,  # 用户名
            auth_key,  # 认证密钥
            priv_key,  # 加密密钥
            authProtocol=auth_protocol,  # 认证协议
            privProtocol=priv_protocol  # 加密协议
        ),
        await UdpTransportTarget.create((ip, port)),  # 配置目的地址和端口号
        ContextData(),
        0, count,  # non-repeaters 和 max-repetitions
        ObjectType(ObjectIdentity(oid)),  # OID
        lexicographicMode=True
    )

    # 获取结果
    error_indication, error_status, error_index, var_binds = await iterator

    # 错误处理
    if error_indication:
        print(f"读取错误!!!\n{error_indication}")
    elif error_status:
        print(f"读取错误!!!\n{error_status} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
    else:
        # 处理返回的 varBinds
        result = []
        for var_bind_table_row in var_binds:
            get_oid = str(var_bind_table_row[0])
            get_value = str(var_bind_table_row[1])
            if oid not in get_oid:  # 超过OID范围跳出循环
                break
            result.append((get_oid, get_value))
        return result


if __name__ == "__main__":
    # SNMPv3 配置
    ip_address = "196.21.5.211"
    username = "qytanguser"
    auth_key = 'Cisc0123'
    priv_key = 'Cisc0123'

    # 获取接口名称
    raw_name_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.2", port=161))
    if_name_list = [raw_if_name[1] for raw_if_name in raw_name_list]

    # 获取接口速率
    raw_speed_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.5", port=161))
    if_speed_list = [raw_speed[1] for raw_speed in raw_speed_list]

    # 获取进接口字节数
    raw_in_bytes_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.10", port=161))
    if_in_bytes_list = [raw_in_bytes[1] for raw_in_bytes in raw_in_bytes_list]

    # 获取出接口字节数
    raw_out_bytes_list = asyncio.run(snmpv3_getbulk(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.16", port=161))
    if_out_bytes_list = [raw_out_bytes[1] for raw_out_bytes in raw_out_bytes_list]

    # 汇总接口信息
    interface_list = []
    for name, speed, in_bytes, out_bytes in zip(if_name_list, if_speed_list, if_in_bytes_list, if_out_bytes_list):
        interface_list.append({
            'interface_name': name,
            'interface_speed': speed,
            'in_bytes': in_bytes,
            'out_bytes': out_bytes
        })

    # 打印接口信息
    from pprint import pprint
    pprint(interface_list)
