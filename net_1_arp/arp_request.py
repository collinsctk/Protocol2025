#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

#  grep -r "from fractions import gcd" .
#  上面搜索存在from fractions import gcd这句话的文件，把它改为from math import gcd

# CryptographyDeprecationWarning: Blowfish has been deprecated cipher=algorithms.Blowfish,
# CryptographyDeprecationWarning: CAST5 has been deprecated cipher=algorithms.CAST5,
# vim ./lib/python3.11/site-packages/kamene/layers/ipsec.py, 注释掉Blowfish和CAST5的部分

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from tools.scapy_iface import scapy_iface  # 获取scapy iface的名字


def arp_request(ip_address, ifname):
    try:  # 发送ARP请求并等待响应
        result_raw = sr1(ARP(pdst=ip_address),
                         timeout=1,
                         iface=scapy_iface(ifname),
                         verbose=False
                         )
        return ip_address, result_raw.getlayer(ARP).fields.get('hwsrc')

    except AttributeError:
        return ip_address, None


if __name__ == "__main__":
    # Windows Linux均可使用
    import platform
    if platform.system() == "Linux":
        input_ifname = 'ens224'
    elif platform.system() == "Windows":
        input_ifname = 'VMware Network Adapter VMnet1'
    arp_result = arp_request('10.10.1.1',
                             input_ifname
                             )
    print("IP地址:", arp_result[0], "MAC地址:", arp_result[1])
