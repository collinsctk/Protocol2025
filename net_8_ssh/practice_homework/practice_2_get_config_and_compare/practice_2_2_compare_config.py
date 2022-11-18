#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import sqlite3
from net_12_ssh.practice_homework.practice_2_get_config_and_compare.practice_2_0_diff_conf import diff_txt


def def_config_id(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # 注意group by查询的使用, 找到那些唯一的MD5值
    cursor.execute("select md5 as md5,COUNT(*) as count from router_config_md5 group by md5")
    yourresults = cursor.fetchall()
    md5_list = []
    for i in yourresults:
        md5_list.append(i[0])

    # 找到唯一MD5值的ID
    id_list = []
    for md5 in md5_list:
        cursor.execute("select id from router_config_md5 where md5 = ?", (md5,))  # 注意必须传元组
        yourresults = cursor.fetchall()
        id_list.append(min([x[0] for x in yourresults]))  # 找到多个ID, 把最小的放入列表
    id_list = sorted(id_list)  # 列表排序

    # 找到ID与获取配置的时间
    id_time_list = []
    for id in id_list:
        cursor.execute("select id,record_time from router_config_md5 where id = ?", (id,))  # 注意必须传元组
        yourresults = cursor.fetchall()
        id_time_list.append(yourresults[0])

    # 打印ID与获取配置的时间
    for i in id_time_list:
        print('配置ID:', i[0], '获取配置时间:', i[1])

    # 等待客户选择ID,进行比较
    print('请选择需要比较的配置ID:')
    id_1 = int(input('ID1:'))
    id_2 = int(input('ID2:'))
    cursor.execute("select config from router_config_md5 where id = ?", (id_1,))
    yourresults = cursor.fetchall()
    id_1_config = yourresults[0][0]
    cursor.execute("select config from router_config_md5 where id = ?", (id_2,))
    yourresults = cursor.fetchall()
    id_2_config = yourresults[0][0]

    print(diff_txt(id_1_config, id_2_config))


if __name__ == '__main__':
    def_config_id('./db_file/config_db.sqlite')
