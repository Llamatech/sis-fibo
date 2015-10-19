#-*- coding:iso-8859-1 -*-

import os
import sys
import cx_Oracle
import datetime
from model.vos import tipo
from model.vos import cuenta
from model.vos import usuario
from model.vos import cliente
from model.vos import prestamo
from model.vos import oficina
from model.vos import operacion


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

    def obtener_clientes(self, search_term):
        search_term = "'"+search_term+"%'"
        stmt = """SELECT * FROM CLIENTE_INF 
                  WHERE (TO_CHAR(ID) LIKE %s OR
                  EMAIL LIKE %s OR
                  NUM_DOCUMENTO LIKE %s OR
                  NOMBRE LIKE %s OR APELLIDO LIKE %s)
                  ORDER BY ID"""
        stmt = stmt % (search_term, search_term, search_term, search_term, search_term)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: cliente.ClienteR(x[0], x[1], x[2], x[3], x[4], x[5], x[6]), data)
        return data

        """
        La trasacción involucrada en registrar un cliente maneja un
        nivel de aislamiento READ COMMITTED. Este nivel se utiliza 
        para evitar que alguna consulta lea algún cliente para el cual
        no se ha terminado el proceso de registro. No es necesario
        un mayor nivel de aislamiento, puesto que las consultas deberían 
        poder hacerse mientras se esta registrando un nuevo cliente,
        para mantener la disponibilidad.
        No se hace ninguna sentencia adicional dado que este es el nivel 
        de aislamiento por defecto en Oracle.
        """
    def registrar_cliente(self, _usuario, _cliente):
        stmt_0 = 'SELECT MAX(ID) FROM USUARIO'
        stmt = 'INSERT INTO USUARIO(ID, PIN, EMAIL, TIPO) VALUES %s'
        stmt_2 = 'INSERT INTO CLIENTE (ID, TIPO_DOCUMENTO, NUM_DOCUMENTO,' \
                 + 'NOMBRE, APELLIDO, DIRECCION, TELEFONO, FECHA_INSCRIPCION, ' +\
                 'FECHA_NACIMIENTO, CIUDAD, DEPARTAMENTO, COD_POSTAL) VALUES %s'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt_0)
        _id = cur.fetchall()[0][0]+1
        _usuario.id = _id
        _cliente.id = _id
        stmt = stmt % (str(_usuario))
        stmt_2 = stmt_2 % (str(_cliente))
        print stmt_2
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

    def obtener_tipo_usuarioR(self):
        tabla_consulta = 'TIPOUSUARIO'
        stmt = 'SELECT * FROM %s WHERE ID <= 2'
        self.establecer_conexion()
        cur = self.conn.cursor()
        tipo_usuario_l = []
        try:
            cur.execute(stmt % (tabla_consulta))
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

    def obtener_frecuencia_nomina(self):
        stmt = 'SELECT * FROM FRECUENCIANOMINA'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: tipo.FrecuenciaNomina(x[0], x[1]), data)
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


        """
        La trasacción involucrada en registrar una cuenta maneja un
        nivel de aislamiento READ COMMITTED. Este nivel se utiliza 
        para evitar que alguna consulta lea alguna cuenta para la cual
        no se ha terminado el proceso de registro. No es necesario
        un mayor nivel de aislamiento, puesto que las consultas deberían 
        poder hacerse mientras se esta registrando una nueva cuenta,
        para mantener la disponibilidad.
        No se hace ninguna sentencia adicional dado que este es el nivel 
        de aislamiento por defecto en Oracle.
        """
    def registrar_cuenta(self, tipo, idCliente, idOficina, saldo):
        stmt = "SELECT * FROM USUARIO u WHERE u.id= %d" % (idCliente)
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
        print "Oficina: "+str(idOficina) 
        stmt = """INSERT INTO CUENTA(NUMERO, SALDO, TIPO_CUENTA, CLIENTE, OFICINA) 
                  VALUES (%d, %f, %d, %d, %d)"""
        stmt = stmt % (numero+1, saldo, tipo, idCliente, idOficina)
        cur = self.conn.cursor()
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

    def get_id_oficina(self, idGerente):
        stmt = " SELECT id FROM OFICINA WHERE " + "gerente = " + \
        str(idGerente)
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

    def obtener_cuentas(self, idUsuario, cond = None, closed = True):
        stmt = "SELECT * FROM CUENTA where cliente = " + "'"+str(idUsuario)+ "'"
        if cond:
            stmt += ' AND TIPO_CUENTA <= 2'
        if not closed:
            stmt += " AND CERRADA = 'N'"
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

    def obtener_cuentasN(self, search_term):
        stmt = """SELECT * FROM 
                  (SELECT NUMERO FROM CUENTA c, USUARIO u 
                  WHERE TO_CHAR(c.NUMERO) LIKE '%s' 
                  AND c.CLIENTE = u.ID AND u.TIPO = 1
                  AND c.CERRADA = 'N' 
                  ORDER BY c.NUMERO)
                  WHERE ROWNUM <= 20""" % (search_term+'%')
        #print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: cuenta.CuentaR(x[0], None, None, None, 
                                            None, None, None, None, 
                                            None, None, None), data)
        return data

    def obtener_cuentas_NC(self, search_term):
        stmt = """SELECT * FROM 
                  (SELECT NUMERO FROM CUENTA c 
                  WHERE TO_CHAR(c.NUMERO) LIKE '%s' 
                  AND c.CERRADA = 'N' 
                  ORDER BY c.NUMERO)
                  WHERE ROWNUM <= 20""" % (search_term+'%')
        #print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: cuenta.CuentaR(x[0], None, None, None, 
                                            None, None, None, None, 
                                            None, None, None), data)
        return data

    def obtener_prestamos_NC(self, search_term):
        stmt = """SELECT * FROM 
                  (SELECT ID FROM PRESTAMO c 
                  WHERE TO_CHAR(c.ID) LIKE '%s' 
                  AND c.CERRADO = 'N' 
                  ORDER BY c.ID)
                  WHERE ROWNUM <= 20""" % (search_term+'%')
        #print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: prestamo.PrestamoR(x[0], None, None, None, 
                                            None), data)
        return data

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
        print "DATA:"
        print data[0][0]
        if data[0][0]==None:
            return '1'
        else:
            print "el maximo es: "+ str(data[0][0])
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

        """
        La trasacción involucrada en el registro de una operacion sobre una cuenta tiene
        nivel de aislamiento SERIALIZABLE, puesto que involucra el cambiar cantidades
        de dinero en los saldos de una cuenta. Si no se hiciera SERIALIZABLE, sería posible
        retirar todo el dinero de una cuenta dos veces, si se hace al tiempo, por lo que el resultado
        sería que el cliente puede retirar más plata de la que posee. Otros tipos de error 
        como este con posibles, por lo que se usa el mayor nivel de aislamiento.
        """
    def registrar_operacion_cuenta(self, operacion):
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        stmt = "SELECT * FROM CUENTA c, PERMITEOPERACIONCU p WHERE c.tipo_cuenta=p.id_tipocuenta AND p.id_tipooperacion="+"'"+str(operacion.tipo_operacion)+"'"+" AND c.numero="+"'"+str(operacion.cuenta)+"'"+" AND (p.monto>="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 232 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por cuenta oper")
            cur.close()
            self.conn.close()
            return "Debido a reglas del negocio, el tipo de cuenta no permite la operacion a realizar."


        stmt = "SELECT * FROM PERMITEOPERACIONPA p WHERE  p.id_tipooperacion="+"'"+operacion.tipo_operacion+"'"+" AND p.id_tipopuntoatencion="+"'"+operacion.punto_atencion+"'"+" AND( p.monto<="+"'"+operacion.valor+"' OR p.monto IS NULL)"
        print(stmt+" 242 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por punto")
            cur.close()
            self.conn.close()
            return "Debido a reglas del negocio, el tipo de punto de atención no permite la operacion a realizar."

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
        stmt = 'INSERT INTO OPERACION VALUES ('+"'"+str(operacion.numero)+"','"+str(operacion.tipo_operacion)+"','"+str(operacion.cliente)+"','"+str(operacion.valor)+"','"+str(operacion.punto_atencion)+"',"+str(operacion.cajero)+",'"+str(operacion.cuenta)+"',TO_DATE('"+operacion.fecha+"','YYYY-MM-DD')"+ ",NULL)"
        print(stmt)
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

        """
        La trasacción involucrada en el registro de una operacion sobre una cuenta desde una cuenta origen tiene
        nivel de aislamiento SERIALIZABLE, puesto que involucra el cambiar cantidades
        de dinero en los saldos de una cuenta. Si no se hiciera SERIALIZABLE, sería posible
        retirar todo el dinero de una cuenta dos veces, si se hace al tiempo, por lo que el resultado
        sería que el cliente puede retirar más plata de la que posee. Otros tipos de error 
        como este con posibles, por lo que se usa el mayor nivel de aislamiento.
        """
    def registrar_op_cuenta_origen(self, operacion, origen):
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        stmt = "SELECT * FROM CUENTA c, PERMITEOPERACIONCU p WHERE c.tipo_cuenta=p.id_tipocuenta AND p.id_tipooperacion="+"'"+str(operacion.tipo_operacion)+"'"+" AND c.numero="+"'"+str(operacion.cuenta)+"'"+" AND (p.monto>="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 398 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por cuenta oper")
            cur.close()
            self.conn.close()
            return "Debido a reglas del negocio, el tipo de cuenta no permite la operacion a realizar."


        stmt = "SELECT * FROM PERMITEOPERACIONPA p WHERE  p.id_tipooperacion="+"'"+operacion.tipo_operacion+"'"+" AND p.id_tipopuntoatencion="+"'"+operacion.punto_atencion+"'"+" AND( p.monto<="+"'"+operacion.valor+"' OR p.monto IS NULL)"
        print(stmt+" 242 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            print("no permite por punto")
            cur.close()
            self.conn.close()
            return "Debido a reglas del negocio, el tipo de punto de atención no permite la operacion a realizar."

        stmt = "SELECT saldo FROM CUENTA WHERE numero ="+"'"+operacion.cuenta+"'"
        print(stmt+" 421 dao")
        cur.execute(stmt)
        saldo = float(cur.fetchall()[0][0])+float(operacion.valor)

        stmt = "UPDATE CUENTA SET saldo="+"'"+str(saldo)+"'"+" WHERE numero ="+"'"+operacion.cuenta+"'"
        print(stmt + " 259 dao")
        cur.execute(stmt)


        stmt = "SELECT saldo FROM CUENTA WHERE numero ="+"'"+origen+"'"
        print(stmt+" 426 dao")
        cur.execute(stmt) 
        saldo = float(cur.fetchall()[0][0])-float(operacion.valor)


        stmt = "UPDATE CUENTA SET saldo="+"'"+str(saldo)+"'"+" WHERE numero ="+"'"+origen+"'"
        print(stmt + " 259 dao")
        cur.execute(stmt)


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


        """
        La trasacción involucrada en el registro de una operacion sobre un prestamo tiene
        nivel de aislamiento SERIALIZABLE, puesto que involucra el cambiar cantidades
        de dinero en los montos de un prestamo. Si no se hiciera SERIALIZABLE, sería posible
        pagar todo el prestamo 2 veces, si se hace al tiempo, por lo que el resultado
        sería que el cliente puede pagar todo el prestamo 2 veces, pero solo se veria
        reflejado 1 vez en la base de datos . Otros tipos de error 
        como este con posibles, por lo que se usa el mayor nivel de aislamiento.
        """
    def registrar_operacion_prestamo(self, operacion):
        stmt = "SELECT * FROM PRESTAMO c, PERMITEOPERACIONPRE p WHERE c.tipo=p.id_tipoprestamo AND p.id_tipooperacion="+"'"+str(operacion.tipo_operacion)+"'"+" AND c.id="+"'"+str(operacion.cuenta)+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 232 dao")
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE')
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            return "El tipo de prestamo no permite esta operacion o sobrepasa el monto maximo"
            cur.close()
            self.conn.close()
            return False


        stmt = "SELECT * FROM PERMITEOPERACIONPA p WHERE  p.id_tipooperacion="+"'"+operacion.tipo_operacion+"'"+" AND p.id_tipopuntoatencion="+"'"+operacion.punto_atencion+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 242 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            return "El tipo de punto de atencion no permite esta operacion o sobrepasa el monto maximo"
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
        stmt = 'INSERT INTO OPERACION VALUES ('+"'"+str(operacion.numero)+"','"+str(operacion.tipo_operacion)+"','"+str(operacion.cliente)+"','"+str(operacion.valor)+"','"+str(operacion.punto_atencion)+"','"+str(operacion.cajero)+"',NULL,TO_DATE('"+str(operacion.fecha)+"','YYYY-MM-DD'),'"+str(operacion.cuenta)+ "')"
        print(stmt)
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True

        """
        La trasacción involucrada en el registro de una operacion sobre un prestamo desde una cuenta origen tiene
        nivel de aislamiento SERIALIZABLE, puesto que involucra el cambiar cantidades
        de dinero en los saldos de un prestamo. Si no se hiciera SERIALIZABLE, sería posible
        retirar todo el dinero de una cuenta al pagar el prestamo y reitrar por otro lado, 
        por lo que el resultado si se hace al tiempo, 
        sería que el cliente puede retirar más plata de la que posee. Otros tipos de error 
        como este son posibles, por lo que se usa el mayor nivel de aislamiento.
        """
    def registrar_operacion_prestamo_origen(self, operacion,origen):
        stmt = "SELECT * FROM PRESTAMO c, PERMITEOPERACIONPRE p WHERE c.tipo=p.id_tipoprestamo AND p.id_tipooperacion="+"'"+str(operacion.tipo_operacion)+"'"+" AND c.id="+"'"+str(operacion.cuenta)+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 544 dao")
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            return "El tipo de prestamo no permite esta operacion o sobrepasa el monto maximo"
            cur.close()
            self.conn.close()
            return False


        stmt = "SELECT * FROM PERMITEOPERACIONPA p WHERE  p.id_tipooperacion="+"'"+operacion.tipo_operacion+"'"+" AND p.id_tipopuntoatencion="+"'"+operacion.punto_atencion+"'"+" AND (p.monto<="+"'"+str(operacion.valor)+"' OR p.monto IS NULL)"
        print(stmt+" 558 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            return "El tipo de punto de atencion no permite esta operacion o sobrepasa el monto maximo"
            cur.close()
            self.conn.close()
            return False

        stmt = "SELECT * FROM CUENTA WHERE  numero="+"'"+str(origen)+"'"
        print(stmt+" 569 dao")
        cur.execute(stmt)
        data = cur.fetchall()

        if len(data)<=0:
            return "La cuenta de origen no existe"
            cur.close()
            self.conn.close()
            return False

        stmt = "SELECT cerrada FROM CUENTA c WHERE c.numero="+"'"+str(origen)+"'"
        self.establecer_conexion()
        cur = self.conn.cursor()
        print(stmt+" 385 dao")
        cur.execute(stmt)
        data = cur.fetchall()
        cerrada = data[0][0]

        if cerrada == 'S':
            print("no permite por cuenta cerrada")
            cur.close()
            self.conn.close()
            return "La cuenta origen se encuentra cerrada"

        stmt = "SELECT monto FROM PRESTAMO WHERE id ="+"'"+operacion.cuenta+"'"
        print(stmt+" 255 dao")
        cur.execute(stmt)
        saldo = float(cur.fetchall()[0][0])-float(operacion.valor)

        stmt = "UPDATE PRESTAMO SET monto="+"'"+str(saldo)+"'"+" WHERE id ="+"'"+operacion.cuenta+"'"
        print(stmt + " 259 dao")
        cur.execute(stmt) 
        stmt = 'INSERT INTO OPERACION VALUES ('+"'"+str(operacion.numero)+"','"+str(operacion.tipo_operacion)+"','"+str(operacion.cliente)+"','"+str(operacion.valor)+"','"+str(operacion.punto_atencion)+"','"+str(operacion.cajero)+"',NULL,TO_DATE('"+str(operacion.fecha)+"','YYYY-MM-DD'),'"+str(operacion.cuenta)+ "')"
        print(stmt)
        cur.execute(stmt)

        stmt = "SELECT saldo FROM CUENTA WHERE numero ="+"'"+str(origen)+"'"
        print(stmt+" 619 dao")
        cur.execute(stmt)
        saldo = float(cur.fetchall()[0][0])-float(operacion.valor) 

        stmt = "UPDATE CUENTA SET saldo="+"'"+str(saldo)+"'"+" WHERE numero ="+"'"+str(origen)+"'"
        print(stmt + " 624 dao")
        cur.execute(stmt)
        # stmt = 'INSERT INTO OPERACION VALUES ('+"'"+str(operacion.numero)+"','"+str(operacion.tipo_operacion)+"','"+str(operacion.cliente)+"','"+str(operacion.valor)+"','"+str(operacion.punto_atencion)+"','"+str(operacion.cajero)+"','"+str(operacion.cuenta)+"',TO_DATE('"+operacion.fecha+"','YYYY-MM-DD')"+ ",NULL)"
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
            search_term = params['search_term']+'%' 
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

    def obtener_prestamosL(self, col, order, a, b, perm, params, _id=None):
        view = 'PRESTAMO_INF'
        cond = ''
        if params['search_term'] != "":
            search_term = params['search_term']+'%' 
            if params['client']:
                cond += "(NOMBRE LIKE '%s' OR APELLIDO LIKE '%s') " % (search_term, search_term)
            elif params['loan']:
                cond += "(TIPO_P LIKE '%s') " % (search_term)
        if params['last_movement'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "VENCIMIENTO_CUOTA >= TO_DATE('%s', 'dd/mm/yyyy') " % (params['last_movement'][0].strftime('%d/%m/%Y'))
        if params['last_movement'][1] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "VENCIMIENTO_CUOTA <= TO_DATE('%s', 'dd/mm/yyyy') " % (params['last_movement'][1].strftime('%d/%m/%Y'))
        if params['app_date'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHA_CREACION >= TO_DATE('%s', 'dd/mm/yyyy') " % (params['existance'][0].strftime('%d/%m/%Y'))
        if params['app_date'][1] is not None:
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
            cond += 'OFICINA = %d' % (of)
        elif perm['cliente']:
            if len(cond) > 0:
               cond += 'AND '
            cond += 'ID_CLIENTE = %d' % (_id)
        info, search_count = self.obtener_elementos_ordenados(view, col, order, a, b, cond)
        stmt = 'SELECT count(*) FROM PRESTAMO_INF'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        count = cur.fetchall()[0][0]
        # search_count = len(info)
        # info = info[a:b]
        print info[0]
        info = map(lambda x: prestamo.PrestamoR2(x[0], x[1], x[2], x[3],
                                                x[4], x[5], x[6], x[7],
                                                x[8], x[9], x[10], x[11],
                                                x[12], x[13], x[14], x[15], x[16]), info)
        return search_count, count, info

    def obtener_operacionL(self, col, order, a, b, perm, params, _id):
        view = 'OPERACION_INF'
        cond = ''
        if params['search_term'] != "":
            search_term = params['search_term']+'%'
            if params['client']:
                cond += "(NOMBRE LIKE '%s' OR APELLIDO LIKE '%s') " % (search_term, search_term)
            elif params['account']:
                cond += "TO_CHAR(CUENTA) LIKE '%s' " % (search_term)
            else:
                cond += "TO_CHAR(PRESTAMO) LIKE '%s' " % (search_term)
        if params['op_type'] != -1:
            if len(cond) > 0:
                cond += "AND "
            cond += " TIPO_OP = %d " % (params['op_type'])
        if params['last_movement'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHA >= TO_DATE('%s', 'dd/mm/yyyy') " % (params['last_movement'][0].strftime('%d/%m/%Y'))
        if params['last_movement'][1] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "FECHA <= TO_DATE('%s', 'dd/mm/yyyy') " % (params['last_movement'][1].strftime('%d/%m/%Y'))
        if params['sum'][0] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "VALOR >= %s " % (str(params['sum'][0]))
        if params['sum'][1] is not None:
            if len(cond) > 0:
               cond += 'AND '
            cond += "VALOR <= %s " % (str(params['sum'][1]))

        if perm['goficina']:
            if len(cond) > 0:
               cond += 'AND '
            id_of = self.get_id_oficina(_id)
            cond += "ID_OFICINA = %d " % (id_of)
        elif perm['cliente']:
            if len(cond) > 0:
               cond += 'AND '
            cond += "ID_CLIENTE = %d" % (_id)

        info, search_count = self.obtener_elementos_ordenados(view, col, order, a, b, cond)
        stmt = 'SELECT count(*) FROM OPERACION_INF'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        count = cur.fetchall()[0][0]
        info = map(lambda x: operacion.OperacionR(x[0], x[1], x[2], x[3], x[4],
                                                  x[5], x[6], x[7], x[8], x[9],
                                                  x[10], x[11], x[12], x[13],
                                                  x[14], x[15], x[16]), info)
        return search_count, count, info        

        """
        La trasacción involucrada en el cierre de una cuenta tiene
        nivel de aislamiento SERIALIZABLE, puesto que involucra el cambiar cantidades
        de dinero en los saldos de una cuenta. Si no se hiciera SERIALIZABLE, sería posible
        retirar retirar dinero de una cuenta que esta siendo cerrada, por lo que el resultado
        sería que el cliente puede retirar plata aunque la cuenta este cerrada. Otros tipos de error 
        como este son posibles, por lo que se usa el mayor nivel de aislamiento.
        """
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

    def obtener_prestamos_cliente(self, idUsuario):
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
            prestamoo = prestamo.Prestamo(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8])
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

    """
       Debido a que antes de realizar una operación, éste debe existir. Toda operación que desee realiza
       una consulta sobre los préstamos del sistema BancAndes, debería realizarla nuevamente, si desea 
       visualizar nuevos préstamos, esto implica que el nivel de aislamiento definido corresponde a READ COMMITTED.
    """
    def registrar_prestamo(self, _prestamo):
        stmt = 'INSERT INTO PRESTAMO(id, interes, monto, vencimiento_cuota, num_cuotas, valor_cuota, tipo, cliente, oficina) VALUES %s'
        stmt_2 = 'SELECT MAX(ID) FROM PRESTAMO'
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt_2)
        _id = cur.fetchall()[0][0]
        _prestamo.id = _id+1
        stmt = stmt % (str(_prestamo))
        cur.execute(stmt)
        self.conn.commit()
        cur.close()
        self.conn.close()

    """
        Para cerrar un préstamo, es necesario que el saldo de este, sea equivalente a cero.
        Esto implica que otra transacción no puede realizar una operación sobre el mismo préstamo,
        y por lo tanto, el modo de aislamiento corresponde a READ COMMITTED (Modo de aislamiento
        transaccional definido por defecto en Oracle 12c).
    """
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
        print stmt
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: prestamo.PrestamoR(x[0], x[1], x[2], x[3], x[4]), data)
        return data

    def obtener_tipo_cliente(self, idUsuario):
        stmt = 'SELECT t.tipo FROM USUARIO u, TIPOUSUARIO t WHERE u.tipo=t.id AND u.id='+"'"+str(idUsuario)+"'" 
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        return data[0][0]

    def obtener_nombre_cliente(self, idUsuario):
        stmt = 'SELECT nombre FROM CLIENTE WHERE id='+"'"+str(idUsuario)+"'" 
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        return data[0][0]

    """
        Debido a que la inserción de nuevas cuentas en una nómina no debe modificar el proceso
        de pago de la misma, si éste ha iniciado. Es decir, que las cuentas que se añaden a una
        nómina, mientras esta es pagada, no deberían incrementar su saldo. Por lo tanto, el nivel
        de aislamiento definido corresponde a READ COMMITED (Nivel definido por defecto).  
    """
    def actualizar_nomina(self, cuenta, cuenta_empl, salario, frecuencia):
        stmt = """INSERT INTO NOMINA(CUENTA_EMPLEADO, CUENTA_EMPRESA, SALARIO, FRECUENCIA)
                  VALUES (%d, %d, %s, %d)""" % (cuenta_empl, cuenta, salario, frecuencia)
        self.establecer_conexion()
        cur = self.conn.cursor()
        try:
            cur.execute(stmt)
        except cx_Oracle.IntegrityError:
            self.conn.rollback()
            cur.close()
            self.conn.close()
            return False, 400, "La cuenta del empleado ya se encuentra asignada a una nómina" 
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True, 200, "Success"

    """
        Debido a que el proceso de pagar la nómina de un empleador, depende del saldo actual disponible en la cuenta empresarial,
        éste debe permanecer constante y estático durante la transacción, y por lo tanto, otra operación que desee modificar el saldo
        debe esperar hasta que esta transacción finalice. Esto implica que el modo de aislamiento actual de la transaccción debe
        ser SERIALIZABLE. 
    """
    def pagar_nomina(self, cuenta):
        stmt ="SELECT n.CUENTA_EMPLEADO, n.SALARIO FROM NOMINA n WHERE n.CUENTA_EMPRESA="+ str(cuenta) 
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute('SET TRANSACTION ISOLATION LEVEL SERIALIZABLE')
        cur.execute(stmt)
        data = cur.fetchall()
        noPagos = []
        ok = True
        for x in data:
            if ok:
                ok = self.pagar_empleado(cuenta, x[0],x[1],cur)
            if not ok:
                noPagos.append(x[0])

        if not ok:
            for y in noPagos:
                self.notificar_empleado(y,cur)
            r = self.obtener_nombres_empleados(noPagos, cur)
            cur.close()
            self.conn.close()
            return r
        else:
            cur.close()
            self.conn.close()
            return True


    def pagar_empleado(self, cuenta_empresa,cuenta_empleado,salario,cur):
        stmt = "SELECT SALDO FROM CUENTA WHERE NUMERO =" + str(cuenta_empresa)
        cur.execute(stmt)
        data = cur.fetchall()
        saldo = float(data[0][0])-float(salario)
        if saldo < 0:
            return False
        stmt = "UPDATE CUENTA SET SALDO ="+str(saldo)+" WHERE NUMERO="+str(cuenta_empresa)
        print stmt
        cur.execute(stmt)
        stmt = "SELECT SALDO FROM CUENTA WHERE NUMERO =" + str(cuenta_empresa)
        cur.execute(stmt)
        data = cur.fetchall()
        saldo = float(data[0][0])+float(salario)
        stmt = "UPDATE CUENTA SET SALDO ="+str(saldo)+" WHERE NUMERO="+str(cuenta_empleado)
        cur.execute(stmt)
        self.conn.commit() #savepoint
        return True

    def notificar_empleado(self, cuenta_empleado, cur):
        stmt = "SELECT u.ID FROM CLIENTE u, CUENTA c WHERE c.CLIENTE=u.ID AND c.NUMERO ="+str(cuenta_empleado)
        cur.execute(stmt)
        data = cur.fetchall()
        id = data[0][0]
        stmt = "INSERT INTO NOTIFICACIONES(USUARIO,MENSAJE,FECHA) VALUES("+str(id)+",'Su nomina no pudo ser pagada por fondos insuficientes en la cuenta corporativa. Fecha y hora: "+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"', TO_DATE('"+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"','YYYY-MM-DD hh24:mi:ss')"+")"
        print stmt
        cur.execute(stmt)
        self.conn.commit() #Savepoint

    def obtener_nombres_empleados(self, cuentas, cur):
        l = ['NUMERO = '+str(cuentas[0])]
        for x in range(1,len(cuentas)):
            l.append(' OR NUMERO = '+str(x))
        s = ''.join(l)
        stmt = "SELECT p.NOMBRE FROM CUENTA c, CLIENTE p WHERE p.id=c.cliente AND ("+s+')'
        print stmt + "dao 1023"
        cur.execute(stmt)
        data = cur.fetchall()
        nom_cuenta = []
        for x in range(0, len(cuentas)):
            nom_cuenta.append({'nombre':data[x][0], 'cuenta':cuentas[x]})

        return nom_cuenta

    def obtener_tipo_operacion(self):
        stmt = "SELECT * FROM TIPOOPERACION"
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        cur.close()
        self.conn.close()
        data = map(lambda x: tipo.TipoOperacion(x[0], x[1]), data)
        return data

    def cuenta_nomina(self, acc_number):
        stmt = "SELECT COUNT(*) FROM NOMINA WHERE CUENTA_EMPRESA = %d" % (acc_number)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()[0][0]
        cur.close()
        self.conn.close()
        return data > 0

    def obtener_notificaciones_cliente(self, idCliente):
        stmt = "SELECT MENSAJE FROM NOTIFICACIONES WHERE USUARIO ="+  str(idCliente)
        self.establecer_conexion()
        cur = self.conn.cursor()
        cur.execute(stmt)
        data = cur.fetchall()
        stmt2 = "DELETE FROM NOTIFICACIONES WHERE USUARIO ="+  str(idCliente)
        print stmt2
        cur.execute(stmt2)
        self.conn.commit()#Que susto Jajajaja, el commit fantasma Delusionando
        cur.close()
        self.conn.close()
        return data

    """
        El nivel de aislamiento transaccional definido por defecto en Oracle 12c, es READ COMMITTED.
        Debido a que la sentencia expresada solo debe considerar las cuentas registradas y existentes en la tabla
        NOMINA al momento de realizar la consulta, el procedimiento para realizar la migración de nómina entre cuentas,
        se realiza con un nivel de aislamiento READ COMMITTED
     """
    def migrar_nomina(self, acc_old, acc_new):
        stmt = 'UPDATE NOMINA SET CUENTA_EMPRESA = %d WHERE CUENTA_EMPRESA = %d' % (acc_new, acc_old)
        self.establecer_conexion()
        cur = self.conn.cursor()
        try:
            cur.execute(stmt)
        except cx_Oracle.DatabaseError:
            self.conn.rollback()
            cur.close()
            return False, 500
        self.conn.commit()
        cur.close()
        self.conn.close()
        return True, 200
