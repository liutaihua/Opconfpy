#coding=utf8

#system modules:
import sys
import os

#tornado modules:
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import options

import common.session
import config.web_config
import config.db_config

#controllers:
from common.base_httphandler import BaseHandler
from common.base_httphandler import ProxyHandler

from controller.confpy import ListmodulesHandler
from controller.confpy import Listmod_configsHandler
from controller.confpy import Listmod_serversHandler, Listmod_conf_serversHandler, ReadModConfHandler

class MainHandler(BaseHandler):
    def get(self):
        self.render('index.html')
class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

settings = dict(
                cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                debug=True,
                session_secret='some secret password!!',
                session_dir='sessions',
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=False,
            )

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
           
            (r'/gifonc/modules.json', ListmodulesHandler),
            (r'/gifonc/(.*)/confs.json', Listmod_configsHandler),
            (r'/gifonc/(.*)/servers.json', Listmod_serversHandler),
            (r'/gifonc/(.*)/(.*)/cservers.json', Listmod_conf_serversHandler),
            (r'/gifonc/(.*)/(.*)/(.*).json', ReadModConfHandler),
            ]
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = common.session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])
        self.db = tornado.database.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)


def main(port):
    tornado.options.parse_command_line()
    print "start on port %s..."%port

    app = Application()
    app.listen(port)
    if True:
        application = tornado.ioloop.IOLoop.instance()
        tornado.autoreload.start(application)
        application.start()
    else:
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = tornado.options.options.port
    main(int(port))
