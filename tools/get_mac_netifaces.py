#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import netifaces
import platform
import pprint
pp = pprint.PrettyPrinter(indent=4)


def get_mac_address(ifname):
    if platform.system() == "Linux":
        # pp.pprint(netifaces.ifaddresses(ifname))
        # 所有地址信息 2 为IPv4(AF_INET), 10 为IPv6(AF_INET6), 17 为以太网(AF_LINK)
        # {   2: [   {   'addr': '10.1.1.80',
        #                'broadcast': '10.1.1.255',
        #                'netmask': '255.255.255.0'}],
        #     10: [   {'addr': '2001:1::80', 'netmask': 'ffff:ffff:ffff:ffff::/64'},
        #             {   'addr': 'fe80::250:56ff:feab:2508%ens33',
        #                 'netmask': 'ffff:ffff:ffff:ffff::/64'}],
        #     17: [{'addr': '00:50:56:ab:25:08', 'broadcast': 'ff:ff:ff:ff:ff:ff'}]}

        # AF_LINK表示以太网
        # print(netifaces.AF_LINK)  # 17
        try:
            return netifaces.ifaddresses(ifname)[netifaces.AF_LINK][0]['addr']
        except ValueError:
            return None
    elif platform.system() == "Windows":
        from tools.win_ifname import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        if not if_id:
            return None
        else:
            # 此处依然要提供WIN的网卡ID, 而不是名字
            return netifaces.ifaddresses(if_id)[netifaces.AF_LINK][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


if __name__ == '__main__':
    import platform
    if platform.system() == "Linux":
        print(get_mac_address('ens224'))
    elif platform.system() == "Windows":
        print(get_mac_address('VMware Network Adapter VMnet1'))
