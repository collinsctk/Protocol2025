#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from socket import *

# 连接的服务器地址
myHost = '10.1.1.180'
# 连接的服务器端口号
myPort = 6666

mss = 1460

# 创建TCP Socket, AF_INET为IPv4，SOCK_STREAM为TCP
sockobj = socket(AF_INET, SOCK_STREAM)
# 连接到套接字地址，地址为（host，port）的元组
sockobj.connect((myHost, myPort))

while True:  # 一直执行循环直到break出现！
    msg = input("请输入回显信息(exit退出):")
    if msg == "":
        print("请输入正确信息!!!")
    elif msg != 'exit':
        sockobj.send(msg.encode())
        echo_msg = sockobj.recv(mss)
        print(echo_msg.decode())
    else:
        break
sockobj.close()
print("连接已经结束！！！")
