from toffee.view import RequestHandler
import toffee.db

class Dashboard(RequestHandler):

    def get(self):
        self.render('dashboard.html')

Dashboard.add_route('/dashboard')
