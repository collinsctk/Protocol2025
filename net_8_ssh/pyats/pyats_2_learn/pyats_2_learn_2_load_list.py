from genie.testbed import load
from pprint import pprint

devices_list = [{"device_name": "C8Kv1",
                 "device_ip": "196.21.5.211",
                 "platform": "iosxe",
                 "username": "admin",
                 "password": "Cisc0123"},
                {"device_name": "C8Kv2",
                 "device_ip": "196.21.5.212",
                 "platform": "iosxe",
                 "username": "admin",
                 "password": "Cisc0123"}
                ]

device_details = {}

# 构建testbed数据结构
for device in devices_list:
    device_dict = {device["device_name"]: {
                                            "connections": {"cli": {"protocol": "ssh",
                                                                    'ip': device['device_ip']}},
                                            "credentials": {"default": {"username": device['username'],
                                                                        "password": device['password']}},
                                            "os": device['platform'],
                                            "type": device['platform']
                                        }}
    device_details.update(device_dict)

testbed_device_details = {"devices": device_details}

# pprint(testbed_device_details)

testbed = load({"devices": device_details})

# print(testbed.devices)
# 输出: TopologyDict({'C8Kv1': <Device C8Kv1 at 0x7f4de433de90>, 'C8Kv2': <Device C8Kv2 at 0x7f4de531d510>})

device = testbed.devices['C8Kv1']

device.connect(learn_hostname=True,
               log_stdout=False,
               ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

# # 执行普通命令
# print(device.execute('show version'))
"""
{'devices': {'C8Kv1': {'connections': {'cli': {'ip': '196.21.5.211',
                                               'protocol': 'ssh'}},
                       'credentials': {'default': {'password': 'Cisc0123',
                                                   'username': 'admin'}},
                       'os': 'iosxe',
                       'type': 'iosxe'},
             'C8Kv2': {'connections': {'cli': {'ip': '196.21.5.212',
                                               'protocol': 'ssh'}},
                       'credentials': {'default': {'password': 'Cisc0123',
                                                   'username': 'admin'}},
                       'os': 'iosxe',
                       'type': 'iosxe'}}}
"""

if __name__ == '__main__':
    # 分析命令输出结果
    pprint(device.parse('show version'))

    # 详细learn清单
    # https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models
    pprint(device.learn('ospf').to_dict())

