#-*- coding:iso-8859-1 -*-

"""
Clase que modela la información de un usuario en el sistema    
"""
class Usuario(object):
    
    def __init__(self, id, pwd, email):
        self.id = id
        self.pwd = pwd
        self.email = email

    def __repr__(self):
        return 'id: %d ; password: %s ; email: %s' % (self.id, self.pwd, self.email)

    def __str__(self):
        return self.__repr__()
