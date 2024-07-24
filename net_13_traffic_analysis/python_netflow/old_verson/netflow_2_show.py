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
from net_13_traffic_analysis.python_netflow.old_verson.netflow_0_v9_process_module import db_dir
# 协议名称映射表
protocol_map = {'6/22': 'SSH',
                '6/23': 'Telnet',
                '17/137': 'UDP NETBIOS Name Service',
                '17/138': 'UDP NETBIOS Datagram Service',
                '17/5353': 'MDNS',
                '17/53': 'DNS',
                '17/514': 'Syslog',
                '17/2055': 'Netflow',
                '6/80': 'HTTP',
                '1/0': 'ICMP',
                '6/443': 'HTTPS',
                '17/5355': 'LLMNR'}

# 连接数据库
conn = sqlite3.connect(db_dir + 'netflow.sqlite')
cursor = conn.cursor()

one_hour_before = datetime.datetime.now() - datetime.timedelta(hours=1)
# 找到唯一的目的端口和协议
cursor.execute("select 目的端口,协议 from netflowdb group by 目的端口,协议 and 记录时间 > ?",
               (one_hour_before, ))
yourresults = cursor.fetchall()

application_list = []

# 找到出现的应用(协议,目的端口)
for dbinfo in yourresults:
    application_list.append(dbinfo)

protocol_list = []
protocol_bytes = []
for x in application_list:
    # 提取应用(协议,目的端口)的入向字节数
    # 过滤近期一个小时的数据
    cursor.execute("select 入向字节数 from netflowdb where 协议=? and 目的端口=? and 记录时间 > ?",
                   (x[1], x[0], one_hour_before))
    yourresults = cursor.fetchall()
    bytes_sum = 0
    # 把每一个会话的字节数加起来
    for dbinfo in yourresults:
        bytes_sum += dbinfo[0]
    protocol_port = str(x[1]) + '/' + str(x[0])
    # 把协议清单写入protocol_list
    print(protocol_bytes)
    protocol_list.append(protocol_map.get(protocol_port, protocol_port))
    # 把协议对于的字节数,写入protocol_bytes
    protocol_bytes.append(bytes_sum)

print(protocol_list)
print(protocol_bytes)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
# 调节图形大小，宽，高
plt.figure(figsize=(6, 6))

# 使用count_list的比例来绘制饼图
# 使用level_list作为注释
patches, l_text, p_text = plt.pie(protocol_bytes, labels=protocol_list,
                                  labeldistance=1.1, autopct='%3.1f%%', shadow=False,
                                  startangle=90, pctdistance=0.6)

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
plt.axis('equal')
plt.legend(loc='upper left')
plt.show()
