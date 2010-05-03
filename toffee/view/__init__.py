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

    def get_current_user(self):
        """Get the currently logged in user."""

        cookie = self.get_secure_cookie('user')
        if not cookie:
            return

        def clear_and_redirect():
            selc.clear_cookie('user')
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
import toffee.view.signup
import toffee.view.static_page
