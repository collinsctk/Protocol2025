#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from ldap3 import Server, Connection, AUTO_BIND_NO_TLS

server = Server('ldap://10.1.1.200')


def qytldap(username, password):
    try:
        # 连接服务器
        c = Connection(server, auto_bind=AUTO_BIND_NO_TLS, read_only=True, check_names=True, user="qytang\\"+username, password=password)
        # 提取域qytang.com, 用户的memberOf和sn信息
        c.search(search_base='dc=qytang,dc=com', search_filter='(&(samAccountName=' + username + '))', attributes=['memberOf', 'sn'], paged_size=5)
        # 返回获取的memberOf和sn信息
        return c.response[0]['attributes']['memberOf'], c.response[0]['attributes']['sn']
    except Exception:
        return None


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    print(qytldap('qytanguser', 'Cisc0123'))
