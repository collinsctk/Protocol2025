#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from ldap3 import Connection
from net_12_ldap.vip_ldap3_0_login_info import server, ad_admin_username, ad_admin_password


def get_user_info(username):
    # 返回用户属于的组与用户名
    try:
        # 连接服务器
        c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)
        # 提取域qytang.com, 用户的memberOf,sn和department信息
        c.search(search_base='dc=qytang,dc=com',
                 search_filter='(&(samAccountName=' + username + '))',
                 attributes=['memberOf',
                             'sn',
                             'department',
                             'createTimeStamp',
                             'accountExpires',
                             'userAccountControl',
                             'objectClass',
                             'pwdLastSet'],
                 paged_size=5)
        # 返回获取的memberOf,sn和department信息
        return {'dn': c.response[0]['dn'],
                'memberOf': c.response[0]['attributes']['memberOf'],
                'sn': c.response[0]['attributes']['sn'],
                'department': c.response[0]['attributes']['department'],
                'createTimeStamp': c.response[0]['attributes']['createTimeStamp'],
                'accountExpires': c.response[0]['attributes']['accountExpires'],
                'userAccountControl': c.response[0]['attributes']['userAccountControl'],
                'objectClass': c.response[0]['attributes']['objectClass'],
                'pwdLastSet': c.response[0]['attributes']['pwdLastSet'],}
    except Exception:
        return None


def get_user_self_info(username, password):
    # 返回用户属于的组与用户名
    try:
        # 连接服务器
        c = Connection(server, auto_bind=True, user="qytang\\"+username, password=password)
        # 提取域qytang.com, 用户的memberOf,sn和department信息
        c.search(search_base='dc=qytang,dc=com',
                 search_filter='(&(samAccountName=' + username + '))',
                 attributes=['memberOf',
                             'sn',
                             'department',
                             'createTimeStamp',
                             'accountExpires',
                             'userAccountControl',
                             'objectClass',
                             'pwdLastSet'],
                 paged_size=5)
        # 返回获取的memberOf,sn和department信息
        return {'dn': c.response[0]['dn'],
                'memberOf': c.response[0]['attributes']['memberOf'],
                'sn': c.response[0]['attributes']['sn'],
                'department': c.response[0]['attributes']['department'],
                'createTimeStamp': c.response[0]['attributes']['createTimeStamp'],
                'accountExpires': c.response[0]['attributes']['accountExpires'],
                'userAccountControl': c.response[0]['attributes']['userAccountControl'],
                'objectClass': c.response[0]['attributes']['objectClass'],
                'pwdLastSet': c.response[0]['attributes']['pwdLastSet'],}
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # 可以查詢用戶
    from pprint import pprint
    pprint(get_user_info('qyt-qink'))
    pprint(get_user_self_info('qyt-qink', 'Cisc0123'))
    # 可以查詢組
    # print(get_user_info('vipgroup'))
    # userAccountControl
    # https://lesca.me/archives/common-useraccountcontrol-values.html
