import os
import hashlib
import datetime
import simplejson
import datetime

from toffee.db import Base, session, Session
from sqlalchemy import *

class Flowstate(Base):

    __tablename__ = 'flowstate'

    user_id = Column(Integer, primary_key=True)
    keyname = Column(String, primary_key=True)
    json = Column(String, nullable=False)
    time_created = Column(DateTime, nullable=False, default=datetime.datetime.now())

    @classmethod
    def set(cls, user_id, keyname, data):
        serialized = simplejson.dumps(data)
        with sesion() as s:
            obj = Flowstate(user_id=user_id, keyname=keyname, json=serialized)
            s.add(obj)

    @classmethod
    def get(cls, user_id, keyname):
        with session() as s:
            flow = s.query(cls).filter(cls.user_id == user_id).filter(cls.keyname == keyname).first()
        if flow:
            return simplejson.loads(flow.json)
        else:
            return None

    @classmethod
    def get_multiple(cls, user_id, *keynames):
        result = dict((k, None) for k in keynames)
        with session() as s:
            flows = s.query(cls).filter(cls.user_id == user_id).filter(cls.keyname.in_(keynames))
        for flow in flows:
            result[flow.keyname] = simplejson.loads(flow.json)
        return result

    @classmethod
    def delete(cls, user_id, keyname):
        with session() as s:
            s.query(cls).filter(cls.user_id == user_id).filter(cls.keyname == keyname).delete()

__all__ = ['Flowstate']
