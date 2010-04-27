from toffee.view import RequestHandler

class Home(RequestHandler):

    def get(self):
        self.render('home.html')

Home.add_route('/')
