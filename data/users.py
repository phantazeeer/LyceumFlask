import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hashed_pass = Column(String, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    sec_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    info = Column(Text, nullable=True)
    platforms = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.datetime.now().date())
    birth = Column(DateTime, nullable=True)
    liked = Column(String, nullable=True)