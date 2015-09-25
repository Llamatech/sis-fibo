import os
import sys
import tornado.web
import datetime
from tornado import gen
from model.vos import operacion
from model.fachada import bancandes 

class RegistroHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        self.es_cajero = inst.es_cajero(self.get_cookie("authcookie").split('-')[0])
        self.cuentas = inst.obtener_cuentas(self.get_cookie("authcookie").split('-')[0])

    @tornado.gen.coroutine
    def get(self):
    	# a = range(0, 5)
        # b = {2:4, 5:7}
        
        #self.render('template.html', a=a, b=b)
       
        if self.es_cajero:
            self.render('../../static/registrarOperacionCuentaCajero.html')
        else:
            self.render('../../static/registrarOperacionCuenta2.html', cuentas=self.cuentas)

    @tornado.gen.coroutine
    def post(self):
        numeroCuenta = self.get_body_argument("cuenta")
        tipoOperacion = self.get_body_argument("cambiar")
        id='0'
        monto = '0'
        if tipoOperacion == 'consignar':
            id='3'
            monto = self.get_body_argument("montoCons")
        elif tipoOperacion == 'retirar':
            id='4'
            monto = self.get_body_argument("montoRet")


        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        numero = inst.generar_numero_operacion()
        idPuntoAtencion = inst.get_id_pa(self.get_cookie("authcookie").split('-')[0])
        if idPuntoAtencion == -1:
            idPuntoAtencion = '3'
        cliente='0'
        cajero = 'NULL'
        if self.es_cajero:
            cliente = inst.duenio_cuenta(numeroCuenta)
            cajero = self.get_cookie("authcookie").split('-')[0]
            print("es cajero")
        else:
            cliente = self.get_cookie("authcookie").split('-')[0]
            print("no es cajero")
            #(self, numero, tipo_operacion, cliente, valor, punto_atencion, cajero, cuenta, fecha)
        oper = operacion.Operacion(numero,id,cliente,monto,idPuntoAtencion, cajero, numeroCuenta, datetime.datetime.today())
        print(oper)
        exists = inst.registrar_operacion_cuenta(oper)
        if not exists:
            if self.es_cajero:
                self.render('../../static/registrarOperacionCuentaCajeroError.html')
            else:
                self.render('../../static/registrarOperacionCuentaError.html', cuentas=self.cuentas)
        else:
        	self.render('../../static/transaccionExitosa.html')
