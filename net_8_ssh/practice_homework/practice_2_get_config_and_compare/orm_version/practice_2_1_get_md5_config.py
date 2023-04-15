#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from net_8_ssh.ssh_sftp.ssh_client_netmiko import netmiko_show_cred
import re
import hashlib
from datetime import datetime


def get_md5_config(host, username, password):
    try:
        # 获取完整的running-configuration
        device_config_raw = netmiko_show_cred(host, username, password, 'show run')
        print(device_config_raw)
        split_result = re.split(r'\nhostname \S+\n', device_config_raw)
        run_config = device_config_raw.replace(split_result[0], '').strip()
        # 计算MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 获取配置的MD5值
        # md5 = netmiko_show_cred(host, username, password, 'verify /md5 system:running-config')

        # 返回ip, 时间, 配置, md5值
        return host, datetime.now(), run_config, md5_value
    except Exception as e:
        print('%stErrorn %s' % (host, e))


if __name__ == '__main__':
    from sqlalchemy.orm import sessionmaker
    from practice_2_0_create_table import RouterConfig, db_file_name
    from sqlalchemy import create_engine

    engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False',
                           # echo=True
                           )
    Session = sessionmaker(bind=engine)
    session = Session()

    r = get_md5_config('10.1.1.253', 'admin', 'Cisc0123')
    if r:
        router_config = RouterConfig(
                                     device_ip=r[0],
                                     record_time=r[1],
                                     config=r[2],
                                     md5=r[3])

        session.add(router_config)
        session.commit()

