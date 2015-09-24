import os
import sys
import tornado.web
from tornado import gen
from model.fachada import bancandes 

class RegistroHandler(tornado.web.RequestHandler):
    def initialize(self, some_attribute=None):
        self.some_attribute = some_attribute

    @tornado.gen.coroutine
    def get(self):
    	# a = range(0, 5)
        # b = {2:4, 5:7}
        inst = bancandes.BancAndes.dar_instancia()
        inst.inicializar_ruta('data/connection')
        cuentas = inst.obtener_cuentas(self.getCookie("authcookie").slpit('-')[0])
        print len(tipos_cuenta)
        #self.render('template.html', a=a, b=b)
        self.es_cajero = inst.es_cajero(self.getCookie("authcookie").slpit('-')[0])
        if self.es_cajero:
            self.render('../../static/registrarOperacionCuentaCajero.html', cuentas=cuentas)
        else:
            self.render('../../static/registrarOperacionCuenta2.html')

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
        idPuntoAtencion = inst.get_id_pa(self.getCookie("authcookie").split('-')[0])
        if idPuntoAtencion == -1:
            idPuntoAtencion = '4'
        cliente='0'
        cajero = 'NULL'
        if self.es_cajero:
            cliente = inst.duenio_cuenta(numeroCuenta)
            cajero = self.getCookie("authcookie").split('-')[0]
        else:
            cliente = self.getCookie("authcookie").split('-')[0]
        exists = inst.registrarCuenta(tipo, idCliente,idOficina)

        operacion = operacion.Operacion(numero,id,cliente,monto,)
        if not exists:
            self.render('../../static/registrarOficinaError.html')
        else:
        	self.render('../../static/transaccionExitosa.html')
