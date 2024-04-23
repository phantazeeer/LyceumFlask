import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, nullable=True)
    post_id = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    text = Column(Text, nullable=True)
    pic = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.datetime.now().date())