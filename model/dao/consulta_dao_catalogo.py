#-*- coding:iso-8859-1 -*-

import os
import sys
import cx_Oracle
from model.vos import tipo
from model.vos import usuario
from model.vos import oficina
from model.vos import empleado
from model.vos import puntos_atencion


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
        stmt = "SELECT * FROM %s WHERE TIPO <> 'NIT' AND TIPO <> 'Tarjeta de Identidad'" % (tabla_consulta)
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

    def obtener_tipo_documento_R(self):
        tabla_consulta = 'TIPOIDENTIFICACION'
        stmt = "SELECT * FROM %s WHERE TIPO" % (tabla_consulta)
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
        stmt = 'SELECT * FROM %s WHERE ID > 2' % (tabla_consulta)
        self.establecer_conexion()
        cur = self.conn.cursor()
        tipo_usuario_l = []
        try:
            cur.execute(stmt)
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

    def obtener_tipo_usuarioR(self):
        tabla_consulta = 'TIPOUSUARIO'
        stmt = 'SELECT * FROM %s WHERE ID <= 2' % (tabla_consulta)
        self.establecer_conexion()
        cur = self.conn.cursor()
        tipo_usuario_l = []
        try:
            cur.execute(stmt)
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

    def obtener_oficinas(self):
        tabla_consulta = 'OFICINA'
        stmt = 'SELECT * FROM %s ORDER BY ID' % (tabla_consulta)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        offices = []
        for t in data:
            offices.append(oficina.Oficina(t[0], t[1], t[2], t[3], t[4]))
        # print offices
        return offices

    def registrar_oficina(self, name, address, phone, id_manager):
        stmt = 'SELECT max(id) FROM OFICINA'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        numero = cur.fetchall()[0][0]
        stmt = 'INSERT INTO OFICINA VALUES ('+"'"+str(numero+1)+"','"+name+"','"+address+"','"+phone+"',"+str(id_manager)+")"
        print(stmt)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        stmt2 = 'UPDATE EMPLEADO SET OFICINA = %d WHERE ID = %d' % (numero+1, id_manager)
        cur.execute(stmt2)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

    def registrar_empleado(self, usuario, empleado):
        stmt = 'INSERT INTO USUARIO (ID, PIN, EMAIL, TIPO) VALUES %s'
        stmt_2 = 'INSERT INTO EMPLEADO (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
                 + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
                 'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL, OFICINA) VALUES %s'
        g_oficina = self.es_gerente_oficina(usuario.tipo)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute('SELECT max(ID) FROM USUARIO')
        user_id = cur.fetchall()[0][0]+1
        empleado.id = user_id
        usuario.id = user_id
        print str(empleado)
        cur.execute(stmt % (str(usuario)))
        cur.execute(stmt_2 % (str(empleado)))
        if g_oficina:
            cur.execute('UPDATE OFICINA SET GERENTE = %d WHERE ID = %d' % (empleado.id, empleado.oficina))
        self.conn.commit()
        cur.close()
        self.conn.close()

    def obtener_elementos_ordenados(self, tab, col, order, a, b):
        stmt = """SELECT * FROM
                    (SELECT u.*, ROWNUM r
                      FROM
                      (SELECT * 
                       FROM %s
                       ORDER BY LPAD(%s, 30) %s) u)
                  WHERE r >= %d AND r <= %d
               """
        stmt = stmt % (tab, col, order, a, b)
        print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        data = map(lambda x: x[0:-1], data)
        cur.close()
        self.conn.close()
        return data

    def obtener_empleados(self, col='ID', orden='ASC', a=0, b=100):
        view = 'EMP_SIMP'
        #22, 'Cedula de Ciudadania', 'cedula22', 'empleado22', 'apellido22', 'ciudad21', None, None, 'gerente_general2@bancandes.com.co', 3, 'Gerente General'
        #TIPO_DOC,NUM_DOCUMENTO,NOMBRE,APELLIDO,CIUDAD,ID_OFICINA,NOMBRE_OFICINA,EMAIL,TIPO_U,ID,TIPO_UN
        info = self.obtener_elementos_ordenados(view, col, orden, a, b)

        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute('SELECT count(*) FROM EMP_SIMP')
        count = cur.fetchall()[0][0]
        cur.close()
        self.conn.close()

        data = map(lambda x: empleado.EmpleadoR(x[0], x[1], x[2], x[3], x[4], 
                                                x[5], x[6], x[7], x[8], x[9], x[10]), info)
        return count, data

    def es_gerente_oficina(self, tipo_usuario):
        stmt = 'SELECT TIPO FROM TIPOUSUARIO WHERE ID = %d' % (tipo_usuario)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        result = cur.fetchall()
        cur.close()
        self.conn.close()
        if result[0][0] == 'Gerente general':
            return True
        return False

    def eliminar_empleado(self, _id, tipo_usuario, oficina):
        stmt = 'DELETE FROM EMPLEADO WHERE ID = %d' % (_id)
        stmt2 = 'DELETE FROM USUARIO WHERE ID = %d' % (_id)
        g_oficina = self.es_gerente_oficina(tipo_usuario)
        self.establecer_conexion()
        cur = self.conn.cursor()
        try:
            cur.execute(stmt)
            cur.execute(stmt2)
            if g_oficina:
                cur.execute('UPDATE OFICINA SET GERENTE = null WHERE ID = %d' % (oficina))
        except cx_Oracle.Error, e:
            self.conn.rollback()
            raise e
        self.conn.commit()
        cur.close()
        self.conn.close()

    def buscar_usuario(self, _id):
        stmt = 'SELECT * FROM USUARIO WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        t = data[0]
        _usuario = usuario.Usuario(t[0], t[1], t[2], t[3])
        return _usuario

    def buscar_empleado(self, _id):
        stmt = 'SELECT * FROM EMPLEADO WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        t = data[0]
        empl = empleado.Empleado(t[0], t[1], t[2], t[3], t[4],
                                 t[5], t[6], t[7], t[8], t[9],
                                 t[10], t[11], t[12])
        return empl

    def actualizar_empleado(self, _usuario, _empleado):
        stmt = "UPDATE USUARIO SET PIN = '%s', TIPO = %d WHERE ID = %d"
        stmt_alt = "UPDATE USUARIO SET TIPO = %d WHERE ID = %d"
        stmt2 = """UPDATE EMPLEADO 
                   SET TIPO_DOCUMENTO = %d,
                       NUM_DOCUMENTO = '%s',
                       NOMBRE = '%s',
                       APELLIDO = '%s',
                       DIRECCION = '%s',
                       TELEFONO = '%s',
                       CIUDAD = '%s',
                       DEPARTAMENTO = '%s',
                       COD_POSTAL = '%s',
                       OFICINA = %d
                    WHERE ID = %d
                """
        if _usuario.pwd != '': 
            stmt = stmt % (_usuario.pwd, _usuario.tipo, _usuario.id)
        else:
            stmt = stmt_alt % (_usuario.tipo, _usuario.id)
        stmt2 = stmt2 % (_empleado.tipo_doc, _empleado.num_documento,
                         _empleado.nombre, _empleado.apellido,
                         _empleado.direccion, _empleado.telefono,
                         _empleado.ciudad, _empleado.departamento,
                         _empleado.cod_postal, _empleado.oficina,
                         _empleado.id)

        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        cur.execute(stmt2)
        self.conn.commit()
        cur.close()
        self.conn.close()
        # stmt3 = 'UPDATE OFICINA SET GERENTE = null WHERE ID = %d' % (oficina)

    def obtener_oficinasL(self, col='ID', orden='ASC', a=0, b=100):
        view = 'OFICINA_SIMP'
        #22, 'Cedula de Ciudadania', 'cedula22', 'empleado22', 'apellido22', 'ciudad21', None, None, 'gerente_general2@bancandes.com.co', 3, 'Gerente General'
        #TIPO_DOC,NUM_DOCUMENTO,NOMBRE,APELLIDO,CIUDAD,ID_OFICINA,NOMBRE_OFICINA,EMAIL,TIPO_U,ID,TIPO_UN
        info = self.obtener_elementos_ordenados(view, col, orden, a, b)

        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute('SELECT count(*) FROM OFICINA_SIMP')
        count = cur.fetchall()[0][0]
        cur.close()
        self.conn.close()
        data = map(lambda x: oficina.OficinaR(x[0], x[1], x[2], x[3], x[4], x[5], x[6]), info)
        return count, data

    def obtener_gerentes_oficinaC(self, search_term):
        search_term = "'"+search_term+"%'"
        stmt = """SELECT * FROM EMP_SIMP WHERE
                  (TO_CHAR(ID) LIKE %s OR
                  EMAIL LIKE %s OR
                  NUM_DOCUMENTO LIKE %s)
                  AND TIPO_U = 4
                  ORDER BY ID"""
        stmt = stmt % (search_term, search_term, search_term)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: empleado.EmpleadoR(x[0], x[1], x[2], x[3], x[4], 
                                                x[5], x[6], x[7], x[8], x[9], x[10]), data)
        return data

    def eliminar_oficina(self, _id, gerente):
        stmt_0 = 'UPDATE EMPLEADO SET OFICINA = null WHERE OFICINA = %d' % (_id)
        stmt = 'DELETE FROM PUNTOSATENCION WHERE OFICINA = %d' % (_id)
        stmt_3 = 'DELETE FROM OFICINA WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt_0)
        cur.execute(stmt)
        print "First statement executed!"
        print stmt_3
        cur.execute(stmt_3)
        self.conn.commit()
        cur.close()
        self.conn.close()
        print "Third statement executed!"

    def obtener_oficina(self, _id):
        stmt = 'SELECT * FROM OFICINA WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        data = data[0]
        office = oficina.Oficina(data[0], data[1], data[2], data[3], data[4])
        stmt2 = 'SELECT * FROM EMP_SIMP WHERE ID = %d' % (office.gerente)
        cur.execute(stmt2)
        x = cur.fetchall()[0]
        cur.close()
        self.conn.close()
        gerente = empleado.EmpleadoR(x[0], x[1], x[2], x[3], x[4], 
                                     x[5], x[6], x[7], x[8], x[9], x[10])
        return office, gerente

    def actualizar_oficina(self, _id, name, phone, address, idGerente):
        stmt = 'SELECT * FROM OFICINA WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        data = data[0]
        office = oficina.Oficina(data[0], data[1], data[2], data[3], data[4])
        values = ''
        if office.nombre != name:
            values += "NOMBRE = '%s'\n" % (name)
        if office.telefono != phone:
            values += "TELEFONO = '%s'\n" % (phone)
        if office.direccion != address:
            values += "DIRECCION = '%s'\n" % (address)
        if office.gerente != idGerente:
            stmt2 = 'UPDATE EMPLEADO SET OFICINA = null WHERE ID = %d' % (office.gerente)
            stmt3 = 'UPDATE EMPLEADO SET OFICINA = %d WHERE ID = %d' % (_id, idGerente)
            cur.execute(stmt2)
            cur.execute(stmt3)
            values += 'GERENTE = %d\n' % (idGerente)
        if values != '':
            upd_stmt = 'UPDATE OFICINA SET %s WHERE ID = %d' % (values, _id)
            cur.execute(upd_stmt)
            self.conn.commit()
            cur.close()
            self.conn.close() 

    def obtener_oficinasC(self, search_term):
        search_term = "'"+search_term+"%'"
        stmt = """SELECT * FROM OFICINA WHERE
                  TO_CHAR(ID) LIKE %s OR
                  NOMBRE LIKE %s
                  ORDER BY ID"""
        stmt = stmt % (search_term, search_term)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: oficina.OficinaR(x[0], None, x[1], x[2], x[3], x[4], None), data)
        return data

    def obtener_puntos_atL(self, col='ID', orden='ASC', a=0, b=100):
        view = 'PA_SIMP'
        #22, 'Cedula de Ciudadania', 'cedula22', 'empleado22', 'apellido22', 'ciudad21', None, None, 'gerente_general2@bancandes.com.co', 3, 'Gerente General'
        #TIPO_DOC,NUM_DOCUMENTO,NOMBRE,APELLIDO,CIUDAD,ID_OFICINA,NOMBRE_OFICINA,EMAIL,TIPO_U,ID,TIPO_UN
        info = self.obtener_elementos_ordenados(view, col, orden, a, b)

        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute('SELECT count(*) FROM PA_SIMP')
        count = cur.fetchall()[0][0]
        cur.close()
        self.conn.close()
        print info
        data = map(lambda x: puntos_atencion.PuntoAtencionR(x[0], x[1], x[2], x[3], x[4]), info)
        print data
        return count, data

    def obtener_tipo_pa(self):
        stmt = 'SELECT * FROM TIPOPUNTOSATENCION'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: tipo.TipoPuntoAtencion(x[0], x[1]), data)
        return data

    def registrar_pa(self, localizacion, tipo, oficina):
        id_stmt = 'SELECT max(ID) FROM PUNTOSATENCION'
        stmt = 'INSERT INTO PUNTOSATENCION(ID, LOCALIZACION, TIPO, OFICINA) VALUES %s'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(id_stmt)
        _id = cur.fetchall()[0][0]+1
        values = "(%d, '%s', %d" % (_id, localizacion, tipo)
        if oficina < 0:
            values += ', null)'
        else:
            values += ', %d)' % (oficina)
        stmt = stmt % (values)
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def eliminar_pa(self, _id):
        stmt = 'DELETE FROM PUNTOSATENCION WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def actualizar_pa(self, _id, localizacion, tipo, oficina):
        stmt = """UPDATE PUNTOSATENCION 
                  SET localizacion = '%s',
                      tipo = %d,
                  """ % (localizacion, tipo)
        if oficina < 0:
            stmt += 'oficina = null\n'
        else:
            stmt += 'oficina = %d\n' % (oficina)
        stmt += "WHERE ID = %d" % (_id)
        print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def obtener_pa(self, _id):
        stmt = 'SELECT * FROM PA_SIMP WHERE ID = %d' % (_id)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = data[0]
        return puntos_atencion.PuntoAtencionR(data[0], data[1], data[2], data[3], data[4])



# SELECT * FROM
# (SELECT u.*, ROWNUM r
# FROM
# (SELECT * 
# FROM EMPLEADO
# ORDER BY LPAD(NUM_DOCUMENTO, 30) ASC) u)
# WHERE r >= 1 AND r <= 100;