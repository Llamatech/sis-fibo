#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de una cuenta en el sistema    
"""
# NUMERO.valor.punto_atencion,cajero,cuenta,fecha

class Operacion(object):

    def __init__(self, numero, tipo_operacion, cliente, valor, punto_atencion, cajero, cuenta, fecha):
        self.numero = numero
        self.tipo_operacion=tipo_operacion
        self.cliente=cliente
        self.valor = valor
        self.punto_atencion = punto_atencion
        self.cajero = cajero
        self.cuenta = cuenta
        self.fecha = fecha

    def __repr__(self):
    	args = [self.numero, self.tipo_operacion, self.cliente, self.valor, self.punto_atencion, self.cajero, self.cuenta, self.fecha]
    	args = map(str, args)
        return "numero: %s; cliente:%s; tipo_operacion:%s; valor: %s; punto_atencion:%s; cajero:%s; cuenta: %s; fecha: %s" % tuple(args)

    def __str__(self):
        return self.__repr__()
