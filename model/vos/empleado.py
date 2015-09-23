#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de un empleado en el sistema    
"""
# ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
# + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
# 'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL, OFICINA

class Empleado(object):

    def __init__(self, id, tipo_doc, 
                 num_documento, nombre, apellido, 
                 direccion, telefono, fecha_ins, fecha_nac,
                 ciudad, departamento, cod_postal, oficina):
        self.id = id
        self.tipo_doc = tipo_doc
        self.num_documento = num_documento
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.telefono = telefono
        self.fecha_ins = fecha_ins
        self.fecha_nac = fecha_nac
        self.ciudad = ciudad
        self.departamento = departamento
        self.cod_postal = cod_postal
        self.oficina = oficina

    def __repr__(self):
    	args = (self.id, int(self.tipo_doc), self.num_documento, self.nombre,
                self.apellido, self.direccion, self.telefono,
                "TO_DATE('%s', 'dd/mm/yyyy')" % (self.fecha_ins.strftime('%d/%m/%y')),"TO_DATE('%s', 'dd/mm/yyyy')" % (self.fecha_nac.strftime('%d/%m/%y')), self.ciudad,
                self.departamento, self.cod_postal, int(self.oficina))
        return str(args).replace("\"", '')

    def __str__(self):
        return self.__repr__()