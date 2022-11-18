#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.proto import rfc1902
import sys

# Create SNMP engine instance
snmpEngine = engine.SnmpEngine()

# Setup transport endpoint and bind it with security settings yielding
# a target name (choose one entry depending of the transport needed).
# UDP/IPv4
config.addSocketTransport(snmpEngine, udp.domainName, udp.UdpSocketTransport().openClientMode())


# Error/response reciever
def cb_fun(send_request_handle, error_indication, error_status, error_index, var_bind_table, cb_ctx):
    if error_indication:
        print("写入失败!!!")
        print(error_indication)
    elif error_status:
        print("写入失败!!!")
        print('%s at %s' % (error_status.prettyPrint(), error_index and var_bind_table[-1][int(error_index) - 1] or '?'))
    else:
        print("写入成功!!!")
        for oid, val in var_bind_table:
            print('%s = %s' % (oid.prettyPrint(), val))


def snmpv3_set(ip='', user='', hash_meth=None, hash_key=None, cry_meth=None, cry_key=None, oid='', customer_string=''):
    # usmHMACMD5AuthProtocol - MD5 hashing
    # usmHMACSHAAuthProtocol - SHA hashing
    # usmNoAuthProtocol - no authentication
    # usmDESPrivProtocol - DES encryption
    # usm3DESEDEPrivProtocol - triple-DES encryption
    # usmAesCfb128Protocol - AES encryption, 128-bit
    # usmAesCfb192Protocol - AES encryption, 192-bit
    # usmAesCfb256Protocol - AES encryption, 256-bit
    # usmNoPrivProtocol - no encryption

    # 添加目标，'yourDevice'(OID与处理方法），'my-creds'（用户，密码，安全模型），目的IP与端口号
    config.addTargetAddr(snmpEngine, 'yourDevice', udp.domainName, (ip, 161), 'my-creds')
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
    config.addV3User(snmpEngine, user, hashval, hash_key, cryval, cry_key)
    config.addTargetParams(snmpEngine, 'my-creds', user, model)  # 创建'my-creds',里边有用户和安全模型

    # Prepare and send a request message
    # 创建'yourDevice'，有OID和处理方法cbFun
    if isinstance(customer_string, str):
        set_value = rfc1902.OctetString(customer_string)
    elif isinstance(customer_string, int):
        set_value = rfc1902.Integer(customer_string)

    cmdgen.SetCommandGenerator().sendReq(snmpEngine, 'yourDevice', ((oid, set_value),), cb_fun)

    # Run I/O dispatcher which would send pending queries and process responses
    snmpEngine.transportDispatcher.runDispatcher()  # 运行实例


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # 配置主机名
    snmpv3_set('10.1.1.253', 'qytanguser', 'sha', 'Cisc0123', 'des', 'Cisc0123', '1.3.6.1.2.1.1.5.0', 'R1')
    # shutdown G2
    snmpv3_set('10.1.1.253', 'qytanguser', 'sha', 'Cisc0123', 'des', 'Cisc0123', '1.3.6.1.2.1.2.2.1.7.2', 1)