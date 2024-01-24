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


def get_tcp_stream(pcap_file, sid):
    # 提取PCAP文件中,特定tcp流ID的数据包
    cap = pyshark.FileCapture(pcap_file,
                              keep_packets=False,
                              display_filter='tcp.stream eq {0}'.format(sid))  # 打开PCAP文件

    return cap  # 返回清单


if __name__ == '__main__':
    all_telnet_data = ''
    i = 1
    for pkt in get_tcp_stream(pcap_data_dir + 'telnet_session.pcap', 3):
        try:
            # 提取Telnet数据部分的字段
            for x in pkt.telnet.data.fields:
                # 拼接字符串到all_telnet_data
                all_telnet_data += x.showname_value
        except AttributeError:
            pass
        i += 1

    # 逐行('\r\n'分隔)打印内容
    for line in all_telnet_data.split(r'\r\n'):
        print(line)
