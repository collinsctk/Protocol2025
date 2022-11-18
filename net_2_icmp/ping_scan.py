#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import logging
import ipaddress
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)
import sys
if sys.platform == 'linux':
    from multiprocessing.pool import Pool
else:
    from multiprocessing.pool import ThreadPool as Pool

from net_2_icmp.ping_one import scapy_ping_one
from kamene.all import *
from tools.sort_ip import sort_ip
from net_1_arp.time_decorator import run_time


@run_time()
def scapy_ping_scan(network):
    net = ipaddress.ip_network(network)
    ip_list = [str(ip_add) for ip_add in net]  # 把网络(net)中的IP放入ip_list
    pool = Pool(processes=100)  # 创建多进程的进程池（并发为10）
    # pool = ThreadPool(processes=100)  # 创建多进程的进程池（并发为10）

    # 方案一
    # result = []
    # for i in ip_list:
    #     result.append(pool.apply_async(scapy_ping_one, args=(i,)))

    # 方案二
    result = pool.map(scapy_ping_one, ip_list)  # 关联函数与参数，并且提取结果到result

    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束

    scan_list = []  # 扫描结果IP地址的清单
    # print(result)
    # 方案一
    # for scan_result in result:
    #     ip_address, ok = scan_result.get()
    #     if ok:  # 如果ok为True
    #         scan_list.append(ip_address)  # 把IP地址放入scan_list清单里边
    # 方案二
    for ip_address, ok in result:
        if ok:  # 如果ok为True
            scan_list.append(ip_address)  # 把IP地址放入scan_list清单里边
    return sort_ip(scan_list)  # 排序并且打印清单


if __name__ == '__main__':
    # Windows Linux均可使用
    for ip in scapy_ping_scan("10.1.1.0/24"):
        print(str(ip))

