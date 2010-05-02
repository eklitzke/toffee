from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Zone(Base):

    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    qclass = Column(Integer, default=1, nullable=False)
    qtype = Column(Integer, nullable=False)
    ttl = Column(Integer, default=120, nullable=False)
    rdata = Column(BLOB, nullable=False)

_is_configured = False
Session = sessionmaker()

def bind_engine(engine):
    global _is_configured
    assert not _is_configured
    Session.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all()
