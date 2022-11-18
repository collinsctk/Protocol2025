from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime

tzutc_8 = datetime.timezone(datetime.timedelta(hours=8))  # 设置时区为东八区

engine = create_engine('sqlite:///sqlalchemy_sqlite3.db?check_same_thread=False',
                       # echo=True
                       )

Base = declarative_base()


class RouterMonitor(Base):
    __tablename__ = 'router_monitor'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    cpu_useage_percent = Column(Integer, nullable=False)
    mem_use = Column(Integer, nullable=False)
    mem_free = Column(Integer, nullable=False)
    record_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.record_datetime} " \
               f"| CPU_Usage_Percent: {self.cpu_useage_percent} " \
               f"| MEM Use: {self.mem_use} " \
               f"| MEM Free: {self.mem_free})"


if __name__ == '__main__':
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)
