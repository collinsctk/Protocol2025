#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from socket import socket, AF_PACKET, SOCK_RAW
from tools.checksum import do_checksum
from tools.change_ip_to_bytes import change_ip_to_bytes
from tools.change_mac_to_bytes import change_mac_to_bytes
import struct
import random


def ether(src, dst, ether_type="0800"):
    # 构建源MAC地址,6个字节
    src_mac_addr = change_mac_to_bytes(src)
    # 构建目的MAC地址,6个字节
    dst_mac_addr = change_mac_to_bytes(dst)
    # 以太网类型为2个字节
    ether_type = struct.pack('!H', int(ether_type, 16))
    # 拼接以太网头部,并返回
    return src_mac_addr + dst_mac_addr + ether_type


def ip(version=4, header_length=5, tos=b"\x00", total_length=100, identifier=random.randint(1, 65535),
       ip_flags_d=0, ip_flags_m=0, offset=0, ttl=128, protocol=17, src="127.0.0.1", dst="127.0.0.1"):
    # 构建IP版本与IP头部长度的第一个字节
    version_headerlength = struct.pack('B', (((version << 4) + header_length) & 0xff))

    # TOS为以传入的内容为准, TOS为第二个字节

    # 构建IP总长度,第三,第四个字节
    total_length = struct.pack("!H", total_length)

    # 构建IP ID,第五,第六个字节
    identifier = struct.pack("!H", identifier)

    # 构建分片相关部分,第七,第八个字节
    fragment = struct.pack('!H', (((ip_flags_d << 14) + (ip_flags_m << 13) + offset) & 0xffff))

    # TTL,第九个字节
    ttl = struct.pack("B", ttl)

    # 协议,第十个字节
    protocol = struct.pack("B", protocol)

    # 初始校验和填0,第十一,第十二个字节
    pre_ip_check_sum = b"\x00\x00"

    # 源IP地址,第十三到第十六个字节
    src_ip_address = change_ip_to_bytes(src)

    # 目的IP地址,第十七到第二十个字节
    dst_ip_address = change_ip_to_bytes(dst)

    # 为了计算校验和,把IP头部拼接起来
    pre_ip_header = version_headerlength + tos + total_length + identifier + fragment + ttl + protocol + pre_ip_check_sum + src_ip_address + dst_ip_address

    # 计算校验和
    checksum = do_checksum(pre_ip_header)

    # 重新拼接IP头部,放入校验和字段
    ip_hder = version_headerlength + tos + total_length + identifier + fragment + ttl + protocol + checksum + src_ip_address + dst_ip_address

    # 返回IP头部
    return ip_hder


def udp(src_port, dst_port, udp_length, u_data, src_ip_address, dst_ip_address, Protocol=17):
    # 构建源端口字段, 第一,第二个字节
    sourc_port = struct.pack("!H", src_port)

    # 构建目的端口字段,第三,第四个字节
    dest_port = struct.pack("!H", dst_port)

    # 构建UDP长度字段,第五,第六个字节
    udp_length = struct.pack("!H", udp_length)

    # 初始化校验和填0
    pre_udp_checksum = b"\x00\x00"

    # UDP数据
    u_data = u_data.encode()

    # 如果长度为偶数,不用添加垫片
    if len(u_data) % 2 == 0:
        pad = b""
    # 如果长度为基数,需要添加垫片b"\x00"
    else:
        pad = b"\x00"

    # 计算UDP校验和
    udp_check_sum = do_checksum(change_ip_to_bytes(src_ip_address) +
                                change_ip_to_bytes(dst_ip_address) +
                                b"\x00" +
                                struct.pack("B", Protocol) +
                                udp_length +
                                sourc_port +
                                dest_port +
                                udp_length +
                                pre_udp_checksum +
                                u_data +
                                pad)

    # 拼接UDP头部,放入校验和
    udp_hder = sourc_port + dest_port + udp_length + udp_check_sum

    # 返回UDP头部
    return udp_hder


if __name__ == "__main__":
    # 只适用于Linux解释器
    # 创建原始套接字
    s = socket(AF_PACKET, SOCK_RAW)
    # 绑定到本地端口
    s.bind(("ens192", 0))

    # 本次试验需要WIN作为服务器,Linux作为客户端连接
    dst_ip = "10.1.1.100"
    src_ip = "10.1.1.180"

    # UDP传输数据
    udp_data = "cisco123456"
    # 计算IP总长度
    t_length = 20 + 8 + len(udp_data)
    # 计算UDP总长度
    u_length = 8 + len(udp_data)
    # 产生以太网头部
    ether_header = ether("00-50-56-A1-FA-B1", "00:50:56:a1:6e:62", "0800")
    # 产生IP头部
    ip_header = ip(total_length=t_length, ip_flags_d=0, ip_flags_m=0, offset=0, ttl=128, protocol=17, src=src_ip,
                   dst=dst_ip)
    # 产生UDP头部
    udp_header = udp(1024, 6666, udp_length=u_length, u_data=udp_data, src_ip_address=src_ip,
                     dst_ip_address=dst_ip)
    # 拼接以太网头部,IP头部,UDP头部
    packet = ether_header + ip_header + udp_header + udp_data.encode()
    # 发送数据包
    s.send(packet)
