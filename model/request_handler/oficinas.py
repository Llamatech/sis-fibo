import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import oficina
from model.fachada import bancandesAdmin 

class ListHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
        # a = range(0, 5)
        # b = {2:4, 5:7}
        # inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        # inst.inicializar_ruta('data/connection')
        # tipos = inst.obtener_tipo_documento()
        # print len(tipos)
        # tipo_usuario = inst.obtener_tipo_usuario()
        # print len(tipo_usuario)
        # oficinas = inst.obtener_oficinas()
        # print oficinas[0]
        #self.render('template.html', a=a, b=b)
        self.render('../../static/listaOficinas.html')

    @tornado.gen.coroutine
    def post(self):
        draw = int(self.get_body_argument("draw"))
        start = int(self.get_body_argument("start"))+1
        length = int(self.get_body_argument("length"))
        order = self.get_body_argument("order[0][dir]")
        ind_column = self.get_body_argument("order[0][column]")
        col_name = self.get_body_argument("columns["+ind_column+"][data]")
        print start, length, order, ind_column, col_name

        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        count,offices = inst.obtener_oficinasL(col_name, order, start, start+length)
        offices = map(lambda x: x.dict_repr(), offices)
        print offices

        data = {"draw": draw,
                "recordsTotal": count,
                "recordsFiltered": count,
                'data':offices}
        self.set_header('Content-Type', 'text/javascript')
        self.write(tornado.escape.json_encode(data))
        # print "Not working..."

    @tornado.gen.coroutine
    def put(self):
        search_term = self.get_body_argument("term")
        inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        inst.inicializar_ruta('data/connection')
        offices = inst.obtener_oficinasC(search_term)
        offices = map(lambda x: x.dict_repr(), offices)
        self.set_header('Content-Type', 'text/javascript')
        self.write(tornado.escape.json_encode(offices))


    # def write_error(self, status_code, **kwargs):
    #     self.write("An error has ocurred")
