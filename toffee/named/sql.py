from contextlib import contextmanager
import sqlalchemy

import toffee._dns as dns
from toffee.named.tables import *

bind_engine(sqlalchemy.create_engine("sqlite:///:memory:", echo=True))
session = Session()

def txn(func):
    def inner(cls, name, *args, **kwargs):
        try:
            func(cls, name, *args, **kwargs)
            SOA.bump_serial(cls.to_base_name(name))
        except:
            session.rollback()
            raise
        else:
            session.commit()
    inner.__name__ = func.__name__
    inner.__doc__ = func.__doc__
    return inner

class DNSResource(object):

    qtype = None
    default_ttl = 120

    @classmethod
    def filter_qtype(cls, qclass=1, name=None):
        print Zone.qclass == qclass
        q = session.query(Zone).filter_by(qclass=qclass).filter_by(qtype=cls.qtype)
        if name is not None:
            return q.filter(Zone.name == name)
        else:
            return q

    @classmethod
    def to_base_name(cls, name):
        split_name = name.split('.')
        assert split_name[-1] == ''
        return '.'.join(split_name[-3:]) # something like foo.com. or bar.org.

    @classmethod
    def new_record(cls, name, rdata, ttl=None):
        kwargs = {'name': name, 'qtype': cls.qtype, 'rdata': rdata}
        if ttl is not None:
            kwargs['ttl'] = ttl
        record = Zone(**kwargs)
        session.add(record)
        return record

    @classmethod
    def bump_serial(cls, name):
        base_name = cls.to_base_name(name)
        soa = session.query.filter(Zone.qclass == 1).filter(Zone.qtype == SOA.qtype).filter(Zone.name == base_name).one()
        soa.serial = soa.serial + 1

class A(DNSResource):

    qtype = 1

    @classmethod
    @txn
    def update(cls, name, address):
        record = cls.filter_qtype(name=name).first()
        rdata = dns.A(address).as_buffer()
        if record:
            record.rdata = rdata
        else:
            record = cls.new_record(name, rdata)
        return record.id

class SOA(DNSResource):

    qtype = 6

    @classmethod
    @txn
    def update(cls, name, mname, rname, serial=0, refresh=86400, retry=3600, expire=3600000, minimum=120):
        if name != cls.to_base_name(name):
            raise ValueError("Cannot create an SOA record for a non-TLD")

        existing = cls.filter_qtype(name=name).first()
        if existing:
            session.delete(existing)

        rdata = dns.SOA(mname, rname, serial, refresh, retry, expire, minimum).as_buffer()
        cls.new_record(name, rdata, ttl=0)

    @classmethod
    def bump_serial(cls, name):
        record = cls.filter_qtype(name=name).one()
        rdata, serial = dns.SOA.increment_serial(record.rdata)
        record.rdata = rdata
        return serial
