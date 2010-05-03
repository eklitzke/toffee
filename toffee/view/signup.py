import re
import logging

import toffee.db
from toffee.view import RequestHandler

class Signup(RequestHandler):

    def post(self):
        if self.current_user:
            self.redirect('/')

        email = self.get_argument('email')
        if not email:
            self.error_msg = 'Missing email'
            self.redirect('/login')
            return
        password = self.get_argument('password')
        if not password:
            self.error_msg = 'Missing password'
            self.redirect('/login')
            return
        password_confirm = self.get_argument('password_confirm')
        if not password_confirm:
            self.error_msg = 'Missing password confirmation'
            self.redirect('/login')
            return

        if password != password_confirm:
            self.error_msg = 'Passwords did not match'
            self.redirect('/login')
            return

        user = toffee.db.Users.new(email, password)
        cookie_text = '%s %d' % (self.request.remote_ip, user.id)
        self.set_secure_cookie('user', cookie_text)
        self.redirect('/')

    def get(self):
        self.redirect('/login')

Signup.add_route('/signup')
