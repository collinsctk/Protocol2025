# pip install jinja2
from netmiko import Netmiko
import yaml
import os
from jinja2 import Template
from part_1_netmiko.netmiko_1_show_client import device_ip, username, password


def netmiko_config_cred(host,
                        username,
                        password,
                        cmds_list,
                        device_type,
                        verbose=False,
                        ssh_port=22):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    # 'global_delay_factor': 2,  # 增加全局延迟因子
                    'session_log': 'session.log',  # 启用会话日志
                    'port': ssh_port
    }
    try:
        net_connect = Netmiko(**device_info)

        if verbose:
            output = net_connect.send_config_set(cmds_list)
            return output
        else:
            net_connect.send_config_set(cmds_list)
        net_connect.disconnect()

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


def config_cmd_list(config_direction_name):
    config_template_dir = './config-template'
    template_file_name = f'{config_direction_name}.jinja2'
    config_data_dir = './config-data'
    data_file_name = f'{config_direction_name}.yaml'

    with open(f'{config_data_dir}{os.sep}{data_file_name}') as data_f:
        data = yaml.safe_load(data_f.read())
        with open(f'{config_template_dir}{os.sep}{template_file_name}') as template_f:
            template = Template(template_f.read())
            config_str = template.render(data)
            # if line.strip() 确认strip后不为空
            return [line.strip() for line in config_str.split('\n') if line.strip()]


if __name__ == '__main__':
    # config_direction = 'snmp'
    config_direction = 'ospf'
    config_cmds = config_cmd_list(config_direction)
    print(netmiko_config_cred(device_ip,
                              username,
                              password,
                              config_cmds,
                              'cisco_ios',
                              verbose=True))
