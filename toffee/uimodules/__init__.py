import tornado.web

all_uimodules = {}

class UIModule(tornado.web.UIModule):

    @classmethod
    def register(cls):
        all_uimodules[cls.__name__] = cls

import toffee.uimodules.dns_record
