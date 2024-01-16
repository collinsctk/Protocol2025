#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

import socket

address = ("10.10.1.100", 6666)
# 创建UDP套接字Socket, AF_INET为IPv4, SOCK_DGRAM为Datagram就是UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # 收集客户输入数据
    msg = input('请输入数据:')
    # 如果客户输入为空,发送空数据,并且退出
    if not msg:
        s.sendto(msg.encode(), address)
        break
    # 如果客户输入不为空,发送数据
    s.sendto(msg.encode(), address)

s.close()

