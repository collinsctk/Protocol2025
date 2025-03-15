#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/
import sys
import os
from pathlib import Path

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()
# 当前目录的路径
current_dir = current_file_path.parent.parent
root_dir = current_dir.parent

sys.path.insert(1, str(root_dir))

from sqlalchemy.orm import sessionmaker
from net_4_snmp.practice_lab.orm_1_create_table import RouterMonitor, db_filename
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from bokeh.plotting import figure, output_file, save
from bokeh.models import DatetimeTickFormatter, HoverTool
import numpy as np
# airflow 调度写入的PSQL数据库
# from net_4_snmp.airflow.dags.orm_1_create_table import engine
from scipy.interpolate import make_interp_spline
import pytz
import os
from pathlib import Path


# 本地循环写入的sqlite3
engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False')
Session = sessionmaker(bind=engine)
session = Session()

# 一个小时之前的时间
one_hours_before = datetime.now() - timedelta(hours=1)

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

#  获取当前文件的绝对路径
images_path = os.path.abspath(f'{current_file_path.parent}{os.sep}images_dir{os.sep}')


def smooth_data(x, y, points=500):
    """使用样条插值平滑曲线"""
    x_numeric = np.array([t.timestamp() for t in x])  # 将时间转换为数字
    spline = make_interp_spline(x_numeric, y)
    x_smooth = np.linspace(x_numeric.min(), x_numeric.max(), points)
    y_smooth = spline(x_smooth)
    x_smooth_dates = [datetime.fromtimestamp(ts, pytz.timezone('Asia/Chongqing')) for ts in x_smooth]
    return x_smooth_dates, y_smooth


def cpu_show(filename):
    time_list = []
    cpu_list = []

    # 把结果写入 time_list 和 cpu_list 的列表，只取一个小时之内的数据
    for i in session.query(RouterMonitor).filter(RouterMonitor.record_datetime > one_hours_before):
        time_list.append(i.record_datetime.astimezone(pytz.timezone('Asia/Chongqing')))
        cpu_list.append(i.cpu_usage_percent)

    # 平滑数据
    time_smooth, cpu_smooth = smooth_data(time_list, cpu_list)

    # 创建 Bokeh 图表，设置 Y 轴范围
    p = figure(title="路由器CPU利用率", x_axis_type='datetime', width=800, height=400, y_range=(0, 100))

    # 添加平滑的线条
    p.line(time_smooth, cpu_smooth, legend_label="CPU 利用率", line_width=2, color='blue')

    # 添加数据点和悬停工具
    p.scatter(time_list, cpu_list, size=8, color='red', legend_label="CPU 数据点")
    hover = HoverTool(tooltips=[("时间", "@x{%F %T}"), ("CPU 利用率", "@y")],
                      formatters={'@x': 'datetime'})
    p.add_tools(hover)

    # 设置 X 轴时间格式，减少标签密度
    p.xaxis.formatter = DatetimeTickFormatter(
        seconds="%H:%M:%S",
        minsec="%H:%M:%S",
        minutes="%H:%M",
        hourmin="%H:%M",
        hours="%H:%M",
        days="%m/%d",
        months="%m/%d",
        years="%Y"
    )
    p.xaxis.major_label_orientation = 0.5  # 设置 X 轴标签旋转角度，避免重叠

    # 设置 X 轴和 Y 轴标签
    p.xaxis.axis_label = '采集时间'
    p.yaxis.axis_label = 'CPU 利用率 (%)'

    # 保存为 HTML 文件
    html_filename = f'{images_path}{os.sep}{filename}.html'

    # 保存图表为 HTML
    output_file(html_filename)  # 使用带前缀的文件名
    save(p)

    return html_filename


def mem_show(filename):
    time_list = []
    mem_list = []

    # 从数据库中获取数据，写入 time_list 和 mem_list
    for i in session.query(RouterMonitor).filter(RouterMonitor.record_datetime > one_hours_before):
        time_list.append(i.record_datetime.astimezone(pytz.timezone('Asia/Chongqing')))
        mem_list.append(i.mem_usage_percent)

    # 检查是否有数据
    if not time_list or not mem_list:
        print("没有足够的数据来生成MEM利用率图表。")
        return

    # 创建 Bokeh 图表，设置 Y 轴范围
    p = figure(title="路由器MEM利用率", x_axis_type='datetime', width=800, height=400, y_range=(0, 100))

    # 连接数据点，直接绘制线条
    p.line(time_list, mem_list, legend_label="MEM 利用率", line_width=2, color='green')

    # 添加数据点和悬停工具
    p.scatter(time_list, mem_list, size=8, color='orange', legend_label="MEM 数据点")
    hover = HoverTool(tooltips=[("时间", "@x{%F %T}"), ("MEM 利用率", "@y")],
                      formatters={'@x': 'datetime'})
    p.add_tools(hover)

    # 格式化 X 轴时间显示，确保 X 轴是时间，减少标签密度
    p.xaxis.formatter = DatetimeTickFormatter(
        seconds="%H:%M:%S",
        minsec="%H:%M:%S",
        minutes="%H:%M",
        hourmin="%H:%M",
        hours="%H:%M",
        days="%m/%d",
        months="%m/%d",
        years="%Y"
    )
    p.xaxis.major_label_orientation = 0.5  # 设置 X 轴标签旋转角度，避免重叠

    # 设置 X 轴和 Y 轴标签
    p.xaxis.axis_label = '采集时间'
    p.yaxis.axis_label = 'MEM 利用率 (%)'

    # 保存为 HTML 文件
    html_filename = f'{images_path}{os.sep}{filename}.html'

    # 保存图表为 HTML
    output_file(html_filename)
    save(p)

    return html_filename


if __name__ == '__main__':
    print(cpu_show("bokeh_cpu_usage"))
    print(mem_show("bokeh_mem_usage"))

