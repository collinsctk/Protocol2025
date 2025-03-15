# pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
import os
from pathlib import Path

tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))  # 设置时区为东八区

# 获取当前文件的路径
current_file_path = Path(__file__).resolve()

# 获取当前文件所在的目录路径
current_dir = current_file_path.parent

db_file_path = f'{current_dir}{os.sep}db-files{os.sep}sqlalchemy_device_config_sqlite3.db'

Base = declarative_base()


class RouterConfig(Base):
    __tablename__ = 'routerconfig'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    config = Column(String(4096), nullable=False)
    md5 = Column(String(1024), nullable=False)
    record_time = Column(DateTime(timezone=False),
                         default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.record_time} " \
               f"| MD5: {self.md5})"


if __name__ == '__main__':
    # 如果希望删除老的数据就取消注释
    if os.path.exists(db_file_path):
        os.remove(db_file_path)

    engine = create_engine(f'sqlite:///{db_file_path}?check_same_thread=False',
                           # echo=True
                           )
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)
