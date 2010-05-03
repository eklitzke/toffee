import os
import hashlib
import datetime

from toffee.db import Base, session, Session
from sqlalchemy import *

SALT_LEN = 8

class UserException(Exception):
    pass

class NoSuchEmail(UserException):
    pass

class BadPassword(UserException):
    pass

class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    time_created = Column(DateTime, nullable=False, default=datetime.datetime.now())
    password = Column(String, nullable=False)
    salt = Column(BLOB, nullable=False)

    @classmethod
    def new(cls, email, password):
        email = email.lower()
        salt = bytes(os.urandom(SALT_LEN))
        password = hashlib.sha1(salt + password).hexdigest()
        with session() as s:
            obj = cls(email=email, password=password, salt=buffer(salt))
            s.add(obj)
        return obj

    @classmethod
    def get_by_email_password(cls, email, password):
        with session() as s:
            user = s.query(Users).filter(Users.email == email).first()
            if user is None:
                raise NoSuchEmail

            hashed_pass = hashlib.sha1(bytes(user.salt) + password).hexdigest()
            if hashed_pass != user.password:
                raise BadPassword
        return user

__all__ = ['UserException', 'NoSuchEmail', 'BadPassword', 'Users']
