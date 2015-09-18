import os
import base64
import random
import datetime
import cx_Oracle

URL = 'fn3.oracle.virtual.uniandes.edu.co'
PORT = 1521
SERV = 'prod'
USER = 'ISIS2304221520'
PWD = 'Xg6YCgZ8wJ3R'

dsn_tns = cx_Oracle.makedsn(URL, PORT, SERV)
cnx = cx_Oracle.connect(USER, PWD, dsn_tns)

cursor = cnx.cursor()

s = 'INSERT INTO USUARIO (ID, PIN, EMAIL, TIPO) VALUES %s'
s2 = 'INSERT INTO EMPLEADO (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
     +'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, '+\
     'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'
s3 = 'INSERT INTO CLIENTE (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
     +'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, '+\
     'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'

cursor.execute('SELECT * FROM TIPOUSUARIO')
u_type = cursor.fetchall()

cursor.execute('SELECT * FROM TIPOIDENTIFICACION')
id_type = cursor.fetchall()

managers = []

for i in range(1, 3001):
    user = (i, base64.b64encode('usuario' + str(i)),
            'usuario' + str(i) + '@example.com')
    stmt = s % str(user)
    cursor.execute(stmt)
    cnx.commit()
