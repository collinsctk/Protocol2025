#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import logging
import socketserver
import re
from net_4_snmp.snmp_v2.snmpv2_get_if_oid import shutdown_if

log_file = './log_dir/pysyslog.log'

# 配置logging.info, 记录文件到本地
# 日志模块的详细介绍
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',     # 字符串格式
                    datefmt='%Y/%m/%d %H:%M:%S',            # 时间格式
                    filename=log_file,                      # log文件
                    filemode='a')                           # 追加模式


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())  # 读取数据
        # ============可以配置过滤器仅仅读取接口up/down信息===============
        if re.match(r'.*%LINEPROTO-5-UPDOWN: Line protocol on Interface \S+, changed state to down.*', data):
            if_name = re.match(r'.*%LINEPROTO-5-UPDOWN: Line protocol on Interface (\S+), changed state to down.*',
                               data).groups()[0]
            device_ip = self.client_address[0]
            community = "tcpiprw"
            shutdown_if(device_ip, community, if_name, 1)

        # 把信息logging到本地, logging level为INFO
        logging.info(f"source_ip: {self.client_address[0]} - message: {str(data)}")


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    # -------------------注意如果是WINDOWS, 需要关闭防火墙, 或者开放514端口-------------------
    try:
        HOST, PORT = "0.0.0.0", 514                                         # 本地地址与端口
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)     # 绑定本地地址，端口和syslog处理方法
        print("Syslog 服务已启用, 写入日志到文本文件!!!")
        server.serve_forever(poll_interval=0.5)                             # 运行服务器，和轮询间隔

    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:                                               # 捕获Ctrl+C，打印信息并退出
        print("Crtl+C Pressed. Shutting down.")
