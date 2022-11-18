#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from tools.get_ifname import get_ifname
import platform


def scapy_iface(os_name):
    if platform.system() == "Linux":
        return os_name
    elif platform.system() == "Windows":
        for x, y in ifaces.items():
            # print(x, y)
            if y.pcap_name is not None:
                # print(y.pcap_name)
                if get_ifname(os_name) == ('{' + y.pcap_name.split('{')[1]):
                    return x
                else:
                    pass


if __name__ == '__main__':
    # print(ifaces)
    print(scapy_iface('Net1'))
