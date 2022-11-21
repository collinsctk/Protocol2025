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


def get_group_users(group_name):
    # 返回属于组的用户
    users_list = []
    try:
        # 连接服务器
        c = Connection(server,
                       auto_bind=True,
                       user="qytang\\"+ad_admin_username,
                       password=ad_admin_password)
        c.search(search_base=get_user_info(group_name).get('dn'),
                 search_filter='(|(objectCategory=group)(objectCategory=user))',
                 search_scope='SUBTREE',
                 attributes=['member', 'objectClass', 'userAccountControl', 'sAMAccountName'],
                 size_limit=0)
        for user in c.entries[0].member:
            users_list.append(user)
        return users_list

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    print(get_group_users('qytanggroup'))
