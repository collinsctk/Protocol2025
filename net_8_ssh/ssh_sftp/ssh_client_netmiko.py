from netmiko import Netmiko


def netmiko_show_cred(host, username, password, cmd, enable='Cisc0123', ssh=True):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
    }
    try:
        net_connect = Netmiko(**device_info)
        return net_connect.send_command(cmd)

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


def netmiko_config_cred(host, username, password, cmds_list, enable='Cisc0123', ssh=True, verbose=False):
    device_info = {
                    'host': host,
                    'username': username,
                    'password': password,
                    'device_type': 'cisco_ios' if ssh else 'cisco_ios_telnet',
                    'secret': enable
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


if __name__ == '__main__':
    # raw_result = netmiko_show_cred('10.1.1.253', 'admin', 'Cisc0123', 'show ip inter brie')
    # raw_result = netmiko_show_cred('r1.qytang.com', 'admin', 'Cisc0123', 'show ip inter brie')
    raw_result = netmiko_show_cred('2001:1::253', 'admin', 'Cisc0123', 'show ip inter brie')
    print(type(raw_result))
    print(raw_result)

    config_commands = ['router ospf 1',
                       'router-id 1.1.1.1',
                       'network 1.1.1.1 0.0.0.0 a 0']

    print(netmiko_config_cred('10.1.1.253', 'admin', 'Cisc0123', config_commands, verbose=True))
