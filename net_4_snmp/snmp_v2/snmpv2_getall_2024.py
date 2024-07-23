#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from net_4_snmp.snmp_v2.snmpv2_getbulk import snmpv2_getbulk
from net_4_snmp.snmp_v2.snmpv2_get import snmpv2_get
"""
{'device_ip': '10.10.1.1',
 'device_name': 'C8kv1',
 'cpu_percent': 11,
 'mem_percent': 67,
 'interface_list': [
    {'interface_name': 'GigabitEthernet1',
     'interface_speed': 1000000000,
     'interface_state': True,
     'in_bytes': 123123123,
     'out_bytes': 324234234},
     ----
 ]
}
"""


def snmpv2_all_2024(ip_address, community):
    final_dict = {'device_ip': ip_address}
    device_name = snmpv2_get(ip_address, community, "1.3.6.1.2.1.1.5.0")[1]
    final_dict['device_name'] = device_name
    cpu_percent = int(snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7")[1])
    final_dict['cpu_percent'] = cpu_percent
    mem_use = int(snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7")[1])
    mem_free = int(snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7")[1])
    mem_percent = round((mem_use / (mem_use + mem_free)) * 100, 2)
    final_dict['mem_used'] = mem_use
    final_dict['mem_free'] = mem_free
    final_dict['mem_percent'] = mem_percent
    interface_name_list = [i[1] for i in snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.2")]
    interface_speed_list = [int(s[1]) for s in snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.5")]
    interface_state_list_raw = [int(state[1]) for state in snmpv2_getbulk(ip_address,
                                                                          community,
                                                                          "1.3.6.1.2.1.2.2.1.7")]
    interface_state_list = []
    for if_state in interface_state_list_raw:
        if if_state == 1:
            interface_state_list.append(True)
        elif if_state == 2:
            interface_state_list.append(False)
    interface_in_bytes = [int(in_bytes[1]) for in_bytes in snmpv2_getbulk(ip_address,
                                                                          community,
                                                                          "1.3.6.1.2.1.2.2.1.10")]
    interface_out_bytes = [int(out_bytes[1]) for out_bytes in snmpv2_getbulk(ip_address,
                                                                             community,
                                                                             "1.3.6.1.2.1.2.2.1.16")]
    interface_list = []
    for interface_zip in zip(interface_name_list,
                             interface_speed_list,
                             interface_state_list,
                             interface_in_bytes,
                             interface_out_bytes):
        if interface_zip[3] and interface_zip[4]:
            interface_list.append(
                {'interface_name': interface_zip[0],
                 'interface_speed': interface_zip[1],
                 'interface_state': interface_zip[2],
                 'in_bytes': interface_zip[3],
                 'out_bytes': interface_zip[4]}
            )
    final_dict['interface_list'] = interface_list
    return final_dict


if __name__ == '__main__':
    from pprint import pprint
    ip_address = '10.10.1.1'
    community = 'tcpipro'
    pprint(snmpv2_all_2024(ip_address, community))
