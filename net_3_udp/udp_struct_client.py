#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

import socket
import struct
import hashlib

# 服务器地址和端口
address = ("196.21.5.218", 6666)
# 创建UDP套接字Socket, AF_INET为IPv4, SOCK_DGRAM为Datagram就是UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 数据类型限制说明:
# 整数 (i): 4字节，范围 -2,147,483,648 到 2,147,483,647
# 短整数 (h): 2字节，范围 -32,768 到 32,767
# 字符串 (ns): n表示字节数，建议不超过100字节
# MD5哈希 (16s): 固定16字节

while True:
    try:
        # 收集用户输入
        number = input('请输入一个整数 (-2147483648 到 2147483647): ')
        if not number:
            break
        
        number = int(number)
        # 验证整数范围
        if number < -2147483648 or number > 2147483647:
            print("整数超出范围!")
            continue
            
        text = input('请输入一个字符串 (不超过100个字符): ')
        if not text:
            break
        
        # 验证字符串长度
        if len(text.encode()) > 100:
            print("字符串太长，请限制在100个字节以内!")
            continue
            
        extra = input('请输入一个短整数 (-32768 到 32767): ')
        if not extra:
            break
            
        extra = int(extra)
        # 验证短整数范围
        if extra < -32768 or extra > 32767:
            print("短整数超出范围!")
            continue
        
        # 使用struct打包数据
        # '>i{len}sh16s' 格式说明:
        # '>' - 大端序
        # 'i' - 4字节整数
        # '{len}s' - 指定长度的字符串
        # 'h' - 2字节短整数
        # '16s' - 16字节MD5哈希
        text_bytes = text.encode()
        
        # 计算MD5哈希值 (对字符串和两个整数的组合进行哈希)
        md5_hash = hashlib.md5()
        md5_hash.update(str(number).encode())
        md5_hash.update(text_bytes)
        md5_hash.update(str(extra).encode())
        hash_value = md5_hash.digest()  # 获取二进制哈希值
        
        # 打包所有数据，包括哈希值
        packed_data = struct.pack(f'>i{len(text_bytes)}sh16s', number, text_bytes, extra, hash_value)
        
        # 发送打包后的数据
        s.sendto(packed_data, address)
        print(f"已发送打包数据: ({number}, '{text}', {extra}, MD5:{hash_value.hex()})")
        
    except ValueError:
        print("请输入有效的数字!")
    except KeyboardInterrupt:
        break

print("客户端关闭")
s.close() 