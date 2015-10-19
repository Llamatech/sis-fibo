import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import oficina
from model.vos import puntos_atencion
from model.fachada import bancandesAdmin 

class EditionHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
        _id = int(self.get_argument('id', None))
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        tipos_pa = inst.obtener_tipo_pa()
        pa = inst.obtener_pa(_id)
        for i,tipo in enumerate(tipos_pa):
            if tipo.tipo == pa.tipo_pa:
                tipos_pa[0], tipos_pa[i] = tipos_pa[i], tipos_pa[0]
        self.render('../../static/informacionPuntoAtencion.html', tipos=tipos_pa, pa = pa)

    @tornado.gen.coroutine
    def delete(self):
        _id = int(self.get_argument('id', None))
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        inst.eliminar_pa(_id)

    @tornado.gen.coroutine
    def post(self):
        _id = int(self.get_argument('id', None))
        tipo = int(self.get_body_argument("tipo"))
        localizacion = self.get_body_argument("localizacion")
        oficina = int(self.get_body_argument("oficina"))

        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        inst.actualizar_pa(_id, localizacion, tipo, oficina)
        self.redirect('/puntosAtencion')