#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de un punto de atención en el sistema    
"""
# ID,NOMBRE,DIRECCION,TELEFONO,GERENTE

class PuntoAtencion(object):

    def __init__(self, _id, localizacion, oficina, tipo):
    	self.id = _id
    	self.localizacion = localizacion,
    	if oficina is None: 
    	   	self.oficina = 'null'
    	else:
    		self.oficina = str(oficina)
    	self.tipo = tipo

    def __repr__(self):
    	args = (self.id, self.localizacion, self.tipo)
    	return str(args)[0:-1]+', '+self.oficina+')'

    def __str__(self):
    	return self.__repr__()

class PuntoAtencionR(object):
	def __init__(self, _id, localizacion, tipo_pa, oficina, nombre):
		self.id = _id
		self.localizacion = localizacion
		self.tipo_pa = tipo_pa
		self.oficina = oficina
		self.nombre = nombre

	def dict_repr(self):
		d = {
			'id':self.id,
			'localizacion':self.localizacion,
			'tipo_pa':self.tipo_pa,
			'oficina':self.oficina,
			'nombre':self.nombre,
			'delete':'/puntoAtencion?id='+str(self.id)+'|/puntoAtencion?id='+str(self.id) 
		}
		return d
