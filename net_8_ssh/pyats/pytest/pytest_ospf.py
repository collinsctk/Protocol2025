#!/usr/bin/env python3.11
# -*- coding=utf-8 -*-

#  pip3.11 install pytest netmiko
import pytest
from netmiko import Netmiko
import os
import time

# # 等待OSPF邻居建立
# time.sleep(5)

# 提取Gitlab CI/CD环境变量
ios_xe_username = 'admin'
ios_xe_password = 'Cisc0123'

# -----------------测试C8Kv1（ip:10.10.1.1）有OSPF邻居（router-id:2.2.2.2）-----------------
test_ospf_router_1 = "196.21.5.211"
test_ospf_neigh_id_2 = "2.2.2.2"
# -----------------测试C8Kv2（ip:10.10.1.2）有OSPF邻居（router-id:1.1.1.1）-----------------
test_ospf_router_2 = "196.21.5.212"
test_ospf_neigh_id_1 = "1.1.1.1"


# netmiko连接设备并获取OSPF邻居信息
# 返回的是一个字典，key是邻居的router-id，value是邻居的状态
# 例如 {"2.2.2.2": "FULL/DR"}
def netmiko_show_cred(ospf_router):
    device_info = {
        'host': ospf_router,
        'username': ios_xe_username,
        'password': ios_xe_password,
        'device_type': 'cisco_ios',
    }
    try:
        net_connect = Netmiko(**device_info)
        nei_dict = {}
        nei_list = net_connect.send_command('show ip ospf neighbor',
                                            use_textfsm=True  # 使用textfsm解析show ip ospf neighbor的输出
                                            )
        if nei_list:
            for n in nei_list:
                nei_dict[n['neighbor_id']] = n['state']

        return nei_dict  # 具体格式: {"2.2.2.2": "FULL/DR"}
    except Exception as e:
        print(e)
        return None


# 测试1，测试C8Kv1的OSPF邻居
def test_ospf_neigh_1():
    test_nei_router_id = test_ospf_neigh_id_2
    test_ospf_router_ip = test_ospf_router_1
    ospf_neigh = netmiko_show_cred(test_ospf_router_ip)
    # ~~~~测试1: 确认存在OSPF邻居~~~~
    assert ospf_neigh is not None, f"获取{test_ospf_router_ip}OSPF邻居信息失败"
    # ~~~~测试2: 期望的邻居存在于当前的邻居清单中~~~~
    assert test_nei_router_id in ospf_neigh, f"检查的OSPF邻居{test_nei_router_id}不在{test_ospf_router_ip}的邻居列表中"
    # ~~~~测试3: 期望的邻居状态是FULL~~~~
    assert 'FULL' in ospf_neigh[test_nei_router_id], f"{test_ospf_router_ip}的邻居{test_nei_router_id}状态不是FULL"


# 测试3，测试C8Kv2的OSPF邻居
def test_ospf_neigh_2():
    test_nei_router_id = test_ospf_neigh_id_1
    test_ospf_router_ip = test_ospf_router_2
    ospf_neigh = netmiko_show_cred(test_ospf_router_ip)
    # ~~~~测试1: 确认存在OSPF邻居~~~~
    assert ospf_neigh is not None, f"获取{test_ospf_router_ip}OSPF邻居信息失败"
    # ~~~~测试2: 期望的邻居存在于当前的邻居清单中~~~~
    assert test_nei_router_id in ospf_neigh, f"检查的OSPF邻居{test_nei_router_id}不在{test_ospf_router_ip}的邻居列表中"
    # ~~~~测试3: 期望的邻居状态是FULL~~~~
    assert 'FULL' in ospf_neigh[test_nei_router_id], f"{test_ospf_router_ip}的邻居{test_nei_router_id}状态不是FULL"


if __name__ == '__main__':
    # 抑制如下警告
    """
    =============================== warnings summary ===============================
    pytest_dir/pytest_ospf.py::test_ospf_neigh
      /usr/local/lib/python3.11/site-packages/netmiko/utilities.py:297: DeprecationWarning: path is deprecated. Use files() 
      instead. Refer to https://importlib-resources.readthedocs.io/en/latest/using.html#migrating-from-legacy for migration 
      advice.
        with pkg_resources.path(
    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    """
    pytest.main(['-v', '-W', 'ignore::DeprecationWarning', __file__])
