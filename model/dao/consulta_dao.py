#-*- coding:iso-8859-1 -*-

import os
import sys
import cx_Oracle
from model.vos import tipo
from model.vos import usuario


class ConsultaDAO(object):

    def inicializar(self, path):
        with open(path, 'rb') as fp:
            lines = fp.readlines()
        self.conn_info = {}
        for line in lines:
            line = line.strip('\n')
            info = line.split(':')
            self.conn_info[info[0]] = eval(info[1])

    def establecer_conexion(self):
        dsn_tns = cx_Oracle.makedsn(self.conn_info['URL'],
                                    self.conn_info['PORT'], self.conn_info['SERV'])
        self.conn = cx_Oracle.connect(
            self.conn_info['USER'], self.conn_info['PWD'], dsn_tns)

    def cerrar_conexion(self):
        self.conn.close()
        self.conn = None

    def obtener_usuarios(self):
        tabla_consulta = 'USUARIO'
        columna = 'email'
        stmt = 'SELECT * FROM ' + tabla_consulta + ' WHERE ' + columna + "= "
        stmt_2 = 'SELECT * FROM ' + tabla_consulta

        self.establecer_conexion()
        cur = self.conn.cursor()
        usuarios = []
        try:
            cur.execute(stmt_2)
            data = cur.fetchall()
            # Usuario: id, contraseña, email
            for t in data:
                print t
                user = usuario.Usuario(t[0], t[1], t[2], t[3])
                usuarios.append(user)
        except cx_Oracle.Error as e:
            raise e
        cur.close()
        self.conn.close()
        return usuarios

    def obtener_tipo_documento(self):
        tabla_consulta = 'TIPOIDENTIFICACION'
        stmt = 'SELECT * FROM ' + tabla_consulta
        self.establecer_conexion()
        cur = self.conn.cursor()
        tipo_documento_l = []
        try:
            cur.execute(stmt)
            data = cur.fetchall()
            # TipoIdentificacion: id, tipo
            for t in data:
                tipoU = tipo.TipoDocumento(t[0], t[1])
                tipo_documento_l.append(tipoU)
        except cx_Oracle.Error as e:
            raise e
        cur.close()
        self.conn.close()
        return tipo_documento_l

    def obtener_tipo_usuario(self):
        tabla_consulta = 'TIPOUSUARIO'
        stmt = 'SELECT * FROM '
        self.establecer_conexion()
        cur = self.conn.cursor()
        tipo_usuario_l = []
        try:
            cur.execute(stmt + tabla_consulta)
            data = cur.fetchall()
            # TipoIdentificacion: id, tipo
            for t in data:
                tipoU = tipo.TipoUsuario(t[0], t[1])
                tipo_usuario_l.append(tipoU)
        except cx_Oracle.Error as e:
            raise e
        cur.close()
        self.conn.close()
        return tipo_usuario_l

    def obtener_usuario(self, email):
        tabla_consulta = 'USUARIO'
        tabla_consulta1 = 'TIPOUSUARIO'
        stmt = 'SELECT u.id, u.pin, u.email, v.tipo FROM ' + tabla_consulta + \
            ' u , ' + tabla_consulta1 + " v WHERE u.email = '" + \
            email + "' AND u.tipo = v.id"
        print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        user = None
        # try:
        cur.execute(stmt)
        data = cur.fetchall()
        # UsuarioTipo: id, pwd, email, tipo
        if len(data) > 0:
            user_d = data[0]
            user = usuario.Usuario(user_d[0], user_d[1], user_d[2], user_d[3])
        # except cx_Oracle.Error as e:
        #     raise e
        cur.close()
        self.conn.close()
        print user
        return user

    def obtener_tipo_cuenta(self):
        tabla_consulta = 'TIPOCUENTA'
        stmt = 'SELECT * FROM ' + tabla_consulta
        self.establecer_conexion()
        cur = self.conn.cursor()
        tipo_cuenta_l = []
        try:
            cur.execute(stmt)
            data = cur.fetchall()
            # TipoIdentificacion: id, tipo
            for t in data:
                tipoU = tipo.TipoCuenta(t[0], t[1])
                tipo_cuenta_l.append(tipoU)
        except cx_Oracle.Error as e:
            raise e
        cur.close()
        self.conn.close()
        return tipo_cuenta_l

    def registrar_cuenta(self, tipo, idCliente, idOficina, saldo):
        stmt = "SELECT * FROM USUARIO u WHERE u.id="+idCliente
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            return False

        stmt = 'SELECT max(numero) FROM CUENTA'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        numero = cur.fetchall()[0][0]
        stmt = 'INSERT INTO CUENTA VALUES ('+"'"+str(numero+1)+"','"+saldo+"','"+tipo+"','N','"+idCliente+"','"+str(idOficina)+ "')"
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

    def get_id_oficina(self, idGerente):
        stmt = " SELECT id FROM OFICINA WHERE " + "gerente = '" + \
        idGerente + "'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        if len(data)<=0:
            return -1
        cur.close()
        self.conn.close()
        return data[0][0]

    def obtener_cuentas(self, idUsuario):
        stmt = "SELECT * FROM CUENTAS where id = " + "'"+idUsuario+ "'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cuentas = []
        for t in data:
            cuenta = cuenta.Cuenta(t[0], t[1], t[2], t[3], t[4], t[5])
            cuentas.append(cuenta)
        return cuentas

    def es_cajero(self, idUsuario):
        stmt = "SELECT * FROM USUARIO u, TIPOUSUARIO t WHERE u.tipo = t.id AND t.tipo='Cajero' AND u.id="+"'"+idUsuario+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        if len(data) > 0:
            return True
        else:
            return False

    def generar_numero_operacion(self):
        stmt = "SELECT max(numero) FROM OPERACION"
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        return data[0][0]

    def get_id_pa(self, idGerente):
        stmt = " SELECT p.id FROM OFICINA o, PUNTOSATENCION p WHERE p.oficina=o.id AND o.gerente="+"'"+idGerente+"'" 
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        if len(data)<=0:
            return -1
        cur.close()
        self.conn.close()
        return data[0][0]