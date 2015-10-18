#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de una cuenta en el sistema    
"""
# NUMERO.SALDO.TIPO_CUENTA,CERRADA,CLIENTE,OFICINA

class Cuenta(object):

    def __init__(self, numero, saldo, tipo_cuenta, cerrada, cliente, oficina):
        self.numero = numero
        self.saldo = saldo
        self.tipo_cuenta = tipo_cuenta
        self.cerrada = cerrada
        self.cliente = cliente
        self.oficina = oficina

    def __repr__(self):
    	args = [self.numero, self.saldo, self.tipo_cuenta, self.cerrada, self.cliente, self.oficina]
    	args = map(str, args)
        return "numero: %s; saldo: %s; tipo_cuenta:%s; cerrada:%s; cliente: %s; oficina: %s" % tuple(args)

    def __str__(self):
        return self.__repr__()

class CuentaR(object):
    def __init__(self, numero, fecha_creacion, saldo, tipo, cerrada, id_cliente, nom_cliente, ap_cliente, id_of, of_nombre, fecha_umov):
        self.numero = numero
        if fecha_creacion is not None:
            self.fecha_creacion = fecha_creacion.strftime('%d/%m/%Y')
        else:
            self.fecha_creacion = None
        self.saldo = saldo
        self.tipo = tipo
        self.cerrada = cerrada
        self.id_cliente = id_cliente
        self.nom_cliente = nom_cliente
        self.ap_cliente = ap_cliente
        self.id_of = id_of
        self.of_nombre = of_nombre
        if fecha_umov is not None:
            self.fecha_umov = fecha_umov.strftime('%d/%m/%Y')
        else:
            self.fecha_umov = fecha_umov

    def dict_repr(self):
        if self.cerrada == 'N':
           url = '/cuentas?numero='+str(self.numero)
        else:
           url = None
        d = {
             'numero':self.numero,
             'fecha_creacion':self.fecha_creacion,
             'saldo':self.saldo,
             'tipo':self.tipo,
             'cerrada':self.cerrada,
             'id_cliente':self.id_cliente,
             'nom_cliente':self.nom_cliente,
             'ap_cliente':self.ap_cliente,
             'id_of':self.id_of,
             'of_nombre':self.of_nombre,
             'fecha_umov':self.fecha_umov,
             'delete':url
        }
        return d
