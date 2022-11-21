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
from net_13_traffic_analysis.pyshark_traffic_analysis.pyshark_0_pcap_dir import pcap_data_dir
pkt_list = []

# 分析现象级数据包,"tcp重传的数据包"
cap = pyshark.FileCapture(pcap_data_dir + 'dos.pcap', keep_packets=False, display_filter='tcp.analysis.retransmission')


def print_highest_layer(pkt):
    # 通过过滤得到数据包清单
    pkt_list.append(pkt)


cap.apply_on_packets(print_highest_layer)

# pretty_print TCP重传的数据包
for x in pkt_list:
    print('='*80)
    # pretty_print() 和wireshark GUI类似的解码效果
    x.pretty_print()
