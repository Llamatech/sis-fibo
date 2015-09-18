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
        tipos = inst.obtener_tipo_documento()
        print len(tipos)
        tipo_usuario = inst.obtener_tipo_usuario()
        print len(tipo_usuario)
        #self.render('template.html', a=a, b=b)
        self.render('../../static/registrarUsuario.html', roles=tipo_usuario, tipos=tipos)

    @tornado.gen.coroutine
    def post(self):
        data = self.get_argument('data', 'No data recieved')

    def write_error(self, status_code, **kwargs):
        self.write("An error has ocurred")

