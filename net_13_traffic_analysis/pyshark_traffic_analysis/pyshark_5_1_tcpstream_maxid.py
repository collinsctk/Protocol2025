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


def get_max_id(pcap_file):
    # 本代码的主要任务: 找到最大的TCP Stream ID! 这个ID是连续的!
    cap = pyshark.FileCapture(pcap_file, keep_packets=False)

    sess_index = []  # 所有的tcp流索引ID清单

    for pkt in cap:
        try:
            sess_index.append(pkt.tcp.stream)  # 把所有的tcp流索引ID放入清单
        except AttributeError:
            pass

    if len(sess_index) == 0:  # 如果没有任何索引ID就打印错误
        print('No TCP Found')
        return None
    else:
        sess_index_int = [int(sid) for sid in sess_index]  # 把索引ID字符串转换为整数,便于排序
        return max(sess_index_int)  # 返回最大的索引ID


if __name__ == '__main__':
    print(get_max_id(pcap_data_dir + 'dos.pcap'))
