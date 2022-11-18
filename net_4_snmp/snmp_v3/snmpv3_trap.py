#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c
import sys
import re
from pprint import pprint


def analysis(info):
    # 分析Trap信息字典函数
    # 下面是这个大字典的键值与嵌套的小字典
    # 1.3.6.1.2.1.1.3.0 103484528
    # 1.3.6.1.6.3.1.1.4.1.0 1.3.6.1.4.1.9.9.41.2.0.1
    # 1.3.6.1.4.1.9.9.41.1.2.3.1.2.3303 LINK
    # 1.3.6.1.4.1.9.9.41.1.2.3.1.3.3303 4
    # 1.3.6.1.4.1.9.9.41.1.2.3.1.4.3303 UPDOWN
    # 1.3.6.1.4.1.9.9.41.1.2.3.1.5.3303 Interface GigabitEthernet2, changed state to up
    # 1.3.6.1.4.1.9.9.41.1.2.3.1.6.3303 103484527

    # ============================Enter / Exit Configure Mode=========================
    if '1.3.6.1.6.3.1.1.4.1.0' in info.keys():
        if info['1.3.6.1.6.3.1.1.4.1.0'] == '1.3.6.1.4.1.9.9.43.2.0.1':
            print('*' * 20 + '配置模式改变' + '*' * 20)
            print('Enter Configure Mode!!!')
        if info['1.3.6.1.6.3.1.1.4.1.0'] == '1.3.6.1.4.1.9.9.43.2.0.2':
            print('*' * 20 + '配置模式改变' + '*' * 20)
            print('Exit Configure Mode!!!')
        # 需要进一步分析处理
        if info['1.3.6.1.6.3.1.1.4.1.0'] == '1.3.6.1.6.3.1.1.5.3':
            state = 'Down'
            print('*' * 20 + '接口状态改变' + '*' * 20)
            print('%s change state to %s' % (info['1.3.6.1.2.1.2.2.1.2.2'], state))
        if info['1.3.6.1.6.3.1.1.4.1.0'] == '1.3.6.1.6.3.1.1.5.4':
            state = 'UP'
            print('*' * 20 + '接口状态改变' + '*' * 20)
            print('%s change state to %s' % (info['1.3.6.1.2.1.2.2.1.2.2'], state))

    pprint(info)


def cb_fun(snmp_engine, state_reference, context_engine_id, context_name, var_binds, cb_ctx):
    # Callback function for receiving notifications
    result_dict = {}
    for name, val in var_binds:
        result_dict[name.prettyPrint()] = val.prettyPrint()
    analysis(result_dict)
    # # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
    # # ============================Trap 信息处理方法===================================
    #
    # # ============================link up / link down===============================
    # # snmp-server enable traps snmp linkdown linkup
    # if '1.3.6.1.6.3.1.1.4.1.0' in name.prettyPrint() and '1.3.6.1.6.3.1.1.5.3' in val.prettyPrint():
    #     state = 'Down'
    # elif '1.3.6.1.6.3.1.1.4.1.0' in name.prettyPrint() and '1.3.6.1.6.3.1.1.5.4' in val.prettyPrint():
    #     state = 'UP'
    #
    # if '1.3.6.1.2.1.2.2.1.2' in name.prettyPrint():
    #     print('*' * 20 + '接口状态' + '*' * 20)
    #     print('%s change state to %s' % (val.prettyPrint(), state))
    #
    # # ============================Enter / Exit Configure Mode=========================
    # # snmp-server enable traps config
    # if '1.3.6.1.6.3.1.1.4.1.0' in name.prettyPrint():
    #     if '1.3.6.1.4.1.9.9.43.2.0.1' in val.prettyPrint():
    #         print('*' * 20 + '配置模式改变' + '*' * 20)
    #         print('Enter Configure Mode!!!')
    #     elif '1.3.6.1.4.1.9.9.43.2.0.2' in val.prettyPrint():
    #         print('*' * 20 + '配置模式改变' + '*' * 20)
    #         print('Exit Configure Mode!!!')
    #
    # # ============================CPU================================================
    # # process cpu threshold type total rising 1 interval 5
    # # IOS-XE 现在并不能主动发送Trap,但是激活snmp-server enable traps syslog,可以把Console log发过去
    # if '1.3.6.1.4.1.9.9.41.1.2.3.1.4.' in name.prettyPrint():
    #     if 'CPU' in val.prettyPrint():
    #         cpu_state = val.prettyPrint()
    # elif '1.3.6.1.4.1.9.9.41.1.2.3.1.5.' in name.prettyPrint():
    #     if 'CPU' in val.prettyPrint():
    #         print('*' * 20 + cpu_state + '*' * 20)
    #         print(val.prettyPrint())


def snmpv3_trap(user='', hash_meth=None, hash_key=None, cry_meth=None, cry_key=None, engineid='', ip='127.0.0.1',
                port=162):
    # Create SNMP engine with autogenernated engineID and pre-bound
    snmp_engine = engine.SnmpEngine()

    config.addSocketTransport(
        snmp_engine,
        udp.domainName,
        udp.UdpTransport().openServerMode((ip, port))
    )

    # usmHMACMD5AuthProtocol - MD5 hashing
    # usmHMACSHAAuthProtocol - SHA hashing
    # usmNoAuthProtocol - no authentication
    # usmDESPrivProtocol - DES encryption
    # usm3DESEDEPrivProtocol - triple-DES encryption
    # usmAesCfb128Protocol - AES encryption, 128-bit
    # usmAesCfb192Protocol - AES encryption, 192-bit
    # usmAesCfb256Protocol - AES encryption, 256-bit
    # usmNoPrivProtocol - no encryption

    # NoAuthNoPriv
    if hash_meth is None and cry_meth is None:
        hashval = config.usmNoAuthProtocol
        cryval = config.usmNoPrivProtocol
    # AuthNoPriv
    elif hash_meth is not None and cry_meth is None:
        if hash_meth == 'md5':
            hashval = config.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = config.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
        cryval = config.usmNoPrivProtocol
    # AuthPriv
    elif hash_meth is not None and cry_meth is not None:
        if hash_meth == 'md5':
            hashval = config.usmHMACMD5AuthProtocol
        elif hash_meth == 'sha':
            hashval = config.usmHMACSHAAuthProtocol
        else:
            print('哈希算法必须是md5 or sha!')
            return
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
    # 提供的参数不符合标准时给出提示
    else:
        print('三种USM: NoAuthNoPriv, AuthNoPriv, AuthPriv.。请选择其中一种。')
        return

    config.addV3User(
        snmp_engine, user,
        hashval, hash_key,
        cryval, cry_key,
        contextEngineId=v2c.OctetString(hexValue=engineid)
    )

    # Register SNMP Application at the SNMP engine
    ntfrcv.NotificationReceiver(snmp_engine, cb_fun)

    snmp_engine.transportDispatcher.jobStarted(1)  # this job would never finish

    # Run I/O dispatcher which would receive queries and send confirmations
    try:
        snmp_engine.transportDispatcher.runDispatcher()
    except Exception:
        snmp_engine.transportDispatcher.closeDispatcher()
        raise


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    snmpv3_trap('qytanguser', 'sha', 'Cisc0123', 'des', 'Cisc0123', '800000090300005056AB4D19', '10.1.1.180')
