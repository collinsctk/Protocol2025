#!/usr/bin/env python3.11
# -*- coding=utf-8 -*-

#  pip3.11 install pytest pythonping
import pytest
import pythonping

# Ping测试的目标
ping_target_1 = '196.21.5.211'
ping_target_2 = '196.21.5.212'


# ping测试函数，返回一个字典，包含可达性，平均RTT，和总RTT的列表
def ping(target, count=4):
    response_list = pythonping.ping(target, count=count)
    # 如果测试是成功的
    if response_list.success():
        # 所有测试的RTT的列表
        all_rtts = [response.time_elapsed for response in response_list]
        # 计算平均的RTT
        avg_rtt = sum(all_rtts) / len(all_rtts)
        # 返回可达性结果, 平均RTT, 和所有的RTT的列表
        return {
            'reachable': True,
            'avg_rtt': avg_rtt,
            'all_rtts': all_rtts
        }
    else:
        return {
            'reachable': False,
            'avg_rtt': None,
            'all_rtts': []
        }


# 使用pytest执行ping测试，测试ping_target_1
def test_ping_1():
    results = ping(ping_target_1)
    jitter = None
    # 计算抖动
    if results['reachable'] and len(results['all_rtts']) > 1:
        # 一次测试(4次)的rtt最大值 - rtt最小值
        jitter = max(results['all_rtts']) - min(results['all_rtts'])

    # 打印测试结果
    # ------------此处应该添加写入数据库的操作-------------
    print(results['reachable'])
    print(results['all_rtts'])
    print(results['avg_rtt'])
    print(jitter)

    # pytest测试, 判断是否可达
    assert results['reachable'] is True, f"测试目的{ping_target_1}不可达！"


# 使用pytest执行ping测试，测试ping_target_2
def test_ping_2():
    results = ping(ping_target_2)
    jitter = None
    # 计算抖动
    if results['reachable'] and len(results['all_rtts']) > 1:
        # 一次测试(4次)的rtt最大值 - rtt最小值
        jitter = max(results['all_rtts']) - min(results['all_rtts'])

    # 打印测试结果
    # ------------此处应该添加写入数据库的操作-------------
    print(results['reachable'])
    print(results['all_rtts'])
    print(results['avg_rtt'])
    print(jitter)

    # pytest测试, 判断是否可达
    assert results['reachable'] is True, f"测试目的{ping_target_2}不可达！"


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
