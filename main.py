#!/usr/bin/env python

import os
import sys
import tornado.web
import tornado.ioloop
import model.request_handler as handlers


def main():
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}
    application = tornado.web.Application([(r"/", handlers.example.MainHandler)], debug=True, serve_traceback=True, autoreload=True, **settings)
    print "Server is now at: 127.0.0.1:8000"
    application.listen(8000)
    try:
      tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
      pass
    finally:
      print "Closing server..."
      tornado.ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    main()
