#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/

import socket
import struct
import sys
import hashlib

# 绑定地址和端口
address = ("0.0.0.0", 6666)
# 创建UDP套接字Socket, AF_INET为IPv4, SOCK_DGRAM为Datagram就是UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 套接字绑定到地址,元组(host, port)
s.bind(address)

# 数据类型限制说明:
# 整数 (i): 4字节，范围 -2,147,483,648 到 2,147,483,647
# 字符串 (ns): n表示字节数，客户端限制不超过100字节
# 短整数 (h): 2字节，范围 -32,768 到 32,767
# MD5哈希 (16s): 固定16字节

print('UDP结构化数据服务器就绪!等待客户数据!')
print('预期接收格式: >i{n}sh16s (整数+变长字符串+短整数+MD5哈希)')
while True:
    try:
        # 接收UDP套接字的数据,1024为接收的最大数据量
        # UDP数据包大小限制为65507字节，但实际使用建议小于1500字节(MTU)
        data, addr = s.recvfrom(1024)
        
        if not data:
            print("客户端退出!")
            continue
            
        # 尝试解析结构化数据
        try:
            # 数据结构: >i{n}sh16s
            # 首先解析前4个字节的整数
            first_int = struct.unpack('>i', data[0:4])[0]
            
            # 解析最后18个字节: 2字节短整数 + 16字节MD5哈希
            last_short = struct.unpack('>h', data[-18:-16])[0]
            
            # 解析MD5哈希
            received_hash = data[-16:]
            
            # 中间部分是字符串，长度是总长度减去整数、短整数和MD5哈希的长度
            string_length = len(data) - 22  # 4字节整数 + 2字节短整数 + 16字节MD5
            
            # 解析字符串
            string_data = struct.unpack(f'>{string_length}s', data[4:-18])[0].decode()
            
            # 验证MD5哈希 (将所有数据拼接在一起计算哈希)
            combined_data = str(first_int).encode() + string_data.encode() + str(last_short).encode()
            calculated_hash = hashlib.md5(combined_data).digest()
            
            hash_valid = (calculated_hash == received_hash)
            
            print(f"接收到结构化数据: ({first_int}, '{string_data}', {last_short}, MD5:{received_hash.hex()}) 来自于: {addr}")
            print(f"哈希验证: {'成功' if hash_valid else '失败'}")
            
            # 数据范围验证
            if first_int < -2147483648 or first_int > 2147483647:
                print("警告: 接收到的整数超出正常范围")
                
            if last_short < -32768 or last_short > 32767:
                print("警告: 接收到的短整数超出正常范围")
                
            if string_length > 100:
                print(f"警告: 接收到的字符串长度({string_length}字节)超过建议的100字节限制")
                
        except Exception as e:
            print(f"解析数据失败: {e}")
            print(f"原始数据: {data}")
            
    except KeyboardInterrupt:
        print("\n服务器关闭")
        sys.exit()

s.close() 