import os
from part_1_netmiko.netmiko_1_show_client import netmiko_show_cred
from part_1_netmiko.netmiko_2_ntc_template_1_basic import clitable_to_dict
from textfsm import clitable
import yaml
from pprint import pprint
from ntc_templates.parse import parse_output

# 协程相关
import asyncio
import os


# 协程任务循环
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def async_netmiko_ntc_template(ip, username, password, cmd, device_type, ssh_port=22):

    ssh_output = netmiko_show_cred(ip, username, password, cmd, device_type, ssh_port=ssh_port)

    cli_table = clitable.CliTable('index', f'.{os.sep}ntc-template')

    attributes = {'Command': cmd, 'Vendor': device_type}

    try:
        # 尝试使用自定义模板解析
        cli_table.ParseCmd(ssh_output, attributes)
        parse_result = clitable_to_dict(cli_table)
    except Exception as e:
        # 如果自定义模板失败，尝试系统的ntc-template解析
        try:
            parse_result = parse_output(platform=device_type,
                                        command=cmd,
                                        data=ssh_output)
            if not parse_result:
                parse_result = ssh_output
        # 如果既然失败，直接返回ssh输出的原始内容
        except Exception as e:
            return ssh_output

    return {'device_ip': ip,
            'display_cmd': cmd,
            'display_result': parse_result}

tasks = []

display_devices_info_dir = './display-devices-info'
display_devices_info_file_name = 'display_devices.yml'


with open(f'{display_devices_info_dir}{os.sep}{display_devices_info_file_name}') as data_f:
    devices_info = yaml.safe_load(data_f.read())
    # pprint(devices_info)
    for device_info in devices_info:
        # 产生携程任务
        device_ip = device_info.get('device_ip')
        device_type = device_info.get('device_type')
        username = device_info.get('username')
        password = device_info.get('password')
        display_cmds = device_info.get('display_cmds')
        for display_cmd in display_cmds:
            task = loop.create_task(
                async_netmiko_ntc_template(device_ip, username, password, display_cmd, device_type))
            # 把产生的携程任务放入任务列表
            tasks.append(task)

loop.run_until_complete(asyncio.wait(tasks))

for t in tasks:
    result_list = []
    pprint(t.result())
    result_list.append(t.result())



