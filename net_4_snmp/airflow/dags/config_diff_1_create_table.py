from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime

Base = declarative_base()


class RouterConfig(Base):
    __tablename__ = 'routerconfig'

    id = Column(Integer, primary_key=True)
    device_ip = Column(String(64), nullable=False)
    config = Column(String(40960), nullable=False)
    md5 = Column(String(1024), nullable=False)
    record_time = Column(DateTime(timezone=False),
                         default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(Router: {self.device_ip} " \
               f"| Datetime: {self.record_time} " \
               f"| MD5: {self.md5})"


if __name__ == '__main__':
    engine = create_engine('postgresql+psycopg2://qytangdbuser:Cisc0123@196.21.5.218/qytangdb',
                           connect_args={"options": "-c timezone=Asia/Chongqing"})

    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)
