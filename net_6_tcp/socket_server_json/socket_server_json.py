#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import json
from socket import *

# return_data = {'data_recieved': True, 'data': 'Python'*2048}


def server_json(ip, port):
    # 创建TCP Socket, AF_INET为IPv4，SOCK_STREAM为TCP
    sockobj = socket(AF_INET, SOCK_STREAM)
    # 绑定套接字到地址，地址为（host，port）的元组
    sockobj.bind((ip, port))
    # 在拒绝连接前，操作系统可以挂起的最大连接数量，一般配置为5
    sockobj.listen(5)

    mss = 1460

    while True:  # 一直接受请求，直到ctl+c终止程序
        # 接受TCP连接，并且返回（conn,address）的元组，conn为新的套接字对象，可以用来接收和发送数据，address是连接客户端的地址
        connection, address = sockobj.accept()
        # conn.settimeout(5.0)  # 设置连接超时!
        # 打印连接客户端的IP地址
        print('Server Connected by', address)
        recieved_message = b''  # 预先定义接收信息变量
        recieved_message_fragment = connection.recv(mss)  # 读取接收到的信息，写入到接收到信息分片
        if len(recieved_message_fragment) < mss:  # 如果长度小于mss!表示客户发的数据小于mss!
            recieved_message = recieved_message_fragment
            obj = json.loads(recieved_message.decode())  # 把接收到信息json.loads回正常的obj
            print(obj)  # 打印obj，当然也可以选择写入文件或者数据库
            connection.send(json.dumps(obj).encode())  # 返回确认信息
        else:
            # 注意: 此处while + else的用法
            while len(recieved_message_fragment) == mss:  # 等于mss表示还有后续数据!
                recieved_message = recieved_message + recieved_message_fragment  # 把接收到信息分片重组装
                recieved_message_fragment = connection.recv(mss)  # 继续接收后续的mss的数据
            else:
                recieved_message = recieved_message + recieved_message_fragment  # 如果数据小于mss!拼接最后数据
            obj = json.loads(recieved_message.decode())  # 把接收到信息json.loads回正常的obj
            print(obj)  # 打印obj，当然也可以选择写入文件或者数据库
            connection.send(json.dumps(obj).encode())
        connection.close()


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # Server和Client需要分属两个不同的机器
    server_ip = '0.0.0.0'
    server_port = 6666
    server_json(server_ip, server_port)
