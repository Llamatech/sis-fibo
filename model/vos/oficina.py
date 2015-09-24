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

class OficinaR(object):
    def __init__(self, _id, localizacion, nombre, direccion, telefono, id_gerente, gerente):
        self.id = _id
        self.localizacion = localizacion
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.id_gerente = id_gerente
        self.gerente = gerente

    def dict_repr(self):
        d = {
            'id':self.id,
            'localizacion':self.localizacion,
            'nombre':self.nombre,
            'direccion':self.direccion,
            'telefono':self.telefono,
            'id_gerente':self.id_gerente,
            'gerente':self.gerente,
            'delete':'/oficina?id='+str(self.id)+"&gerente ="+str(self.id_gerente)+'|/oficina?id='+str(self.id)
        }
        return d
