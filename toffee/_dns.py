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

    @classmethod
    def from_wire(cls, data):
        return cls.dns_cls.from_wire(cls.rdclass, cls.rdtype, buffer(data), 0, len(data))

class A(ResourceRecord):

    rdtype = 1
    dns_cls = dns.rdtypes.IN.A.A
 
    def __init__(self, address):
        self.dns = self.dns_cls(self.rdclass, self.rdtype, address)
        self.validate()

class SOA(ResourceRecord):

    rdtype = 6
    dns_cls = dns.rdtypes.ANY.SOA.SOA

    def __init__(self, mname, rname, serial, refresh, retry, expire, minimum):
        mname = self.to_dns_name(mname)
        rname = self.to_dns_name(rname)
        self.dns = self.dns_cls(self.rdclass, self.rdtype, mname, rname, serial, refresh, retry, expire, minimum)
        self.validate()

    @classmethod
    def increment_serial(cls, data):
        """Increment the serial in an SOA record"""
        data = cls.from_wire(data)
        data.serial += 1
        buf = StringIO.StringIO()
        data.to_wire(buf)
        return buffer(buf.getvalue()), data.serial
