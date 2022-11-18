#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.carrier.asynsock.dgram import udp


oid_list = []
max_repetitions = 0
# Create SNMP engine instance
snmp_engine = engine.SnmpEngine()  # 添加SNMP引擎实例

# Setup transport endpoint and bind it with security settings yielding
# a target name (choose one entry depending of the transport needed).
# UDP/IPv4
config.addSocketTransport(snmp_engine, udp.domainName, udp.UdpSocketTransport().openClientMode())


# Error/response reciever
def cb_fun(send_request_handle, error_indication, error_status, error_index, var_bind_table, cb_ctx):
    global oid_list
    global max_repetitions
    if error_indication:
        print(error_indication)
        return  # stop on error
    if error_status:
        print('%s at %s' % (error_status.prettyPrint(), error_index and var_bind_table[-1][int(error_index) - 1] or '?'))
        return  # stop on error
    for var_bind_row in var_bind_table:
        if max_repetitions == 0:  # 如果为0
            return  # 停止，并且返回
        else:
            for oid, val in var_bind_table[0]:
                oid_list.append((oid.prettyPrint(), val.prettyPrint()))  # 把oid和val的对添加到全局清单oid_list
        max_repetitions -= 1  # 数量减一

    return True  # signal dispatcher to continue walking#返回一个信号，继续往下查询！


def snmpv3_getbulk(ip='', user='', hash_meth=None, hash_key=None, cry_meth=None, cry_key=None, oid='', num=10):
    # usmHMACMD5AuthProtocol - MD5 hashing
    # usmHMACSHAAuthProtocol - SHA hashing
    # usmNoAuthProtocol - no authentication
    # usmDESPrivProtocol - DES encryption
    # usm3DESEDEPrivProtocol - triple-DES encryption
    # usmAesCfb128Protocol - AES encryption, 128-bit
    # usmAesCfb192Protocol - AES encryption, 192-bit
    # usmAesCfb256Protocol - AES encryption, 256-bit
    # usmNoPrivProtocol - no encryption
    global max_repetitions
    max_repetitions = num

    # 添加目标，'yourDevice'(OID与处理方法），'my-creds'（用户，密码，安全模型），目的IP与端口号
    config.addTargetAddr(snmp_engine, 'yourDevice', udp.domainName, (ip, 161), 'my-creds')
    # ========================下面的操作在判断安全模型==========================
    # NoAuthNoPriv
    if hash_meth is None and cry_meth is None:
        hashval = config.usmNoAuthProtocol  # 配置HASH算法
        cryval = config.usmNoPrivProtocol  # 配置加密算法
        model = 'noAuthNoPriv'  # 配置安全模式
    # AuthNoPriv
    elif hash_meth is not None and cry_meth is None:
        # 配置HASH算法
        if hash_meth == 'md5':
            hashval = config.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = config.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        cryval = config.usmNoPrivProtocol  # 配置加密算法
        model = 'authNoPriv'  # 配置安全模式
    # AuthPriv
    elif hash_meth is not None and cry_meth is not None:
        # 配置HASH算法
        if hash_meth == 'md5':
            hashval = config.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = config.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        # 配置加密算法
        if cry_meth == '3des':
            cryval = config.usm3DESEDEPrivProtocol
        elif cry_meth == 'des':
            cryval = config.usmDESPrivProtocol
        elif cry_meth == 'aes128':
            cryval = config.usmAesCfb128Protocol
        elif cry_meth == 'aes192':
            cryval = config.usmAesCfb192Protocol
        elif cry_meth == 'aes256':
            cryval = config.usmAesCfb256Protocol
        else:
            print('加密算法必须是3des, des, aes128, aes192 or aes256 !')
            return
        model = 'authPriv'  # 配置安全模式
    # 提供的参数不符合标准时给出提示
    else:
        print('三种USM: NoAuthNoPriv, AuthNoPriv, AuthPriv.。请选择其中一种。')
        return
    # ========================判断安全模型结束==========================
    # 添加用户与他的密钥
    config.addV3User(snmp_engine, user, hashval, hash_key, cryval, cry_key)
    config.addTargetParams(snmp_engine, 'my-creds', user, model)  # 创建'my-creds',里边有用户和安全模型

    # Prepare initial request to be sent
    # 创建'yourDevice'，有OID和处理方法cbFun
    cmdgen.BulkCommandGenerator().sendReq(snmp_engine, 'yourDevice', 0, 1, ((oid, None),), cb_fun)

    # Run I/O dispatcher which would send pending queries and process responses
    snmp_engine.transportDispatcher.runDispatcher()  # 运行实例
    return oid_list  # 返回oid_list


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # 接口信息
    for item in snmpv3_getbulk('10.1.1.253',
                               'qytanguser',
                               'sha',
                               'Cisc0123',
                               'des',
                               'Cisc0123',
                               '1.3.6.1.2.1.2.2.1.2',
                               5):
        print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息

    # # 接口速率
    # for item in snmpv3_getbulk('10.1.1.253',
    #                            'qytanguser',
    #                            'sha',
    #                            'Cisc0123',
    #                            'des',
    #                            'Cisc0123',
    #                            '1.3.6.1.2.1.2.2.1.5',
    #                            5):
    #     print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息

    # # 进接口字节数
    # for item in snmpv3_getbulk('10.1.1.253',
    #                            'qytanguser',
    #                            'sha',
    #                            'Cisc0123',
    #                            'des',
    #                            'Cisc0123',
    #                            '1.3.6.1.2.1.2.2.1.10',
    #                            5):
    #     print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息

    # # 出接口字节数
    # for item in snmpv3_getbulk('10.1.1.253',
    #                            'qytanguser',
    #                            'sha',
    #                            'Cisc0123',
    #                            'des',
    #                            'Cisc0123',
    #                            '1.3.6.1.2.1.2.2.1.16',
    #                            5):
    #     print('OID: ', item[0], 'VALUE: ', item[1])  # 从oid_list读取并且打印信息
