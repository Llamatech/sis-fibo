import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import oficina
from model.vos import usuario
from model.vos import empleado
from model.fachada import bancandesAdmin 

class EditionHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
        _id = int(self.get_argument('id', None))
        # inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        # inst.inicializar_ruta('data/connection')
        # tipos = inst.obtener_tipo_documento()
        # tipo_usuario = inst.obtener_tipo_usuario()
        # oficinas = inst.obtener_oficinas()
        # _usuario = inst.buscar_usuario(_id)
        # empl = inst.buscar_empleado(_id)

        # for i, tipo in enumerate(tipos):
        #     if tipo.id == empl.tipo_doc:
        #         tipos[0], tipos[i] = tipos[i], tipos[0]
        #         break

        # if empl.oficina is not None:
        #     for i, _oficina in enumerate(oficinas):
        #         if empl.oficina == _oficina.id:
        #             oficinas[0], oficinas[i] = oficinas[i], oficinas[0]
        #             break
        # else:
        #     oficinas = [oficina.Oficina(None, "", None, None, None)]+oficinas

        # for i, tipo in enumerate(tipo_usuario):
        #     if tipo.id == _usuario.tipo:
        #        tipo_usuario[0], tipo_usuario[i] = tipo_usuario[i], tipo_usuario[0]
        #        break 

        # print empl.fecha_nac


        # self.render('../../static/informacionEmpleado.html', tipos=tipo_usuario, docs=tipos, offices=oficinas, usuario=_usuario, empl=empl)

    @tornado.gen.coroutine
    def delete(self):
        _id = int(self.get_argument('id', None))
        gerente = self.get_argument('gerente', None)
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        inst.eliminar_oficina(_id, gerente)

        # try:
        #     oficina = int(self.get_argument('oficina', None))
        # except ValueError:
        #     oficina = None
        # tipo_usuario = int(self.get_argument('tipo_u', None))
        # print _id, oficina, tipo_usuario
        # inst.eliminar_empleado(_id, tipo_usuario, oficina)

    @tornado.gen.coroutine
    def post(self):
        _id = int(self.get_argument('id', None))
        # tipo_empleado = self.get_body_argument('emp_type', None)
        # oficina = self.get_body_argument('office', None)
        # email = self.get_body_argument('email', None)
        # pwd = self.get_body_argument('pwd', None)
        # nombre = self.get_body_argument('name', None)
        # apellido = self.get_body_argument('lastname', None)
        # tipo_doc = self.get_body_argument('doc_type', None)
        # num_doc = self.get_body_argument('doc_num', None)
        # direccion = self.get_body_argument('dir', None)
        # telefono = self.get_body_argument('tel', None)
        # # fecha_nacimiento = self.get_body_argument('b_date', None)
        # ciudad = self.get_body_argument('city', None)
        # departamento = self.get_body_argument('dep', None)
        # cod_postal = self.get_body_argument('zip', None)

        # # valores_fecha = map(int, fecha_nacimiento.split('/'))
        # # fecha = datetime.date(valores_fecha[2], valores_fecha[1], valores_fecha[0])
        # _empleado = empleado.Empleado(_id, tipo_doc, num_doc, nombre, apellido,
        #             direccion, telefono, None, None, ciudad, departamento,
        #             cod_postal, int(oficina))
        # _usuario = usuario.Usuario(_id, pwd, None, int(tipo_empleado))

        # inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        # inst.inicializar_ruta('data/connection')

        # inst.actualizar_empleado(_usuario, _empleado)

        # self.redirect('/empleados')