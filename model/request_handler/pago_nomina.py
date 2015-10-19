# -*- coding: iso-8859-15 -*-

import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import cuenta
from model.fachada import bancandes

class PagoHandler(tornado.web.RequestHandler):
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
                self.accounts = self.inst.obtener_cuentas(self.id, True)
                self.auth = True
            else:
                self.auth = False
        else:
            self.auth = False

    @tornado.gen.coroutine
    def get(self):
        if self.auth:
            
            self.render('../../static/pagoNomina.html', accounts=self.accounts)
        else:
            self.redirect('/')

    @tornado.gen.coroutine
    def post(self):
        if self.auth:
            cuenta = int(self.get_body_argument("cuenta"))
            exito= self.inst.pagar_nomina(cuenta)
            print exito
            if exito==True:
                self.render('../../static/transaccionExitosa.html')
            else:
                self.render('../../static/pagoNominaError.html',cuentas=exito,accounts=self.accounts)
        else:
            self.set_status(403)

