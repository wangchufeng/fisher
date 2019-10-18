from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger


class SQLAlchemy(_SQLAlchemy):
    # 利用contextmanager，增加调用包的上下文
    # 下面例子是每次数据库提交时候都放在try里面，以防commit出错时候可以rollback
    @contextmanager
    def auto_commit(self):
        try:
            yield
            # 假如在db.session.commit()时候发生错误，并且没有rollback，那么以后对数据库的操作会报错
            # 建议在每次db.session.commit的时候都try,rollback一下
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# 复写数据库查询操作，filter_by函数
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
