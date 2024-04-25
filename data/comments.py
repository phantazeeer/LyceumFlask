import datetime

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, sqlalchemy.ForeignKey("users.id"))
    post_id = Column(Integer, sqlalchemy.ForeignKey("news.id"))
    likes = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    pic = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.datetime.now().date())
    user = orm.relationship('User')
    post = orm.relationship('News')