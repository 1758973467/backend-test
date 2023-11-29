
from datetime import datetime

from Config import db


class User(db.Model):
    __tablename__='User'

    class GENDER:
        MALE=0
        FEMALE=1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    name = db.Column('user_name', db.String, doc='昵称')
    gender = db.Column(db.Integer, default=GENDER.FEMALE, doc='性别')
    is_delete = db.Column(db.Boolean, default=False, doc='是否删除')
    time = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    update_time = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

    def keys(self):
        return ['id', 'name', 'gender']

    def __getitem__(self, item):
        return getattr(self, item)
