from pyats.topology import loader
from pprint import pprint
from pathlib import Path
import os

# 获取当前工作目录
current_file = Path(__file__)

# 获取当前工作目录的父目录
parent_dir = current_file.parent.parent

# 加载top文件
testbed = loader.load(f'{parent_dir}{os.sep}top.yaml')

# print(testbed.devices)
# # ~~~ 输出: TopologyDict({'C8Kv1': <Device C8Kv1 at 0x7f4de433de90>, 'C8Kv2': <Device C8Kv2 at 0x7f4de531d510>})

device = testbed.devices['C8Kv1']

device.connect(learn_hostname=True,
               log_stdout=False,
               ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

# # 执行普通命令
print(device.execute('show version'))

# # 分析命令输出结果
pprint(device.parse('show version'))

# 详细learn清单
# https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models
pprint(device.learn('ospf').to_dict())
