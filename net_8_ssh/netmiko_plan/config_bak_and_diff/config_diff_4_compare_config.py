#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from part_1_netmiko.config_bak_and_diff.config_diff_2_dff_conf import diff_txt
from part_1_netmiko.config_bak_and_diff.config_diff_1_create_table import RouterConfig, db_file_path
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import create_engine

engine = create_engine(f'sqlite:///{db_file_path}?check_same_thread=False',
                       # echo=True
                       )

Session = sessionmaker(bind=engine)
session = Session()


def def_config_id():
    md5_list = []

    # 注意group by查询的使用, 找到那些唯一的MD5值
    for md5_value, md5_count in session.query(RouterConfig.md5,
                                              func.count(RouterConfig.md5)).group_by(RouterConfig.md5).all():
        md5_list.append(md5_value)

    # 找到唯一MD5值的ID
    id_list = []
    for md5 in md5_list:
        your_results = session.query(RouterConfig).filter_by(md5=md5)
        id_list.append(min([x.id for x in your_results]))  # 找到多个ID, 把最小的放入列表
    id_list = sorted(id_list)  # 列表排序

    # 找到ID与获取配置的时间
    id_time_list = []
    for id in id_list:
        your_result = session.query(RouterConfig).filter_by(id=id).one()
        id_time_list.append(your_result)

    # 打印ID与获取配置的时间
    for i in id_time_list:
        print('配置ID:', i.id, '获取配置时间:', i.record_time)

    # 等待客户选择ID,进行比较
    print('请选择需要比较的配置ID:')
    id_1 = int(input('ID1:'))
    id_2 = int(input('ID2:'))
    router_config_id_1 = session.query(RouterConfig).filter_by(id=id_1).one()
    id_1_config = router_config_id_1.config
    router_config_id_2 = session.query(RouterConfig).filter_by(id=id_2).one()
    id_2_config = router_config_id_2.config

    print(diff_txt(id_1_config, id_2_config))


if __name__ == '__main__':
    def_config_id()
