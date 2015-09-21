import os
import sys
import tornado.web
from tornado import gen
from model.fachada import bancandes 

class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
        self.render('../../static/iniciarSesion.html')

    @tornado.gen.coroutine
    def post(self):
        email = self.get_body_argument("email")
        pwd = self.get_body_argument("password")
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        exists, id, tipo = inst.verificar_usuario(email, pwd)
        if exists:
            self.set_cookie("authcookie", "%d-%s" % (id, str(tipo).replace(' ', '_')))
            self.redirect('/')
        else:
            self.render('../../static/iniciarSesionError.html')
        #data = self.get_argument('data', 'No data recieved')

    def write_error(self, status_code, **kwargs):
        self.write("An error has ocurred")

class LogoutHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
        self.set_cookie("authcookie", '')
        self.redirect('/')

    @tornado.gen.coroutine
    def post(self):
        data = self.get_argument('data', 'No data recieved')

    def write_error(self, status_code, **kwargs):
        self.write("An error has ocurred")
