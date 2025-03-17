#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于亁颐堂NetDevOps课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主VIP, 让我们聊点高级的
# https://vip.qytang.com/


from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
from pathlib import Path
import os

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
current_dir = current_file_path.parent

db_filename = f'{current_dir}{os.sep}sqlalchemy_sqlite3.db'

Base = declarative_base()


class RouterMonitor(Base):
    __tablename__ = 'router_monitor'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    cpu_usage_percent = Column(Integer, nullable=False)
    mem_usage_percent = Column(Integer, nullable=False)
    record_datetime = Column(DateTime(timezone='Asia/Chongqing'),
                             default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.record_datetime} " \
               f"| CPU_Usage_Percent: {self.cpu_usage_percent} " \
               f"| MEM_Usage_Percent: {self.mem_usage_percent} "


if __name__ == '__main__':
    import os
    # ~~~~~~~~~~~~~~~~~psql~~~~~~~~~~~~~~~~~
    # psycopg2 (yum install postgresql-devel;pip3 install psycopg2-binary)
    # 修改认证方案
    # https://dothanhlong.org/fix-unable-to-connect-to-postgresql-server-scram-authentication-requires-libpq-version-10-or-above/
    # 运行./psql/docker_run_script.sh拉起psql
    # engine = create_engine('postgresql+psycopg2://qytangdbuser:Cisc0123@10.10.1.200/qytangdb')

    # ~~~~~~~~~~~~~~~~~sqlite3~~~~~~~~~~~~~~~~~
    if os.path.exists(db_filename):
        os.remove(db_filename)

    engine = create_engine(f'sqlite:///{db_filename}?check_same_thread=False',
                           # echo=True
                           )

    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)
