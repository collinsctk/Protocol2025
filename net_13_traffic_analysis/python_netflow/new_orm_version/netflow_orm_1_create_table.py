from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime

db_dir = '../db_dir/'

engine = create_engine(f'sqlite:///{db_dir}sqlalchemy_sqlite3.db?check_same_thread=False',
                       # echo=True
                       )

Base = declarative_base()


class Netflow(Base):
    __tablename__ = 'netflow'

    id = Column(Integer, primary_key=True)
    ipv4_src_addr = Column(String(64), nullable=False)
    ipv4_dst_addr = Column(String(64), nullable=False)
    protocol = Column(Integer, nullable=False)
    l4_src_port = Column(Integer, nullable=False)
    l4_dst_port = Column(Integer, nullable=False)
    input_interface_id = Column(Integer, nullable=False)
    in_bytes = Column(Integer, nullable=False, index=True)
    record_datetime = Column(DateTime(timezone='Asia/Chongqing'), default=datetime.datetime.now)

    def __repr__(self):
        return f"{self.__class__.__name__}(src: {self.ipv4_src_addr} | " \
               f"dst: {self.ipv4_dst_addr} | pro: {self.protocol} | sport: {self.l4_src_port} |" \
               f"dport: {self.l4_dst_port})"


if __name__ == '__main__':
    # checkfirst=True，表示创建表前先检查该表是否存在，如同名表已存在则不再创建。其实默认就是True
    Base.metadata.create_all(engine, checkfirst=True)
