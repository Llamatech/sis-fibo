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

    @tornado.gen.coroutine
    def get(self):
        self.render('../../static/registrarOperacionPrestamo1.html')

    @tornado.gen.coroutine
    def post(self):
        numeroPrestamo = self.get_body_argument("prestamo")
        tipoOperacion = self.get_body_argument("cambiar")
        monto=0
        if tipoOperacion == '8':
            monto=inst.get_monto_prestamo(numeroPrestamo)
        else:
            monto=selg.get_body_argument("monto")


        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        numero = inst.generar_numero_operacion()
        idPuntoAtencion = inst.get_id_pa(self.get_cookie("authcookie").split('-')[0])
        if idPuntoAtencion == -1:
            idPuntoAtencion = '3'
        cliente = inst.duenio_prestamo(numeroPrestamo)
        cajero = self.get_cookie("authcookie").split('-')[0]
        #(self, numero, tipo_operacion, cliente, valor, punto_atencion, cajero, cuenta, fecha)
        oper = operacion.Operacion(numero,tipoOperacion,cliente,monto,idPuntoAtencion, cajero, numeroCuenta, datetime.datetime.today())
        print(oper)
        exists = inst.registrar_operacion_cuenta(oper)
        if not exists:
            if self.es_cajero:
                self.render('../../static/registrarOperacionCuentaCajeroError.html')
            else:
                self.render('../../static/registrarOperacionCuentaError.html', cuentas=self.cuentas)
        else:
            self.render('../../static/transaccionExitosa.html')
