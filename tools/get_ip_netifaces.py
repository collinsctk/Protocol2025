#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# windows安装netifaces需要安装 Build Tools for Visual Studio 2019
# https://visualstudio.microsoft.com/zh-hant/visual-cpp-build-tools/

from netifaces import ifaddresses, AF_INET, AF_INET6
from pprint import pprint
import platform


def get_ip_address(ifname):
    if platform.system() == "Linux":
        try:
            pprint(ifaddresses(ifname))
            """
            {2: [{'addr': '196.21.5.218',
                'broadcast': '196.21.5.255',
                'netmask': '255.255.255.0'}],
            10: [{'addr': '2001:196:21:5:20c:29ff:fe4d:73b3',
                'netmask': 'ffff:ffff:ffff:ffff::/64'},
                {'addr': 'fe80::20c:29ff:fe4d:73b3%ens35',
                'netmask': 'ffff:ffff:ffff:ffff::/64'}],
            17: [{'addr': '00:0c:29:4d:73:b3', 'broadcast': 'ff:ff:ff:ff:ff:ff'}]}
            """
            return ifaddresses(ifname)[AF_INET][0]['addr']
        except ValueError:
            return None
    elif platform.system() == "Windows":
        from tools.win_ifname import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        if not if_id:
            return
        else:
            return ifaddresses(if_id)[AF_INET][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


def get_ipv6_address(ifname):
    if platform.system() == "Linux":
        try:
            return ifaddresses(ifname)[AF_INET6][0]['addr']
        except ValueError:
            return None
    elif platform.system() == "Windows":
        from tools.win_ifname import win_from_name_get_id
        if_id = win_from_name_get_id(ifname)
        if not if_id:
            return
        else:
            # 此处依然要提供WIN的网卡ID, 而不是名字
            return ifaddresses(if_id)[AF_INET6][0]['addr']
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


if __name__ == "__main__":
    if platform.system() == "Linux":
        print(get_ip_address('ens35'))
        print(get_ipv6_address('ens35'))
    elif platform.system() == "Windows":
        print(get_ip_address('VMware Network Adapter VMnet1'))
        print(get_ipv6_address('VMware Network Adapter VMnet1'))
