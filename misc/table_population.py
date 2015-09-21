import os
import base64
import random
import datetime
import cx_Oracle

"""
BancAndes en números:
Cobertura
---------------------------
60 ciudades:
    30 Ciudades: 1 Oficina
    1 Ciudad: 50 Oficinas
    3 Ciudades: 20 Oficinas
    2 Ciudades: 40 Oficinas
    10 Ciudades: 3 Oficinas
    14 Ciudades: 4 Oficinas
---------------------------
Total Oficinas: 306
Reglas de asignación de empleados
---------------------------------
Administradores: 1 x 5 Gerente General
Gerente General: 3 x Gerente Oficina
Gerente Oficina: 1 x Oficina
Cajero: 4 x Oficina 
Empleados:
------------------------------------
Administradores: 20 Funcionarios
Gerentes Generales: 102 Funcionarios
Gerentes Oficina: 306 Funcionarios
Cajeros: 1224 Funcionarios
------------------------------------
Total Empleados: 1652
Clientes:
------------------------
Clientes Naturales: 1500
Clientes Jurídicos: 500
------------------------
Total Clientes: 3000
"""

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
     + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
     'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'
s3 = 'INSERT INTO CLIENTE (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
     + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
     'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'
s4 = 'INSERT INTO OFICINA (ID, NOMBRE, DIRECCION, TELEFONO, GERENTE) VALUES %s'
s5 = 'INSERT INTO PUNTOSATENCION (ID, LOCALIZACION, OFICINA, TIPO) VALUES %s'


cursor.execute('SELECT * FROM TIPOUSUARIO')
u_type = cursor.fetchall()

cursor.execute('SELECT * FROM TIPOIDENTIFICACION')
id_type = cursor.fetchall()

managers = []

# Empleado: ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,
#          NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION,
#          FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL

ciudades = ['ciudad' + str(i) for i in range(1, 60)]
departamentos = ['departamento'+str(i) for i in range(1, 35)]

date = datetime.date.today()

def leap_year(year):
    r = False
    if year % 4 == 0:
       r = True
    elif year % 100 == 0:
       r = True
    elif year % 400 == 0:
       r = True
    return r 

def random_birth_date():
    year = random.randint(1950, 1993)
    month = random.randint(1, 12)
    day_end = 31
    if month == 2:
       if leap_year(year):
          day_end = 29
       else:
          day_end = 28
    elif month < 8:
        if month % 2 == 0:
           day_end = 30
    else:
        if month % 2 != 0:
           day_end = 30
    day = random.randint(1, day_end) 
    print '%d/%d/%d' % (day, month, year) 
    return datetime.date(year, month, day)

for i in range(1, 21):
    i_s = str(i)
    b_date = random_birth_date()
    admin = (i, 2, "cedula" + i_s, "empleado" + i_s, 
             "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
             "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
             "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
             random.choice(ciudades), random.choice(departamentos), '0'*(6-len(str(i)))+str(i))
    #print admin
    stmt = s2 % str(admin).replace("\"", '')
    cursor.execute(stmt)
    stmt = s % str((i, 'contrasena'+str(i), 'admin'+str(i)+'@bancandes.com.co', 6))
    cursor.execute(stmt)
    cnx.commit()

for i in range(22, (102+22)+1):
    i_s = str(i)
    b_date = random_birth_date()
    g_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
             "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
             "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
             "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
             random.choice(ciudades), random.choice(departamentos), '0'*(6-len(str(i)))+str(i))
    stmt = s2 % str(g_manager).replace("\"", '')
    cursor.execute(stmt)
    stmt = s % str((i, 'contrasena'+str(i), 'gerente_general'+str((i+1)-22)+'@bancandes.com.co', 3))
    cursor.execute(stmt)
    cnx.commit()
    stmt = s4 % str()

for i in range(125, 125+31):
    i_s = str(i)
    b_date = random_birth_date()
    o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
             "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
             "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
             "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
             'ciudad'+str(i-124), random.choice(departamentos), '0'*(6-len(str(i)))+str(i))
    stmt = s2 % str(g_manager).replace("\"", '')
    cursor.execute(stmt)
    stmt = s % str((i, 'contrasena'+str(i), 'gerente_oficina'+str((i+1)-125)+'@bancandes.com.co', 4))
    cursor.execute(stmt)
    cnx.commit()
    #ID, NOMBRE, DIRECCION, TELEFONO, GERENTE
    office = (i-124, 'oficina'+str(i-124), 'direccion'+str(i-124), 'telefono'+str(i), i)
    stmt = s4 % str(office)
    cursor.execute(stmt)
    cnx.commit()
    # ID, LOCALIZACION, OFICINA, TIPO
    stmt = s5 % str((i-124, 'ciudad'+str(i-124), i-124, 3))
    cursor.execute(stmt)
    cnx.commit()
    stmt = "UPDATE EMPLEADO SET OFICINA = "+str(i-124)+" WHERE ID = "+str(i)
    cursor.execute(stmt)
    cnx.commit()
    for j in range(0, 3):
        stmt = s5 % str((i-124+j+1, 'ciudad'+str(i-124), i-124, 1))
        cursor.execute(stmt)
    cnx.commit()

for i in range(156, 155+51):
    i_s = str(i)
    b_date = random_birth_date()
    o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
             "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
             "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
             "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
             'ciudad31', random.choice(departamentos), '0'*(6-len(str(i)))+str(i))
    stmt = s2 % str(g_manager).replace("\"", '')
    cursor.execute(stmt)
    stmt = s % str((i, 'contrasena'+str(i), 'gerente_oficina'+str((i+1)-156)+'@bancandes.com.co', 4))
    cursor.execute(stmt)
    cnx.commit()
    office = (i-155, 'oficina'+str(i-155), 'direccion'+str(i-155), 'telefono'+str(i), i)
    stmt = s4 % str(office)
    cursor.execute(stmt)
    cnx.commit()
    stmt = s5 % str((i-155, 'ciudad31', i-155, 3))
    cursor.execute(stmt)
    cnx.commit()
    stmt = "UPDATE EMPLEADO SET OFICINA = "+str(i-155)+" WHERE ID = "+str(i)
    cursor.execute(stmt)
    cnx.commit()
    for j in range(0, 3):
        stmt = s5 % str((i-156+j+1, 'ciudad31', i-155, 1))
        cursor.execute(stmt)
    cnx.commit()    

count = 0
for i in range(206, 210):
    for j in range(0, 21):
        i_s = str(i+j+count)
        b_date = random_birth_date()
        o_manager = (i+j+count, 2, "cedula" + i_s, "empleado" + i_s, 
                "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
                "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
                "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
                'ciudad'+str(i-205), random.choice(departamentos), '0'*(6-len(str(i+j+count)))+str(i+j+count))
        stmt = s2 % str(g_manager).replace("\"", '')
        cursor.execute(stmt)
        stmt = s % str((i+j+count, 'contrasena'+str(i+j+count), 'gerente_oficina'+str((i+j+count)-205)+'@bancandes.com.co', 4))
        cursor.execute(stmt)
        cnx.commit()
        office = (i+j+count-205, 'oficina'+str(i+j+count-205), 'direccion'+str(i+j+count-205), 'telefono'+str(i+j+count-205), i+j+count)
        stmt = s4 % str(office)
        cursor.execute(stmt)
        cnx.commit()
        stmt = s5 % str((i+j+count-205, 'ciudad'+str(i-205), i+j+count-205, 3))
        cursor.execute(stmt)
        cnx.commit()
        for k in range(0, 3):
            stmt = s5 % str((i-206+k+1, 'ciudad31', i-156, 1))
        cursor.execute(stmt)