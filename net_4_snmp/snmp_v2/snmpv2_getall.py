#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from net_4_snmp.snmp_v2.snmpv2_getbulk import snmpv2_getbulk
from net_4_snmp.snmp_v2.snmpv2_get import snmpv2_get


def snmpv2_getall(ip, community, count=25, port=161):
    # cpmCPUTotal5sec
    cpu_usage = snmpv2_get(ip, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)

    # cpmCPUMemoryUsed
    mem_usage = snmpv2_get(ip, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)

    # cpmCPUMemoryFree
    mem_free = snmpv2_get(ip, community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)

    name_list = [x[1] for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.2", count=count, port=port)]
    # print(name_list)

    speed_list = [int(x[1]) for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.5", count=count, port=port)]
    # print(speed_list)

    in_bytes_list = [int(x[1]) for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.10", count=count, port=port)]
    # print(in_bytes_list)

    out_bytes_list = [int(x[1]) for x in snmpv2_getbulk(ip, community, "1.3.6.1.2.1.2.2.1.16", count=count, port=port)]
    # print(out_bytes_list)

    if_list = []
    for name, speed, in_bytes, out_bytes in zip(name_list, speed_list, in_bytes_list, out_bytes_list):
        if in_bytes or out_bytes:
            if_list.append({'name': name, 'speed': speed, 'in_bytes': in_bytes, 'out_bytes': out_bytes})

    final_dict = {'ip': ip,
                  'cpu_usage': int(cpu_usage[1]),
                  'mem_usage': int(mem_usage[1]),
                  'mem_free': int(mem_free[1]),
                  'if_list': if_list}

    return final_dict


def get_all(device_ip, device_community):
    # device_ip = "10.1.1.253"
    # device_community = "tcpipro"
    device_name = snmpv2_get(device_ip, device_community, "1.3.6.1.2.1.1.5.0", port=161)[1]
    # print(device_name)
    cpu_usage = snmpv2_get(device_ip, device_community, "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)[1]
    # print(cpu_usage)
    mem_use = snmpv2_get(device_ip, device_community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)[1]
    # print(mem_use)
    mem_free = snmpv2_get(device_ip, device_community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)[1]
    # print(mem_free)
    memory_usage = round(int(mem_use) / (int(mem_use) + int(mem_free)) * 100, 2)
    # print(memory_usage)
    interface_name_list = [y for x, y in snmpv2_getbulk(device_ip, device_community, "1.3.6.1.2.1.2.2.1.2", port=161)]
    # print(interface_name_list)

    interface_status_list_1_2 = [y for x, y in
                                 snmpv2_getbulk(device_ip, device_community, "1.3.6.1.2.1.2.2.1.7", port=161)]
    interface_status_list = []
    for interface_status in interface_status_list_1_2:
        if interface_status == '1':
            interface_status_list.append(True)
        else:
            interface_status_list.append(False)
    # print(interface_status_list)

    interface_speed_list = [int(y) for x, y in
                            snmpv2_getbulk(device_ip, device_community, "1.3.6.1.2.1.2.2.1.5", port=161)]
    # print(interface_speed_list)

    interface_in_octets_list = [int(y) for x, y in
                                snmpv2_getbulk(device_ip, device_community, "1.3.6.1.2.1.2.2.1.10", port=161)]
    # print(interface_in_octets_list)

    interface_out_octets_list = [int(y) for x, y in
                                 snmpv2_getbulk(device_ip, device_community, "1.3.6.1.2.1.2.2.1.16", port=161)]
    # print(interface_out_octets_list)

    interface_list = []
    for name, status, speed, in_octets, out_octets in zip(interface_name_list,
                                                          interface_status_list,
                                                          interface_speed_list,
                                                          interface_in_octets_list,
                                                          interface_out_octets_list):
        interface_list.append({'interface_name': name,
                               'interface_stats': status,
                               'interface_speed': speed,
                               'interface_in_octets': in_octets,
                               'interface_out_octets': out_octets})

    # print(interface_list)

    device_dict = {"device_ip": device_ip,
                   "device_name": device_name,
                   "cpu_usage": int(cpu_usage),
                   "memory_usage": memory_usage,
                   "interface_list": interface_list}

    # from pprint import pprint

    return device_dict


if __name__ == '__main__':
    from pprint import pprint

    final_result = snmpv2_getall("10.1.1.253", "tcpipro", count=25, port=161)
    pprint(final_result, indent=4)

    get_all_result = get_all("10.1.1.253", "tcpipro")
    pprint(get_all_result, indent=4)
