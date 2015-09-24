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
