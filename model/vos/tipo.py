#-*- coding:iso-8859-1 -*-

class TipoDocumento(object):
 
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        return 'id: %d ; tipo: %s' % (self.id, self.tipo)

    def __str__(self):
        return self.__repr__()

class TipoUsuario(object):
 
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        return 'id: %d ; tipo: %s' % (self.id, self.tipo)

    def __str__(self):
        return self.__repr__()

class TipoCuenta(object):
 
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        return 'id: %d ; tipo: %s' % (self.id, self.tipo)

    def __str__(self):
        return self.__repr__()

class TipoPuntoAtencion(object):
 
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        return 'id: %d ; tipo: %s' % (self.id, self.tipo)

    def __str__(self):
        return self.__repr__()

class TipoPrestamo(object):
 
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo

    def __repr__(self):
        return 'id: %d ; tipo: %s' % (self.id, self.tipo)

    def __str__(self):
        return self.__repr__()


