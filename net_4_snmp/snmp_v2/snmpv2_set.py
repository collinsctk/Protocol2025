#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902


def snmpv2_set(ip, community, oid, value, port=161):
    cmd_gen = cmdgen.CommandGenerator()
    # print(dir(rfc1902))
    # 类型 ['ApplicationSyntax', 'Bits', 'Counter32', 'Counter64', 'Gauge32', 'Integer', 'Integer32', 'IpAddress', 'ObjectIdentifier', 'ObjectName', 'ObjectSyntax', 'OctetString', 'Opaque', 'SimpleSyntax', 'TimeTicks', 'Unsigned32', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'constraint', 'error', 'namedtype', 'namedval', 'rfc1155', 'tag', 'univ', 'version_info']
    # 需要提前通过OIDVIEW查询类型
    # 通过不同的类型写入数据
    if isinstance(value, str):
        set_value = rfc1902.OctetString(value)
    elif isinstance(value, int):
        set_value = rfc1902.Integer(value)

    error_indication, error_status, error_index, var_binds = cmd_gen.setCmd(
        cmdgen.CommunityData(community),  # 写入Community
        cmdgen.UdpTransportTarget((ip, port)),  # IP地址和端口号
                                  (oid, set_value)  # OID和写入的内容，需要进行编码！
        )
    # 错误处理
    if error_indication:
        print("写入错误!!!")
        print(error_indication)
    elif error_status:
        print("写入错误!!!")
        print('%s at %s' % (
            error_status.prettyPrint(),
            error_index and var_binds[int(error_index) - 1][0] or '?'
        )
              )
    else:
        print("写入成功!!!")
    # 打印回显示结果
    for name, val in var_binds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))  # 打印修改的结果


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    # 设置主机名
    snmpv2_set("10.1.1.253", "tcpiprw", "1.3.6.1.2.1.1.5.0", "R1", port=161)
    # shutdown G2
    # 1 为up , 2 为down
    snmpv2_set("10.1.1.253", "tcpiprw", "1.3.6.1.2.1.2.2.1.7.2", 2, port=161)
