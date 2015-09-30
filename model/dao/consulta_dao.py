#-*- coding:iso-8859-1 -*-

import os
import sys
import cx_Oracle
from model.vos import tipo
from model.vos import cuenta
from model.vos import usuario
from model.vos import cliente
from model.vos import prestamo


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

    def obtener_clientes(self):
        stmt = 'SELECT * FROM CLIENTE_INF'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: cliente.ClienteR(x[0], x[1], x[2], x[3], x[4], x[5], x[6]), data)
        return data

    def registrar_cliente(self, _usuario, _cliente):
        stmt = 'INSERT INTO USUARIO(ID, PIN, EMAIL, TIPO) VALUES %s'
        stmt_2 = 'INSERT INTO CLIENTE (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
                 + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
                 'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'
        stmt = stmt % (str(_usuario))
        stmt_2 = stmt_2 % (str(_cliente))
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        cur.execute(stmt_2)
        self.conn.commit()
        cur.close()
        self.conn.close()
    

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

    def obtener_tipo_prestamo(self):
        stmt = 'SELECT * FROM TIPOPRESTAMO'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: tipo.TipoPrestamo(x[0], x[1]), data)
        return data

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
        if numero == 'None':
            numero='1'
        stmt = 'INSERT INTO CUENTA VALUES ('+"'"+str(numero+1)+"','"+saldo+"','"+tipo+"','N','"+idCliente+"','"+str(idOficina)+ "')"
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

    def get_id_oficina(self, idGerente):
        stmt = " SELECT id FROM OFICINA WHERE " + "gerente = '" + \
        str(idGerente) + "'"
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
        stmt = "SELECT * FROM CUENTA where cliente = " + "'"+str(idUsuario)+ "'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cuentas = []
        for t in data:
            cuentaa = cuenta.Cuenta(t[0], t[1], t[2], t[3], t[4], t[5])
            cuentas.append(cuentaa)
        cur.close()
        self.conn.close()
        return cuentas

    def es_cajero(self, idUsuario):
        stmt = "SELECT * FROM USUARIO u, TIPOUSUARIO t WHERE u.tipo = t.id AND t.tipo='Cajero' AND u.id="+"'"+idUsuario+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        if len(data) > 0:
            return True
        else:
            return False

    def generar_numero_operacion(self):
        stmt = "SELECT max(numero) FROM OPERACION"
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        if data[0][0]=='None':
            return '1'
        else: 
            return str(int(data[0][0])+1)

    def get_id_pa(self, idGerente):
        stmt = " SELECT p.tipo FROM OFICINA o, PUNTOSATENCION p WHERE p.oficina=o.id AND o.gerente="+"'"+idGerente+"'" 
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

    def registrar_operacion_cuenta(self, operacion):
        stmt = "SELECT cerrada FROM CUENTA c WHERE c.numero="+"'"+str(operacion.cuenta)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt+" 227 dao")
        cur.execute(stmt)
        data = cur.fetchall()
        cerrada = data[0][0]

        if cerrada == 'S':
            print("no permite por cuenta cerrada")
            cur.close()
            self.conn.close()
            return False

        stmt = "SELECT * FROM CUENTA c, PERMITEOPERACIONCU p WHERE c.tipo_cuenta=p.id_tipocuenta AND p.id_tipooperacion="+"'"+str(operacion.tipo_operacion)+"'"+" AND c.numero="+"'"+str(operacion.cuenta)+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 232 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por cuenta oper")
            cur.close()
            self.conn.close()
            return False


        stmt = "SELECT * FROM PERMITEOPERACIONPA p WHERE  p.id_tipooperacion="+"'"+operacion.tipo_operacion+"'"+" AND p.id_tipopuntoatencion="+"'"+operacion.punto_atencion+"'"+" AND() p.monto<="+"'"+operacion.valor+"' OR p.monto IS NULL)"
        print(stmt+" 242 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por punto")
            cur.close()
            self.conn.close()
            return False

        stmt = "SELECT saldo FROM CUENTA WHERE numero ="+"'"+operacion.cuenta+"'"
        print(stmt+" 255 dao")
        cur.execute(stmt)
        if operacion.tipo_operacion == '3':
            saldo = float(cur.fetchall()[0][0])+float(operacion.valor)
        elif operacion.tipo_operacion == '4':
            saldo = float(cur.fetchall()[0][0])-float(operacion.valor) 

        stmt = "UPDATE CUENTA SET saldo="+"'"+str(saldo)+"'"+" WHERE numero ="+"'"+operacion.cuenta+"'"
        print(stmt + " 259 dao")
        cur.execute(stmt)
        print("PAPI") #Llami, regreso en un par de horas!
        stmt = 'INSERT INTO OPERACION VALUES ('+"'"+str(operacion.numero)+"','"+str(operacion.tipo_operacion)+"','"+str(operacion.cliente)+"','"+str(operacion.valor)+"','"+str(operacion.punto_atencion)+"','"+str(operacion.cajero)+"','"+str(operacion.cuenta)+"',TO_DATE('"+operacion.fecha+"','YYYY-MM-DD')"+ ",NULL)"
        print(stmt)
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

    def duenio_cuenta(self, numeroCuenta):
        stmt = "SELECT CLIENTE FROM CUENTA WHERE numero ="+"'"+numeroCuenta+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        return data[0][0]

    def duenio_prestamo(self, numeroPrestamo):
        stmt = "SELECT CLIENTE FROM PRESTAMO WHERE id ="+"'"+numeroPrestamo+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        return data[0][0]

    def existe_cuenta(self, numeroCuenta):
        stmt="SELECT * FROM CUENTA WHERE numero = "+ "'"+numeroCuenta+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        if len(data)<=0:
            return False
        else:
            return True

    def existe_prestamo(self, numeroPrestamo):
        stmt="SELECT * FROM PRESTAMO WHERE id = "+ "'"+numeroPrestamo+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        if len(data)<=0:
            return False
        else:
            return True


    def registrar_operacion_prestamo(self, operacion):
        stmt = "SELECT * FROM PRESTAMO c, PERMITEOPERACIONPRE p WHERE c.tipo=p.id_tipoprestamo AND p.id_tipooperacion="+"'"+str(operacion.tipo_operacion)+"'"+" AND c.id="+"'"+str(operacion.cuenta)+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 232 dao")
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por prestamo oper")
            cur.close()
            self.conn.close()
            return False


        stmt = "SELECT * FROM PERMITEOPERACIONPA p WHERE  p.id_tipooperacion="+"'"+operacion.tipo_operacion+"'"+" AND p.id_tipopuntoatencion="+"'"+operacion.punto_atencion+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 242 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por punto")
            cur.close()
            self.conn.close()
            return False

        stmt = "SELECT monto FROM PRESTAMO WHERE id ="+"'"+operacion.cuenta+"'"
        print(stmt+" 255 dao")
        cur.execute(stmt)
        saldo = float(cur.fetchall()[0][0])-float(operacion.valor)

        stmt = "UPDATE PRESTAMO SET monto="+"'"+str(saldo)+"'"+" WHERE id ="+"'"+operacion.cuenta+"'"
        print(stmt + " 259 dao")
        cur.execute(stmt)
        print("PAPI") 
        stmt = 'INSERT INTO OPERACION VALUES ('+"'"+str(operacion.numero)+"','"+str(operacion.tipo_operacion)+"','"+str(operacion.cliente)+"','"+str(operacion.valor)+"','"+str(operacion.punto_atencion)+"','"+str(operacion.cajero)+"',NULL,TO_DATE('"+str(operacion.fecha)+"','YYYY-MM-DD'),'"+str(operacion.cuenta)+ "')"
        print(stmt)
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

    def get_monto_prestamo(self, numeroPrestamo):
        stmt = "SELECT VALOR_CUOTA FROM PRESTAMO WHERE id="+"'"+str(numeroPrestamo)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        return data[0][0]

    def obtener_elementos_ordenados(self, tab, col, order, a, b, cond = ''):
        if len(cond) == 0:
            stmt = """SELECT * FROM
                        (SELECT u.*, ROWNUM r
                          FROM
                          (SELECT * 
                           FROM %s
                           ORDER BY LPAD(%s, 30) %s) u)
                      WHERE r >= %d AND r <= %d
                   """
            internal_stmt = """SELECT COUNT(*) 
                           FROM %s
                           ORDER BY LPAD(%s, 30) %s
            """
            stmt = stmt % (tab, col, order, a, b)
            internal_stmt = internal_stmt % (tab, col, order)
        else:
            stmt = """SELECT * FROM
                        (SELECT u.*, ROWNUM r
                          FROM
                          (SELECT * 
                           FROM %s
                           WHERE %s
                           ORDER BY LPAD(%s, 30) %s) u)
                      WHERE r >= %d AND r <= %d
                   """
            internal_stmt = """SELECT COUNT(*) 
                           FROM %s
                           WHERE %s
                           ORDER BY LPAD(%s, 30) %s
            """
            stmt = stmt % (tab, cond, col, order, a, b)
            internal_stmt = internal_stmt % (tab, cond, col, order)
        print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        data = map(lambda x: x[0:-1], data)
        cur.execute(internal_stmt)
        search_count = cur.fetchall()[0][0]
        cur.close()
        self.conn.close()
        return data, search_count

    def obtener_cuentasL(self, col, order, a, b, perm, params, _id=None):
        view = 'CUENTAS_INF'
        print params
        cond = ''
        if params['search_term'] != "":
            search_term = '%'+params['search_term'] 
            if params['client']:
                cond += "(NOM_CLIENTE LIKE '%s' OR AP_CLIENTE LIKE '%s') " % (search_term, search_term)
            elif params['account']:
                cond += "(TIPO LIKE '%s') " % (search_term)
        if params['last_movement'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHAU_MOV >= TO_DATE('%s', 'dd/mm/yyyy') " % (params['last_movement'][0].strftime('%d/%m/%Y'))
        if params['last_movement'][1] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHAU_MOV <= TO_DATE('%s', 'dd/mm/yyyy') " % (params['last_movement'][1].strftime('%d/%m/%Y'))
        if params['existance'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHA_CREACION >= TO_DATE('%s', 'dd/mm/yyyy') " % (params['existance'][0].strftime('%d/%m/%Y'))
        if params['existance'][1] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHA_CREACION <= TO_DATE('%s', 'dd/mm/yyyy') " % (params['existance'][1].strftime('%d/%m/%Y'))
        if params['sum'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "SALDO >= %s " % (str(params['sum'][0]))
        if params['sum'][1] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "SALDO <= %s " % (str(params['sum'][1]))
        if perm['goficina']:
            if len(cond) > 0:
               cond += 'AND '
            of = self.get_id_oficina(_id)
            cond += 'ID_OF = %d' % (of)
        elif perm['cliente']:
            if len(cond) > 0:
               cond += 'AND '
            cond += 'ID_CLIENTE = %d' % (_id)
        info, search_count = self.obtener_elementos_ordenados(view, col, order, a, b, cond)
        stmt = 'SELECT count(*) FROM CUENTAS_INF'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        count = cur.fetchall()[0][0]
        # search_count = len(info)
        # info = info[a:b]
        info = map(lambda x: cuenta.CuentaR(x[0], x[1], x[2], x[3],
                                            x[4], x[5], x[6], x[7],
                                            x[8], x[9], x[10]), info)
        return search_count, count, info
        
    def cerrar_cuenta(self, numero):
        stmt = "UPDATE CUENTA SET SALDO = 0, CERRADA = 'S' WHERE NUMERO = %d"
        stmt = stmt % (numero)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def obtener_tipo_de_usuario(self, idUsuario):
        stmt = "SELECT t.tipo FROM USUARIO u, TIPOUSUARIO t WHERE u.tipo = t.id AND u.id="+"'"+str(idUsuario)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        if len(data)>0:
            return data[0][0]

    def obtener_prestamos(self, idUsuario):
        stmt = "SELECT * FROM PRESTAMO WHERE cliente="+"'"+str(idUsuario)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        prestamos = []
        for t in data:
            prestamoo = prestamo.Prestamo(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])
            prestamos.append(prestamoo)
        return prestamos

    def obtener_operaciones(self, idUsuario):
        stmt = "SELECT * FROM OPERACION WHERE cliente="+"'"+str(idUsuario)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        operaciones = []
        for t in data:
            operacionn = operacion.Operacion(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7])
            operaciones.append(operacionn)
        return operaciones

    def obtener_oficinas(self, idUsuario):
        stmt = "SELECT o.* FROM OFICINA o, CUENTA c  WHERE o.id=c.oficina AND c.cliente="+"'"+str(idUsuario)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        oficinas = []
        for t in data:
            oficinaa = oficina.Oficina(t[0], t[1], t[2], t[3], t[4])
            oficinas.append(oficinaa)
        return oficinas

    def obtener_cuentas_oficina(self, idUsuario, idOficina):
        stmt = "SELECT c.* FROM OFICINA o, CUENTA c  WHERE o.id=c.oficina AND c.cliente="+"'"+str(idUsuario)+"' AND o.id ='"+str(idOficina)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt)
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        cuentas = []
        for t in data:
            cuentaa = cuenta.Cuenta(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9])
            cuentas.append(cuentaa)
        return cuentas

    def registrar_prestamo(self, _prestamo):
        stmt = 'INSERT INTO PRESTAMO(id, interes, monto, vencimiento_cuota, num_cuotas, valor_cuota, tipo, cliente, oficina) VALUES %s'
        stmt_2 = 'SELECT MAX(ID) FROM PRESTAMO'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt_2)
        _id = cur.fetchall()[0][0]
        _prestamo.id = _id
        stmt = stmt % (str(_prestamo))
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def cerrar_prestamo(self, _numero):
        stmt = "UPDATE PRESTAMO SET CERRADO = 'S' WHERE ID = %d"
        stmt = stmt % (_numero)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def obtener_prestamos(self, id_oficina, search_term):
        search_term = "'"+search_term+"%'"
        stmt = """SELECT ID, TIPO_P, NOMBRE, APELLIDO, MONTO 
                  FROM PRESTAMO_INF 
                  WHERE OFICINA = %d AND MONTO = 0 AND CERRADO = 'N' 
                  AND (TO_CHAR(ID) LIKE %s OR
                  NOMBRE LIKE %s OR
                  APELLIDO LIKE %s OR NUM_DOCUMENTO LIKE %s)
                  ORDER BY ID"""
        stmt = stmt % (id_oficina, search_term, search_term, search_term, search_term)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: prestamo.PrestamoR(x[0], x[1], x[2], x[3], x[4]), data)
        return data

