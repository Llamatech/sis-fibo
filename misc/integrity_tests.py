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

def get_schema_tables():
    cursor.execute('SELECT TABLE_NAME FROM USER_TABLES')
    tables = cursor.fetchall()
    tables = [table[0] for table in tables]
    return tables

def get_table_columns(tab):
    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, NULLABLE FROM USER_TAB_COLS WHERE TABLE_NAME = '"+tab+"'")
    columns = cursor.fetchall()
    col_info = {}
    for column in columns:
        nullable = False
        if column[3] == 'Y':
            nullable = True
        col_info[column[0]] = {'dtype':column[1], 'length':column[2], 'nullable':nullable}
    return col_info

# ('EMPLEADO_DOCUMENTO_UQ', 'NUM_DOCUMENTO', 'U', None, None, None, None, None)
# ('EMPLEADO_ID', 'ID', 'R', None, 'USUARIO_PK', 'USUARIO_PK', 'USUARIO', 'ID')
# ('SYS_C0011021', 'TIPO_DOCUMENTO', 'C', '"TIPO_DOCUMENTO" IS NOT NULL', None, None, None, None)
# ('EMPLEADO_PK', 'ID', 'P', None, None, None, None, None)
def get_table_constraints(tab):
    s = """SELECT CONS_NAME, COLUMN_NAME, CONSTRAINT_TYPE, SEARCH_CONDITION, R_CONSTRAINT_NAME, CONSTRAINT_NAME, TAB_REF, COL_REF 
           FROM SCHEMA_CONS WHERE TABLE_NAME = '%s'""" % (tab)
    cursor.execute(s)
    cons = cursor.fetchall()
    constraints = {}
    type_c = {}
    indices = {}
    for c in cons:
        try:
            constraint = constraints[c[0]]
        except KeyError:
            constraint = {}
            constraints[c[0]] = constraint
        constraint['type'] = c[2]
        try:
            type_c[c[2]].append(c[0])
        except KeyError:
            type_c[c[2]] = [c[0]]
        try:
            constraint['cols'].append(c[1])
        except KeyError:
            constraint['cols'] = [c[1]]
        try:
            indices[c[1]].append(c[0])
        except KeyError:
            indices[c[1]] = [c[0]]
        if constraint['type'] == 'R':
            constraint['ref_table'] = c[6]
            try:
                constraint['ref_cols'].append(c[-1])
            except KeyError:
                constraint['ref_cols'] = [c[-1]]
        elif constraint['type'] == 'C':
            constraint['check'] = c[3]
    return constraints, type_c, indices
        
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

def auto_test():
        # if os.name == 'nt':
    #     cmd = 'cls'
    # else:
    #     cmd = 'clear'
    ins_exec = 'INSERT INTO %s VALUES %s'
    del_exec = 'DELETE FROM %s WHERE %s'
    tables = get_schema_tables()
    for table in tables:
        # os.system(cmd)
        print '\nNow testing: '+table+'\n'
        cols = get_table_columns(table)
        constraints, type_c, indices = get_table_constraints(table)
        print '%d constraints found!\n' % (len(constraints))
        print 'Testing Primary Key constraints...'
        values = {}
        for col in cols:
            values[col] = {'valid':None, 'invalid':None}
        try:
            pk  = type_c['P']:
            print 'Constraint name: '+pk
            pk_cols = constraints[pk]['cols']
            print 'Primary key index: '+reduce(lambda x,y:str(x)+', '+str(y), pk_cols)+'\n'
            print 'Checking for additional constraints...'
            for col in pk_cols:
                diff = list(set(indices[col])-set([pk]))
                if len(diff) > 0:
                    diff = filter(lambda x: constraints[x] == 'R', diff)
                    rest = diff[0]
                else:
                    if cols[col]['dtype'].find('NUMBER') != -1:
                        num = get_max_num(table, col)
                        values[col]['valid'] = num+1
                    else:
                        None
        except KeyError:
            print 'No Primary Key found!'

def manual_test():
    insert_stmt = 'INSERT INTO %s VALUES %s'
    print "Probando: USUARIO\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    usuario_cols = 'USUARIO (ID, PIN, EMAIL, TIPO)'
    max_value = get_max_num('USUARIO', 'ID')
    _type = get_random_tuple('TIPOUSUARIO', 'ID')
    tup = (max_value+1, 'testValue', 'testValue1', _type)
    stmt = insert_stmt % (usuario_cols, str(tup))
    try:
        cursor.execute(stmt)
        print 'Tupla con Llave primaria única insertada'
    except cx_Oracle.IntegrityError:
        raise Exception("Error! La tupla debería ser insertada de forma correcta")
    print 'Insertando una tupla con llave primaria duplicada'
    try:
        cursor.execute(stmt)
        raise Exception("Error! La tupla debería no debería ser insertada")
    except cx_Oracle.IntegrityError:
        pass
    print "Prueba 2: Restricciones de Llave Foránea"
    max_type = get_max_num('TIPOUSUARIO', 'ID')
    print "Insertando una tupla con Tipo de Usuario inexistente"
    tup = (max_value+2, 'testValue', 'testValue2', max_type+1)
    stmt = insert_stmt % (usuario_cols, str(tup))
    try:
        cursor.execute(stmt)
        raise Exception("Error! La tupla debería no debería ser insertada")
    except cx_Oracle.IntegrityError:
        pass
    cnx.rollback()
    print "Probando: EMPLEADO\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "Insertando un empleado duplicado"
    _id = 7774
    cursor.execute('SELECT * FROM EMPLEADO WHERE ID = 7774')
    data = cursor.fetchall()[0][0]
    max_type = get_max_num('EMPLEADO', 'ID')
    data[0] =  max_type+1
    data[7] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[7].strftime('%d/%m/%Y'))
    data[8] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[8].strftime('%d/%m/%Y'))
    try:
        cursor.execute('INSERT INTO EMPLEADO VALUES %s') % (str(data).replace("\"", ''))
        print "La tupla no debería ser insertada"
    except cx_Oracle.IntegrityError:
        pass
    print "Prueba 2: Restrcciones de LLave Foránea"
    print "Insertando un Empleado que no se encuentra registrado como USUARIO"
    max_type = get_max_num('USUARIO', 'ID')
    data[0] = max_type+1
    try:
        cursor.execute('INSERT INTO EMPLEADO VALUES %s') % (str(data).replace("\"", ''))
        print "La tupla no debería ser insertada"
    except cx_Oracle.IntegrityError:
        pass
    cnx.rollback()
    print "Probando: CLIENTE\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "Insertando un cliente duplicado"
    cursor.execute('SELECT * FROM CLIENTE WHERE ID = 1669')
    data = cursor.fetchall()[0][0]
    max_type = get_max_num('CLIENTE', 'ID')
    data[0] =  max_type+1
    data[7] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[7].strftime('%d/%m/%Y'))
    data[8] = "TO_DATE('%s' ,'dd/mm/yyyy')" % (data[8].strftime('%d/%m/%Y'))
    try:
        cursor.execute('INSERT INTO CLIENTE VALUES %s') % (str(data).replace("\"", ''))
        print "La tupla no debería ser insertada"
    except cx_Oracle.IntegrityError:
        pass
    print "Prueba 2: Restrcciones de LLave Foránea"
    print "Insertando un Cliente que no se encuentra registrado como USUARIO"
    max_type = get_max_num('USUARIO', 'ID')
    data[0] = max_type+1
    try:
        cursor.execute('INSERT INTO CLIENTE VALUES %s') % (str(data).replace("\"", ''))
        print "La tupla no debería ser insertada"
    except cx_Oracle.IntegrityError:
        pass
    cnx.rollback()
    print "Probando: CUENTA\n"
    print "Prueba 1: Unicidad de Llaves Primarias"
    print "Insertando una CUENTA duplicada"
    _id = 144
    cursor.execute('SELECT * FROM CUENTA WHERE NUMERO = '+_id)
    data = cursor.fetchall()[0][0]
    try:
        cursor.execute('INSERT INTO CUENTA VALUES %s' % (str(data)))
        print "La tupla no debería ser insertada"
    except cx_Oracle.IntegrityError:
        pass
    print "Prueba 2: Restricción de Llave Foránea"
    print "Insertando una Tupla que contiene un Cliente inexistente"
    max_num = get_max_num('CUENTA', 'NUMERO')




    

if __name__ == '__main__':
    manual_test()