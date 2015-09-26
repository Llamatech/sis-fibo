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
    	# a = range(0, 5)
        # b = {2:4, 5:7}
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        tipos_pa = inst.obtener_tipo_pa()
        #self.render('template.html', a=a, b=b)
        self.render('../../static/registrarPuntoAtencion.html', tipos=tipos_pa)
        self.redirect('/puntosAtencion')

    @tornado.gen.coroutine
    def post(self):
        tipo = int(self.get_body_argument("tipo"))
        localizacion = self.get_body_argument("localizacion")
        oficina = int(self.get_body_argument("oficina"))

        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        inst.registrar_pa(localizacion, tipo, oficina) 

        # exists = inst.registrar_cuenta(tipo, idCliente, idOficina, saldo)
        # if not exists:
        #     self.render('../../static/registrarOficinaError.html')
        # else:
        # 	self.render('../../static/transaccionExitosa.html')