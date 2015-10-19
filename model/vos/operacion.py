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

class OperacionR(object):
    def __init__(self, numero, tipo_op, tipo, id_cliente, nombre, apellido, valor, punto_atencion, tipo_pa, id_oficina, nombre_oficina, cajero, nombre_emp, apellido_emp, cuenta, prestamo, fecha):
        self.numero = numero
        self.tipo_op = tipo_op
        self.tipo = tipo
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.valor = valor
        self.punto_atencion = punto_atencion
        self.tipo_pa = tipo_pa 
        self.id_oficina = id_oficina
        self.nombre_oficina = nombre_oficina
        self.cajero = cajero
        self.nombre_emp = nombre_emp
        self.apellido_emp = apellido_emp
        self.cuenta = cuenta
        self.prestamo = prestamo
        self.fecha = fecha.strftime('%d/%m/%Y')

    def dict_repr(self):
        d = {
            'numero':self.numero,
            'fecha':self.fecha,
            'tipo':self.tipo,
            'id_cliente':self.id_cliente,
            'nombre':self.nombre,
            'apellido':self.apellido,
            'cuenta':self.cuenta,
            'prestamo':self.prestamo,
            'valor':self.valor,
            'punto_atencion':self.punto_atencion,
            'tipo_pa':self.tipo_pa,
            'id_oficina':self.id_oficina,
            'nombre_oficina':self.nombre_oficina,
            'cajero':self.cajero,
            'nombre_emp':self.nombre_emp,
            'apellido_emp':self.apellido_emp
        }
        return d
