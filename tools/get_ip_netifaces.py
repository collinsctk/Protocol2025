#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# windows安装netifaces需要安装 Build Tools for Visual Studio 2019
# https://visualstudio.microsoft.com/zh-hant/visual-cpp-build-tools/

from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6
import platform
from pprint import pprint


def get_ip_address(ifname):
    if platform.system() == "Linux":
        try:
            # pprint(ifaddresses(ifname))
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
        print(get_ip_address('ens224'))
        print(get_ipv6_address('ens224'))
    elif platform.system() == "Windows":
        print(get_ip_address('VMware Network Adapter VMnet1'))
        print(get_ipv6_address('VMware Network Adapter VMnet1'))
