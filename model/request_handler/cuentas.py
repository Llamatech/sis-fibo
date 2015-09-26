import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import cuenta
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

    @tornado.gen.coroutine
    def get(self):
        cookie = self.get_cookie("authcookie")
        if not cookie:
            self.redirect('/login')
        else:
            values = cookie.split('-')
            id = int(values[0])
            tipo = values[1].replace('_', ' ')
            if tipo != 'Administrador':
                if tipo != 'Gerente Oficina':
                    self.render('../../static/listaCuentas.html', role='ggeneral')
                else:
                    self.render('../../static/listaCuentas.html', role='goficina')
            else:
                self.set_status(403)

    @tornado.gen.coroutine
    def post(self):
        cookie = self.get_cookie("authcookie")
        if not cookie:
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
            exists_since = self.get_body_argument("creacionStart")
            exists_upto = self.get_body_argument("creacionStop")
            last_movement_from = self.get_body_argument("uMovStart")
            last_movement_upto = self.get_body_argument("uMovStop")
            sum_from = self.get_body_argument("saldoFrom")
            sum_upto = self.get_body_argument("saldoTo")
            values = cookie.split('-')

            exists_since = from_timestamp(exists_since)
            exists_upto = from_timestamp(exists_upto)
            last_movement_from = from_timestamp(last_movement_from)
            last_movement_upto = from_timestamp(last_movement_upto)

            if sum_from != '':
                sum_from = float(sum_from)
            else:
                sum_from = None

            if sum_upto != '':
                sum_upto = float(sum_upto)
            else:
                sum_upto = None

            params = {'client':False, 'account':False, 
                      'existance':[exists_since, exists_upto],
                      'last_movement':[last_movement_from, last_movement_upto],
                      'sum':[sum_from, sum_upto],
                      'search_term':search_term}
            if searching_by == 1:
                params['client'] = True
            elif searching_by == 2:
                params['account'] = True


            _id = int(values[0])
            tipo = values[1].replace('_', ' ')
            inst = bancandes.BancAndes.dar_instancia()
            inst.inicializar_ruta('data/connection')
            perm = {'ggeneral':False, 'goficina':False, 'cliente':False}
            if tipo == 'Gerente General':
                perm['ggeneral'] = True 
            elif tipo == 'Gerente Oficina':
                perm['goficina'] = True
            elif tipo == 'Cliente Natural' or tipo == 'Cliente Juridico':
                perm['cliente'] = True

            search_count, count, cuentas = inst.obtener_cuentasL(col_name, order, start, start+length, perm, params, _id)
            cuentas = map(lambda x: x.dict_repr(), cuentas)

            data = {"draw": draw,
                    "recordsTotal": count,
                    "recordsFiltered": search_count,
                    'data':cuentas}
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))

    @tornado.gen.coroutine
    def delete(self):
        cookie = self.get_cookie("authcookie")
        if not cookie:
            self.set_status(403)
        else:
            _id = int(values[0])
            tipo = values[1].replace('_', ' ')
            if tipo != 'Gerente Oficina':
                self.set_status(403)
            else:
                numero = int(self.get_argument('numero', None))
                inst = bancandes.BancAndes.dar_instancia()
                inst.inicializar_ruta('data/connection')
                inst.cerrar_cuenta(numero)