# -*- coding: iso-8859-15 -*-

import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import cuenta
from model.fachada import bancandes

class RegistroHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        self.inst = bancandes.BancAndes.dar_instancia()
        self.inst.inicializar_ruta('data/connection')
        cookie = self.get_cookie("authcookie")
        if cookie:
            values = cookie.split("-")
            self.id = int(values[0])
            self.tipo = values[1].replace('_', ' ')
            if self.tipo == r'Cliente Juridico':
                self.auth = True
            else:
                self.auth = False
        else:
            self.auth = False

    @tornado.gen.coroutine
    def get(self):
        if self.auth:
            accounts = self.inst.obtener_cuentas(self.id, True)
            tipos = self.inst.obtener_frecuencia_nomina()
            self.render('../../static/registrarNomina.html', accounts=accounts, frecuencia=tipos)
        else:
            self.redirect('/')

    @tornado.gen.coroutine
    def post(self):
        if self.auth:
            cuenta = int(self.get_body_argument("cuenta"))
            cuenta_empl = int(self.get_body_argument("cuenta_empl"))
            salario = float(self.get_body_argument("salario"))
            frecuencia = int(self.get_body_argument("frec"))
            succ, code, msg = self.inst.actualizar_nomina(cuenta, cuenta_empl, salario, frecuencia)
            data = {'succ':succ, 'code':code, 'msg':msg}
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))
        else:
            self.set_status(403)

