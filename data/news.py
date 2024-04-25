import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, sqlalchemy.ForeignKey("users.id"))
    likes = Column(Integer, nullable=True)
    pic = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    created = Column(DateTime, default=datetime.datetime.now().date())
    user = orm.relationship('User')
    comments = orm.relationship("Comment", back_populates="post")