from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

class _Base(object): 

    @classmethod
    def get_by_id(cls, id):
        s = Session()
        return s.query(cls).filter(cls.id == id).first()

Base = declarative_base(cls=_Base)

_is_configured = False
Session = sessionmaker()

@contextmanager
def session():
    sess = Session()
    try:
        yield sess
    except:
        sess.rollback()
        raise
    else:
        sess.commit()

def bind_engine(engine):
    global _is_configured
    assert not _is_configured
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all()
    _is_configured = True

from toffee.db.tables import *
