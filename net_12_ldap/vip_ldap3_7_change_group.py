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


# 从用户组用删除用户
def remove_user_from_group(username, groupname):
    c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)
    c.extend.microsoft.remove_members_from_groups(get_user_info(username).get('dn'), get_user_info(groupname).get('dn'))


# 添加用户到用户组
def add_user_to_group(username, groupname):
    c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)
    c.extend.microsoft.add_members_to_groups(get_user_info(username).get('dn'), get_user_info(groupname).get('dn'))


if __name__ == '__main__':
    remove_user_from_group('qyt-qink', 'qytanggroup')
    print(get_user_info('qyt-qink').get('memberOf'))

    add_user_to_group('qyt-qink', 'qytanggroup')
    print(get_user_info('qyt-qink').get('memberOf'))
