#-*-encoding=utf-8-*-

import tornado.ioloop
import tornado.options
import tornado.httpserver
from jyall_cloud.application import AppCloud

from tornado.options import define,options
define("port",default=8891,help="run on th given port",type=int)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(AppCloud())
    http_server.listen(options.port)
    print 'Development server is running at http://127.0.0.1:%s/' % options.port
    print 'Quit the server with Control-C'
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()