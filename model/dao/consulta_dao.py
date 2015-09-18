#-*- coding:iso-8859-1 -*-

import os
import sys
import cx_Oracle
from model.vos import usuario

archivo_conexion = '../data/connection'
tabla_consulta = 'USUARIO'
columna = 'email'

stmt = 'SELECT * FROM ' + tabla_consulta + ' WHERE ' + columna + "= "
stmt_2 = 'SELECT * FROM ' + tabla_consulta


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
        self.establecer_conexion()
        cur = self.conn.cursor()
        usuarios = []
        try:
            cur.execute(stmt_2)
            data = cur.fetchall()
            #Usuario: id, contraseña, email
            for t in data:
                print t
                user = usuario.Usuario(t[0], t[1], t[2])
                usuarios.append(user)
        except cx_Oracle.Error as e:
            raise e
        cur.close()
        self.conn.close()
        return usuarios
