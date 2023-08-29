from snmpv2_get import snmpv2_get
from snmpv2_getbulk import snmpv2_getbulk


def snmpv2_getall(ip, community, count=25, port=161):
    cpu_usage = int(snmpv2_get("10.1.1.253", community, "1.3.6.1.4.1.9.9.109.1.1.1.1.3.7", port=161)[1])
    mem_free = snmpv2_get("10.1.1.253", community, "1.3.6.1.4.1.9.9.109.1.1.1.1.13.7", port=161)[1]
    mem_use = snmpv2_get("10.1.1.253", community, "1.3.6.1.4.1.9.9.109.1.1.1.1.12.7", port=161)[1]
    mem_usage = round((int(mem_use) / (int(mem_use) + int(mem_free))) * 100, 2)

    router_all_dict = {
        'ip': ip,
        'cpu_usage': cpu_usage,
        'mem_usage': mem_usage

    }

    if_name_list = [i[1] for i in snmpv2_getbulk("10.1.1.253", "tcpipro", "1.3.6.1.2.1.2.2.1.2", count=25, port=161)]
    # print(if_name_list)
    if_state_list_raw = [i[1] for i in snmpv2_getbulk("10.1.1.253", "tcpipro", "1.3.6.1.2.1.2.2.1.7", count=25, port=161)]
    # print(if_state_list_raw)
    if_state_list = []
    for i in if_state_list_raw:
        if i == '1':
            if_state_list.append(True)
        else:
            if_state_list.append(False)
    # print(if_state_list)
    if_in_bytes_list = [int(i[1]) for i in snmpv2_getbulk("10.1.1.253", "tcpipro", "1.3.6.1.2.1.2.2.1.10", port=161)]
    # print(if_in_bytes_list)
    if_out_bytes_list = [int(i[1]) for i in snmpv2_getbulk("10.1.1.253", "tcpipro", "1.3.6.1.2.1.2.2.1.16", port=161)]
    # print(if_out_bytes_list)

    if_zip = zip(if_name_list, if_state_list, if_in_bytes_list, if_out_bytes_list)

    # ----------------------------------interface_dict---------------------------------
    # interface_dict = {}
    # for ifname, if_state, if_in_bytes, if_out_bytes in if_zip:
    #     interface_dict.update({
    #         ifname: {
    #             'interface_state': if_state,
    #             'interface_in_bytes': if_in_bytes,
    #             'interface_out_bytes': if_out_bytes
    #         }
    #     })
    # router_all_dict.update({'interface_dict': interface_dict})
    """
    {'cpu_usage': 11,
     'interface_dict': {'GigabitEthernet1': {'interface_in_bytes': 1183175132,
                                             'interface_out_bytes': 1612533,
                                             'interface_state': True},
                        'GigabitEthernet2': {'interface_in_bytes': 1184273704,
                                             'interface_out_bytes': 0,
                                             'interface_state': True},
                        'GigabitEthernet3': {'interface_in_bytes': 806709,
                                             'interface_out_bytes': 0,
                                             'interface_state': False},
                        'Null0': {'interface_in_bytes': 0,
                                  'interface_out_bytes': 0,
                                  'interface_state': True},
                        'VoIP-Null0': {'interface_in_bytes': 0,
                                       'interface_out_bytes': 0,
                                       'interface_state': True}},
     'ip': '10.1.1.253',
     'mem_usage': 70.54}
    """
    # ----------------------------------interface_list---------------------------------
    interface_list = []
    for ifname, if_state, if_in_bytes, if_out_bytes in if_zip:
        interface_list.append({
            'interface_name': ifname,
            'interface_state': if_state,
            'interface_in_bytes': if_in_bytes,
            'interface_out_bytes': if_out_bytes
        })
    router_all_dict['interface_list'] = interface_list
    """
    {'cpu_usage': 10,
     'interface_list': [{'interface_in_bytes': 1183261814,
                         'interface_name': 'GigabitEthernet1',
                         'interface_out_bytes': 1615340,
                         'interface_state': True},
                        {'interface_in_bytes': 1184363193,
                         'interface_name': 'GigabitEthernet2',
                         'interface_out_bytes': 0,
                         'interface_state': True},
                        {'interface_in_bytes': 806709,
                         'interface_name': 'GigabitEthernet3',
                         'interface_out_bytes': 0,
                         'interface_state': False},
                        {'interface_in_bytes': 0,
                         'interface_name': 'VoIP-Null0',
                         'interface_out_bytes': 0,
                         'interface_state': True},
                        {'interface_in_bytes': 0,
                         'interface_name': 'Null0',
                         'interface_out_bytes': 0,
                         'interface_state': True}],
     'ip': '10.1.1.253',
     'mem_usage': 70.54}
    """
    return router_all_dict


if __name__ == "__main__":
    from pprint import pprint
    pprint(snmpv2_getall('10.1.1.253', 'tcpipro'))