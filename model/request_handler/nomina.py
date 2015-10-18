# -*- coding: iso-8859-15 -*-

import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import cuenta
from model.fachada import bancandes

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        self.inst = bancandes.BancAndes.dar_instancia()
        self.inst.inicializar_ruta('data/connection')
        cookie = self.get_cookie("authcookie")
        if cookie:
            values = cookie.split("-")
            self.id = int(values[0])
            self.tipo = values[1].replace('_', ' ')
            if self.tipo == r'Cliente Jurídico':
                self.auth = True
            else:
                self.auth = False
        else:
            self.auth = False

    @tornado.gen.coroutine
    def get(self):
    	if self.auth:
    		self.render('../../static/pagoNomina.html')
    	else:
    		self.redirect('/')

