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
# airflow 调度写入的PSQL数据库
# from net_4_snmp.airflow.dags.orm_1_create_table import engine
import pygal  # 引入 Pygal
from pygal.style import Style
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import cairosvg  # 导入 cairosvg，用于转换 SVG 为 PNG
import os
from pathlib import Path

# 本地循环写入的sqlite3
engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False')

Session = sessionmaker(bind=engine)
session = Session()

# 五分钟之前的时间
five_minutes_before = datetime.now() - timedelta(minutes=5)

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

#  获取当前文件的绝对路径
images_path = os.path.abspath(f'{current_file_path.parent}{os.sep}images_dir{os.sep}')


def cpu_show(filename):
    time_list = []
    cpu_list = []

    # 把结果写入 time_list 和 cpu_list 的列表，只取五分钟之内的数据
    for i in session.query(RouterMonitor).filter(RouterMonitor.record_datetime > five_minutes_before):
        time_list.append(i.record_datetime.strftime("%H:%M:%S"))  # 将时间格式转换为字符串，便于 Pygal 使用
        cpu_list.append(i.cpu_usage_percent)

    # 设置中文字体style
    custom_style = Style(
        title_font_family='Noto Sans CJK SC',
        legend_font_family='Noto Sans CJK SC',
        label_font_family='Noto Sans CJK SC',
        major_label_font_family='Noto Sans CJK SC',
        value_font_family='Noto Sans CJK SC'
    )

    # 使用 Pygal 创建平滑的折线图
    line_chart = pygal.Line(interpolate='cubic', range=(0, 100), style=custom_style)  # 启用平滑过渡
    # svg 不会有乱码,但是保持到png会有中文乱码
    line_chart.title = '主题: 路由器CPU利用率'
    line_chart.x_labels = time_list
    # svg 不会有乱码,但是保持到png会有中文乱码
    line_chart.add('CPU利用率', cpu_list)

    # 解决时间标签重叠问题，旋转标签
    line_chart.x_label_rotation = 45  # 将X轴标签旋转45度，避免重叠

    # 保存为 SVG 文件
    svg_filename = f'{images_path}{os.sep}{filename}.svg'
    # 保存为 PNG 文件
    png_filename = f'{images_path}{os.sep}{filename}.png'

    line_chart.render_to_file(svg_filename)
    cairosvg.svg2png(url=svg_filename, write_to=png_filename)

    return svg_filename, png_filename


def mem_show(filename):
    time_list = []
    mem_list = []

    # 把结果写入 time_list 和 mem_list 的列表，只取五分钟之内的数据
    for i in session.query(RouterMonitor).filter(RouterMonitor.record_datetime > five_minutes_before):
        time_list.append(i.record_datetime.strftime("%H:%M:%S"))  # 将时间格式转换为字符串，便于 Pygal 使用
        mem_list.append(i.mem_usage_percent)

    # 设置中文字体style
    custom_style = Style(
        title_font_family='Noto Sans CJK SC',
        legend_font_family='Noto Sans CJK SC',
        label_font_family='Noto Sans CJK SC',
        major_label_font_family='Noto Sans CJK SC',
        value_font_family='Noto Sans CJK SC'
    )

    # 使用 Pygal 创建平滑的折线图
    line_chart = pygal.Line(interpolate='cubic', range=(0, 100), style=custom_style)  # 启用平滑过渡
    # svg 不会有乱码,但是保持到png会有中文乱码
    line_chart.title = '主题: 路由器内存利用率'
    line_chart.x_labels = time_list
    # svg 不会有乱码,但是保持到png会有中文乱码
    line_chart.add('MEM利用率', mem_list)

    # 解决时间标签重叠问题，旋转标签
    line_chart.x_label_rotation = 45  # 将X轴标签旋转45度，避免重叠

    # 保存为 SVG 文件
    svg_filename = f'{images_path}{os.sep}{filename}.svg'
    # 保存为 PNG 文件
    png_filename = f'{images_path}{os.sep}{filename}.png'

    line_chart.render_to_file(svg_filename)
    cairosvg.svg2png(url=svg_filename, write_to=png_filename)

    return svg_filename, png_filename


if __name__ == '__main__':
    print(cpu_show('pygal_cpu_usage'))
    print(mem_show('pygal_mem_usage'))
