#-*- coding:iso-8859-1 -*-

import os
import sys
import time
import random
import datetime
import cx_Oracle

URL = 'fn3.oracle.virtual.uniandes.edu.co'
PORT = 1521
SERV = 'prod'
USER = 'ISIS2304221520'
PWD = 'Xg6YCgZ8wJ3R'

init_u = 1653
end_u = 7775

# cur.execute('SELECT MAX(ID) FROM PUNTOSATENCION')
max_pa = 1228

min_c = 429
max_c = 1124 

def get_user_assets(id):
    stmt_1 = "SELECT NUMERO FROM CUENTA WHERE CLIENTE = %d AND CERRADA = 'N'"
    stmt_2 = "SELECT ID FROM PRESTAMO WHERE CLIENTE = %d AND CERRADO = 'N'"
    cur.execute(stmt_1 % (id))
    acc = cur.fetchall()
    cur.execute(stmt_2 % (id))
    loans = cur.fetchall()
    if len(acc) == 0:
        acc = None
    else:
        acc = map(lambda x: x[0], acc)
    if len(loans) == 0:
        loans = None
    else:
        loans = map(lambda x: x[0], loans)
    assets = {'acc':acc, 'loans':loans}
    return assets



stmt = """INSERT INTO OPERACION(NUMERO, TIPO_OPERACION, CLIENTE, 
          VALOR, PUNTO_ATENCION, CAJERO, CUENTA, FECHA, PRESTAMO) 
          VALUES %s"""

# (%d,%d, %d,%d,%d,%d,%d,TO_DATE(%s, 'dd/mm/yyyy'),%s)            

# 3 Consignar
# 4 Retirar
# 8 Pagar cuota
# 9 Pagar cuota f iraor dmia

 #Incrementando un día
#date = datetime.date(2015, 10, 7) #Iniciando el 7 de Octubre

def insert_operations(cur, cnx, num_seq, date, days, assets_l, init = None):
    delta = datetime.timedelta(1)
    end = end_u
    reset = False
    if init is None:
        init = init_u      
    else:
        reset = True
    try:
        while days > 0 : #Tres años (Aprox)
            for client in range(init, end+1): #Para todos los clientes
                try:
                    assets = assets_l[client]
                except KeyError:
                    assets = get_user_assets(client)
                    assets_l[client] = assets 
                num_op = random.randint(3, 5)
                for j in range(0, num_op):
                    c = random.randint(min_c, max_c)
                    pa = random.randint(1, max_pa)
                    op = random.choice([random.randint(3, 4), random.randint(8, 9)])
                    if op <= 4:
                        # NUMERO, TIPO_OPERACION, CLIENTE, 
                  # VALOR, PUNTO_ATENCION, CAJERO, CUENTA, FECHA, PRESTAMO
                        #Accounts
                        if assets['acc'] is not None:
                            a = random.choice(assets['acc'])
                            f = "TO_DATE('%s', 'dd/mm/yyyy')" % (date.strftime('%d/%m/%Y'))
                            values = (num_seq, op, client, abs(random.uniform(30000, 5000000)), 
                                      pa, c, a, f)
                            #values = values.replace("\"", '')
                            values = str(values)[0:-1]+', null)' 
                            values = str(values).replace('\"', '')
                            print values
                            print stmt % (values) 
                            cur.execute(stmt % (values))
                            cnx.commit()
                            num_seq += 1
                    else:
                        if assets['loans'] is not None:
                            a = random.choice(assets['loans'])
                            f = "TO_DATE('%s', 'dd/mm/yyyy')" % (date.strftime('%d/%m/%Y'))
                            values = (num_seq, op, client, abs(random.uniform(30000, 5000000)), 
                                      pa, c)#, f, a)
                            values = str(values)[0:-1]+', null, '+f+', '+str(a)+')'
                            values = str(values).replace('\"', '')
                            print values
                            print stmt % (values)
                            cur.execute(stmt % (values))
                            cnx.commit()
                            num_seq += 1
                        #Loans
            days -= 1
            date += delta
            if reset:
                init = init_u
                reset = False
    except cx_Oracle.Error:
        return num_seq, date, days, assets_l, client, False

    return num_seq, date, days, assets_l, client, True 

# cur.close()
# cnx.close()

if __name__ == '__main__':
    dsn_tns = cx_Oracle.makedsn(URL, PORT, SERV)
    cnx = cx_Oracle.connect(USER, PWD, dsn_tns)
    cur = cnx.cursor()
    # cursor, cnx, num_seq, date, days, assets_l
    date = sys.argv[1].split('/')
    date = map(int, date)
    date = datetime.date(date[2], date[1], date[0])
    days = int(sys.argv[2])
    num_seq = int(sys.argv[3])
    assets_l = {}
    init = init_u
    while True:
        num_seq, date, days, assets_l, init, stat = insert_operations(cur, cnx, num_seq, date, days, assets_l, init)
        if not stat:
            cur.close()
            cnx.close()
            print "Reloading..."
            cnx = cx_Oracle.connect(USER, PWD, dsn_tns)
            cur = cnx.cursor()
        else:
            break








