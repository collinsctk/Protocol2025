import sys
import os
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
current_root = current_file.parent

pcap_data_dir = f'{current_root}{os.sep}pcap_data{os.sep}'