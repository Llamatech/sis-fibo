#-*- coding:iso-8859-1 -*-

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
     'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL, OFICINA) VALUES %s'
s3 = 'INSERT INTO CLIENTE (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
     + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
     'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'
s4 = 'INSERT INTO OFICINA (ID, NOMBRE, DIRECCION, TELEFONO, GERENTE) VALUES %s'
s5 = 'INSERT INTO PUNTOSATENCION (ID, LOCALIZACION, OFICINA, TIPO) VALUES %s'


# cursor.execute('SELECT * FROM TIPOUSUARIO')
# u_type = cursor.fetchall()

# cursor.execute('SELECT * FROM TIPOIDENTIFICACION')
# id_type = cursor.fetchall()

# managers = []

uf = open('usuario.csv', 'wb')
cf = open('cliente.csv', 'wb')
ef = open('empleado.csv', 'wb')
of = open('oficina.csv', 'wb')
paf = open('puntos_atencion.csv', 'wb')


u_header = 'ID,PIN,EMAIL,TIPO\n'
c_header = 'ID,TIPO_DOCUMENTO,NUM_DOCUMENTO,' \
     + 'NOMBRE,APELLIDO,DIRECCION,TELEFONO,FECHA_INSCRIPCION,' +\
     'FECHA_NACIMIENTO,CIUDAD,DEPARTAMENTO,COD_POSTAL\n'
e_header = 'ID,TIPO_DOCUMENTO,NUM_DOCUMENTO,' \
     + 'NOMBRE,APELLIDO,DIRECCION,TELEFONO,FECHA_INSCRIPCION,' +\
     'FECHA_NACIMIENTO,CIUDAD,DEPARTAMENTO,COD_POSTAL,OFICINA\n'
o_header = 'ID,NOMBRE,DIRECCION,TELEFONO,GERENTE\n'
pa_header = 'ID,LOCALIZACION,OFICINA,TIPO\n'

uf.write(u_header)
ef.write(e_header)
cf.write(e_header)
of.write(o_header)
paf.write(pa_header)

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

def random_birth_date(start=1950, end=1993):
    year = random.randint(start, end)
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
    # print '%d/%d/%d' % (day, month, year) 
    return datetime.date(year, month, day)

# print 'Populating system admins...'
# for i in range(1, 21):
#     i_s = str(i)
#     b_date = random_birth_date()
#     admin = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              random.choice(ciudades), random.choice(departamentos), '0'*(6-len(str(i)))+str(i),)
#     #print admin
#     user = (i, 'admin'+str(i), 'admin'+str(i)+'@bancandes.com.co', 6)
#     line = str(admin).replace("\"", '')[1:-1].replace(', ', ',')+",\n" # stmt = s2 % str(admin).replace("\"", '')
#     line_2 = str(user)[1:-1]+"\n"
#     uf.write(line_2.replace(', ', ','))
#     ef.write(line)
#     # print str(admin).replace("\"", '')
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(admin).replace("\"", '')[0:-1]+', null)')
#     except cx_Oracle.IntegrityError:
#         pass

# cnx.commit()

# print 'Populating general bank managers...'
# for i in range(21, (102+21)):
#     i_s = str(i)
#     b_date = random_birth_date()
#     g_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              random.choice(ciudades), random.choice(departamentos), '0'*(6-len(str(i)))+str(i))
#     user = (i, 'gerente_general'+str(i-20), 'gerente_general'+str((i+1)-21)+'@bancandes.com.co', 3)
#     line_2 = str(g_manager).replace("\"", '')[1:-1].replace(', ', ',')+",\n"
#     line = str(user)[1:-1]+'\n'
#     uf.write(line.replace(', ', ','))
#     ef.write(line_2)
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(g_manager).replace("\"", '')[0:-1]+', null)')
#     except cx_Oracle.IntegrityError:
#         pass

# cnx.commit()

# print 'Populating bank offices...'
# atm_count = 0
# for i in range(123, 123+30):
#     i_s = str(i)
#     b_date = random_birth_date()
#     o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              'ciudad'+str(i-122), 'departamento'+str(i-122), '0'*(6-len(str(i)))+str(i), i-122)
#     user = (i, 'gerente_oficina'+str(i-122), 'gerente_oficina'+str((i+1)-123)+'@bancandes.com.co', 4)
#     office = (i-122, 'oficina'+str(i-122), 'direccion'+str(i-122), 'telefono'+str(i), i)
#     pa = (i+atm_count-122, 'ciudad'+str(i-122), i-122, 3)
#     line = str(o_manager).replace("\"", '')[1:-1].replace(', ', ',')+"\n"
#     line_2 = str(user)[1:-1]+'\n'
#     line_3 = str(office)[1:-1]+'\n'
#     line_4 = str(pa)[1:-1]+'\n'
#     ef.write(line.replace(', ', ','))
#     uf.write(line_2.replace(', ', ','))
#     of.write(line_3.replace(', ', ','))
#     paf.write(line_4.replace(', ', ','))
#     atm_count += 1
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(o_manager).replace("\"", ''))
#         cursor.execute(s4 % str(office))
#         cursor.execute(s5 % str(pa))
#     except cx_Oracle.IntegrityError:
#         pass 
#     for j in range(0, 3):
#         atm = (i+j+atm_count-122, 'ciudad'+str(i-122), i-122, 1)
#         line = str(atm)[1:-1]+'\n'
#         paf.write(line.replace(', ', ','))
#         # print pa
#         # print atm
#         try:
#             cursor.execute(s5 % str(atm))
#         except cx_Oracle.IntegrityError:
#             pass
#     atm_count += 2

# cnx.commit()

# city_count = i-122
# for i in range(153, 153+50):
#     i_s = str(i)
#     b_date = random_birth_date()
#     o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              'ciudad'+str(city_count+1), 'departamento'+str(city_count+1), '0'*(6-len(str(i)))+str(i), i-122)
#     user = (i, 'gerente_oficina'+str(i-122), 'gerente_oficina'+str((i+1)-123)+'@bancandes.com.co', 4)
#     line = str(o_manager).replace("\"", '')[1:-1].replace(', ', ',')+"\n"
#     office = (i-122, 'oficina'+str(i-122), 'direccion'+str(i-122), 'telefono'+str(i), i)
#     pa = (i+atm_count-122, 'ciudad'+str(city_count+1), i-122, 3)
#     line_2 = str(user)[1:-1]+'\n'
#     line_3 = str(office)[1:-1]+'\n'
#     line_4 = str(pa)[1:-1]+'\n'
#     ef.write(line.replace(', ', ','))
#     uf.write(line_2.replace(', ', ','))
#     of.write(line_3.replace(', ', ','))
#     paf.write(line_4.replace(', ', ','))
#     atm_count += 1
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(o_manager).replace("\"", ''))
#         cursor.execute(s4 % str(office))
#         cursor.execute(s5 % str(pa))
#     except cx_Oracle.IntegrityError:
#         pass
#     for j in range(0, 3):
#         atm = (i+j+atm_count-122, 'ciudad'+str(city_count+1), i-122, 1)
#         line = str(atm)[1:-1]+'\n'
#         paf.write(line.replace(', ', ','))
#         try:
#             cursor.execute(s5 % str(atm))
#         except cx_Oracle.IntegrityError:
#             pass
#     atm_count += 2

# cnx.commit()

# city_count += 1
# num_offices = 0
# for i in range(203, 203+3*20):
#     i_s = str(i)
#     b_date = random_birth_date()
#     o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              'ciudad'+str(city_count+1), 'departamento'+str(city_count+1), '0'*(6-len(str(i)))+str(i), i-122)
#     user = (i, 'gerente_oficina'+str(i-122), 'gerente_oficina'+str((i+1)-123)+'@bancandes.com.co', 4)
#     line = str(o_manager).replace("\"", '')[1:-1].replace(', ', ',')+"\n"
#     office = (i-122, 'oficina'+str(i-122), 'direccion'+str(i-122), 'telefono'+str(i), i)
#     pa = (i+atm_count-122, 'ciudad'+str(city_count+1), i-122, 3)
#     line_2 = str(user)[1:-1]+'\n'
#     line_3 = str(office)[1:-1]+'\n'
#     line_4 = str(pa)[1:-1]+'\n'
#     ef.write(line.replace(', ', ','))
#     uf.write(line_2.replace(', ', ','))
#     of.write(line_3.replace(', ', ','))
#     paf.write(line_4.replace(', ', ','))
#     atm_count += 1
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(o_manager).replace("\"", ''))
#         cursor.execute(s4 % str(office))
#         cursor.execute(s5 % str(pa))
#     except cx_Oracle.IntegrityError:
#         pass
#     for j in range(0, 3):
#         atm = (i+j+atm_count-122, 'ciudad'+str(city_count+1), i-122, 1)
#         line = str(atm)[1:-1]+'\n'
#         paf.write(line.replace(', ', ','))
#         try:
#             cursor.execute(s5 % str(atm))
#         except cx_Oracle.IntegrityError:
#             pass
#     atm_count += 2
#     num_offices += 1
#     if num_offices % 20 == 0:
#        city_count += 1   

# cnx.commit()
# # city_count += 1
# num_offices = 0
# for i in range(263, 263+2*40):
#     i_s = str(i)
#     b_date = random_birth_date()
#     o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              'ciudad'+str(city_count), 'departamento'+str(city_count), '0'*(6-len(str(i)))+str(i), i-122)
#     user = (i, 'gerente_oficina'+str(i-122), 'gerente_oficina'+str((i+1)-123)+'@bancandes.com.co', 4)
#     line = str(o_manager).replace("\"", '')[1:-1].replace(', ', ',')+"\n"
#     office = (i-122, 'oficina'+str(i-122), 'direccion'+str(i-122), 'telefono'+str(i), i)
#     pa = (i+atm_count-122, 'ciudad'+str(city_count+1), i-122, 3)
#     line_2 = str(user)[1:-1]+'\n'
#     line_3 = str(office)[1:-1]+'\n'
#     line_4 = str(pa)[1:-1]+'\n'
#     ef.write(line.replace(', ', ','))
#     uf.write(line_2.replace(', ', ','))
#     of.write(line_3.replace(', ', ','))
#     paf.write(line_4.replace(', ', ','))
#     atm_count += 1
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(o_manager).replace("\"", ''))
#         cursor.execute(s4 % str(office))
#         cursor.execute(s5 % str(pa))
#     except cx_Oracle.IntegrityError:
#         pass
#     for j in range(0, 3):
#         atm = (i+j+atm_count-122, 'ciudad'+str(city_count+1), i-122, 1)
#         line = str(atm)[1:-1]+'\n'
#         paf.write(line.replace(', ', ','))
#         try:
#             cursor.execute(s5 % str(atm))
#         except cx_Oracle.IntegrityError:
#             pass
#     atm_count += 2
#     num_offices += 1
#     if num_offices % 40 == 0:
#        city_count += 1
# cnx.commit()
# # city_count += 1
# num_offices = 0
# for i in range(343, 343+10*3):
#     i_s = str(i)
#     b_date = random_birth_date()
#     o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              'ciudad'+str(city_count), 'departamento'+str(city_count), '0'*(6-len(str(i)))+str(i), i-122)
#     user = (i, 'gerente_oficina'+str(i-122), 'gerente_oficina'+str((i+1)-123)+'@bancandes.com.co', 4)
#     line = str(o_manager).replace("\"", '')[1:-1].replace(', ', ',')+"\n"
#     office = (i-122, 'oficina'+str(i-122), 'direccion'+str(i-122), 'telefono'+str(i), i)
#     pa = (i+atm_count-122, 'ciudad'+str(city_count+1), i-122, 3)
#     line_2 = str(user)[1:-1]+'\n'
#     line_3 = str(office)[1:-1]+'\n'
#     line_4 = str(pa)[1:-1]+'\n'
#     ef.write(line.replace(', ', ','))
#     uf.write(line_2.replace(', ', ','))
#     of.write(line_3.replace(', ', ','))
#     paf.write(line_4.replace(', ', ','))
#     atm_count += 1
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(o_manager).replace("\"", ''))
#         cursor.execute(s4 % str(office))
#         cursor.execute(s5 % str(pa))
#     except cx_Oracle.IntegrityError:
#         pass
#     for j in range(0, 3):
#         atm = (i+j+atm_count-122, 'ciudad'+str(city_count+1), i-122, 1)
#         line = str(atm)[1:-1]+'\n'
#         paf.write(line.replace(', ', ','))
#         try:
#             cursor.execute(s5 % str(atm))
#         except cx_Oracle.IntegrityError:
#             pass
#     atm_count += 2
#     num_offices += 1
#     if num_offices % 3 == 0:
#        city_count += 1

# # city_count += 1
# num_offices = 0
# for i in range(373, 373+14*4):
#     i_s = str(i)
#     b_date = random_birth_date()
#     o_manager = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              'ciudad'+str(city_count), 'departamento'+str(city_count), '0'*(6-len(str(i)))+str(i), i-122)
#     user = (i, 'gerente_oficina'+str(i-122), 'gerente_oficina'+str((i+1)-123)+'@bancandes.com.co', 4)
#     line = str(o_manager).replace("\"", '')[1:-1].replace(', ', ',')+"\n"
#     office = (i-122, 'oficina'+str(i-122), 'direccion'+str(i-122), 'telefono'+str(i), i)
#     pa = (i+atm_count-122, 'ciudad'+str(city_count+1), i-122, 3)
#     line_2 = str(user)[1:-1]+'\n'
#     line_3 = str(office)[1:-1]+'\n'
#     line_4 = str(pa)[1:-1]+'\n'
#     ef.write(line.replace(', ', ','))
#     uf.write(line_2.replace(', ', ','))
#     of.write(line_3.replace(', ', ','))
#     paf.write(line_4.replace(', ', ','))
#     atm_count += 1
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(o_manager).replace("\"", ''))
#         cursor.execute(s4 % str(office))
#         cursor.execute(s5 % str(pa))
#     except cx_Oracle.IntegrityError:
#         pass
#     for j in range(0, 3):
#         atm = (i+j+atm_count-122, 'ciudad'+str(city_count+1), i-122, 1)
#         line = str(atm)[1:-1]+'\n'
#         paf.write(line.replace(', ', ','))
#         try:
#             cursor.execute(s5 % str(atm))
#         except cx_Oracle.IntegrityError:
#             pass
#     atm_count += 2
#     num_offices += 1
#     if num_offices % 4 == 0:
#        city_count += 1
# cnx.commit()

def get_office_info(id):
    cursor.execute('SELECT p.localizacion FROM OFICINA o, PUNTOSATENCION p WHERE o.id = %d AND p.oficina = o.id AND p.tipo = 3' % (id))
    loc = cursor.fetchall()
    # print id,loc
    return loc[0][0]



# print "Creating bank clerks..."
# count = 0
# office_id = 1
# city = get_office_info(office_id)
# for i in range(429, 429+306*4):
#     i_s = str(i)
#     b_date = random_birth_date()
#     clerk = (i, 2, "cedula" + i_s, "empleado" + i_s, 
#              "apellido" + i_s, "direccion" + i_s, "telefono"+i_s, 
#              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
#              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
#              city, 'departamento'+city[-1], '0'*(6-len(str(i)))+str(i), office_id)
#     user = (i, 'cajero'+str(i-428), 'cajero'+str(i-428)+'@bancandes.com.co', 5)
#     uf.write(str(user)[1:-1]+'\n'.replace(', ', ','))
#     ef.write(str(clerk)[1:-1]+'\n'.replace(', ', ',').replace("\"", ''))
#     try:
#         cursor.execute(s % str(user))
#         cursor.execute(s2 % str(clerk).replace("\"", ''))
#     except cx_Oracle.IntegrityError:
#         pass
#     count += 1
#     if count % 4 == 0:
#         office_id += 1
#         try:
#             city = get_office_info(office_id)
#         except IndexError:
#             pass


# cnx.commit()
#Tipo Documento:
#1,Tarjeta de Identidad : 1998-2003
#2,Cedula de Ciudadanía: -1997
#4,Pasaporte: -2003
#3,Cédula de Extranjería: -1997
#5, NIT: Debe ser una persona jurídica

#Tipo Usuario:
#1, Cliente Natural
#2, Cliente Jurídico

num_ti = 1
num_passport = 1
num_cc = i+1
num_ce = 1
num_nit = 1

doc_info = {1:[(1998, 2003),"num_ti", "tarjetai", 'cliente'], 2:[(1920, 1997),"num_cc", 'cedula', 'cliente'],
            3:[(1920, 1997), "num_ce", 'cedulae', 'cliente'], 4:[(1920, 2003), "num_passport", 'pasaporte', 'cliente'],
            5:[(1900, 2015), "num_nit", 'nit', 'empresa']}

def get_id_doc(idx):
    doc = random.choice(doc_info.keys())
    years, count, prefix, name = doc_info[doc]
    b_year = random_birth_date(years[0], years[1])
    doc_num = prefix+str(eval(count))
    instr = compile(count+' += 1', '<string>', 'exec')
    exec instr
    name = name+str(idx)
    lastname = 'apellido'+str(random.randint(1, idx))
    if doc == 5:
       name = name+str(num_nit)
       lastname = 'null'
    return b_year, doc_num, doc, name, lastname

office_id = 1
city = get_office_info(office_id)

print "Populating bank users..."
for i in range(1653, 1653+20*306):
    i_s = str(i)
    u_type = random.choice([1,2])
    b_date, doc_num, doc_t, name, lastname = get_id_doc(i-1652)
    client = (i, doc_t, doc_num, name, 
              "%s", "direccion" + i_s, "telefono"+ i_s, 
              "TO_DATE('"+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+"', 'dd/mm/yyyy')",
              "TO_DATE('"+str(b_date.day)+'/'+str(b_date.month)+'/'+str(b_date.year)+"', 'dd/mm/yyyy')",
              city, 'departamento'+city[-1], '0'*(6-len(str(i)))+str(i))
    client_str = str(client).replace("\"", '') % (lastname)
    print client_str


       

uf.close()
cf.close()
ef.close()
of.close()
paf.close()
cursor.close()
cnx.close()