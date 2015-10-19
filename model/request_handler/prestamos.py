import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import prestamo
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
            if self.tipo == 'Gerente Oficina':
                self.auth = True
                self.oficina = self.inst.get_id_oficina(self.id)
            else:
                self.auth = False
        else:          
            self.auth = False


    @tornado.gen.coroutine
    def get(self):
        if self.auth:
            self.render('../../static/cerrarPrestamo.html')
        else:
            self.set_status(403)
            self.write("No dispone con permisos suficientes para acceder a esta funcionalidad")

    @tornado.gen.coroutine
    def put(self):
        if self.auth:
            search_term = self.get_body_argument("term")
            data = self.inst.obtener_prestamos(self.oficina, search_term)
            data = map(lambda x: x.dict_repr(), data)
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(data))
        else:
            self.set_status(403)

    @tornado.gen.coroutine
    def delete(self):
        if self.auth:
            _id = int(self.get_body_argument("id"))
            self.inst.cerrar_prestamo(_id)
        else:
            self.set_status(403)

    @tornado.gen.coroutine
    def post(self):
        draw = int(self.get_body_argument("draw"))
        start = int(self.get_body_argument("start"))
        length = int(self.get_body_argument("length"))
        order = self.get_body_argument("order[0][dir]")
        ind_column = self.get_body_argument("order[0][column]")
        col_name = self.get_body_argument("columns["+ind_column+"][data]")
        searching_by = int(self.get_body_argument("test"))
        search_term = self.get_body_argument("search[value]")

        app_from = self.get_body_argument("creacionStart")
        app_to = self.get_body_argument("creacionStop")
        last_movement_from = self.get_body_argument("uMovStart")
        last_movement_upto = self.get_body_argument("uMovStop")
        sum_from = self.get_body_argument("saldoFrom")
        sum_upto = self.get_body_argument("saldoTo")

        last_movement_from = from_timestamp(last_movement_from)
        last_movement_upto = from_timestamp(last_movement_upto)

        app_to = from_timestamp(app_to)
        app_from = from_timestamp(app_from)

        if sum_from != '':
            sum_from = float(sum_from)
        else:
            sum_from = None

        if sum_upto != '':
            sum_upto = float(sum_upto)
        else:
            sum_upto = None

        params = {'client':False, 'loan':False,
                  'app_date':[app_from, app_to], 
                  'last_movement':[last_movement_from, last_movement_upto],
                  'sum':[sum_from, sum_upto],
                  'search_term':search_term}
        if searching_by == 1:
            params['client'] = True
        elif searching_by == 2:
            params['loan'] = True

        




class NotClosedHandler(tornado.web.RequestHandler):
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

    def post(self):
        if self.auth:
            search_term = self.get_body_argument("term")
            acc = self.inst.obtener_prestamos_NC(search_term)
            acc = map(lambda x: x.dict_repr(), acc)
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(acc))
        else:
            self.set_status(403)

