#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from net_4_snmp.snmp_v2.snmpv2_getbulk import snmpv2_getbulk
from net_4_snmp.snmp_v2.snmpv2_get import snmpv2_get


def snmpv2_all_2024(ip_address, community):
    get_all_dict = {}
    # cpmCPUTotal5sec
    cpu = snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.6.7", port=161)
    # cpmCPUMemoryUsed
    mem_used = snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)
    # cpmCPUMemoryFree
    mem_free = snmpv2_get(ip_address, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)
    get_all_dict['cpu'] = int(cpu[1])
    get_all_dict['mem_used'] = int(mem_used[1])
    get_all_dict['mem_free'] = int(mem_free[1])
    get_all_dict['mem_percent'] = round((int(mem_used[1]) / (int(mem_used[1]) + int(mem_free[1]))) * 100, 2)
    get_all_dict['ip_address'] = ip_address

    interface_list = []

    if_name_list = [x[1] for x in snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.2", count=25, port=161)]
    if_state_list = [x[1] for x in snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.8", count=25, port=161)]
    if_in_bytes_list = [int(x[1]) for x in snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.10", count=25, port=161)]
    if_out_bytes_list = [int(x[1]) for x in snmpv2_getbulk(ip_address, community, "1.3.6.1.2.1.2.2.1.16", count=25, port=161)]

    if_final_state_list = []
    for state in if_state_list:
        if state == '1':
            if_final_state_list.append(True)
        else:
            if_final_state_list.append(False)

    for if_name, if_status, if_in_bytes, if_out_bytes in zip(if_name_list, if_final_state_list, if_in_bytes_list, if_out_bytes_list):
        interface_list.append({'name': if_name, 'status': if_status, 'in_bytes': if_in_bytes, 'out_bytes': if_out_bytes})

    get_all_dict['interface_list'] = interface_list
    return get_all_dict


if __name__ == '__main__':
    from pprint import pprint
    ip_address = '10.10.1.11'
    community = 'qytangro'
    pprint(snmpv2_all_2024(ip_address, community))
