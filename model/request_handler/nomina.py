# -*- coding: iso-8859-15 -*-

import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import cuenta
from model.fachada import bancandes

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        self.inst = bancandes.BancAndes.dar_instancia()
        self.inst.inicializar_ruta('data/connection')
        cookie = self.get_cookie("authcookie")
        if cookie:
            values = cookie.split("-")
            self.id = int(values[0])
            self.tipo = values[1].replace('_', ' ')
            if self.tipo == r'Cliente Jurídico':
                self.auth = True
            else:
                self.auth = False
        else:
            self.auth = False

    @tornado.gen.coroutine
    def get(self):
        if self.auth:
            self.render('../../static/pagoNomina.html')
        else:
            self.redirect('/')


class MigrationHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        self.inst = bancandes.BancAndes.dar_instancia()
        self.inst.inicializar_ruta('data/connection')
        cookie = self.get_cookie("authcookie")
        if cookie:
            values = cookie.split("-")
            self.id = int(values[0])
            self.tipo = values[1].replace('_', ' ')
            if self.tipo == r'Gerente Oficina':
                self.auth = True
            else:
                self.auth = False
        else:
            self.auth = False

    @tornado.gen.coroutine
    def post(self):
        if self.auth:
            acc_number = int(self.get_argument('numero', None))
            has = self.inst.cuenta_nomina(acc_number)
            data = {'has':has}
            if has:
                 acc = self.inst.obtener_cuentas(self.inst.duenio_cuenta(str(acc_number)), True, False)
                 acc = [{'numero':a.numero} for a in acc if a.numero != acc_number]
                 data['acc'] = acc
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))
        else:
            self.set_status_code(403)

    @tornado.gen.coroutine
    def put(self):
        if self.auth:
            acc_number_from = int(self.get_argument('numero', None))
            acc_number_to = int(self.get_body_argument('numero_acc', None))
            succ, code = self.inst.migrar_nomina(acc_number_from, acc_number_to)
            data = {'succ':succ, 'code':code}
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))
        else:
            self.set_status_code(403)

