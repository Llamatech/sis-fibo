#!/usr/bin/env python

import os
import sys
import pika
import logging
import tornado.web
import coloredlogs
import tornado.ioloop
from model.queue_client import publisher, client
import model.request_handler as handlers

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
coloredlogs.install(level='info')

clr = 'clear'
if os.name == 'nt':
   clr = 'cls'

def main():
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}
    application = tornado.web.Application([(r"/", handlers.home.HomeHandler),
        (r"/registrar/usuario", handlers.registro_usuario.RegistroHandler),
        (r"/registrar/empleado", handlers.registro_empleado.RegistroHandler),
        (r"/login", handlers.login_handler.LoginHandler),
        (r"/registrar/cuenta", handlers.registro_cuenta.RegistroHandler),
        (r"/logout", handlers.login_handler.LogoutHandler), 
        (r"/registrar/oficina", handlers.registro_oficina.RegistroHandler),
        (r"/empleados", handlers.empleados.ListHandler),
        (r"/empleado", handlers.empleado.EditionHandler),
        (r"/registrar/operacion/cuenta", handlers.registrar_op_cuenta.RegistroHandler),
        (r"/registrar/operacion/prestamo", handlers.registrar_op_prestamo.RegistroHandler),
        (r"/oficinas", handlers.oficinas.ListHandler),
        (r"/oficina", handlers.oficina.EditionHandler),
        (r"/registrar/puntoAtencion", handlers.registro_pa.RegistroHandler),
        (r"/puntosAtencion", handlers.puntos_atencion.ListHandler),
        (r"/puntoAtencion", handlers.punto_atencion.EditionHandler),
        (r"/cuentas", handlers.cuentas.ListHandler),
        (r"/cuentas/naturales", handlers.cuentas.NatHandler),
        (r"/cuentas/nocerradas", handlers.cuentas.NotClosedHandler),
        (r"/prestamos/nocerrados", handlers.prestamos.NotClosedHandler),
        (r"/informacion/cliente", handlers.consultar_info_cliente.ListHandler),
        (r"/usuarios", handlers.usuarios.ListHandler),
        (r"/registrar/prestamo", handlers.registro_prestamo.RegistroHandler),
        (r"/cerrar/prestamo", handlers.prestamos.ListHandler),
        (r"/nomina", handlers.nomina.MainHandler),
        (r"/pago/nomina", handlers.pago_nomina.PagoHandler),
        (r"/registrar/nomina", handlers.registro_nomina.RegistroHandler),
        (r"/operaciones", handlers.operacion.ListHandler),
        (r"/consignaciones", handlers.consignacion.ListHandler),
        (r"/nomina/migrar", handlers.nomina.MigrationHandler),
        (r"/prestamos", handlers.prestamos.MainHandler),
        (r"/ws", handlers.web_socket.WebSocketHandlerTest)], 
        debug=True, serve_traceback=True, autoreload=True, **settings)
    print "Server is now at: 127.0.0.1:8000"
    ioloop = tornado.ioloop.IOLoop.instance()
    pc = publisher.ExamplePublisher(LOGGER)
    outq = client.ExampleConsumer(LOGGER)
    application.outq = outq
    application.pc = pc
    application.pc.connect()
    application.outq.connect()

    application.listen(8000)
    try:
      ioloop.start()
    except KeyboardInterrupt:
      pass
    finally:
      print "Closing server...\n"
      tornado.ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    os.system(clr)
    main()
