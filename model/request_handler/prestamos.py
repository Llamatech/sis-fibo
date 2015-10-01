import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import prestamo
from model.fachada import bancandes

class ListHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        self.inst = bancandes.BancAndes.dar_instancia()
        self.inst.inicializar_ruta('data/connection')
        cookie = self.get_cookie("authcookie")
        if cookie:
            values = cookie.split("-")
            self.id = int(values[0])
            self.tipo = values[1].replace('_', ' ')
            if self.tipo == 'Gerente Oficina':
                self.auth = True
                self.oficina = self.inst.get_id_oficina(self.id)
            else:
                self.auth = False
        else:
            self.auth = False


    @tornado.gen.coroutine
    def get(self):
        if self.auth:
            self.render('../../static/cerrarPrestamo.html')
        else:
            self.set_status(403)
            self.write("No dispone con permisos suficientes para acceder a esta funcionalidad")

    @tornado.gen.coroutine
    def put(self):
        if self.auth:
            search_term = self.get_body_argument("term")
            data = self.inst.obtener_prestamos(self.oficina, search_term)
            data = map(lambda x: x.dict_repr(), data)
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))
        else:
            self.set_status(403)

    @tornado.gen.coroutine
    def delete(self):
        if self.auth:
            _id = int(self.get_body_argument("id"))
            self.inst.cerrar_prestamo(_id)
        else:
            self.set_status(403)            