import os
import sys
import tornado.web
from tornado import gen
from model.fachada import bancandes 

class HomeHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
        cookie = self.get_cookie("authcookie")
        if not cookie:
           self.redirect('/login')
        else:
           info = cookie.value
           values = info.split(':')
           id = int(values[0])
           self.write('%d : %s' % (id, values[1]))



    @tornado.gen.coroutine
    def post(self):
        self.write("An error has ocurred")
        #data = self.get_argument('data', 'No data recieved')

    def write_error(self, status_code, **kwargs):
        self.write("An error has ocurred")