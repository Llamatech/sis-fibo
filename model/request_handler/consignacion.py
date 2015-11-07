# -*- coding: iso-8859-15 -*-

import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import operacion
from model.fachada import bancandes

def from_timestamp(date):
    if date != '':
        date = map(int, date.split('/'))
        return datetime.date(date[2], date[1], date[0])
    else:
        return None

class ListHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        self.inst = bancandes.BancAndes.dar_instancia()
        self.inst.inicializar_ruta('data/connection')
        cookie = self.get_cookie("authcookie")
        if cookie:
            values = cookie.split("-")
            self.id = int(values[0])
            self.tipo = values[1].replace('_', ' ')
            if self.tipo != r'Administrador':
                self.auth = True
            else:
                self.auth = False
        else:
            self.auth = False

    @tornado.gen.coroutine
    def get(self):
        if not self.auth:
            self.redirect('/login')
        else:
            if self.tipo != 'Administrador':
                tipos = self.inst.obtener_tipo_prestamo()
                self.render('../../static/listaConsignaciones.html', tipos = tipos)
            else:
                self.set_status(403)
                self.write("No dispone con permisos suficientes para acceder a esta funcionalidad")

    @tornado.gen.coroutine
    def post(self):
        if not self.auth:
            self.set_status(403)
        else:
            draw = int(self.get_body_argument("draw"))
            start = int(self.get_body_argument("start"))
            length = int(self.get_body_argument("length"))
            order = self.get_body_argument("order[0][dir]")
            ind_column = self.get_body_argument("order[0][column]")
            col_name = self.get_body_argument("columns["+ind_column+"][data]")
            searching_by = int(self.get_body_argument("test"))
            search_term = self.get_body_argument("search[value]")
            pre_type = int(self.get_body_argument("tPrestamo"))
            sum_from = self.get_body_argument("saldoFrom")
            sum_upto = self.get_body_argument("saldoTo")


            if sum_from != '':
                sum_from = float(sum_from)
            else:
                sum_from = None

            if sum_upto != '':
                sum_upto = float(sum_upto)
            else:
                sum_upto = None

            params = {'client':False, 'account':False, 
                      'pre_type':pre_type,
                      'sum':[sum_from, sum_upto],
                      'search_term':search_term}\

            search_count, count, cuentas = self.inst.obtener_operacionP(col_name, order, start, start+length, perm, params, self.id)
            cuentas = map(lambda x: x.dict_repr(), cuentas)

            data = {"draw": draw,
                    "recordsTotal": count,
                    "recordsFiltered": search_count,
                    'data':cuentas}
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))

