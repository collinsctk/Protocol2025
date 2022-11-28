#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from sqlalchemy.orm import sessionmaker
from orm_1_create_table import RouterMonitor, engine
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as mtick

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
plt.rcParams['font.family'] = 'sans-serif'

Session = sessionmaker(bind=engine)
session = Session()


def cpu_show(dbname):
    time_list = []
    cpu_list = []

    # 把结果写入time_list和cpu_list的列表
    for i in session.query(RouterMonitor).all():
        time_list.append(i.record_datetime)
        cpu_list.append(i.cpu_useage_percent)

    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行, 每行一图, 第一图
    ax = fig.add_subplot(111)

    # 添加主题和注释
    plt.title('路由器CPU利用率')
    plt.xlabel('采集时间')
    plt.ylabel('CPU利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 格式化X轴
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))#设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置时间标签显示格式
    # 格式化Y轴
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f%%'))#格式化Y轴
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))  # 格式化Y轴
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, cpu_list, linestyle='solid', color='r', label='CPU利用率')
    # 设置Y轴 最小值 和 最大值
    ax.set_ylim(bottom=0, top=100)

    # 设置说明的位置
    ax.legend(loc='upper left')

    # 显示图像
    plt.show()


def mem_show(dbname):
    time_list = []
    mem_list = []

    # 把结果写入time_list和cpu_list的列表
    for i in session.query(RouterMonitor).all():
        time_list.append(i.record_datetime)

        mem_list.append((i.mem_use/(i.mem_use + i.mem_free))*100)

    # 调节图形大小，宽，高
    fig = plt.figure(figsize=(6, 6))
    # 一共一行, 每行一图, 第一图
    ax = fig.add_subplot(111)

    # 添加主题和注释
    plt.title('路由器MEM利用率')
    plt.xlabel('采集时间')
    plt.ylabel('MEM利用率')

    fig.autofmt_xdate()  # 当x轴太拥挤的时候可以让他自适应

    # 格式化X轴
    # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))#设置时间标签显示格式
    ax.xaxis.set_major_formatter(mdate.DateFormatter("%H:%M:%S"))  # 设置时间标签显示格式
    # 格式化Y轴
    # ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2f%%'))#格式化Y轴
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%d%%'))  # 格式化Y轴
    # 传入数据,time为X轴,cpu为Y轴
    ax.plot(time_list, mem_list, linestyle='solid', color='r', label='MEM利用率')
    # 设置Y轴 最小值 和 最大值
    ax.set_ylim(bottom=0, top=100)

    # 设置说明的位置
    ax.legend(loc='upper left')
    # 显示图像
    plt.show()


if __name__ == '__main__':
    cpu_show("deviceinfo.sqlite")
    mem_show("deviceinfo.sqlite")
