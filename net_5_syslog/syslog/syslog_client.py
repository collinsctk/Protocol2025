#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import socket


class Facility:
    # Syslog facilities
    KERN, USER, MAIL, DAEMON, AUTH, SYSLOG, LPR, NEWS, UUCP, CRON, AUTHPRIV, FTP = range(12)

    LOCAL0, LOCAL1, LOCAL2, LOCAL3, LOCAL4, LOCAL5, LOCAL6, LOCAL7 = range(16, 24)


class Level:
    # Syslog levels
    EMERG, ALERT, CRIT, ERR, WARNING, NOTICE, INFO, DEBUG = range(8)


class Syslog:
    # A syslog client that logs to a remote server.
    def __init__(self, host="localhost", port=514, facility=Facility.LOCAL7):
        self.host = host
        self.port = port
        self.facility = facility
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 如果使用send就需要给LEVEL
    def send(self, message, level):
        # Send a syslog message to remote host using UDP.
        # 185 二进制为 1011 1001
        # 前5位为facility  >> 3 获取前5位
        # 后3位为severity_level  & 0b111 获取后3位
        # level + self.facility * 8 [乘以8的原因就在于后三位为severity_level]
        data = "<%d>%s" % (level + self.facility * 8, message)
        self.socket.sendto(data.encode(), (self.host, self.port))

    # 非send的方法,会使用默认LEVEL
    def warn(self, message):
        # Send a syslog warning message.
        self.send(message, Level.WARNING)

    def notice(self, message):
        # Send a syslog notice message.
        self.send(message, Level.NOTICE)

    def error(self, message):
        # Send a syslog error message.
        self.send(message, Level.ERR)


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    log = Syslog("10.1.1.100")
    log.send("qytang syslog test", Level.NOTICE)
    log.notice("qytang syslog test")
