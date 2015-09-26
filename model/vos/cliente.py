#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de un cliente en el sistema    
"""

# ID
# TIPO_DOCUMENTO
# NUM_DOCUMENTO
# NOMBRE
# APELLIDO
# DIRECCION
# TELEFONO
# FECHA_INSCRIPCION
# FECHA_NACIMIENTO
# CIUDAD
# DEPARTAMENTO
# COD_POSTAL


class Cliente(object):

    def __init__(self, id, tipo_documento, num_documento, nombre, apellido, direccion, telefono, fecha_inscripcion, fecha_nacimiento,ciudad,departamento,codigo_postal):
        self.id = id
        self.tipo_documento = tipo_documento
        self.num_documento = num_documento
        self.nombre = nombre
        self.apellido=apellido
        self.direccion=direccion
        self.telefono=telefono
        self.fecha_inscripcion=fecha_inscripcion
        self.fecha_nacimiento=fecha_nacimiento
        self.ciudad=ciudad
        self.departamento=departamento
        self.codigo_postal=codigo_postal

    def __repr__(self):
        return str((self.id, self.tipo_documento,self.num_documento,self.nombre,self.apellido,self.direccion,self.telefono,self.fecha_inscripcion,self.fecha_nacimiento,self.ciudad,self.departamento,self.codigo_postal))

    def __str__(self):
        return self.__repr__()


class ClienteR(object):
    def __init__(self, _id, tipo_doc, num_documento, nombre, apellido, 
                 ciudad, email):
        self.id = _id
        self.tipo_doc = tipo_doc
        self.num_documento = num_documento
        self.nombre = nombre
        self.apellido = apellido
        self.ciudad = ciudad
        self.email = email

    def dict_repr(self):
        d = {
            'id':self.id,
            'tipo_doc':self.tipo_doc,
            'num_documento':self.num_documento,
            'nombre':self.nombre,
            'apellido':self.apellido,
            'ciudad':self.ciudad,
            'email':self.email
        }
        return d
