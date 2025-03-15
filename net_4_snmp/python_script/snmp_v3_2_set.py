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
from snmp_v3_3_getbulk import snmpv3_getbulk


# 异步SNMPv3 SET请求
async def snmpv3_set(ip, username, auth_key, priv_key, oid, value, auth_protocol=usmHMACSHAAuthProtocol,
                     priv_protocol=usmAesCfb128Protocol, port=161):
    # 根据值的类型，选择相应的 SNMP 类型
    if isinstance(value, str):
        snmp_value = OctetString(value)
    elif isinstance(value, int):
        snmp_value = Integer(value)
    else:
        raise ValueError(f"不支持的值类型: {type(value)}")

    # 创建 SNMP 引擎
    snmp_engine = SnmpEngine()

    # 配置 SNMPv3 用户数据
    user_data = UsmUserData(
        username,  # 用户名
        auth_key,  # 认证密钥
        priv_key,  # 加密密钥
        authProtocol=auth_protocol,  # 认证协议
        privProtocol=priv_protocol  # 加密协议
    )

    # 配置 SNMP 目标地址
    target = await UdpTransportTarget.create((ip, port))

    # 执行 SET 请求
    errorIndication, errorStatus, errorIndex, varBinds = await set_cmd(
        snmp_engine,
        user_data,  # 使用 SNMPv3 用户数据
        target,
        ContextData(),
        ObjectType(ObjectIdentity(oid), snmp_value)  # OID 和要设置的值
    )

    # 错误处理
    if errorIndication:
        print(f"写入错误!!!\n{errorIndication}")
    elif errorStatus:
        print(f"写入错误!!!\n{errorStatus} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
    else:
        print("写入成功!!!")
    # 打印回显示结果
    for name, val in varBinds:
        print(f'{name.prettyPrint()} = {val.prettyPrint()}')  # 打印修改的结果


# 获取特定接口 ---> 接口状态的OID
def get_if_oid(ip, username, auth_key, priv_key, if_name):
    if_result = asyncio.run(snmpv3_getbulk(ip, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.2", count=25, port=161))
    # print(if_result)
    if_result_dict = {}
    for x, y in if_result:
        if_result_dict.update({y: x})
    if_oid = if_result_dict.get(if_name)
    if_oid_final = if_oid.replace('1.3.6.1.2.1.2.2.1.2', '1.3.6.1.2.1.2.2.1.7')
    return if_oid_final


# 根据名称 up/down 接口
# 1 为 up , 2 为 down
def shutdown_if(ip, username, auth_key, priv_key, if_name, op=1):
    no_shutdown_oid = get_if_oid(ip, username, auth_key, priv_key, if_name)
    asyncio.run(snmpv3_set(ip, username, auth_key, priv_key, no_shutdown_oid, op))


if __name__ == "__main__":
    # SNMPv3 配置
    ip_address = "196.21.5.211"
    username = "qytanguser"
    auth_key = 'Cisc0123'
    priv_key = 'Cisc0123'

    # 设置主机名
    asyncio.run(snmpv3_set(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.1.5.0", "C8Kv1", port=161))

    # shutdown G2 接口
    # 1 为 up , 2 为 down
    asyncio.run(snmpv3_set(ip_address, username, auth_key, priv_key, "1.3.6.1.2.1.2.2.1.7.2", 1, port=161))

    # 根据名称 up/down 接口
    shutdown_if(ip_address, username, auth_key, priv_key, "GigabitEthernet2", op=1)
