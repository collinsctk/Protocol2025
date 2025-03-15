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
from kamene.all import *
import os
import sys

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from net_2_icmp.ping_one import scapy_ping_one
from tools.sort_ip import sort_ip
from net_1_arp.time_decorator import run_time


@run_time()
def scapy_ping_scan(network):
    net = ipaddress.ip_network(network)
    ip_list = [str(ip_add) for ip_add in net]  # 把网络(net)中的IP放入ip_list
    pool = Pool(processes=100)  # 创建多进程的进程池（并发为10）
    # pool = ThreadPool(processes=100)  # 创建多进程的进程池（并发为10）

    result = []
    for i in ip_list:
        result.append(pool.apply_async(scapy_ping_one, args=(i,)))

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
    for ip in scapy_ping_scan("196.21.5.0/24"):
        print(str(ip))

