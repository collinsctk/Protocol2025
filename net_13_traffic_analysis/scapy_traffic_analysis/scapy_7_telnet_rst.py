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
import re
from kamene.all import *
from tools.scapy_iface import scapy_iface
from net_13_traffic_analysis.scapy_traffic_analysis.scapy_0_pcap_dir import pcap_dir

qyt_string = b''


def reset_tcp(pkt):
    # 本代码主要任务: 对传入的数据包,发送TCP Rest进行会话重置
    source_mac = pkt[Ether].fields['src']
    destination_mac = pkt[Ether].fields['dst']
    source_ip = pkt[IP].fields['src']
    destination_ip = pkt[IP].fields['dst']
    source_port = pkt[TCP].fields['sport']
    destination_port = pkt[TCP].fields['dport']
    seq_sn = pkt[TCP].fields['seq']
    ack_sn = pkt[TCP].fields['ack']

    a = Ether(src=source_mac, dst=destination_mac) / IP(src=source_ip, dst=destination_ip) / TCP(dport=destination_port,
                                                                                                 sport=source_port,
                                                                                                 flags=4, seq=seq_sn)
    b = Ether(src=destination_mac, dst=source_mac) / IP(src=destination_ip, dst=source_ip) / TCP(dport=source_port,
                                                                                                 sport=destination_port,
                                                                                                 flags=4, seq=ack_sn)
    sendp(a,
          iface=global_if,
          verbose=False)
    sendp(b,
          iface=global_if,
          verbose=False)


def telnet_monitor_callback(pkt):
    # 通过对Telnet会话数据的拼接,判断是否出现show ver字段, 如果出现重置会话
    global qyt_string
    try:
        if pkt.getlayer(TCP).fields['dport'] == 23:
            if pkt.getlayer(Raw).fields['load'].decode():
                qyt_string = qyt_string + pkt.getlayer(Raw).fields['load']  # 不断提取数据,拼接到qyt_string
    except Exception:
        pass

    if re.match(br'(.*\r\n.*)*sh.*\s+ver.*', qyt_string):  # 如果出现show ver字段,就Rest踢掉此会话
        reset_tcp(pkt)
        

def telnet_rst(user_filter, ifname):
    # 本代码主要任务: 使用过滤器捕获数据包, 把捕获的数据包交给telnet_monitor_callback进行处理
    global global_if
    global_if = scapy_iface(ifname)
    ptks = sniff(prn=telnet_monitor_callback,
                 filter=user_filter,
                 store=1,
                 iface=global_if,
                 timeout=10)
    wrpcap(pcap_dir + "temp.cap", ptks)
    print(qyt_string)


if __name__ == "__main__":
    telnet_rst("tcp port 23 and ip host 10.10.1.1", "ens224")
