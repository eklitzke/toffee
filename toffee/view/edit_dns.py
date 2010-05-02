import re
import logging

from toffee.view import RequestHandler
from toffee import named

class DNSEditor(RequestHandler):

    def normalize_name(self, name):
        while name and name[-1] == '.':
            name = name[:-1]
        name += '.'
        return named.DNSResource.to_base_name(name)

    def group_records(self, records):
        result = { 'soa': None, 'a': []}
        for record in records:
            if record.qtype == named.A.qtype:
                result['a'].append(record)
            elif record.qtype == named.SOA.qtype:
                result['soa'] = record
        return result

    def get(self, name):
        base_name = self.normalize_name(name)
        if name != base_name[:-1]:
            self.redirect('/edit/' + base_name[:-1])
        records = named.fetch_records_for_base_name(base_name)
        self.env['records'] = self.group_records(records)
        self.render('home.html')

DNSEditor.add_route('/edit/([\w.]+)')
