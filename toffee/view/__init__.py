import datetime
import tornado.web
import tornado.escape

routes = []

def safe_escape(s):
    if s is not None:
        return tornado.escape.url_escape(s)
    return None

def safe_unescape(s):
    if s is not None:
        return tornado.escape.url_unescape(s)
    return None

class RequestHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(RequestHandler, self).prepare()
        self.info_msg = None
        self.error_msg = None
        self.env = {}
        self.env['info_msg'] = safe_unescape(self.get_cookie('info_msg'))
        self.env['error_msg'] = safe_unescape(self.get_cookie('error_msg'))
        self.env['today'] = datetime.date.today()

    def update_info_cookies(self):
        if self.info_msg:
            self.set_cookie('info_msg', safe_escape(self.info_msg))
        elif self.env['info_msg']:
            self.clear_cookie('info_msg')

        if self.error_msg:
            self.set_cookie('error_msg', safe_escape(self.error_msg))
        elif self.env['error_msg']:
            self.clear_cookie('error_msg')

    def redirect(self, url, permanent=False):
        self.update_info_cookies()
        super(RequestHandler, self).redirect(url, permanent=permanent)
    
    def render(self, template_name, **kwargs):
        self.update_info_cookies()
        self.env.update(kwargs)
        return super(RequestHandler, self).render(template_name, **self.env)

    def get_current_user(self):
        """Get the currently logged in user."""

        cookie = self.get_secure_cookie('user')
        if not cookie:
            return

        print 'cookie: %r' % (cookie,)

        def clear_and_redirect():
            self.clear_cookie('user')
            self.redirect(self.request.uri, permanent=False)

        ip, user_id = cookie.split(' ', 1)

        # If the user's ip address has changed, clear the cookie and redirect to
        # the current page
        if ip != self.request.remote_ip:
            clear_and_redirect()
            return

        user = toffee.db.Users.get_by_id(user_id)
        if not user:
            clear_and_redirect()
            return
        return user

    def new_session(self, user):
        cookie_text = self.request.remote_ip + user.id
        self.set_secure_cookie('user', cookie_text)

    @classmethod
    def add_route(cls, regex):
        routes.append((regex, cls))

import toffee.view.edit_dns
import toffee.view.login
import toffee.view.logout
import toffee.view.signup
import toffee.view.static_page
