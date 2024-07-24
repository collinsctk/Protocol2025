#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from ldap3 import Connection, MODIFY_REPLACE
from net_12_ldap.vip_ldap3_0_login_info import server, ad_admin_username, ad_admin_password
from net_12_ldap.vip_ldap3_1_get_user_info import get_user_info
from net_12_ldap.vip_ldap3_0_get_pinyin_name import get_pinyin_name
from random import randint, choice
import string
from datetime import timedelta, datetime


def random_password():
    length = randint(3, 4)
    first1 = str(choice(string.digits))
    first2 = choice(string.ascii_letters).upper()
    first3 = choice(string.ascii_letters).lower()
    first4 = choice('.-')
    lastpassword = ''.join(choice(string.ascii_letters + string.digits) for i in range(length))
    return first1 + first2 + first3 + first4 + lastpassword


# 添加域账号
def add_ad_user(xingming, phone, qq, mail, group='qytanggroup', random_pass=False):
    # 转换汉字到拼音
    hanzi = xingming

    try:
        xingming = get_pinyin_name(xingming)
    except Exception:
        pass

    # 根据类型找到组
    if group == 'qytanggroup':
        group_dn = get_user_info(group).get('dn')
        add_username = 'qyt-' + xingming

    while True:
        if get_user_info(add_username):
            name_randint = str(randint(1, 100))
            add_username += name_randint
        else:
            break

    user_dn = 'cn=' + add_username + ',' + ','.join(group_dn.split(',')[1:])
    try:
        # 连接服务器
        c = Connection(server, auto_bind=True, user="qytang\\"+ad_admin_username, password=ad_admin_password)

        end_time = datetime.today() + timedelta(days=100)

        c.add(user_dn, attributes={'objectClass':  ['top', 'person', 'organizationalPerson', 'user'],
                                   # 用户名
                                   'sAMAccountName': add_username,
                                   # 用户名
                                   'userPrincipalName': add_username,
                                   # 有效期一年半
                                   'accountExpires': end_time,
                                   # 姓为中文的汉字
                                   'sn': hanzi,
                                   # 显示名为用户名
                                   'displayName': add_username,
                                   # 电话
                                   "telephoneNumber": phone,
                                   # 邮件
                                   "Mail": mail,
                                   # QQ
                                   "description": hanzi + qq
                                   })
        # 添加用户到组
        c.extend.microsoft.add_members_to_groups(user_dn, group_dn)
        # 产生随机密码
        if random_pass:
            password = random_password()
        else:
            password = 'Cisc0123'
        c.extend.microsoft.modify_password(user_dn, new_password=password)
        # 激活用户
        c.modify(user_dn, {'userAccountControl': [(MODIFY_REPLACE, [512])]})

        return add_username, password

    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # print(random_password())
    print(add_ad_user('秦柯',
                      '13297055555',
                      '2350512555',
                      '2350512555@qq.com',
                      'qytanggroup',
                      random_pass=True))
