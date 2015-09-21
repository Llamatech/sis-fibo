import os
import sys
import tornado.web
from tornado import gen
from model.fachada import bancandes 

class RegistroHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
    	# a = range(0, 5)
        # b = {2:4, 5:7}
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        tipos_cuenta = inst.obtener_tipo_cuenta()
        print len(tipos_cuenta)
        #self.render('template.html', a=a, b=b)
        self.render('../../static/registrarCuenta.html', tipos=tipos_cuenta)

    @tornado.gen.coroutine
    def post(self):
        name = self.get_body_argument("nombre")
        address = self.get_body_argument("direccion")
        phone = self.get_body_argument("telefono")
        idGerente = self.get_body_argument("gerente")
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        esGerente = inst.registrarOficina(name, phone, address, email)
        if not exists:
            self.render('../../static/registrarOficinaError.html')
        else:
        	self.render('../../static/transaccionExitosa.html')
