import socket
import cStringIO as StringIO

import dns.name
import dns.rdtypes.ANY.SOA
import dns.rdtypes.IN.A

class ResourceRecord(object):

    rdclass = 1

    @classmethod
    def to_dns_name(cls, name):
        return dns.name.Name(name.split('.'))

    @classmethod
    def inet_aton(addr, as_buffer=False):
        return to_buffer(socket.inet_aton(addr), as_buffer)

    def as_buffer(self):
        buf = StringIO.StringIO()
        self.dns.to_wire(buf)
        return buffer(buf.getvalue())

    def validate(self):
        return self.dns.validate()

class A(ResourceRecord):

    rdtype = 1

    def __init__(self, address):
        self.dns = dns.rdtypes.IN.A.A(self.rdclass, self.rdtype, address)
        self.validate()

class SOA(ResourceRecord):

    rdtype = 6

    def __init__(self, mname, rname, serial, refresh, retry, expire, minimum):
        mname = self.to_dns_name(mname)
        rname = self.to_dns_name(rname)
        self.dns = dns.rdtypes.ANY.SOA.SOA(self.rdclass, self.rdtype, mname, rname, serial, refresh, retry, expire, minimum)
        self.validate()

__all__ = ['A', 'SOA']
