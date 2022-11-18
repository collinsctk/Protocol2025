from netmiko import Netmiko

CSR = {
        'username': 'admin',
        'password': 'Cisc0123',
        # 'device_type': 'cisco_ios_telnet',  # Telnet
        'device_type': 'cisco_ios',  # SSH
        'secret': 'Cisc0123'
        }


def netmiko_show(device_ip, cmd):
    print(f'Start {device_ip}')
    CSR.update({'host': device_ip})
    try:
        net_connect = Netmiko(**CSR)
        return device_ip, net_connect.send_command(cmd)
    except Exception:
        return


if __name__ == '__main__':
    # 下面是协程实战内容
    from datetime import datetime
    import gevent
    from gevent import monkey
    monkey.patch_all()
    # 设备清单
    devices_list = ['10.1.1.253', '10.1.1.252', '10.1.1.253', '10.1.1.252', '10.1.1.253', '10.1.1.252']
    # 把ip和cmd放到一个列表, 便于后续使用*device来传多参数
    devices_cmd_list = [[d, 'show run'] for d in devices_list]
    # devices_cmd_list = [['10.1.1.253', 'show ip interface brief'], ['10.1.1.252', 'show ip interface brief'], ]
    # 多参数使用*device来传

    # 协程部分
    start_time = datetime.now()
    tasks = [gevent.spawn(netmiko_show, *device) for device in devices_cmd_list]
    all_result = gevent.joinall(tasks)
    for s in all_result:
        if s.get():
            print('='*40 + s.get()[0] + '='*40)
            print(s.get()[1])
    end_time = datetime.now()
    print((end_time - start_time).seconds)

    # 普通操作
    start_time = datetime.now()
    for d in devices_cmd_list:
        ip, cmd_result = netmiko_show(*d)
        print('=' * 40 + ip + '=' * 40)
        print(cmd_result)
    end_time = datetime.now()
    print((end_time - start_time).seconds)
