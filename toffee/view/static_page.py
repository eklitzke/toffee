from toffee.view import routes, RequestHandler

class StaticPage(RequestHandler):

    routes = {}

    @classmethod
    def add_route(cls, uri, template):
        cls.routes[uri] = template
        routes.append((uri, cls))

    def get(self):
        if self.request.uri in self.routes:
            self.render(self.routes[self.request.uri])
        else:
            raise HTTPError(404)
    
StaticPage.add_route('/', 'home.html')
StaticPage.add_route('/technical_details', 'technical_details.html')
