#!/usr/bin/env python

import os
import sys
import tornado.web
import tornado.ioloop
import model.request_handler as handlers


def main():
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
        (r"/oficinas", handlers.oficinas.ListHandler)], 
        debug=True, serve_traceback=True, autoreload=True, **settings)
    print "Server is now at: 127.0.0.1:8000"
    application.listen(8000)
    try:
      tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
      pass
    finally:
      print "Closing server..."
      tornado.ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    main()
