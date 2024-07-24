#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import sqlite3
import datetime
from matplotlib import pyplot as plt
from sqlalchemy.orm import sessionmaker
from netflow_orm_1_create_table import engine, Netflow
from sqlalchemy import func

Session = sessionmaker(bind=engine)
session = Session()


# 协议名称映射表
protocol_map = {'6/22': 'SSH',
                '6/23': 'Telnet',
                '17/137': 'UDP NETBIOS NS',
                '17/138': 'UDP NETBIOS DS',
                '17/5353': 'MDNS',
                '17/53': 'DNS',
                '17/514': 'Syslog',
                '17/2055': 'Netflow',
                '6/80': 'HTTP',
                '1/0': 'ICMP',
                '2/34': 'IGMP',
                '6/443': 'HTTPS',
                '17/5355': 'LLMNR'}

# 一个小时之前
one_hour_before = datetime.datetime.now() - datetime.timedelta(hours=1)
application_list = []

# 找到最近一个小时, 唯一的目的端口和协议号的组合
for l4_dst_port, protocol in session.query(Netflow.l4_dst_port, Netflow.protocol).group_by(
        Netflow.l4_dst_port, Netflow.protocol).filter(Netflow.record_datetime >= one_hour_before):
    application_list.append((l4_dst_port, protocol))


protocol_list = []
protocol_bytes = []
for x in application_list:
    # 提取应用(协议,目的端口)的入向字节数
    # 过滤近期一个小时的数据
    application_bytes = session.query(Netflow.in_bytes).filter(Netflow.l4_dst_port == x[0],
                                                               Netflow.protocol == x[1],
                                                               Netflow.record_datetime >= one_hour_before)
    # 把所有记录的字节数相加
    application_bytes_list = [a[0] for a in application_bytes]
    bytes_sum = sum(application_bytes_list)

    # 拼接协议和端口号
    protocol_port = str(x[1]) + '/' + str(x[0])
    # print(protocol_port)
    # print(bytes_sum)

    # 通过拼接后的协议和端口号, 找到协议名称, 然后把协议名称放入protocol_list
    protocol_list.append(protocol_map.get(protocol_port, protocol_port))
    # 把协议总和字节数放入protocol_bytes
    protocol_bytes.append(bytes_sum)

print(protocol_list)
print(protocol_bytes)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
# 调节图形大小，宽，高
plt.figure(figsize=(6, 6))

# 使用count_list的比例来绘制饼图
# 使用level_list作为注释
patches, l_text, p_text = plt.pie(protocol_bytes,
                                  labels=protocol_list,
                                  labeldistance=1.1,
                                  autopct='%3.1f%%',
                                  shadow=False,
                                  startangle=90,
                                  pctdistance=0.6)

# labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
# autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
# shadow，饼是否有阴影
# startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
# pctdistance，百分比的text离圆心的距离
# patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本

# 改变文本的大小
# 方法是把每一个text遍历。调用set_size方法设置它的属性
for t in l_text:
    t.set_size = 30
for t in p_text:
    t.set_size = 20
# 设置x，y轴刻度一致，这样饼图才能是圆的
plt.title('NetFlow流量分布')  # 主题
plt.axis('equal')
plt.legend(loc='upper left')
plt.show()
