#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from socket import *
import pickle
import struct
from pathlib import Path

def server_pickle(ip, port):
    # 创建TCP Socket, 并且绑定到端口上
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.bind((ip, port))
    sockobj.listen(5)

    print('Server is online')

    while True:  # 一直接受客户端的请求，直到ctl+c终止程序
        try:
            connection, address = sockobj.accept()
            print('Server Connected by', address)  # 打印客户端的地址
            mss = 1460  # 定义接收缓存区的大小
            buffer = []  # 创建缓存，存储接收到的数据
            while True:  # 一直接收数据，直到接收完毕
                data = connection.recv(mss)  # 接收数据
                if data:  # 如果接收到数据
                    buffer.append(data)  # 把接收到的数据，添加到缓存中
                else:  # 如果没有接收到数据，表示客户端已经发送完毕
                    obj = pickle.loads(b''.join(buffer))  # 把缓存中的数据拼接起来，并且unpickle
                    if isinstance(obj, dict):  # 如果是字典
                        print(obj)  # 打印字典
                    else:  # 如果是数据
                        # 使用Path获取当前文件的目录，然后找到file_dir目录
                        current_dir = Path(__file__).parent
                        file_dir = current_dir / 'file_dir'
                        # 如果file_dir目录不存在就创建它
                        file_dir.mkdir(exist_ok=True)
                        # 构建接收文件的完整路径
                        received_file = file_dir / 'Recieved_img.jpg'
                        # 写入文件
                        myfile = open(received_file, 'wb')
                        myfile.write(obj)
                        myfile.close()
                        print(f'文件接收成功, 并保存到{received_file}!')
                    break
            connection.close()
        except KeyboardInterrupt:  # 如果ctl+c
            break  # 退出while True
    sockobj.close()  # 关闭socket


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # Server和Client需要分属两个不同的机器
    server_ip = '0.0.0.0'
    server_port = 5555
    server_pickle(server_ip, server_port)
