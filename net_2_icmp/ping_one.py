#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/
import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from kamene.all import *


def scapy_ping_one(host, ifname):
    packet = IP(dst=host) / ICMP() / b'Welcome to qytang'  # 构造Ping数据包
    ping = sr1(packet,
               timeout=1,
               iface=ifname,  # 使用指定的接口发包
               verbose=False)  # 获取响应信息，超时为2秒，关闭详细信息

    try:
        if ping.getlayer(IP).fields['src'] == host and ping.getlayer(ICMP).fields['type'] == 0:
            # 如果收到目的返回的ICMP ECHO-Reply包
            return host, True  # 返回主机和结果，1为通
        else:
            return host, False  # 返回主机和结果，2为不通
    except AttributeError:
        return host, False  # 出现异常也返回主机和结果，2为不通


if __name__ == '__main__':
    # Windows Linux均可使用
    import platform
    if platform.system() == "Linux":
        input_ifname = 'ens224'
    elif platform.system() == "Windows":
        # 注意网卡有两个名字
        # 名称1: VMware Network Adapter VMnet1 ---- 显示的网卡名字（名字可以改）
        # 名称2: VMware Virtual Ethernet Adapter for VMnet1 ---- Kamene需要这个名字（不能改）
        # 可以使用函数get_ifname()从名称1得到名称2, 但是速度很慢，建议直接手动输入名称2
        input_ifname = 'VMware Virtual Ethernet Adapter for VMnet1'

    print(scapy_ping_one("10.10.1.1", input_ifname))
    # print(scapy_ping_one(sys.argv[1]))
