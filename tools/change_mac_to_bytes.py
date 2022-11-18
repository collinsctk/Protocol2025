#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import struct
import re
import binascii


def change_mac_to_bytes(mac):
    # # 去除各种MAC地址的分隔符
    # mac_value = int(re.sub('[ :.-]', '', mac), 16)
    #
    # # 通过移位操作,得到MAC地址的6个字节
    # section1 = mac_value >> 40 & 0xff
    # section2 = mac_value >> 32 & 0xff
    # section3 = mac_value >> 24 & 0xff
    # section4 = mac_value >> 16 & 0xff
    # section5 = mac_value >> 8 & 0xff
    # section6 = mac_value & 0xff
    # # 拼接MAC地址的6个字节,返回转换为字节的MAC地址
    #
    # Bytes_MAC = struct.pack('!6B', section1, section2, section3, section4, section5, section6)
    # return Bytes_MAC
    return binascii.unhexlify(re.sub('[ :.-]', '', mac).encode())


if __name__ == "__main__":
    a = change_mac_to_bytes("00:0c:29:8d:5c:b6")
    print(a)
