import os
import sys
import tornado.web
from tornado import gen
from model.vos import cliente
from model.vos import usuario
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
        tipos = inst.obtener_tipo_documentoR()
        # print len(tipos)
        tipo_usuario = inst.obtener_tipo_usuarioR()
        # print len(tipo_usuario)
        #self.render('template.html', a=a, b=b)
        self.render('../../static/registrarUsuario.html', tipos=tipo_usuario, docs=tipos)

    @tornado.gen.coroutine
    def post(self):
        tipo_cliente = self.get_body_argument('client_type', None)
        email = self.get_body_argument('email', None)
        pwd = self.get_body_argument('pwd', None)
        nombre = self.get_body_argument('name', None)
        apellido = self.get_body_argument('lastname', None)
        tipo_doc = self.get_body_argument('doc_type', None)
        num_doc = self.get_body_argument('doc_num', None)
        direccion = self.get_body_argument('dir', None)
        telefono = self.get_body_argument('tel', None)
        fecha_nacimiento = self.get_body_argument('b_date', None)
        ciudad = self.get_body_argument('city', None)
        departamento = self.get_body_argument('dep', None)
        cod_postal = self.get_body_argument('zip', None)

        valores_fecha = map(int, fecha_nacimiento.split('/'))
        fecha = datetime.date(valores_fecha[2], valores_fecha[1], valores_fecha[0])
        fecha_ins = datetime.date.today()

        _cliente = cliente.Cliente(None, tipo_doc, num_doc, nombre, apellido,
                    direccion, telefono, fecha_ins, fecha, ciudad, departamento,
                    cod_postal)
        _usuario = usuario.Usuario(48, pwd, email, int(tipo_empleado))
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        inst.registrar_cliente(_usuario, _cliente)
        self.redirect('/registrar/usuario')

    def write_error(self, status_code, **kwargs):
        self.write("An error has ocurred")

