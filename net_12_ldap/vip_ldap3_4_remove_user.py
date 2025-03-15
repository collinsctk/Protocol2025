#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from ldap3 import Connection
import sys
from pathlib import Path

# 获取当前文件所在目录
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))

from vip_ldap3_0_login_info import server, ad_admin_username, ad_admin_password
from vip_ldap3_1_get_user_info import get_user_info


def delete_user(username):
    try:
        # 连接服务器
        c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)

        c.delete(get_user_info(username).get('dn'))

        return True

    except Exception:
        return False


if __name__ == '__main__':
    from net_12_ldap.vip_ldap3_2_get_group_users import get_group_users
    delete_user('qyt-qink66')
    print(get_group_users('qytanggroup'))
