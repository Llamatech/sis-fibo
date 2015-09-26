import os
import sys
import tornado.web
from tornado import gen
from model.vos import prestamo
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
        tipos_pa = inst.obtener_tipo_prestamo()
        #self.render('template.html', a=a, b=b)
        self.render('../../static/registrarPrestamo.html', tipos=tipos_pa)
        self.redirect('/')

    @tornado.gen.coroutine
    def post(self):
        tipo = int(self.get_body_argument("pre_type"))
        id_cliente = int(self.get_body_argument("cliente"))
        interes = float(self.get_body_argument("rate"))
        monto = float(self.get_body_argument("value"))
        due = self.get_body_argument("due")
        num_cuotas = self.get_body_argument("num_pay")
        valor_cuota = float(self.get_body_argument("valor_cuota"))
        tipo_doc = int(self.get_body_argument("doc_type"))
        doc_num = self.get_body_argument("doc_num")
        _dir = self.get_body_argument("dir")
        tel = self.get_body_argument("tel")
        b_date = self.get_body_argument("b_date")
        city = self.get_body_argument("city")
        cod_postal = self.get_body_argument("cod_postal")


        cookie = self.get_cookie("authcookie")
        values = cookie.split("-")
        _id = int(values[0])
        tipoO = values[1].replace('_', ' ')

        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')

        id_oficina = get_id_oficina(_id)

        _prestamo = prestamo.Prestamo(None, interes, monto, due, num_cuotas, valor_cuota, tipo, id_cliente, _id)
        inst.registrar_prestamo(_prestamo)
        self.redirect('/registrar/prestamo')


        # exists = inst.registrar_cuenta(tipo, idCliente, idOficina, saldo)
        # if not exists:
        #     self.render('../../static/registrarOficinaError.html')
        # else:
        # 	self.render('../../static/transaccionExitosa.html')