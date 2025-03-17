from deepdiff import DeepDiff
from pprint import pprint
import json
from pathlib import Path
import sys
import os

# 获取当前工作目录
current_file = Path(__file__)
# 获取当前工作目录的父目录
current_dir = current_file.parent
# 获取当前工作目录的父目录
parent_dir = current_file.parent.parent

# 将父目录添加到Python路径
sys.path.append(str(parent_dir))

from pyats_2_learn.pyats_2_learn_2_load_list import testbed

# ~~~~~~~~~~~~~~~~~~注意是C8Kv2~~~~~~~~~~~~~~~~~~~~~~~~~~~~
device = testbed.devices['C8Kv2']

device.connect(learn_hostname=True,
               log_stdout=False,
               ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

# ~~~~~~~~~~~~~~~~写入原始数据~~~~~~~~~~~~~~~~~~~
# print(json.dumps(device.parse('show ip route ospf'), indent=4))

# with open('pyats_3_diff_2_python.json', 'w') as f:
#     json.dump(device.parse('show ip route ospf'), f, indent=4)
# ~~~~~~~~~~~~~~~~写入原始数据~~~~~~~~~~~~~~~~~~~

# 读取原始数据
with open(f'{current_dir}{os.sep}pyats_3_diff_2_python.json') as f:
    original_show_ip_route_ospf = json.load(f)
# pprint(original_show_ip_route_ospf)

# 读取当前数据
# device.parse('show ip route ospf') 不是字典，也没有to_dict(), 所以用json做两次转换
now_show_ip_route_ospf = json.loads(json.dumps(device.parse('show ip route ospf')))
# pprint(now_show_ip_route_ospf)


# ~~~~~~~~~~~~~~~~~~注意是C8Kv2~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 使用DeepDiff比较两个字典，排除包含 'updated' 的字段
diff = DeepDiff(original_show_ip_route_ospf,
                now_show_ip_route_ospf,
                exclude_regex_paths=["root\\['.*updated'.*\\]"])

# 打印差异
pprint(diff)
