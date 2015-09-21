import os
import sys
import tornado.web
from tornado import gen
from model.fachada import bancandesAdmin 

class RegistroHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
    	self.render("../../static/registrarOficina.html")

    @tornado.gen.coroutine
    def post(self):
        name = self.get_body_argument("nombre")
        address = self.get_body_argument("direccion")
        phone = self.get_body_argument("telefono")
        idGerente = self.get_body_argument("gerente")
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        esGerente = inst.registrar_oficina(name, phone, address, idGerente)
        if not exists:
            self.render('../../static/registrarOficinaError.html')
        else:
        	self.render('../../static/transaccionExitosa.html')
