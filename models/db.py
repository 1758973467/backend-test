import contextlib
from datetime import datetime

from sqlalchemy import create_engine, Column, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/interview'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_POOL_SIZE=200
    SQLALCHEMY_POOL_MAX_SIZE=500
    SQLALCHEMY_POOL_RECYCLE=5000


class BaseMixin:
    """model的基类,所有model都必须继承"""
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, index=True)
    deleted_at = Column(DateTime)  # 可以为空, 如果非空, 则为软删


engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,  # SQLAlchemy 数据库连接串，格式见下面
    echo=bool(Config.SQLALCHEMY_ECHO),  # 是不是要把所执行的SQL打印出来，一般用于调试
    pool_size=int(Config.SQLALCHEMY_POOL_SIZE),  # 连接池大小
    max_overflow=int(Config.SQLALCHEMY_POOL_MAX_SIZE),  # 连接池最大的大小
    pool_recycle=int(Config.SQLALCHEMY_POOL_RECYCLE),  # 多久时间回收连接
)
Session = sessionmaker(bind=engine)

Base = declarative_base()


@contextlib.contextmanager
def get_session():
    s = Session()
    try:
        yield s
        s.commit()
    except Exception as e:
        s.rollback()
        raise e
    finally:
        s.close()

