import os
import sys
import cx_Oracle
import numpy as np
import tornado.web
import tornado.ioloop
from tornado import gen
import tornado.platform.twisted
tornado.platform.twisted.install()
from toradbapi import ConnectionPool
from twisted.internet import reactor

URL = 'fn3.oracle.virtual.uniandes.edu.co'
PORT = 1521
SERV = 'prod'
USER = 'ISIS2304221520'
PWD = 'Xg6YCgZ8wJ3R'
DSN = URL+'/'+SERV

dsn_tns = cx_Oracle.makedsn(URL, PORT, SERV)
#dbpool = ConnectionPool('cx_Oracle', user = USER, password = PWD, dsn = dsn_tns)


def setup_database():
    # just to ensure that database and table exist
    cnx = cx_Oracle.connect(USER, PWD, dsn_tns)
    cursor = cnx.cursor()
    try:
        cursor.execute('SELECT * FROM PARRANDEROS.BEBIDAS')
        print cursor.fetchall()
    except Exception:
        # do nothing if database exists
        pass
    cursor.close()
    cnx.close()


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        iter_cols = yield self.db.run_query("SELECT COLUMN_NAME FROM ALL_TAB_COLS WHERE OWNER = 'PARRANDEROS' AND TABLE_NAME='BARES' AND HIDDEN_COLUMN='NO'")
        cols = [col for col in iter_cols]
#        print cols
        order = ''.join([i[0]+',' for i in cols])[0:-1]
        order = 'SELECT '+order+" FROM PARRANDEROS.BARES"
        iter_order = yield self.db.run_query(order)
        values = [i for i in iter_order]
        values = [[col[0] for col in cols]]+values
        self.render('template.html', title=order, values=values)

class TemplateHandler(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db

    @tornado.gen.coroutine
    def get(self):
        self.render('static/index.html')       

if __name__ == "__main__":
#    setup_database()
    pool = ConnectionPool('cx_Oracle', user = USER, password = PWD, dsn = dsn_tns)
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        # "login_url": "/login",
        # "xsrf_cookies": True,
    }  
    application = tornado.web.Application([
        (r"/", MainHandler, {'db':pool}),
        (r"/template", TemplateHandler, {'db':pool})
    ], debug=True, serve_traceback=True, autoreload=True, **settings)
    application.listen(8000)
    #tornado.ioloop.IOLoop.current().start()
    try:
      tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
      pass
    finally:
      pool.close()
      tornado.ioloop.IOLoop.instance().stop()
