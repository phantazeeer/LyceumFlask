import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    hashed_pass = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    sec_name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    projects = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    created = Column(DateTime, default=datetime.datetime.now().date())
    birth = Column(DateTime, nullable=True)
    liked_posts = Column(String, nullable=True)
    liked_somments = Column(String, nullable=True)
    news = orm.relationship("News", back_populates="user")
    comments = orm.relationship("Comment", back_populates="user")

    def set_password(self, password):
        self.hashed_pass = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_pass, password)