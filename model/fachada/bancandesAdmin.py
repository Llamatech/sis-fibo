#-*- coding:iso-8859-1 -*-

import os
import sys
from model.dao import consulta_dao_catalogo

class BancAndesAdmin(object):
    """
    ======================================
    Gestor principal del sistema bancario - Versión administrador
    ======================================
    BancAndesAdmin()

    Clase que representa el sistema de gestión bancaria de la entidad bancaria
    BancAndes. Esta clase establece un enlace directo entre el gestor de consulta
    de bases de datos, y la interfaz principal. Ofrece todas las funcionalidades que
    son utilizadas por un usuario administrador de BancAndes.

    Atributos
    ---------
    instancia: vos.BancAndes
        Única instancia existente de la clase, definida con el fin de atender solicitudes
    dao: dao.ConsultaDAO
        Definición y referencia al gestor de Base de Datos especializado
    """

    instancia = None

    def __init__(self):
        """
        Constructor principal de la clase

        Parámetros
        ----------
        Ninguno
        """
        self.dao = consulta_dao_catalogo.ConsultaDAOcatalogo()

    @classmethod
    def dar_instancia(cls):
        """
        Retorna la única instancia existente de la clase.

        Parámetros
        ----------
        Ninguno

        Retorna
        -------
        instancia: BancAndes()
            La única instancia existente del gestor principal en el sistema
        """
        if cls.instancia is None:
           cls.instancia = cls()
        return cls.instancia

    def inicializar_ruta(self, ruta):
        """
        Establece la ruta del archivo que contiene los parámetros de acceso y 
        conexión con la base de datos.

        Parámetros
        ----------
        ruta: str
            Linea de texto que describe la ubicación del archivo de configuración
            bajo la estructura de archivos actual.
        """
        self.dao.inicializar(ruta)

    def buscar_usuarios(self):
        return self.dao.obtener_usuarios()

    def buscar_usuario(self, _id):
        return self.dao.buscar_usuario(_id)

    def obtener_tipo_documento(self):
        return self.dao.obtener_tipo_documento()

    def obtener_tipo_usuario(self):
        return self.dao.obtener_tipo_usuario()

    def verificar_usuario(self, email, pwd):
        auth_data = self.dao.obtener_usuario(email)
        if auth_data is not None:
           if auth_data.pwd == pwd:
              return [True, auth_data.id, auth_data.tipo] 
        else:
            return [False, None, None]

    def obtener_oficinas(self):
        return self.dao.obtener_oficinas()

    def registrar_oficina(self, name, phone, address):
        return self.dao.registrar_oficina(name,phone,address)

    def registrar_empleado(self, usuario, empleado):
        self.dao.registrar_empleado(usuario, empleado)

    def obtener_empleados(self, col, orden, a, b):
        count, data = self.dao.obtener_empleados(col, orden, a, b)
        return count, data

    def eliminar_empleado(self, _id, tipo_usuario, oficina):
        self.dao.eliminar_empleado(_id, tipo_usuario, oficina)

    def buscar_empleado(self, _id):
        return self.dao.buscar_empleado(_id)

    def actualizar_empleado(self, _usuario, _empleado):
        self.dao.actualizar_empleado(_usuario, _empleado)

    def obtener_oficinasL(self, col, orden, a, b):
        count, data = self.dao.obtener_oficinasL(col, orden, a, b)
        return count, data
