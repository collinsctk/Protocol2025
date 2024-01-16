#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

# IPv6参考文档
# https://www.idsv6.de/Downloads/IPv6PacketCreationWithScapy.pdf
# https://www.ernw.de/download/Advanced%20Attack%20Techniques%20against%20IPv6%20Networks-final.pdf

# -----------路由器配置IPv6-------------
# ipv6 unicast-routing
# interface GigabitEthernet1
#  ipv6 address 2001:1::1/64
#  ipv6 enable

#  -----------Linux配置IPv6-------------
# 修改 /etc/NetworkManager/system-connections/ens224.nmconnection
# [ipv6]
# method=manual
# addresses1=2001:1::200/64

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from tools.get_ip_netifaces import get_ipv6_address
from tools.scapy_iface import scapy_iface  # 获取scapy iface的名字


def scapy_pingv6_one(host, ifname):
    # 可以省略src=get_ipv6_address(ifname)来提高效率
    # packet = IPv6(src=get_ipv6_address(ifname), dst=host) / ICMPv6EchoRequest(data="Welcome to qytang!!!" * 10)  # 构造Ping数据包

    # 最简单包
    packet = IPv6(dst=host) / ICMPv6EchoRequest()  # 构造Ping数据包
    ping = sr1(packet,
               timeout=1,
               iface=ifname,  # 使用指定的接口发包
               verbose=False)  # 获取响应信息，超时为2秒，关闭详细信息

    try:
        if ping.getlayer(IPv6).fields['src'] == host and ping.getlayer("ICMPv6 Echo Reply").fields['type'] == 129:
            # 如果收到目的返回的ICMP ECHO-Reply包
            return host, True  # 返回主机和结果，1为通
        else:
            return host, False  # 返回主机和结果，2为不通
    except Exception:
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
    print(scapy_pingv6_one('2001:1::1', input_ifname))
