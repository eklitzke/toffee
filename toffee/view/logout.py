import re
import logging

import toffee.db
from toffee.view import RequestHandler

class Logout(RequestHandler):

    def get(self):
        if self.current_user:
            self.clear_cookie('user')
        self.redirect('/')

Logout.add_route('/logout')
