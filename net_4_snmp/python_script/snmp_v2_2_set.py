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
from pathlib import Path
import sys

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
current_dir = current_file_path.parent
# 将根目录添加到Python路径
sys.path.insert(1, str(current_dir))

from snmp_v2_3_getbulk import snmpv2_getbulk


# SNMP Set 操作
async def snmpv2_set(ip, community, oid, value, port=161):
    # 根据值的类型，选择相应的 SNMP 类型
    if isinstance(value, str):
        snmp_value = OctetString(value)
    elif isinstance(value, int):
        snmp_value = Integer(value)
    else:
        raise ValueError(f"不支持的值类型: {type(value)}")

    # 使用 set_cmd 执行 SNMP SET 操作
    error_indication, error_status, error_index, var_binds = await set_cmd(
        SnmpEngine(),
        CommunityData(community),  # 配置 community
        await UdpTransportTarget.create((ip, port)),  # 配置目的地址和端口号
        ContextData(),
        ObjectType(ObjectIdentity(oid), snmp_value)  # OID 和要设置的值
    )

    # 错误处理
    if error_indication:
        print(f"写入错误!!!\n{error_indication}")
    elif error_status:
        print(f"写入错误!!!\n{error_status} at {error_index and var_binds[int(error_index) - 1][0] or '?'}")
    else:
        print("写入成功!!!")
    # 打印回显示结果
    for name, val in var_binds:
        print(f'{name.prettyPrint()} = {val.prettyPrint()}')  # 打印修改的结果


# 获取特定接口 ---> 接口状态的OID
def get_if_oid(ip, community, if_name):
    if_result = asyncio.run(snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.2", count=25, port=161))
    # print(if_result)
    if_result_dict = {}
    for x, y in if_result:
        if_result_dict.update({y: x})
    # 找到特定接口的OID
    if_oid = if_result_dict.get(if_name)
    # 替换前缀, 替换为接口状态的OID
    if_oid_final = if_oid.replace('1.3.6.1.2.1.2.2.1.2', '1.3.6.1.2.1.2.2.1.7')
    # 返回接口状态的OID
    return if_oid_final


# 根据名称 up/down 接口
# 1 为 up , 2 为 down
def shutdown_if(ip, community, if_name, op=1):
    no_shutdown_oid = get_if_oid(ip, community, if_name)
    asyncio.run(snmpv2_set(ip, community, no_shutdown_oid, op))


if __name__ == "__main__":
    # ip 地址与 snmp community 字符串
    ip_address = "196.21.5.211"
    write_community = "qytangrw"
    # 设置主机名
    asyncio.run(snmpv2_set(ip_address, write_community, "1.3.6.1.2.1.1.5.0", "C8Kv1", port=161))
    # shutdown G2
    # 1 为 up , 2 为 down
    asyncio.run(snmpv2_set(ip_address, write_community, "1.3.6.1.2.1.2.2.1.7.2", 1, port=161))
    # 根据名称 up/down 接口
    shutdown_if(ip_address, write_community, "GigabitEthernet2", op=1)
