#-*- coding:iso-8859-1 -*-

import os
import sys
from model.dao import consulta_dao

class BancAndes(object):
    """
    ======================================
    Gestor principal del sistema bancario
    ======================================
    BancAndes()

    Clase que representa el sistema de gestión bancaria de la entidad bancaria
    BancAndes. Esta clase establece un enlace directo entre el gestor de consulta
    de bases de datos, y la interfaz principal.

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
        self.dao = consulta_dao.ConsultaDAO()

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

    def obtener_clientes(self, search_term):
        return self.dao.obtener_clientes(search_term)

    def registrar_cliente(self, _usuario, _cliente):
        self.dao.registrar_cliente(_usuario, _cliente)

    def obtener_tipo_documento(self):
        return self.dao.obtener_tipo_documento()

    def obtener_tipo_usuario(self):
        return self.dao.obtener_tipo_usuario()

    def obtener_tipo_prestamo(self):
        return self.dao.obtener_tipo_prestamo()

    def verificar_usuario(self, email, pwd):
        auth_data = self.dao.obtener_usuario(email)
        if auth_data is not None:
           if auth_data.pwd == pwd:
              print True
              return [True, auth_data.id, auth_data.tipo] 
        else:
            print False
            return [False, None, None]

    def obtener_tipo_cuenta(self):
        return self.dao.obtener_tipo_cuenta()

    def registrar_cuenta(self,tipo,idCliente,idOficina, saldo):
        return self.dao.registrar_cuenta(tipo, idCliente, idOficina, saldo)

    def get_id_oficina(self, idGerente):
        return self.dao.get_id_oficina(idGerente)

    def obtener_cuentas(self, idUsuario, cond = None, closed=True):
        return self.dao.obtener_cuentas(idUsuario, cond, closed)

    def es_cajero(self, idUsuario):
        return self.dao.es_cajero(idUsuario)

    def generar_numero_operacion(self):
        return self.dao.generar_numero_operacion()

    def get_id_pa(self, idGerente):
        return self.dao.get_id_pa(idGerente)

    def duenio_cuenta(self, numeroCuenta):
        return self.dao.duenio_cuenta(numeroCuenta)

    def registrar_operacion_cuenta(self, operacion):
        return self.dao.registrar_operacion_cuenta(operacion)

    def duenio_prestamo(self, numeroPrestamo):
        return self.dao.duenio_prestamo(numeroPrestamo)

    def existe_cuenta(self, numeroCuenta):
        return self.dao.existe_cuenta(numeroCuenta)

    def existe_prestamo(self, numeroPrestamo):
        return self.dao.existe_prestamo(numeroPrestamo)

    def get_monto_prestamo(self, numeroPrestamo):
        return self.dao.get_monto_prestamo(numeroPrestamo)

    def registrar_operacion_prestamo(self, operacion):
        return self.dao.registrar_operacion_prestamo(operacion)

    def obtener_cuentasL(self, col, orden, a, b, perm, params, _id):
        search_count, count, data = self.dao.obtener_cuentasL(col, orden, a, b, perm, params, _id)
        return search_count, count, data

    def obtener_operacionL(self, col, orden, a, b, perm, params, _id):
        search_count, count, data = self.dao.obtener_operacionL(col, orden, a, b, perm, params, _id)
        return search_count, count, data

    def obtener_tipo_de_usuario(self, idUsuario):
        return self.dao.obtener_tipo_de_usuario(idUsuario)

    def cerrar_cuenta(self, numero):
        return self.dao.cerrar_cuenta(numero)

    def obtener_prestamos_cliente(self, idUsuario):
        return self.dao.obtener_prestamos_cliente(idUsuario)

    def obtener_operaciones(self, idUsuario):
        return self.dao.obtener_operaciones(idUsuario)

    def obtener_oficinas(self, idUsuario):
        return self.dao.obtener_oficinas(idUsuario)

    def obtener_cuentas_oficina(self, idUsuario, idOficina):
        return self.dao.obtener_cuentas_oficina(idUsuario, idOficina)

    def registrar_prestamo(self, _prestamo):
        self.dao.registrar_prestamo(_prestamo)

    def cerrar_prestamo(self, _id):
        self.dao.cerrar_prestamo(_id)

    def obtener_prestamos(self, id_oficina, search_term):
        return self.dao.obtener_prestamos(id_oficina, search_term)

    def obtener_tipo_usuarioR(self):
        return self.dao.obtener_tipo_usuarioR()

    def obtener_tipo_cliente(self, idUsuario):
        return self.dao.obtener_tipo_cliente(idUsuario)

    def obtener_nombre_cliente(self, idUsuario):
        return self.dao.obtener_nombre_cliente(idUsuario)

    def registrar_op_cuenta_origen(self, operacion, origen):
        return self.dao.registrar_op_cuenta_origen(operacion, origen)

    def registrar_operacion_prestamo_origen(self, oper,origen):
        return self.dao.registrar_operacion_prestamo_origen(oper,origen)

    def obtener_frecuencia_nomina(self):
        return self.dao.obtener_frecuencia_nomina()

    def obtener_cuentasN(self, search_term):
        return self.dao.obtener_cuentasN(search_term)

    def actualizar_nomina(self, cuenta, cuenta_empl, salario, frecuencia):
        succ, code, msg = self.dao.actualizar_nomina(cuenta, cuenta_empl, salario, frecuencia)
        return succ, code, msg

    def obtener_cuentasNC(self, search_term):
        return self.dao.obtener_cuentas_NC(search_term)

    def obtener_prestamos_NC(self, search_term):
        return self.dao.obtener_prestamos_NC(search_term)

    def pagar_nomina(self, cuenta):
        return self.dao.pagar_nomina(cuenta)

    def obtener_tipo_operacion(self):
        return self.dao.obtener_tipo_operacion()

    def cuenta_nomina(self, acc_number):
        return self.dao.cuenta_nomina(acc_number)

    def obtener_notificaciones_cliente(self, idCliente):
        return self.dao.obtener_notificaciones_cliente(idCliente)

    def migrar_nomina(self, acc_old, acc_new):
        succ, code = self.dao.migrar_nomina(acc_old, acc_new)
        return succ, code