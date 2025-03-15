from netmiko import Netmiko
import yaml
import os
from jinja2 import Template
from pprint import pprint
import asyncio
import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def netmiko_config_cred(host,
                              username,
                              password,
                              cmds_list,
                              device_type,
                              enable='Cisc0123',
                              verbose=False,
                              ssh_port=22
                              ):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'secret': enable,
                    'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)
        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


config_devices_info_dir = f'{current_dir}{os.sep}config-devices-info'
devices_config_file_name = 'devices_config.yaml'

config_template_dir = f'{current_dir}{os.sep}config-template'

# 任务的列表
tasks = []

with open(f'{config_devices_info_dir}{os.sep}{devices_config_file_name}') as data_f:
    devices_config_data = yaml.safe_load(data_f.read())
    for device in devices_config_data:
        configs = device.get('configs')
        device_ip = device.get('device_ip')
        device_type = device.get('device_type')
        username = device.get('username')
        password = device.get('password')
        total_cmd_list = []
        for config in configs:
            config_direction = config.get('config_direction')
            template_file_name = f'{config_direction}.jinja2'
            with open(f'{config_template_dir}{os.sep}{template_file_name}') as template_f:
                template = Template(template_f.read())
                config_str = template.render(config.get('config_data'))
                cmd_list = [line.strip() for line in config_str.split('\n') if line.strip()]
                total_cmd_list.extend(cmd_list)
        pprint(total_cmd_list)
        task = loop.create_task(netmiko_config_cred(device_ip,
                                                    username,
                                                    password,
                                                    total_cmd_list,
                                                    device_type,
                                                    verbose=True
                                                    ))
        tasks.append(task)


# 等待任务完成
loop.run_until_complete(asyncio.wait(tasks))

# 使用".result()"提取任务结果
result_list = []
for i in tasks:
    print(i.result())
    result_list.append(i.result())
