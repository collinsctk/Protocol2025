#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# IPv6参考文档
# https://www.idsv6.de/Downloads/IPv6PacketCreationWithScapy.pdf
# https://www.ernw.de/download/Advanced%20Attack%20Techniques%20against%20IPv6%20Networks-final.pdf

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
from tools.get_ip_netifaces import get_ipv6_address


def scapy_pingv6_one(host):
    # 可以省略src=get_ipv6_address(ifname)来提高效率
    # packet = IPv6(src=get_ipv6_address(ifname), dst=host) / ICMPv6EchoRequest(data="Welcome to qytang!!!" * 10)  # 构造Ping数据包

    # 最简单包
    packet = IPv6(dst=host) / ICMPv6EchoRequest()  # 构造Ping数据包
    ping = sr1(packet, timeout=1, verbose=False)  # 获取响应信息，超时为2秒，关闭详细信息
    # ping.show()
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
    print(scapy_pingv6_one('2001:1::253'))
