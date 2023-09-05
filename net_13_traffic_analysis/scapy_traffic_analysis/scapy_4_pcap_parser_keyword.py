#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging
import warnings
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
warnings.filterwarnings("ignore")
from kamene.all import *
import re
from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir


def pcap_parser(filename, keyword):
    # 本代码主要任务: 搜索PCAP文件里边的所有数据包,找到匹配关键字的数据包
    pkts_list = rdpcap(filename)  # 使用scapy的rdpcap函数打开pcap文件
    return_pkts_list = []  # 返回匹配数据包的清单！
    for packet in pkts_list.res:  # 遍历每一个数据包
        try:
            pkt_load = packet.getlayer('Raw').fields['load'].decode().strip()  # 提取负载内容
            re_keyword = '.*' + keyword + '.*'
            # 如果负载内容匹配，并且源端口为23，把数据包添加到return_pkts_list
            if re.match(re_keyword, pkt_load) and packet.getlayer('TCP').fields['sport'] == 23:
                return_pkts_list.append(packet)
        except Exception:
            pass
    return return_pkts_list  # 返回匹配数据包的清单！


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    # 搜索PCAP文件"login_invalid.pcap"中,出现invalid关键字的数据包
    pkts = pcap_parser(pcap_dir + "login_invalid.pcap", 'invalid')
    i = 1
    for pkt in pkts:
        print('==================第' + str(i) + "个包==================")
        pkt.show()
        i += 1
