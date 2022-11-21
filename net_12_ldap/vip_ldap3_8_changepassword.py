#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from ldap3 import Connection
from net_12_ldap.vip_ldap3_0_login_info import server, ad_admin_username, ad_admin_password
from net_12_ldap.vip_ldap3_1_get_user_info import get_user_info
from net_12_ldap.vip_ldap3_3_add_user import random_password


# 修改用户密码
def change_user_password(username, newpass=''):
    c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)
    if newpass == '':
        newpass = random_password()

    c.extend.microsoft.modify_password(get_user_info(username).get('dn'), newpass)
    return newpass


if __name__ == '__main__':
    print(change_user_password('qyt-qink'))
