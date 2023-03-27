from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
from sqlalchemy.orm import sessionmaker


# -------------------------sqlite3-------------------------
engine = create_engine('sqlite:///sqlalchemy_sqlite3.db?check_same_thread=False',
                       # echo=True
                       )


Base = declarative_base()

Session = sessionmaker(bind=engine)

# 创建session对象
session = Session()


class RouterConfig(Base):
    __tablename__ = 'router_config'

    id = Column(Integer, primary_key=True)
    router_ip = Column(String(64), nullable=False, index=True)
    router_config = Column(String(9999), nullable=False)
    config_hash = Column(String(500), nullable=False)
    record_time = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(路由器IP地址: {self.router_ip} | 配置Hash: {self.config_hash} | " \
               f"记录时间: {self.record_time})"


if __name__ == '__main__':
    # 创建数据库
    Base.metadata.create_all(engine, checkfirst=True)

