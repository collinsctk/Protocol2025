#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/
import logging
import logging
logging.getLogger("kamene.runtime").setLevel(logging.ERROR)  # 清除报错
from kamene.all import ICMP, IP, sr1


def scapy_ping_one(host):
    packet = IP(dst=host) / ICMP() / b'Welcome to qytang'  # 构造Ping数据包
    ping = sr1(packet,
               timeout=1,
               verbose=False)  # 获取响应信息，超时为2秒，关闭详细信息

    try:
        if ping.getlayer(IP).fields['src'] == host and ping.getlayer(ICMP).fields['type'] == 0:
            # 如果收到目的返回的ICMP ECHO-Reply包
            return host, True  # 返回主机和结果，1为通
        else:
            return host, False  # 返回主机和结果，2为不通
    except AttributeError:
        return host, False  # 出现异常也返回主机和结果，2为不通


if __name__ == '__main__':
    # Windows Linux均可使用
    print(scapy_ping_one("196.21.5.1"))
    # print(scapy_ping_one(sys.argv[1]))
