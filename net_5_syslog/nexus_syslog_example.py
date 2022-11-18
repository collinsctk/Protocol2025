#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from cli import *
from nxos import *
import time

time.sleep(10)
PORT_LIST = [
    # port, asic, slice, N
    ["E1/49", "0", "1", "7"],
    ["E1/50", "0", "1", "8"],
    ["E1/51", "0", "0", "7"],
    ["E1/52", "0", "0", "8"],
]


def IFMBR_check(ints, asic, slice, N):
    BD_VAULE = int(cli("slot 1 show system internal iftmc info interface %s | in \"LIF =\"" % ints).split()[5]) - 4096
    IFMBR_VAULE = cli(
        "slot 1 debug hardware internal dav dump asic %s slice %s table tah_dav_rwx_rwouterbdstatetable %s c f | in ifmbr" % (
        asic, slice, BD_VAULE))
    if N == "7":
        IFMBR_VAULE_FINAL = list(IFMBR_VAULE.strip())[-7]
    elif N == "8":
        IFMBR_VAULE_FINAL = list(IFMBR_VAULE.strip())[-8]
    if (int(IFMBR_VAULE_FINAL, 16) % 2) == 0:  # 如果判断Bug条件成立!就shutdown/no shutdown端口,修复问题,并且产生syslog
        py_syslog(3, "Rwxouterbdstatetable for %s is incorrect!!" % ints)
        cli("conf t ; interface nve1 ; shutdown ; no shutdown")  # Reset the incorrect port
    else:   # 如果Bug条件不成立,依然产生syslog
        py_syslog(3, "Rwxouterbdstatetable for %s is correct!!" % ints)


while True:
    for i in PORT_LIST:
        IFMBR_check(i[0], i[1], i[2], i[3])
    time.sleep(10)

