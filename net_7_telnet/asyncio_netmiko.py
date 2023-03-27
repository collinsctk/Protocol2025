# 协程相关
import asyncio
import os
import threading

from net_8_ssh.ssh_sftp.ssh_client_netmiko import netmiko_show_cred
from datetime import datetime

# 协程任务循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

CSR = {
        'username': 'admin',
        'password': 'Cisc0123',
        # 'device_type': 'cisco_ios_telnet',  # Telnet
        'device_type': 'cisco_ios',  # SSH
        'secret': 'Cisc0123'
        }


# 定义netmiko的携程函数
async def async_netmiko(task_id, ip, username, password, cmd):
    print(f'ID: {task_id} Started')
    print(os.getpid(), threading.currentThread().ident)
    result = await loop.run_in_executor(None, netmiko_show_cred, ip, username, password, cmd)
    print(f'ID: {task_id} Stopped')
    return ip, result


if __name__ == '__main__':
    # 设备清单
    devices_list = ['10.1.1.253', '10.1.1.252', '10.1.1.253', '10.1.1.252', '10.1.1.253', '10.1.1.252']
    # 把ip, username, password, cmd放到一个列表, 便于后续使用*device来传多参数
    devices_cmd_list = [[d, 'admin', 'Cisc0123', 'show run'] for d in devices_list]
    # 多参数使用*device来传

    # 协程部分
    start_time = datetime.now()

    # 循环任务计数号
    task_no = 1

    # 协程的任务清单
    tasks = []

    for d in devices_cmd_list:
        # 产生携程任务
        task = loop.create_task(async_netmiko(task_no, *d))
        # 把产生的携程任务放入任务列表
        tasks.append(task)
        # 任务号加1
        task_no += 1

    # 等待所有任务执行完毕
    loop.run_until_complete(asyncio.wait(tasks))

    # 提取并且打印结果, 0号位为IP, 1号位为命令执行结果
    for s in tasks:
        if s.result():
            print('='*40 + s.result()[0] + '='*40)
            print(s.result()[1])

    # 打印结束时间
    end_time = datetime.now()
    print((end_time - start_time).seconds)

    # 普通操作
    # start_time = datetime.now()
    # for d in devices_cmd_list:
    #     cmd_result = netmiko_show_cred(*d)
    #     print('=' * 40 + d[0] + '=' * 40)
    #     print(cmd_result)
    # end_time = datetime.now()
    # print((end_time - start_time).seconds)
