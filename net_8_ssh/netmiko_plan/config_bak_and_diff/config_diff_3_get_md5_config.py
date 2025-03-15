#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import sys
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
root_dir = current_file.parent.parent.parent.parent
sys.path.append(str(root_dir))
from net_8_ssh.netmiko_plan.config_bak_and_diff.config_diff_1_create_table import RouterConfig, db_file_path
from net_8_ssh.netmiko_plan.netmiko_1_show_client import netmiko_show_cred, device_ip, username, password
import re
import hashlib
from datetime import datetime


def get_md5_config(host, username, password):
    try:
        # 获取完整的running-configuration
        device_config_raw = netmiko_show_cred(host,
                                              username,
                                              password,
                                              'show run',
                                              device_type='cisco_ios')
        # print(device_config_raw)
        split_result = re.split(r'\nhostname \S+\n', device_config_raw)
        run_config = device_config_raw.replace(split_result[0], '').strip()
        # 计算MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 返回ip, 时间, 配置, md5值
        return host, datetime.now(), run_config, md5_value
    except Exception as e:
        print('%stErrorn %s' % (host, e))


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine

    engine = create_engine(f'sqlite:///{db_file_path}?check_same_thread=False',
                           # echo=True
                           )
    Session = sessionmaker(bind=engine)
    session = Session()

    r = get_md5_config(device_ip, username, password)
    if r:
        router_config = RouterConfig(
                                     device_ip=r[0],
                                     record_time=r[1],
                                     config=r[2],
                                     md5=r[3])

        session.add(router_config)
        session.commit()

