from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
import datetime
from pathlib import Path

# 获取当前文件所在目录的父目录（项目根目录）并添加到Python路径
current_file = Path(__file__)
root_root = current_file.parent.parent

db_dir = root_root / 'db_dir' / 'netflow.sqlite'

engine = create_engine(f'sqlite:///{db_dir}?check_same_thread=False',
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
    if db_dir.exists():
        db_dir.unlink()
    Base.metadata.create_all(engine, checkfirst=True)
