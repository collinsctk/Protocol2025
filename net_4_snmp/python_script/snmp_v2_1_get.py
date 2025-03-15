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


async def snmpv2_get(ip, community, oid, port=161):
    # 使用 get_cmd 执行 SNMP GET 操作
    error_indication, error_status, error_index, var_binds = await get_cmd(
        SnmpEngine(),
        CommunityData(community),  # 配置 community
        await UdpTransportTarget.create((ip, port)),  # 配置目的地址和端口号
        ContextData(),
        ObjectType(ObjectIdentity(oid))  # 读取的 OID
    )

    # 错误处理
    if error_indication:
        print(error_indication)
    elif error_status:
        print(f'{error_status} at {error_index and var_binds[int(error_index) - 1][0] or "?"}')
    else:
        # 获取返回的第一个 varBind
        var_bind = var_binds[0]
        # 获取其值并解码为 UTF-8 字符串
        value = var_bind[1]
        if isinstance(value, bytes):
            # 将十六进制的字节串转换为字符串
            result_str = bytes.fromhex(value[2:].decode('utf-8')).decode('utf-8', errors='ignore')
        else:
            result_str = str(value)
        # 返回 OID 和解码后的字符串结果
        return var_bind[0].prettyPrint(), result_str

if __name__ == "__main__":
    # ip 地址与 snmp community 字符串
    ip_address = "196.21.5.211"
    community = "qytangro"

    # 系统描述
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.1.0", port=161)))
    # 联系人
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.4.0", port=161)))
    # # 主机名
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.5.0", port=161)))
    # 地点
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.6.0", port=161)))
    # cpmCPUTotal5sec
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7", port=161)))
    # cpmCPUMemoryUsed
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)))
    # cpmCPUMemoryFree
    print(asyncio.run(snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)))