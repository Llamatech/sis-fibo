# -*- coding: iso-8859-15 -*-

import os
import sys
import tornado.web
import tornado.escape
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
           # print cookie
           #info = cookie.value
           values = cookie.split('-')
           id = int(values[0])
           tipo = values[1].replace('_', ' ')
           if tipo == 'Administrador':
                self.render('../../static/admin-menu.html')
           elif tipo == 'Gerente General':
                self.render('../../static/ggeneral-menu.html')
           elif tipo == 'Gerente Oficina':
                self.render('../../static/goficina_menu.html')
           elif tipo == 'Cajero':
                self.render('../../static/cajero-menu.html')
           elif tipo == 'Cliente Natural':
                inst = bancandes.BancAndes.dar_instancia()
                inst.inicializar_ruta('data/connection')
                notificaciones = inst.obtener_notificaciones_cliente(id)
                print notificaciones
                self.render('../../static/cliente-menu.html',notifications=notificaciones)
           elif tipo == 'Cliente Juridico':
                self.render('../../static/clientej-menu.html') 
           else:
                self.write('%d : %s' % (id, values[1]))



    @tornado.gen.coroutine
    def post(self):
        self.write("An error has ocurred")
        #data = self.get_argument('data', 'No data recieved')

    def write_error(self, status_code, **kwargs):
        self.write("An error has ocurred")