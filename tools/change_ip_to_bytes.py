#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import struct
import re
import socket


def change_ip_to_bytes(IP):
    # section1 = int(IP.split('.')[0])
    # section2 = int(IP.split('.')[1])
    # section3 = int(IP.split('.')[2])
    # section4 = int(IP.split('.')[3])
    # Bytes_IP = struct.pack('>4B', section1, section2, section3, section4)
    #
    # return Bytes_IP
    return socket.inet_aton(IP)


if __name__ == "__main__":
    print(change_ip_to_bytes("10.1.1.80"))