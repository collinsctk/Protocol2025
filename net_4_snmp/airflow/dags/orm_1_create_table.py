# https://www.cnblogs.com/lsdb/p/9835894.html

from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, orm
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float


engine = create_engine('postgresql+psycopg2://qytangdbuser:Cisc0123@196.21.5.218/qytangdb',
                       connect_args={"options": "-c timezone=Asia/Chongqing"})

Base = orm.declarative_base()

# 定义东八区时区
GMT_PLUS_8 = timezone(timedelta(hours=8))


class RouterMonitor(Base):
    __tablename__ = 'router_monitor'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    cpu_usage_percent = Column(Integer, nullable=False)
    mem_usage_percent = Column(Integer, nullable=False)
    record_datetime = Column(DateTime(timezone=False), nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.record_datetime} " \
               f"| CPU_Usage_Percent: {self.cpu_usage_percent} " \
               f"| MEM_Usage_Percent: {self.mem_usage_percent} "


if __name__ == '__main__':
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)

