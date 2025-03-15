#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from ldap3 import Connection, MODIFY_REPLACE
import sys
from pathlib import Path

# 获取当前文件所在目录
current_file = Path(__file__)
current_dir = current_file.parent
sys.path.append(str(current_dir))

from vip_ldap3_0_login_info import server, ad_admin_username, ad_admin_password
from vip_ldap3_1_get_user_info import get_user_info


def disable_user(username):
    # 禁用用户
    try:
        c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)
        c.modify(get_user_info(username).get('dn'), {'userAccountControl': [(MODIFY_REPLACE, [514])]})
        return True
    except Exception as e:
        print(e)
        return False


def enable_user(username):
    # 激活用户
    try:
        c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)
        c.modify(get_user_info(username).get('dn'), {'userAccountControl': [(MODIFY_REPLACE, [512])]})
        return True
    except Exception:
        return False


if __name__ == '__main__':
    # print(disable_user('qyt-qink'))
    enable_user('qyt-qink')
