import re
import logging

from toffee.view import RequestHandler
import toffee.db
from toffee.db import NoSuchEmail

class Login(RequestHandler):

    def post(self):
        if self.current_user:
            self.redirect('/')
            return
        email = self.get_argument('email')
        password = self.get_argument('password')
        if not (email or password):
            self.redirect('/')
            return

        try:
            user = toffee.db.Users.get_by_email_password(email, password)
        except NoSuchEmail:
            print 'no such email'
            self.redirect('/login')
            return
        print 'user = %s' % (user,)
        self.redirect('/login')

    def get(self):
        if self.current_user:
            self.redirect('/')
            return
        self.render('login.html')

Login.add_route('/login')
