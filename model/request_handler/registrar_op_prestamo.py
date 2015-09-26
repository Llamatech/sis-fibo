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
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        numeroPrestamo = self.get_body_argument("prestamo")
        tipoOperacion = self.get_body_argument("cambiar")
        existe = inst.existe_prestamo(numeroPrestamo)
        if not existe:
            self.render('../../static/prestamoNoExiste.html')
            return
        monto=0
        if tipoOperacion == '8':
            monto=inst.get_monto_prestamo(numeroPrestamo)
        else:
            monto=self.get_body_argument("monto")
  
        numero = inst.generar_numero_operacion()
        idPuntoAtencion = inst.get_id_pa(self.get_cookie("authcookie").split('-')[0])
        if idPuntoAtencion == -1:
            idPuntoAtencion = '3'
        cliente = inst.duenio_prestamo(numeroPrestamo)
        cajero = self.get_cookie("authcookie").split('-')[0]
        #(self, numero, tipo_operacion, cliente, valor, punto_atencion, cajero, cuenta, fecha)
        oper = operacion.Operacion(numero,tipoOperacion,cliente,monto,idPuntoAtencion, cajero, numeroPrestamo, datetime.date.today())
        print(oper)
        exists = inst.registrar_operacion_prestamo(oper)
        if not exists:
            self.render('../../static/registrarOperacionPrestamoError.html')
        else:
            self.render('../../static/transaccionExitosa.html')
