from textfsm import clitable
from netmiko import Netmiko
import os


def clitable_to_dict(cli_table):
    objs = []
    # print(cli_table)  # cli_table是cli_table.ParseCmd(ifstate_ouput, attributes)解析结果
    """
    INTERFACE, LINK_STATUS, ADMIN_STATE, HARDWARE_TYPE, ADDRESS, BIA, DESCRIPTION, IP_ADDRESS, MTU, DUPLEX, SPEED, BANDWIDTH, ENCAPSULATION
    GigabitEthernet2, up, up, vNIC, 0050.56a1.3448, 0050.56a1.3448, , , 1500, Full Duplex, 1000Mbps, 1000000 Kbit, ARPA
    """
    for row in cli_table:
        # 提取每一行
        # GigabitEthernet2, up, up, vNIC, 0050.56a1.3448, 0050.56a1.3448, , , 1500, Full Duplex, 1000Mbps, 1000000 Kbit, ARPA, up, up, vNIC, 0050.56a1.3448, 0050.56a1.3448, , , 1500, Full Duplex, 1000Mbps, 1000000 Kbit, ARPA
        temp_dict = {}
        # index, element
        # 0    , GigabitEthernet2
        for index, element in enumerate(row):
            # cli_table.header
            # INTERFACE, LINK_STATUS, ADMIN_STATE, HARDWARE_TYPE, ADDRESS, BIA, DESCRIPTION, IP_ADDRESS, MTU, DUPLEX, SPEED, BANDWIDTH, ENCAPSULATION
            temp_dict[cli_table.header[index].lower()] = element  # {'interface': 'GigabitEthernet2'}
        # print(temp_dict)
        """
        {'interface': 'GigabitEthernet2', 'link_status': 'up', 'admin_state': 'up', 'hardware_type': 'vNIC', 'address': '0050.56a1.3448', 'bia': '0050.56a1.3448', 'description': '', 'ip_address': '', 'mtu': '1500', 'duplex': 'Full Duplex', 'speed': '1000Mbps', 'bandwidth': '1000000 Kbit', 'encapsulation': 'ARPA'}
        """
        objs.append(temp_dict)
    return objs


def netmiko_show_cred(host, username, password, cmd, device_type, enable='Cisc0123'):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


def netmiko_ntc_template(ip, username, password, cmd, device_type):
    ssh_ouput = netmiko_show_cred(ip, username, password, cmd, device_type)

    # 指定模板所在文件和索引文件
    # https://github.com/networktocode/ntc-templates/tree/master/ntc_templates/templates
    cli_table = clitable.CliTable('index', f'.{os.sep}template')

    # 设置属性, 命令为:show inerface, 厂商为: self.device_type
    attributes = {'Command': cmd, 'Vendor': device_type}

    # 分析命令输出结果
    # ifstate_ouput: 命令执行的原始字符串结果
    # attributes: 相关属性, 介绍什么命令, 什么厂商的系统
    # cli_table: 找到特定厂商的命令解析模板, 然后解析命令

    # "index" 文件的内容
    # Template(模板), Hostname(主机), Vendor(厂商系统), Command(命令)
    # cisco_ios_show_interfaces.template, .*, cisco_ios, sh[[ow]] inte[[rfaces]]
    # arista_eos_show_interfaces.template, .*, arista_eos, sh[[ow]] inte[[rfaces]]
    # cisco_ios_show_ip_ospf_neighbor.template, .*, cisco_ios, sh[[ow]] ip os[[pf]] nei[[ghbor]]
    # arista_eos_show_ip_ospf_neighbor.template, .*, arista_eos, sh[[ow]] ip os[[pf]] nei[[ghbor]]

    cli_table.ParseCmd(ssh_ouput, attributes)

    parse_result = clitable_to_dict(cli_table)
    return parse_result


if __name__ == "__main__":
    from pprint import pprint
    pprint(netmiko_ntc_template('10.1.1.253', 'admin', 'Cisc0123', 'show interfaces', 'cisco_ios'))