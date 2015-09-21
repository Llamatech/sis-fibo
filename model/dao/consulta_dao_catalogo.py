#-*- coding:iso-8859-1 -*-

import os
import sys
import cx_Oracle
from model.vos import tipo
from model.vos import usuario


class ConsultaDAOcatalogo(object):

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
        return user

        

    def registrar_oficina(self, name, address, phone, idGerente):
        tabla_consulta= 'USUARIO'
        tabla_consulta1= 'TIPOUSUARIO'
        stmt = "SELECT * FROM USUARIO u, TIPOUSUARIO t WHERE u.id="+idGerente+"AND u.tipo=v.id AND v.tipo='Gerente Oficina"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        gerente=None

        if len(data)<=0:
            return false

        numero = 'SELECT count(*) FROM OFICINA'
        stmt = 'INSERT INTO OFICINA VALUES ('+numero+','+name+','+address+','+phone+','+idGerente+')'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)