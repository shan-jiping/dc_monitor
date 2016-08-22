# coding=utf-8

import os
from tornado.web import Application
from jyall_cloud.urllist import urls

class AppCloud(Application):
    def __init__(self):
        handlers = urls
        
        settings = dict(
            title = u"金色家园,云家园",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
           # ui_modules={"Entry": EntryModule},
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="~/auth/login",
            debug=True,
            )

        super(AppCloud,self).__init__(handlers,**settings)

