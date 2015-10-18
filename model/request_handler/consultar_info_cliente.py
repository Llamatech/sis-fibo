#-*- coding:iso-8859-1 -*-

import os
import sys
import datetime
import tornado.web
import tornado.escape
from tornado import gen
from model.vos import oficina
from model.fachada import bancandes

class ListHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        self.tipo = inst.obtener_tipo_de_usuario(self.get_cookie("authcookie").split('-')[0])

    @tornado.gen.coroutine
    def get(self):
        if self.tipo == 'Cliente Natural' or self.tipo == 'Cliente Jurídico':
            idUsuario = None
            cuentas = None
            inst = bancandes.BancAndes.dar_instancia()
            inst.inicializar_ruta('data/connection')
            idUsuario=self.get_cookie("authcookie").split('-')[0]
            cuentas=inst.obtener_cuentas(idUsuario)

            prestamos=inst.obtener_prestamos_cliente(idUsuario)
            oficinas=inst.obtener_oficinas(idUsuario)
            operaciones=inst.obtener_operaciones(idUsuario)
            nombre = inst.obtener_nombre_cliente(idUsuario)
            self.render('../../static/resultadosInfoClienteGGeneral.html', tipo=self.tipo,nombre=nombre,cuentas=cuentas,prestamos=prestamos,oficinas=oficinas,operaciones=operaciones)
        else:
            self.render('../../static/infoClienteEmpleado.html')


    @tornado.gen.coroutine
    def post(self):
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        idUsuario = None
        cuentas = None
        print ("tipo: "+self.tipo)
        if self.tipo == 'Cliente Natural' or self.tipo == 'Cliente Jurídico':
            idUsuario=self.get_cookie("authcookie").split('-')[0]
            
        else:
            idUsuario = int(self.get_body_argument("idCliente"))
            


        if self.tipo == 'Gerente Oficina':
            cuentas=inst.obtener_cuentas_oficina(idUsuario, inst.get_id_oficina(self.get_cookie("authcookie").split('-')[0]))
        else:
            cuentas=inst.obtener_cuentas(idUsuario)

        prestamos=inst.obtener_prestamos_cliente(idUsuario)
        oficinas=inst.obtener_oficinas(idUsuario)
        operaciones=inst.obtener_operaciones(idUsuario)
        tipo = inst.obtener_tipo_cliente(idUsuario)
        nombre=inst.obtener_nombre_cliente(idUsuario)
        print(cuentas)
        self.render('../../static/resultadosInfoClienteGGeneral.html', tipo=tipo,nombre=nombre,cuentas=cuentas,prestamos=prestamos,oficinas=oficinas,operaciones=operaciones)

