#-*- coding:iso-8859-1 -*-

import os
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


def get_max_num(tab, col):
    stmt = 'SELECT max(%s) FROM %s' % (col, tab);
    cursor.execute(stmt)
    res = cursor.fetchall()[0][0]
    return res

def get_random_tuple(tab, col):
    stmt = """SELECT * FROM
            (
              SELECT %s 
              FROM %s
              ORDER BY dbms_random.value
            )
            WHERE rownum = 1""" % (col, tab)
    cursor.execute(stmt)
    return cursor.fetchall()[0][0]

def manual_test():
    insert_stmt = 'INSERT INTO %s VALUES %s'
    print "Probando: USUARIO\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print '1.1 Insertando tupla con llave primaria única'
    usuario_cols = 'USUARIO (ID, PIN, EMAIL, TIPO)'
    max_value = get_max_num('USUARIO', 'ID')
    _type = get_random_tuple('TIPOUSUARIO', 'ID')
    tup = (max_value+1, 'testValue', 'testValue1', _type)
    stmt = insert_stmt % (usuario_cols, str(tup))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Aprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Reprobada"
    print '\n1.2 Insertando una tupla con llave primaria duplicada'
    try:
        print stmt
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    print "\nPrueba 2: Restricciones de Llave Foránea"
    max_type = get_max_num('TIPOUSUARIO', 'ID')
    print "2.1 Insertando una tupla con Tipo de Usuario inexistente\n"
    tup = (max_value+2, 'testValue', 'testValue2', max_type+1)
    stmt = insert_stmt % (usuario_cols, str(tup))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Insertando una tupla con Email nulo\n"
    tup = (max_value+1, 'testValue', None, max_type+1)
    stmt = insert_stmt % (usuario_cols, str(tup).replace('None', 'null'))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n-------------------------------------------------------------------------------"

    print "\nProbando: EMPLEADO\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "1.1 Insertando un empleado duplicado"
    _id = 7774
    cursor.execute('SELECT * FROM EMPLEADO WHERE ID = 7774')
    data = cursor.fetchall()[0]
    max_type = get_max_num('EMPLEADO', 'ID')
    data = list(data)
    data[0] =  max_type+1
    data[7] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[7].strftime('%d/%m/%Y'))
    data[8] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[8].strftime('%d/%m/%Y'))
    data = tuple(data)
    stmt_e = 'INSERT INTO EMPLEADO VALUES %s' % (str(data).replace("\"", ''))
    stmt_e = stmt_e.replace('None', 'null')
    print stmt_e
    try:
        cursor.execute(stmt_e)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 2: Restrcciones de LLave Foránea"
    print "2.1 Insertando un Empleado que no se encuentra registrado como USUARIO"
    max_type = get_max_num('USUARIO', 'ID')
    data = list(data)
    data[0] = max_type+1
    data = tuple(data)
    stmt = 'INSERT INTO EMPLEADO VALUES %s' % (str(data).replace("\"", ''))
    stmt = stmt.replace('None', 'null')
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.2 Actualizando una tupla, cuyo identificador de tipo de documento no existe"
    max_type = get_max_num('TIPOIDENTIFICACION', 'ID')
    max_emp = get_max_num('EMPLEADO', 'ID')
    stmt = 'UPDATE EMPLEADO SET TIPO_DOCUMENTO = %d WHERE ID = %d' % (max_type+1, max_emp)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Actualizando el número de documento de un empleado, cuyo valor es nulo"
    stmt = 'UPDATE EMPLEADO SET NUM_DOCUMENTO = null WHERE ID = %d' % (max_emp)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n-------------------------------------------------------------------------------"

    print "\nProbando: CLIENTE\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "1.1 Insertando un cliente duplicado"
    cursor.execute('SELECT * FROM CLIENTE WHERE ID = 1669')
    data = cursor.fetchall()[0]
    max_type = get_max_num('CLIENTE', 'ID')
    data = list(data)
    data[0] =  max_type
    data[7] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[7].strftime('%d/%m/%Y'))
    data[8] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[8].strftime('%d/%m/%Y'))
    data = tuple(data)
    stmt = 'INSERT INTO CLIENTE VALUES %s' % (str(data).replace("\"", ''))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    print "\nPrueba 2: Restrcciones de LLave Foránea"
    print "2.1 Insertando un Cliente que no se encuentra registrado como USUARIO"
    max_type = get_max_num('USUARIO', 'ID')
    data = list(data)
    data[0] = max_type+1
    data = tuple(data)
    stmt = 'INSERT INTO CLIENTE VALUES %s' % (str(data).replace("\"", ''))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.2 Actualizando una tupla, cuyo identificador de tipo de documento no existe"
    max_type = get_max_num('TIPOIDENTIFICACION', 'ID')
    max_emp = get_max_num('CLIENTE', 'ID')
    stmt = 'UPDATE CLIENTE SET TIPO_DOCUMENTO = %d WHERE ID = %d' % (max_type+1, max_emp)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Actualizando el número de documento de un cliente, cuyo valor es nulo"
    stmt = 'UPDATE CLIENTE SET NUM_DOCUMENTO = null WHERE ID = %d' % (max_emp)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n-------------------------------------------------------------------------------"

    print "\nProbando: CUENTA\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "1.1 Insertando una cuenta duplicada"
    max_num = get_max_num('CUENTA', 'NUMERO')
    cursor.execute('SELECT * FROM CUENTA WHERE NUMERO = %d' % (max_num))
    data = cursor.fetchall()[0]
    data = list(data)
    data[-1] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[-1].strftime('%d/%m/%Y'))
    data = tuple(data) 
    stmt = 'INSERT INTO CUENTA VALUES %s' % (str(data))
    stmt = stmt.replace("\"", '')
    print stmt 
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    print "\nPrueba 2: Restricción de Llave Foránea"
    print "2.1 Insertando una Tupla que contiene un Cliente inexistente"
    cnx.rollback()
    max_client = get_max_num('CLIENTE', 'ID')
    data = list(data)
    data[0] = data[0]+1
    data[4] = max_client+1
    data = tuple(data)
    stmt = 'INSERT INTO CUENTA VALUES %s' % (str(data))
    stmt = stmt.replace("\"", '')
    print stmt 
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.2 Insertando una Tupla que contiene una Oficina inexistente"
    max_office = get_max_num('OFICINA', 'ID')
    data = list(data)
    data[4] = max_client
    data[5] = max_office+1
    data = tuple(data)
    stmt = 'INSERT INTO CUENTA VALUES %s' % (str(data))
    stmt = stmt.replace("\"", '')
    print stmt 
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.3 Reemplazando el tipo de Cuenta de una cuenta existente, por un valor inexistente"
    max_type = get_max_num('TIPOCUENTA', 'ID')
    stmt = 'UPDATE CUENTA SET TIPO_CUENTA = %d WHERE NUMERO = %d' % (max_type+1, max_num)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Modificar el estado de la columna cerrada con un valor incorrecto"
    stmt = "UPDATE CUENTA SET CERRADA = 'K' WHERE NUMERO = %d" % (max_num)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n-------------------------------------------------------------------------------"
    
    print "\nProbando: PRESTAMO\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "1.1 Insertando un préstamo duplicado"
    max_num = get_max_num('PRESTAMO', 'ID')
    cursor.execute('SELECT * FROM PRESTAMO WHERE ID = %d' % (max_num))
    data = cursor.fetchall()[0]
    data = list(data)
    data[3] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[3].strftime('%d/%m/%Y'))
    data[9] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[9].strftime('%d/%m/%Y'))
    data = tuple(data) 
    stmt = 'INSERT INTO PRESTAMO VALUES %s' % (str(data))
    stmt = stmt.replace("\"", '')
    print stmt 
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    print "\nPrueba 2: Restricción de Llave Foránea"
    print "2.1 Insertando una Tupla que contiene un Cliente inexistente"
    cnx.rollback()
    max_client = get_max_num('CLIENTE', 'ID')
    data = list(data)
    data[0] = data[0]+1
    data[7] = max_client+1
    data = tuple(data)
    stmt = 'INSERT INTO PRESTAMO VALUES %s' % (str(data))
    stmt = stmt.replace("\"", '')
    print stmt 
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.2 Insertando una Tupla que contiene una Oficina inexistente"
    max_office = get_max_num('OFICINA', 'ID')
    data = list(data)
    data[7] = max_client
    data[8] = max_office+1
    data = tuple(data)
    stmt = 'INSERT INTO PRESTAMO VALUES %s' % (str(data))
    stmt = stmt.replace("\"", '')
    print stmt 
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.3 Reemplazando el tipo de préstamo de un préstamo existente, por un valor inexistente"
    max_type = get_max_num('TIPOPRESTAMO', 'ID')
    stmt = 'UPDATE PRESTAMO SET TIPO = %d WHERE ID = %d' % (max_type+1, max_num)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Modificar el estado de la columna cerrado con un valor incorrecto"
    stmt = "UPDATE PRESTAMO SET CERRADO = 'K' WHERE ID = %d" % (max_num)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n-------------------------------------------------------------------------------"

    print "\nProbando: PUNTOSATENCION\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "1.1 Insertando un punto de atención duplicado"
    max_pa = get_max_num('PUNTOSATENCION', 'ID')
    stmt = 'SELECT * FROM PUNTOSATENCION WHERE ID = %d' % (max_pa)
    cursor.execute(stmt)
    data = cursor.fetchall()[0]
    stmt = 'INSERT INTO PUNTOSATENCION VALUES %s' % (str(data))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 2: Restricción de Llave Foránea"
    print "2.1 Insertando una tupla cuyo tipo de oficina es inexistente"
    max_type = get_max_num('TIPOPUNTOSATENCION', 'ID')
    data = list(data)
    data[0] = max_pa+1
    data[-1] = max_type+1
    data = tuple(data)
    stmt = 'INSERT INTO PUNTOSATENCION VALUES %s' % (str(data))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n2.2 Insertando una tupla cuya oficina designada, no existe"
    max_office = get_max_num('OFICINA', 'ID')
    data = list(data)
    data[2] = max_office+1
    data[-1] = max_type-1
    data = tuple(data)
    stmt = 'INSERT INTO PUNTOSATENCION VALUES %s' % (str(data))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Reemplazar la localización de un punto de atención por un valor nulo"
    stmt = 'UPDATE PUNTOSATENCION SET LOCALIZACION = null WHERE ID = %d' % (max_pa)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\n-------------------------------------------------------------------------------"

    print "\nProbando: OFICINA\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "1.1 Insertando una oficina duplicada"
    max_office = get_max_num('OFICINA', 'ID')
    stmt = 'SELECT * FROM OFICINA WHERE ID = %d' % (max_office)
    cursor.execute(stmt)
    data = cursor.fetchall()[0]
    stmt = 'INSERT INTO OFICINA VALUES %s' % (str(data))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 2: Restricción de Llave Foránea"
    print "2.1 Insertar una tupla cuyo identificador de gerente sea inexistente"
    max_gerente = get_max_num('EMPLEADO', 'ID')
    data = list(data)
    data[0] += 1
    data[-1] = max_gerente+1
    data = tuple(data)
    stmt = 'INSERT INTO OFICINA VALUES %s' % (str(data))
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.IntegrityError:
        print "\nPrueba: Aprobada"
    cnx.rollback()
    print "\nPrueba 3: Restricciones y verificación"
    print "3.1 Reemplazar el nombre de una oficina por un valor nulo"
    stmt = 'UPDATE OFICINA SET NOMBRE = null WHERE ID = %d' % (max_office)
    print stmt
    try:
        cursor.execute(stmt)
        print "\nPrueba: Reprobada"
    except cx_Oracle.DatabaseError:
        print "\nPrueba: Aprobada"
    

if __name__ == '__main__':
    manual_test()
    cursor.close()
    cnx.close()