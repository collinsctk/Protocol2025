#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import paramiko
import time

def ssh_client_one_cmd(ip, username, password, cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建SSH Client
        ssh.load_system_host_keys()  # 加载系统SSH密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
        
        # 连接到设备
        ssh.connect(ip, port=22, username=username, password=password, timeout=10, allow_agent=False, look_for_keys=False)
        
        stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
        x = stdout.read().decode()  # 读取回显
        ssh.close()
        return x

    except Exception as e:
        print(f'{ip}\tError\n {e}')
        return None


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    result = ssh_client_one_cmd('196.21.5.212',
                                'admin',
                                'Cisc0123',
                                'show version')
    
    print(result)