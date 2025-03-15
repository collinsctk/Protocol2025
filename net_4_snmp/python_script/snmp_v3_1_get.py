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


# 异步SNMPv3 GET请求
async def snmpv3_get(ip,
                     username,
                     auth_key,
                     priv_key,
                     oid,
                     auth_protocol=usmHMACSHAAuthProtocol,
                     priv_protocol=usmAesCfb128Protocol,
                     port=161):

    # 创建 SNMP 引擎
    snmp_engine = SnmpEngine()

    # 配置SNMPv3的认证和加密密钥
    user_data = UsmUserData(
        username,  # 用户名
        auth_key,  # 认证密钥
        priv_key,  # 加密密钥
        authProtocol=auth_protocol,  # 认证协议
        privProtocol=priv_protocol  # 加密协议
    )

    # 使用目标主机和端口
    target = await UdpTransportTarget.create((ip, port))

    # 构造OID和请求
    object_type = ObjectType(ObjectIdentity(oid))

    # 执行 GET 请求
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        snmp_engine,
        user_data,  # 使用 SNMPv3 用户数据
        target,
        ContextData(),
        object_type
    )

    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(f'{errorStatus} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')
    else:
        # 获取返回的第一个 varBind
        var_bind = varBinds[0]
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
    username = "qytanguser"
    qytang_auth_key = 'Cisc0123'
    qytang_priv_key = 'Cisc0123'

    # 系统描述
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.1.1.0")))
    # 联系人
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.1.4.0")))
    # # 主机名
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.1.5.0")))
    # 地点
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key, "1.3.6.1.2.1.1.6.0")))
    # cpmCPUTotal5sec
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key,
                                 "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7")))
    # cpmCPUMemoryUsed
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key,
                                 "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7")))
    # cpmCPUMemoryFree
    print(asyncio.run(snmpv3_get(ip_address, username, qytang_auth_key, qytang_priv_key,
                                 "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7")))
