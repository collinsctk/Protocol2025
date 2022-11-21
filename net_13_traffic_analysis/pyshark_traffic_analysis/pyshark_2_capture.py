#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

# pyshark 特点分析
# 1.解码能力强,提供丰富的字段,远远强于Scapy
# 2.能够直接使用wireshark强大的display_filter
# 3.能够找到现象级数据包,例如重传 display_filter='tcp.analysis.retransmission'
# 3.能够使用wireshark的follow tcp stream的技术,找到特定tcp stream的数据包

# pyshark 问题
# 抓包在3.6环境出现问题
# 不能保存分析后的数据包到PCAP

import pyshark
import pprint

# bpf为捕获过滤器, 过滤Telnet流量
capture = pyshark.LiveCapture(interface='ens192', bpf_filter='ip and tcp port 23')
# using the sniff() method to capture a given amount of packets (or for a given amount of time) and then read the packets from the capture object as a list
# capture.sniff(timeout=5)

# use the sniff_continously() method as a generator and work on each packet as it arrives.
capture.sniff_continuously()


def print_highest_layer(pkt):
    # 打印包中的特定字段
    pkt_dict = {}
    try:
        for layer in pkt.__dict__.get('layers'):
            pkt_dict.update(layer.__dict__.get('_all_fields'))
        pprint.pprint(pkt_dict, indent=4)
    except AttributeError:
        pass


# 把函数应用到数据包
capture.apply_on_packets(print_highest_layer)
