#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from socket import *
from datetime import datetime

# 配置本地服务器IP地址
myHost = '0.0.0.0'
# 配置本地服务器端口号
myPort = 6666

# 创建TCP Socket, AF_INET为IPv4，SOCK_STREAM为TCP
sockobj = socket(AF_INET, SOCK_STREAM)
# 绑定套接字到地址，地址为（host，port）的元组
sockobj.bind((myHost, myPort))
# 在拒绝连接前，操作系统可以挂起的最大连接数量，一般配置为5
# 注意:并不支持并发!
sockobj.listen(5)
mss = 1460
print('Server Started!')
while True:  # 一直接受请求，直到ctl+c终止程序
    # 接受TCP连接，并且返回（conn,address）的元组，conn为新的套接字对象，可以用来接收和发送数据，address是连接客户端的地址
    connection, address = sockobj.accept()
    # 打印连接客户端的IP地址
    print('Server Connected by', address)
    while True:
        data = connection.recv(mss)  # 接收数据，1024为bufsize，表示一次接收的最大数据量！
        if not data:
            break  # 如果没有数据就退出循环
        # 添加时间并发送回显数据给客户，注意Python3.x后，发送和接收的数据必须为二进制！
        connection.send(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Server send Echo ==> '.encode() + data)
    connection.close()  # 关闭连接
