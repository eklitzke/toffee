import datetime
import tornado.web
routes = []

class RequestHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(RequestHandler, self).prepare()
        self.env = {}
        self.env['today'] = datetime.date.today()
    
    def render(self, template_name, **kwargs):
        self.env.update(kwargs)
        return super(RequestHandler, self).render(template_name, **self.env)

    @classmethod
    def add_route(cls, regex):
        routes.append((regex, cls))

import toffee.view.static_page
