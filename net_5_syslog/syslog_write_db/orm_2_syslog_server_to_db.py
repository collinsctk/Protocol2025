#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from pathlib import Path
import sys

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
root_dir = current_file_path.parent.parent.parent
# 将根目录添加到Python路径
sys.path.insert(1, str(root_dir))


import socketserver
import re
from dateutil import parser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from net_5_syslog.syslog_write_db.orm_1_syslog_create_table import Syslog, db_file_name

engine = create_engine(f'sqlite:///{db_file_name}?check_same_thread=False',
                       # echo=True
                       )

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

# 定义正则表达式模式
# <187>83: *Apr  4 00:03:12.969: %LINK-3-UPDOWN: Interface GigabitEthernet2, changed state to up
# <189>574: Mar 15 03:00:01.275: %SEC_LOGIN-5-LOGIN_SUCCESS: Login Success [user: admin]
standard_pattern = re.compile(
    r'^<(?P<priority>\d+)>'           # Priority value containing facility and severity
    r'(?P<logid>\d+):\s+'             # Log ID
    r'\*?(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+\.\d+)'    # Timestamp with optional asterisk
    r':\s+%(?P<log_source>[A-Z_]+)-'  # Log source (corrected to capture uppercase letters and underscores)
    r'(?P<severity_level>\d)-'        # Severity level
    r'(?P<description>\w+):\s+'       # Description
    r'(?P<text>.*)$'                  # Message text
)

# 处理其他格式的日志
# <189>574: Mar 15 03:00:01.275: ICMP: echo reply rcvd
# 有些日志会缺失%SYS-5-CONFIG_I, 造成第一个正则表达式无法匹配
# 下面的icmp的debug就是示例
# <191>91: *Apr  4 00:12:29.616: ICMP: echo reply rcvd, src 10.1.1.80, dst 10.1.1.253, topology BASE, dscp 0 topoid 0
alternate_pattern = re.compile(
    r'^<(?P<priority>\d+)>'           # Priority value containing facility and severity
    r'(?P<logid>\d+):\s+'             # Log ID
    r'\*?(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+\.\d+):\s+'    # Timestamp with optional asterisk
    r'(?P<log_source>\w+):\s+'        # Log source
    r'(?P<text>.*)$'                  # Message text
)

class SyslogUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())  # 读取数据
        print('-' * 40)
        print(data)
        print('-' * 40)
        syslog_info_dict = {'device_ip': self.client_address[0]}
        
        # Try standard syslog format first
        match = standard_pattern.match(str(data))
        if match:
            # 185 二进制为 1011 1001
            # 前5位为facility  >> 3 获取前5位
            # 后3位为severity_level  & 0b111 获取后3位
            priority = int(match.group('priority'))
            syslog_info_dict.update({
                'facility': priority >> 3,
                'facility_name': facility_dict[priority >> 3],
                'logid': int(match.group('logid')),
                'time': parser.parse(match.group('timestamp')),
                'log_source': match.group('log_source'),
                'severity_level': int(match.group('severity_level')),
                'severity_level_name': severity_level_dict[int(match.group('severity_level'))],
                'description': match.group('description'),
                'text': match.group('text')
            })
        else:
            # Try alternate format
            match = alternate_pattern.match(str(data))
            if match:
                # 如果在文本部分解析不了severity_level, 切换到priority去获取
                # 185 二进制为 1011 1001
                # 前5位为facility  >> 3 获取前5位
                # 后3位为severity_level  & 0b111 获取后3位
                priority = int(match.group('priority'))
                severity_level = priority & 0b111  # Extract severity from priority
                syslog_info_dict.update({
                    'facility': priority >> 3,
                    'facility_name': facility_dict[priority >> 3],
                    'logid': int(match.group('logid')),
                    'time': parser.parse(match.group('timestamp')),
                    'log_source': match.group('log_source'),
                    'severity_level': severity_level,
                    'severity_level_name': severity_level_dict[severity_level],
                    'description': severity_level_dict[severity_level],
                    'text': match.group('text')
                })
            else:
                print(f"Could not parse message: {data}")
                return

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


