from contextlib import contextmanager
import sqlite3
import toffee._dns as dns

DEFAULT_TTL = 120

SUPPORTED_TLDS = ['.com', '.net', '.org', '.example']

_engine = sqlite3.connect('test.db', isolation_level='DEFERRED')
_engine.row_factory = sqlite3.Row

def maybe_one(query):
    rows = list(query)
    if len(rows) == 0:
        return None
    elif len(rows) == 1:
        return rows[0]
    else:
        raise ValueError("Got %d rows (expected one or zero)" % (len(rows),))

def just_one(query):
    rows = list(query)
    if len(rows) == 1:
        return rows[0]
    else:
        raise ValueError("Got %d rows (expected exactly one)" % (len(rows),))

@contextmanager
def cursor(engine=None):
    engine = engine or _engine
    c = engine.cursor()
    try:
        yield c
    finally:
        c.close()

@contextmanager
def read_txn(self):
    try:
        yield self.conn.cursor()
    finally:
        self.conn.rollback()

@contextmanager
def write_txn(self):
    try:
        yield self.conn.cursor()
    except:
        self.conn.rollback()
        raise
    else:
        self.conn.commit()

class DNSResource(object):

    qtype = None

    @classmethod
    def remove_dups(cls, name, rdata, qtype=None):
        qtype = qtype or cls.qtype
        with cursor() as c:
            c.execute('DELETE FROM responses WHERE name = ? AND qclass = 1 AND qtype = ? AND rdata = ?', (name, qtype, rdata))
  
    @classmethod
    def insert_record(cls, name, ttl, rdata, qtype=None):
        qtype = qtype or cls.qtype
        with cursor() as c:
            c.execute('INSERT INTO responses (name, qclass, qtype, ttl, rdata) VALUES (?, 1, ?, ?, ?)', (name, qtype, ttl, rdata))

    @classmethod
    def to_base_name(cls, name):
        split_name = name.split('.')
        assert split_name[-1] == ''
        return '.'.join(split_name[-3:]) # something like foo.com. or bar.org.

    @classmethod
    def get_records_by_type_and_name(cls, name):
        with cursor() as c:
            return c.execute('SELECT COUNT(*) AS count FROM responses WHERE qclass = 1 AND qtype = ? AND name = ?', (cls.qtype, name))
    
    @classmethod
    def update_ttl_and_rdata_by_id(cls, row_id, ttl, rdata):
        with cursor() as c:
            return c.execute('UPDATE responses SET ttl = ?, rdata = ? WHERE id = ?', (ttl, rdata, row_id))
     
    @classmethod
    def insert_or_update(cls, name, ttl, rdata):
        row = maybe_one(cls.get_records_by_type_and_name(name))
        if row:
            return cls.update_ttl_and_rdata_by_id(row['id'], ttl, rdata)
        else:
            return cls.insert_or_update(name, ttl, rdata)

    @classmethod
    def check_record_uniqueness(cls, name):
        with cursor() as c:
            row = just_one(c.execute('SELECT COUNT(*) AS count FROM responses WHERE qclass = 1 AND qtype = ? AND name = ?', (cls.qtype, name)))
            if row['count'] > 0:
                raise ValueError("Expected a unique record for name %r with qtype %d" % (name, cls.qtype))

    @classmethod
    def increment_serial(cls, name):
        base_name = cls.to_base_name(name)
        with cursor() as c:
            row = just_one(c.execute('SELECT id FROM responses WHERE qclass = 1 AND qtype = 6 AND name = ?', (base_name,)))
            c.execute('UPDATE responses SET ttl = ttl + 1 WHERE id = ?', (row['id'],))

    @classmethod
    def delete_one(cls, name):
        records = list(cls.get_records_by_type_and_name(name))
        if len(records) > 1:
            raise ValueError("Can only use delete_one to delete a unique record")
        if records:
            with cursor() as c:
                c.execute('DELETE FROM responses where id = ?', (records[0]['id'],))
            return True
        return False

class A(DNSResource):

    qtype = 1

    @classmethod
    def update(cls, name, address, ttl=DEFAULT_TTL):
        rdata = dns.A(address)
        cls.insert_or_update(name, ttl, rdata)
        cls.increment_serial(name)

class SOA(DNSResource):

    qtype = 6

    @classmethod
    def create(cls, name, mname, rname, refresh, retry, expire, minimum, ttl=DEFAULT_TTL, serial=1):
        if name != cls.to_base_name(name):
            raise ValueError("Cannot create an SOA record for a non-TLD")
        rdata = dns.SOA(mname, rname, serial, refresh, retry, expire, minimum).as_buffer()
        cls.check_record_uniqueness(name)
        cls.insert_record(name, ttl, rdata)

__all__ = ['just_one', 'maybe_one', 'read_txn', 'write_txn', 'A', 'SOA']
