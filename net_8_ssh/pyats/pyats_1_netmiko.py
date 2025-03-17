# pip install "pyats[full]"
from netmiko import Netmiko

device_ip = '196.21.5.211'
username = 'admin'
password = 'Cisc0123'


def netmiko_show_cred(host,
                      username,
                      password,
                      cmd,
                      device_type,
                      use_genie=False,
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
        result = net_connect.send_command(cmd,
                                          use_genie=use_genie
                                          )
        net_connect.disconnect()
        return result

    except Exception as e:
        print(f'connection error ip: {host} error: {str(e)}')
        return


if __name__ == '__main__':
    from pprint import pprint
    # -------------------命令-------------------
    show_cmd = "show ip interface brief"
    # show_cmd = "show interface"
    # show_cmd = 'show version'

    # -------------------控制textfsm-------------------
    # use_genie = False
    use_genie = True

    # ----------------------ssh------------------------
    raw_result = netmiko_show_cred(device_ip,
                                   username,
                                   password,
                                   show_cmd,
                                   'cisco_ios',
                                   use_genie=use_genie
                                   )
    if use_genie:
        pprint(raw_result)
    else:
        print(raw_result)
