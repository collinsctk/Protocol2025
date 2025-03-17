from genie.libs.conf.interface import Interface
from pathlib import Path
import sys
import os

# 获取当前工作目录
current_file = Path(__file__)

# 获取当前工作目录的父目录
parent_dir = current_file.parent.parent

# 将父目录添加到Python路径
sys.path.append(str(parent_dir))

from pyats_2_learn.pyats_2_learn_2_load_list import testbed

device = testbed.devices['C8Kv1']

device.connect(learn_hostname=True,
               log_stdout=False,
               ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

# 创建配置接口的对象
config_interface = Interface(name="GigabitEthernet3",
                             device=device)

# shutdown接口
config_interface.shutdown = True

# 配置IP和掩码
config_interface.ipv4 = '123.1.1.1'
config_interface.ipv4.netmask = '255.255.255.0'

# 配置设备
output = config_interface.build_config()
print(output)