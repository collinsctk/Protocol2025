# pip3 install pyats
# pip3 install genie

from netmiko import Netmiko


def netmiko_show_cred_use_genie(host, username, password, cmd, enable='Cisc0123', ssh=True):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd, use_genie=True)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


if __name__ == '__main__':
    # 设置环境变量
    # export NET_TEXTFSM=/ntc-templates_pyATS/templates/

    # Linux环境
    from pprint import pprint
    parsed_result = netmiko_show_cred_use_genie('10.1.1.253',
                                                'admin',
                                                'Cisc0123',
                                                'show ip inter brief',
                                                # 'show ip route'
                                                # 'show version',
                                                )
    pprint(parsed_result)
