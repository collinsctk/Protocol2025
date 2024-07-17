#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


import logging
import ipaddress
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
from multiprocessing.pool import ThreadPool as Pool

from net_2_icmp.ping_one import scapy_ping_one
from kamene.all import *
from tools.sort_ip import sort_ip
from net_1_arp.time_decorator import run_time


@run_time()
def scapy_ping_scan(network, ifname):
    net = ipaddress.ip_network(network)
    ip_list = [str(ip_add) for ip_add in net]  # 把网络(net)中的IP放入ip_list
    pool = Pool(processes=100)  # 创建多进程的进程池（并发为10）
    # pool = ThreadPool(processes=100)  # 创建多进程的进程池（并发为10）

    result = []
    for i in ip_list:
        result.append(pool.apply_async(scapy_ping_one, args=(i, ifname)))

    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束

    scan_list = []  # 扫描结果IP地址的清单

    for scan_result in result:
        ip_address, ok = scan_result.get()
        if ok:  # 如果ok为True
            scan_list.append(ip_address)  # 把IP地址放入scan_list清单里边

    return sort_ip(scan_list)  # 排序并且打印清单


if __name__ == '__main__':
    # Windows Linux均可使用
    import platform
    if platform.system() == "Linux":
        input_ifname = 'ens224'
    elif platform.system() == "Windows":
        # 注意网卡有两个名字
        # 名称1: VMware Network Adapter VMnet1 ---- 显示的网卡名字（名字可以改）
        # 名称2: VMware Virtual Ethernet Adapter for VMnet1 ---- Kamene需要这个名字（不能改）
        # 可以使用函数get_ifname()从名称1得到名称2, 但是速度很慢，建议直接手动输入名称2
        input_ifname = 'VMware Virtual Ethernet Adapter for VMnet1'
    for ip in scapy_ping_scan("10.10.1.0/24", input_ifname):
        print(str(ip))

