#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de un usuario en el sistema    
"""


class Usuario(object):

    def __init__(self, id, pwd, email, tipo):
        self.id = id
        self.pwd = pwd
        self.email = email
        self.tipo = tipo

    def __repr__(self):
        return str((self.id, self.pwd, self.email, self.tipo))

    def __str__(self):
        return self.__repr__()
