import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import oficina
from model.fachada import bancandes
from model.vos import puntos_atencion
from model.fachada import bancandesAdmin 

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
        self.render('../../static/listaPuntosAtencion.html')

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
        count,empl = inst.obtener_puntos_atL(col_name, order, start, start+length)
        empl = map(lambda x: x.dict_repr(), empl)

        data = {"draw": draw,
                "recordsTotal": count,
                "recordsFiltered": count,
                'data':empl}
        self.set_header('Content-Type', 'text/javascript')
        self.write(tornado.escape.json_encode(data))
        # print "Not working..."

    @tornado.gen.coroutine
    def put(self):
        search_term = self.get_body_argument("term")
        if self.tipo == 'Gerente General':
            pa = self.inst.obtener_puntos_at(search_term)
            pa = map(lambda x : x.dict_repr(), pa)
            for x in pa:
                x['delete'] = None
            self.set_header('Content-Type', 'text/javascript')
            self.write(tornado.escape.json_encode(pa)) 
        else:
            self.set_status(403)    
        # print search_term
        # inst = bancandesAdmin.BancAndesAdmin.dar_instancia()
        # inst.inicializar_ruta('data/connection')
        # g_oficina = inst.obtener_gerentes_oficinaC(search_term)
        # g_oficina = map(lambda x: x.dict_repr(), g_oficina)
        # self.set_header('Content-Type', 'text/javascript')
        # self.write(tornado.escape.json_encode(g_oficina))