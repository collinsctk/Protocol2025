#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging

logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import *
import re
from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir


def find_pcap_syn_dos(pcap_filename):
    # 本代码的主要任务: 对会话(源,目,目的端口)统计会话数量,用于判断DoS攻击
    pkts_file = rdpcap(pcap_filename)  # 使用scapy的rdpcap函数打开pcap文件
    pkt_list = pkts_file.res  # 提取每一个包到清单pkt_list

    dos_dict = {}  # 最后的结果写入dos_dict,格式为{('196.21.5.12', '196.21.5.254', 5000): 36}!利用字典键值的唯一性
    for packet in pkt_list:
        try:
            if packet.getlayer(TCP).fields['flags'] == 2:  # SYN包
                source_ip = packet.getlayer(IP).fields['src']  # 提取源地址
                destination_ip = packet.getlayer(IP).fields['dst']  # 提取目的地址
                destination_port = packet.getlayer(TCP).fields['dport']  # 提取目的端口号
                conn = source_ip, destination_ip, destination_port  # 用源地址,目的地址和目的端口产生元组
                conn_counts = dos_dict.get(conn, 0)  # 判断是否有这个键值, 没有就返回0
                dos_dict[conn] = conn_counts + 1  # 在返回值的基础上加1
        except Exception:
            pass
    return dos_dict


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    dos_result = find_pcap_syn_dos(pcap_dir + "dos.pcap")

    from matplotlib import pyplot as plt

    # 提取数量大于5的连接
    conn_num_list = sorted([[conn, num] for conn, num in dos_result.items() if num > 5], key=lambda x: x[1])

    conn_list = []
    num_list = []
    for c, n in conn_num_list:
        conn_list.append(str(c))
        num_list.append(n)

    print(conn_list)
    print(num_list)

    plt.barh(conn_list, num_list, height=0.5)

    # ##########################添加注释###################################
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.title('SYN DoS分析')  # 主题
    plt.xlabel('数量')  # X轴注释
    plt.ylabel('连接')  # Y轴注释
    # ##########################添加注释###################################
    plt.show()
