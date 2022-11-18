#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import json
from socket import *


def client_json(ip, port, obj):
    # 创建TCP Socket并连接
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((ip, port))

    mss = 1460

    # 把obj转换为JSON字节字符串
    send_message = json.dumps(obj).encode()
    # 读取mss字节长度数据, 准备发送数据分片
    send_message_fragment = send_message[:mss]
    # 剩余部分数据
    send_message = send_message[mss:]

    while send_message_fragment:
        sockobj.send(send_message_fragment)  # 发送数据分片（如果分片的话）
        send_message_fragment = send_message[:mss]  # 读取mss字节长度数据
        send_message = send_message[mss:]  # 剩余部分数据

    recieved_message = b''  # 预先定义接收信息变量
    recieved_message_fragment = sockobj.recv(mss)  # 读取接收到的信息，写入到接收到信息分片

    while recieved_message_fragment:
        recieved_message = recieved_message + recieved_message_fragment  # 把所有接收到信息分片重组装
        recieved_message_fragment = sockobj.recv(mss)

    print('收到确认数据:', json.loads(recieved_message.decode()))
    sockobj.close()


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # Server和Client需要分属两个不同的机器
    dict1 = {'key1': 'welcome to qytang', 'key2': [1, 2, 3, 4, 5], 'key3': ([3, 4], 'python'), 'key4': 'python'*2048}
    dict2 = {'key1': 'welcome to qytang', 'key2': [1, 2, 3, 4, 5], 'key3': ([3, 4], 'python'), 'key4': 'python'}
    client_json('10.1.1.180', 6666, dict1)
    client_json('10.1.1.180', 6666, dict2)
