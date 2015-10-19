#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de una cuenta en el sistema    
"""
# NUMERO.SALDO.TIPO_CUENTA,CERRADA,CLIENTE,OFICINA

class Prestamo(object):

    def __init__(self, id, interes, monto, vencimiento_cuota, num_cuotas, valor_cuota, tipo, cliente, oficina):
        self.id = id
        self.interes = interes
        self.monto = monto
        self.vencimiento_cuota = vencimiento_cuota
        self.num_cuotas = num_cuotas
        self.valor_cuota = valor_cuota
        self.tipo = tipo
        self.cliente = cliente
        self.oficina = oficina

    def __repr__(self):
        args = (self.id, self.interes, self.monto, "TO_DATE('%s', 'dd/mm/yyyy')" % (str(self.vencimiento_cuota)),
                self.num_cuotas, self.valor_cuota, self.tipo, self.cliente, self.oficina)
        return str(args).replace("\"", '')

    def __str__(self):
        return self.__repr__()

class PrestamoR(object):
    def __init__(self, _id, tipo_p, nombre_cliente, apellido_cliente, saldo):
        self.id = _id
        self.tipo_p = tipo_p
        self.nombre_cliente = nombre_cliente
        self.apellido_cliente = apellido_cliente
        self.saldo = saldo

    def dict_repr(self):
        d = {
             'id':self.id,
             'tipo_p':self.tipo_p,
             'nombre':self.nombre_cliente,
             'apellido':self.apellido_cliente,
             'saldo':self.saldo
            }
        return d


class PrestamoR2(object):
    def __init__(self, nombre, apellido, num_documento, _id, interes, monto, vencimiento_cuota, num_cuotas, valor_cuota, tipo, cliente, oficina, nombre_of, fecha_creacion, cerrado, tipo_p, id_cliente):
       self.nombre = nombre
       self.apellido = apellido
       self.num_documento = num_documento
       self.id = _id
       self.interes = interes
       self.monto = monto
       self.vencimiento_cuota = vencimiento_cuota.strftime('%d/%m/%Y')
       self.num_cuotas = num_cuotas
       self.valor_cuota = valor_cuota
       self.tipo = tipo
       self.cliente = cliente
       self.oficina = oficina
       self.nombre_of = nombre_of
       self.fecha_creacion = fecha_creacion.strftime('%d/%m/%Y')
       self.cerrado = cerrado
       self.tipo_p = tipo_p
       self.id_cliente = id_cliente

    def dict_repr(self):
        d = {
             'id':self.id,
             'cerrado':self.cerrado,
             'monto':self.monto,
             'fecha_creacion':self.fecha_creacion,
             'num_cuotas':self.num_cuotas,
             'valor_cuota':self.valor_cuota,
             'interes':self.interes,
             'id_cliente':self.id_cliente,
             'nombre':self.nombre,
             'apellido':self.apellido,
             'oficina':self.oficina,
             'nombre_of':self.nombre_of
            }
        return d
