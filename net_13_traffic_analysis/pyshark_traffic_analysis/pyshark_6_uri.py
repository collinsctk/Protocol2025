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
import re
from net_13_traffic_analysis.pyshark_traffic_analysis.pyshark_0_pcap_dir import pcap_data_dir
pkt_list = []

cap = pyshark.FileCapture(pcap_data_dir + 'dos.pcap', keep_packets=False, display_filter='http')

url_dict = {}


def print_highest_layer(pkt):
    # 本代码的主要任务: 对HTTP流量进行分析,找到特定host的请求数量
    try:
        # 正则表达式匹配域名
        # https://blog.walterlv.com/post/match-web-url-using-regex.html

        re_result = re.match(r"(^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(?:\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$)",
                             pkt.http.host)
        if re_result:
            host = re_result.groups()[0]
        # 字典数据结构如下
        # 键为method和host, 值为数量
        counts = url_dict.get((pkt.http.request_method, host), 0)
        counts += 1
        url_dict[(pkt.http.request_method, host)] = counts
    except Exception:
        pass


# 应用函数到数据包
cap.apply_on_packets(print_highest_layer)


if __name__ == '__main__':
    # 使用matplot进行图形化展示
    import matplotlib.pyplot as plt

    # 字典的格式 url_dict[(pkt.http.request_method, host)] = counts
    # 取前五的url
    conn_num_list_top_5 = sorted(url_dict.items(), key=lambda x: x[1])[-5:]

    url = [a[0][1] for a in conn_num_list_top_5]
    hits = [a[1] for a in conn_num_list_top_5]
    plt.barh(url, hits, height=0.5)

    # ##########################添加注释###################################
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.title('站点访问量统计')  # 主题
    plt.xlabel('访问数量')  # X轴注释
    plt.ylabel('站点')  # Y轴注释
    # ##########################添加注释###################################
    # 使用WIN来显示图
    plt.show()
