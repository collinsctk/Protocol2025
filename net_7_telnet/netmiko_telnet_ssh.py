#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from netmiko import Netmiko


CSR1 = {
        'host': '10.1.1.253',
        'username': 'admin',
        'password': 'Cisc0123',
        'device_type': 'cisco_ios_telnet',  # Telnet
        # 'device_type': 'cisco_ios',  # SSH
        'secret': 'Cisc0123',
}

# 支持的device_types
# https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
# 主要是CLASS_MAPPER_BASE部分

# ">" 下的exec命令
net_connect = Netmiko(**CSR1)  # ** 表示使用字典映射的方式来传参数
# Netmiko(host='10.1.1.253', username='admin', password='Cisc0123', device_type='cisco_ios_telnet', secret='Cisc0123')
print(net_connect.send_command("show ip interface brief"))

# "#" 下的exec命令
net_connect.enable()  # 如果需要, 使用enable进入特权模式
print(net_connect.send_command("show run"))

# 全局配置模式下的配置命令
config_commands = ['router ospf 1',
                   'router-id 1.1.1.1',
                   'network 1.1.1.1 0.0.0.0 a 0']

output = net_connect.send_config_set(config_commands)
print(output)

net_connect.disconnect()
