import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import usuario
from model.vos import empleado
from model.fachada import bancandes 

class ListHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def put(self):
        cookie = self.get_cookie("authcookie")
        if not cookie:
            self.set_status(403)
        else:
            values = cookie.split("-")
            _id = int(values[0])
            tipo = values[1].replace('_', ' ')
            if tipo != 'Gerente Oficina':
                self.set_status(403)
            else:
                search_term = self.get_body_argument("term")
                # print search_term
                inst = bancandes.BancAndes.dar_instancia()
                inst.inicializar_ruta('data/connection')
                clientes = inst.obtener_clientes(search_term)
                clientes = map(lambda x: x.dict_repr(), clientes)
                self.set_header('Content-Type', 'text/javascript')
                self.write(tornado.escape.json_encode(clientes))