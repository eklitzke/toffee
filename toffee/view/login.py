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
        if not email:
            self.error_msg = 'Missing email'
            self.redirect('/login')
            return
        if not password:
            self.error_msg = 'Missing password'
            self.redirect('/login')
            return

        try:
            user = toffee.db.Users.get_by_email_password(email, password)
        except NoSuchEmail:
            self.error_msg = 'No account registered with that email address'
            self.redirect('/login')
            return

        cookie_text = '%s %d' % (self.request.remote_ip, user.id)
        self.set_secure_cookie('user', cookie_text)
        self.redirect('/login')

    def get(self):
        if self.current_user:
            self.redirect('/')
            return
        self.render('login.html')

Login.add_route('/login')
