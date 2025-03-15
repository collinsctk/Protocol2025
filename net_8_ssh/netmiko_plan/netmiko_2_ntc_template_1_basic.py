import os
from textfsm import clitable
from netmiko_1_show_client import netmiko_show_cred
from part_1_netmiko.netmiko_1_show_client import device_ip, username, password
from ntc_templates.parse import parse_output
from part_2_nornir.vault.python_script.vault_2_nonir import get_secret


def clitable_to_dict(cli_table):
    objs = []
    for row in cli_table:
        temp_dict = {}
        for index, element in enumerate(row):
            temp_dict[cli_table.header[index].lower()] = element
        objs.append(temp_dict)
    if len(objs) == 1:
        return objs[0]  # 只有一条记录，返回字典
    else:
        return objs  # 多条记录，返回列表


def netmiko_ntc_template(ip, username, password, cmd, device_type):
    ssh_output = netmiko_show_cred(ip, username, password, cmd, device_type)

    # 尝试加载自定义模板
    custom_template_path = f'.{os.sep}ntc-template'
    cli_table = clitable.CliTable('index', custom_template_path)

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

    return parse_result


if __name__ == "__main__":
    login_secret = get_secret()
    from pprint import pprint
    pprint(netmiko_ntc_template(device_ip,
                                login_secret.get('username'),
                                login_secret.get('password'),
                                # 'show ip inter brie',
                                # 'show version',
                                # 'show interface',
                                "show run | in username",
                                # 'show flash:',
                                'cisco_ios')
           )
