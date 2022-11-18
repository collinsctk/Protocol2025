#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import socketserver
import re
from dateutil import parser
from sqlalchemy.orm import sessionmaker
from orm_1_syslog_create_table import Syslog, engine


Session = sessionmaker(bind=engine)
session = Session()


# facility与ID的对应关系的字典
facility_dict = {0: 'KERN',
                 1: 'USER',
                 2: 'MAIL',
                 3: 'DAEMON',
                 4: 'AUTH',
                 5: 'SYSLOG',
                 6: 'LPR',
                 7: 'NEWS',
                 8: 'UUCP',
                 9: 'CRON',
                 10: 'AUTHPRIV',
                 11: 'FTP',
                 16: 'LOCAL0',
                 17: 'LOCAL1',
                 18: 'LOCAL2',
                 19: 'LOCAL3',
                 20: 'LOCAL4',
                 21: 'LOCAL5',
                 22: 'LOCAL6',
                 23: 'LOCAL7'}

# severity_level与ID的对应关系的字典
severity_level_dict = {0: 'EMERG',
                       1: 'ALERT',
                       2: 'CRIT',
                       3: 'ERR',
                       4: 'WARNING',
                       5: 'NOTICE',
                       6: 'INFO',
                       7: 'DEBUG'}


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())  # 读取数据
        print(data)
        syslog_info_dict = {'device_ip': self.client_address[0]}
        try:
            # <187>83: *Apr  4 00:03:12.969: %LINK-3-UPDOWN: Interface GigabitEthernet2, changed state to up
            syslog_info = re.match(r'^<(\d*)>(\d*): \*(.*): %(\w+)-(\d)-(\w+): (.*)', str(data)).groups()
            # print(syslog_info[0]) 提取为整数 例如 185
            # 185 二进制为 1011 1001
            # 前5位为facility  >> 3 获取前5位
            # 后3位为severity_level  & 0b111 获取后3位
            syslog_info_dict['facility'] = int(syslog_info[0]) >> 3
            syslog_info_dict['facility_name'] = facility_dict[int(syslog_info[0]) >> 3]
            syslog_info_dict['logid'] = int(syslog_info[1])
            syslog_info_dict['time'] = parser.parse(syslog_info[2])
            syslog_info_dict['log_source'] = syslog_info[3]
            syslog_info_dict['severity_level'] = int(syslog_info[4])
            syslog_info_dict['severity_level_name'] = severity_level_dict[int(syslog_info[4])]
            syslog_info_dict['description'] = syslog_info[5]
            syslog_info_dict['text'] = syslog_info[6]
        except AttributeError:
            # 有些日志会缺失%SYS-5-CONFIG_I, 造成第一个正则表达式无法匹配 , 也无法提取severity_level
            # 下面的icmp的debug就是示例
            # <191>91: *Apr  4 00:12:29.616: ICMP: echo reply rcvd, src 10.1.1.80, dst 10.1.1.253, topology BASE, dscp 0 topoid 0
            syslog_info = re.match(r'^<(\d*)>(\d*): \*(.*): (\w+): (.*)', str(data)).groups()
            print(syslog_info[0])
            syslog_info_dict['facility'] = int(syslog_info[0]) >> 3
            syslog_info_dict['facility_name'] = facility_dict[int(syslog_info[0]) >> 3]
            syslog_info_dict['logid'] = int(syslog_info[1])
            syslog_info_dict['time'] = parser.parse(syslog_info[2])
            syslog_info_dict['log_source'] = syslog_info[3]
            # 如果在文本部分解析不了severity_level, 切换到syslog_info[0]去获取
            # 185 二进制为 1011 1001
            # 前5位为facility  >> 3 获取前5位
            # 后3位为severity_level  & 0b111 获取后3位
            syslog_info_dict['severity_level'] = int(syslog_info[0]) & 0b111
            syslog_info_dict['severity_level_name'] = severity_level_dict[(int(syslog_info[0]) & 0b111)]
            syslog_info_dict['description'] = 'N/A'
            syslog_info_dict['text'] = syslog_info[4]

        print(syslog_info_dict)

        # syslog_record = Syslog(
        #     device_ip=syslog_info_dict.get('device_ip'),
        #     time=syslog_info_dict.get('time'),
        #     facility=syslog_info_dict.get('facility'),
        #     facility_name=syslog_info_dict.get('facility_name'),
        #     severity_level=syslog_info_dict.get('severity_level'),
        #     severity_level_name=syslog_info_dict.get('severity_level_name'),
        #     logid=syslog_info_dict.get('logid'),
        #     log_source=syslog_info_dict.get('log_source'),
        #     description=syslog_info_dict.get('description'),
        #     text=syslog_info_dict.get('text')
        # )

        # 更加简洁的方案
        syslog_record = Syslog(**syslog_info_dict)
        session.add(syslog_record)
        session.commit()


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    try:
        HOST, PORT = "0.0.0.0", 514  # 本地地址与端口
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)  # 绑定本地地址，端口和syslog处理方法
        print("Syslog 服务已启用, 写入日志到数据库!!!")
        server.serve_forever(poll_interval=0.5)  # 运行服务器，和轮询间隔

    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:  # 捕获Ctrl+C，打印信息并退出
        print("Crtl+C Pressed. Shutting down.")
    finally:
        for i in session.query(Syslog).all():
            print(i)


