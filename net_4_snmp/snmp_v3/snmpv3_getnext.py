#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()


def snmpv3_getnext(ip='', user='', hash_meth=None, hash_key=None, cry_meth=None, cry_key=None, oid='', num=1):
    # usmHMACMD5AuthProtocol - MD5 hashing
    # usmHMACSHAAuthProtocol - SHA hashing
    # usmNoAuthProtocol - no authentication
    # usmDESPrivProtocol - DES encryption
    # usm3DESEDEPrivProtocol - triple-DES encryption
    # usmAesCfb128Protocol - AES encryption, 128-bit
    # usmAesCfb192Protocol - AES encryption, 192-bit
    # usmAesCfb256Protocol - AES encryption, 256-bit
    # usmNoPrivProtocol - no encryption

    # ========================下面的操作在判断安全模型==========================
    # NoAuthNoPriv
    if hash_meth is None and cry_meth is None:
        hashval = cmdgen.usmNoAuthProtocol
        cryval = cmdgen.usmNoPrivProtocol
    # AuthNoPriv
    elif hash_meth is not None and cry_meth is None:
        if hash_meth == 'md5':
            hashval = cmdgen.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = cmdgen.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        cryval = cmdgen.usmNoPrivProtocol
    # AuthPriv
    elif hash_meth is not None and cry_meth is not None:
        if hash_meth == 'md5':
            hashval = cmdgen.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = cmdgen.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        if cry_meth == '3des':
            cryval = cmdgen.usm3DESEDEPrivProtocol
        elif cry_meth == 'des':
            cryval = cmdgen.usmDESPrivProtocol
        elif cry_meth == 'aes128':
            cryval = cmdgen.usmAesCfb128Protocol
        elif cry_meth == 'aes192':
            cryval = cmdgen.usmAesCfb192Protocol
        elif cry_meth == 'aes256':
            cryval = cmdgen.usmAesCfb256Protocol
        else:
            print('加密算法必须是3des, des, aes128, aes192 or aes256 !')
            return
    # 提供的参数不符合标准时给出提示
    else:
        print('三种USM: NoAuthNoPriv, AuthNoPriv, AuthPriv.。请选择其中一种。')
        return
    # ========================判断安全模型结束==========================
    error_indication, error_status, error_index, var_bind_table = cmdGen.nextCmd(
        cmdgen.UsmUserData(user, hash_key, cry_key,
                           authProtocol=hashval,
                           privProtocol=cryval),  # 添加用户，散列密钥，加密密钥，散列协议，加密协议
        cmdgen.UdpTransportTarget((ip, 161)),  # 添加目标地址和端口号
        oid,  # 指定oid
        lexicographicMode=True, maxRows=num, ignoreMonIncreasingOid=True  # 指定最大行数
    )

    oid_list = []
    if error_indication:  # 打印错误
        print(error_indication)
    else:
        if error_status:  # 打印错误
            print('%s at %s' % (
                error_status.prettyPrint(),
                error_index and var_bind_table[-1][int(error_index) - 1] or '?'
            )
                  )
        else:
            for varBindTableRow in var_bind_table:
                for oid, val in varBindTableRow:
                    oid_list.append((oid.prettyPrint(), val.prettyPrint()))  # 添加oid和对应值的信息到oid_list

    return oid_list  # 返回oid_list


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # 接口信息
    for item in snmpv3_getnext('10.1.1.253',
                               'qytanguser',
                               'sha',
                               'Cisc0123',
                               'des',
                               'Cisc0123',
                               '1.3.6.1.2.1.2.2.1.2',
                               5):
        print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息
    # 接口速率
    for item in snmpv3_getnext('10.1.1.253',
                               'qytanguser',
                               'sha',
                               'Cisc0123',
                               'des',
                               'Cisc0123',
                               '1.3.6.1.2.1.2.2.1.5',
                               5):
        print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息
    # 进接口字节数
    for item in snmpv3_getnext('10.1.1.253',
                               'qytanguser',
                               'sha',
                               'Cisc0123',
                               'des',
                               'Cisc0123',
                               '1.3.6.1.2.1.2.2.1.10',
                               5):
        print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息
    # 出接口字节数
    for item in snmpv3_getnext('10.1.1.253',
                               'qytanguser',
                               'sha',
                               'Cisc0123',
                               'des',
                               'Cisc0123',
                               '1.3.6.1.2.1.2.2.1.10',
                               5):
        print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息
