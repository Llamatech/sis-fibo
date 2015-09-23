#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de una oficina en el sistema    
"""
# ID,NOMBRE,DIRECCION,TELEFONO,GERENTE

class Oficina(object):

    def __init__(self, id, nombre, direccion, telefono, gerente):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.gerente = gerente

    def __repr__(self):
    	args = [self.id, self.nombre, self.telefono, self.direccion, self.gerente]
    	args = map(str, args)
        return "id: %s; nombre: %s; telefono:%s; direccion:%s; gerente: %s" % tuple(args)

    def __str__(self):
        return self.__repr__()
