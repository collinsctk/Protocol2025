#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from telnetlib import Telnet
# import re,可以使用正则表达式匹配回显，然后做判断，决定下一步的操作
import time


def telnet_client(ip, username, password, cmd_list, enable=None, verbose=True):
    tn = Telnet(ip, 23)
    rackreply = tn.expect([], timeout=1)[2].decode().strip()  # 读取回显
    if verbose:
        print(rackreply)  # 打印回显
    tn.write(username.encode())  # 任何字串都需要转成二进制字串
    tn.write(b'\n')  # 注意一定要打回车
    time.sleep(1)  # 在命令之间留出一定的时间间隔！否则路由器可能反应不过来
    rackreply = tn.expect([], timeout=1)[2].decode().strip()
    if verbose:
        print(rackreply)  # 打印回显
    tn.write(password.encode())
    tn.write(b'\n')
    time.sleep(1)
    rackreply = tn.expect([], timeout=1)[2].decode().strip()
    if verbose:
        print(rackreply)  # 打印回显
    if enable is not None:
        tn.write(b'enable\n')
        time.sleep(1)
        rackreply = tn.expect([], timeout=1)[2].decode().strip()
        if verbose:
            print(rackreply)  # 打印回显
        tn.write(enable.encode())
        tn.write(b'\n')
        rackreply = tn.expect([], timeout=1)[2].decode().strip()
        if verbose:
            print(rackreply)  # 打印回显
    time.sleep(1)
    for cmd in cmd_list:  # 读取命令，并且逐个执行！
        tn.write(cmd.encode() + b'\n')
        rackreply = tn.expect([], timeout=1)[2].decode().strip()
        if verbose:
            print(rackreply)  # 打印回显
        time.sleep(1)
    tn.write(b'exit\n')
    rackreply = tn.expect([], timeout=1)[2].decode().strip()
    if verbose:
        print(rackreply)  # 打印回显
    tn.close()


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    cmds = ['terminal length 0', 'show ver', 'config ter', 'router ospf 1']
    telnet_client('10.1.1.253', 'admin', 'Cisc0123', cmd_list=cmds, verbose=True)
