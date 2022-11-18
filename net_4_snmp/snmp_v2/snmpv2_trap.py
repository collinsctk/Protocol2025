#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from tools.get_ip_netifaces import get_ip_address
from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from pprint import pprint


def analysis(info):
    # 分析Trap信息字典函数
    # 下面是这个大字典的键值与嵌套的小字典
    # 1.3.6.1.2.1.1.3.0 {'value': 'ObjectSyntax', 'application-wide': 'ApplicationSyntax', 'timeticks-value': '103170310'}
    # 1.3.6.1.6.3.1.1.4.1.0 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'objectID-value': '1.3.6.1.6.3.1.1.5.4'}
    # 1.3.6.1.2.1.2.2.1.1.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'integer-value': '2'}
    # 1.3.6.1.2.1.2.2.1.2.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'string-value': 'GigabitEthernet2'}
    # 1.3.6.1.2.1.2.2.1.3.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'integer-value': '6'}

    if '1.3.6.1.6.3.1.1.4.1.0' in info.keys():
        if info["1.3.6.1.6.3.1.1.4.1.0"]['objectID-value'] == '1.3.6.1.6.3.1.1.5.4':
            print(info["1.3.6.1.2.1.2.2.1.2.2"]['string-value'], "UP")
        elif info["1.3.6.1.6.3.1.1.4.1.0"]['objectID-value'] == '1.3.6.1.6.3.1.1.5.3':
            print(info["1.3.6.1.2.1.2.2.1.2.2"]['string-value'], "Down")
    pprint(info, indent=4)  # 打印字典信息


def cb_fun(transport_dispatcher, transport_domain, transport_address, whole_msg):  # 处理Trap信息的函数
    while whole_msg:
        msg_ver = int(api.decodeMessageVersion(whole_msg))  # 提取版本信息
        if msg_ver in api.protoModules:  # 如果版本兼容
            p_mod = api.protoModules[msg_ver]
        else:  # 如果版本不兼容，就打印错误
            print('Unsupported SNMP version %s' % msg_ver)
            return
        req_msg, whole_msg = decoder.decode(
            whole_msg, asn1Spec=p_mod.Message(),  # 对信息进行解码


        )
        print('Notification message from %s:%s: ' % (
            transport_domain, transport_address  # 打印发送TRAP的源信息
        )
              )
        req_pdu = p_mod.apiMessage.getPDU(req_msg)
        if req_pdu.isSameTypeWith(p_mod.TrapPDU()):
            if msg_ver == api.protoVersion1:  # SNMPv1的特殊处理方法,可以提取更加详细的信息
                print('Enterprise: %s' % (
                    p_mod.apiTrapPDU.getEnterprise(req_pdu).prettyPrint()
                )
                      )
                print('Agent Address: %s' % (
                    p_mod.apiTrapPDU.getAgentAddr(req_pdu).prettyPrint()
                )
                      )
                print('Generic Trap: %s' % (
                    p_mod.apiTrapPDU.getGenericTrap(req_pdu).prettyPrint()
                )
                      )
                print('Specific Trap: %s' % (
                    p_mod.apiTrapPDU.getSpecificTrap(req_pdu).prettyPrint()
                )
                      )
                print('Uptime: %s' % (
                    p_mod.apiTrapPDU.getTimeStamp(req_pdu).prettyPrint()
                )
                      )
                var_binds = p_mod.apiTrapPDU.getVarBindList(req_pdu)
            else:  # SNMPv2c的处理方法
                var_binds = p_mod.apiPDU.getVarBindList(req_pdu)
                
            result_dict = {}  # 每一个Trap信息,都会整理返回一个字典
            # 下面是这个大字典的键值与嵌套的小字典
            # 1.3.6.1.2.1.1.3.0 {'value': 'ObjectSyntax', 'application-wide': 'ApplicationSyntax', 'timeticks-value': '103170310'}
            # 1.3.6.1.6.3.1.1.4.1.0 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'objectID-value': '1.3.6.1.6.3.1.1.5.4'}
            # 1.3.6.1.2.1.2.2.1.1.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'integer-value': '2'}
            # 1.3.6.1.2.1.2.2.1.2.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'string-value': 'GigabitEthernet2'}
            # 1.3.6.1.2.1.2.2.1.3.2 {'value': 'ObjectSyntax', 'simple': 'SimpleSyntax', 'integer-value': '6'}
            for x in var_binds:  # 打印详细Trap信息
                result = {}
                for x, y in x.items():
                    # print(x, y.prettyPrint())  # 最原始信息打印
                    # 处理信息到字典
                    if x == "name":
                        id = y.prettyPrint()  # 把name写入字典的键
                    else:
                        bind_v = [x.strip() for x in y.prettyPrint().split(":")]
                        for v in bind_v:
                            if v == '_BindValue':
                                continue
                            else:
                                result[v.split('=')[0]] = v.split('=')[1]
                result_dict[id] = result
            # 把字典传到分析模块进行分析
            analysis(result_dict)

    return whole_msg


def snmp_trap_receiver(ifname, port=162):
    if_ip = get_ip_address(ifname)
    transport_dispatcher = AsynsockDispatcher()  # 创建实例

    transport_dispatcher.registerRecvCbFun(cb_fun)  # 调用处理Trap信息的函数

    # UDP/IPv4
    transport_dispatcher.registerTransport(
        udp.domainName, udp.UdpSocketTransport().openServerMode((if_ip, port))  # 绑定到本地地址与UDP/162号端口
    )

    transport_dispatcher.jobStarted(1)  # 开始工作
    print("SNMP Trap Receiver Started!!!")
    try:
        # Dispatcher will never finish as job#1 never reaches zero
        transport_dispatcher.runDispatcher()  # 运行
    except Exception:
        transport_dispatcher.closeDispatcher()
        raise


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    snmp_trap_receiver("ens192")
