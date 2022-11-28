#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from net_4_snmp.snmp_v2.snmpv2_getbulk import snmpv2_getbulk
from net_4_snmp.snmp_v2.snmpv2_set import snmpv2_set


def get_if_oid(ip, community, if_name):
    if_result = snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.2", count=25, port=161)
    print(if_result)
    if_result_dict = {}
    for x, y in if_result:
        if_result_dict.update({y: x})
    print(if_result_dict)
    if_oid = if_result_dict.get(if_name)
    if_oid_final = if_oid.replace('SNMPv2-SMI::mib-2.2.2.1.2', '1.3.6.1.2.1.2.2.1.7')
    return if_oid_final


def shutdown_if(ip, community, if_name, op=1):
    no_shutdown_oid = get_if_oid(ip, community, if_name)
    snmpv2_set(ip, community, no_shutdown_oid, op)


if __name__ == '__main__':
    # no_shutdown_oid = get_if_oid('10.1.1.253', 'tcpipro', 'GigabitEthernet2')
    # print(no_shutdown_oid)
    # from net_7_snmp.snmp_v2.snmpv2_set import snmpv2_set
    # snmpv2_set("10.1.1.253", "tcpiprw", no_shutdown_oid, 1, port=161)
    shutdown_if('10.1.1.253', 'tcpiprw', 'GigabitEthernet2', op=1)
