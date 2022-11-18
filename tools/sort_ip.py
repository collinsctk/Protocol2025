#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from socket import inet_aton
import struct
import ipaddress

ip_list = ['172.16.12.123',
           '172.16.12.3',
           '172.16.12.234',
           '172.16.12.12',
           '172.16.12.23',
           '10.1.2.3',
           '192.168.2.3',
           '172.16.1.2'
           ]


def sort_ip(ips):
    # inet_aton(ip) 转换IP到直接字符串
    # >>> inet_aton("172.16.1.1")
    # b'\xac\x10\x01\x01'
    # 了解struct https://docs.python.org/2/library/struct.html
    # struct.unpack("!L", inet_aton(ip))[0] 把直接字符串转换为整数
    # >>> struct.unpack("!L", inet_aton("172.16.1.1"))
    # (2886729985,)
    # >>> struct.unpack("!L", inet_aton("172.16.1.1"))[0]
    # 2886729985
    # 根据整数排序,然后返回排序后的ips列表
    # return sorted(ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])
    return sorted(ips, key=lambda ip: ipaddress.ip_address(ip))


if __name__ == "__main__":
    print(sort_ip(ip_list))
