from toffee.db import Base, session
from sqlalchemy import *

class Record(object):

    def __init__(self, id, name, qtype, ttl, rdata):
        self.id = id
        self.name = name
        self.qtype = qtype
        self.ttl = ttl

        if qtype == dns.A.rdclass:
            self.dns = dns.A.from_wire(rdata)
            self.rr = 'A'
        elif qtype == dns.SOA.rdclass:
            self.dns = dns.SOA.from_wire(rdata)
            self.rr = 'SOA'

class Zone(Base):

    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    qclass = Column(Integer, default=1, nullable=False)
    qtype = Column(Integer, nullable=False)
    ttl = Column(Integer, default=120, nullable=False)
    rdata = Column(BLOB, nullable=False)

    def as_record(self):
        return Record(self.id, self.name, self.qtype, self.ttl, self.rdata)

__all__ = ['Record', 'Zone']
