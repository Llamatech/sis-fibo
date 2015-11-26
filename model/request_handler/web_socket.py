# -*- coding: utf-8 -*-

import os
import sys
import json
import datetime
import tornado.escape
from tornado import gen
import tornado.websocket

class WebSocketHandlerTest(tornado.websocket.WebSocketHandler):
 
    def open(self, *args, **kwargs):
        # self.application.pc.add_event_listener(self)
        print("WebSocket opened")

 
    def on_close(self):
        print("WebSocket closed")
        self.application.outq.remove_listener(self.sec_num)
        # self.application.pc.remove_event_listener(self)

    def on_message(self, message):
        #"op_type;amount;acc_local;acc_remote"
        # print message

        self.sec_num = self.application.outq.add_listener(self)
        info = json.loads(message)
        # {“estado”: <”comienzo”|”confirmacion”|”error”>, 
        #  “id”: nId, “tipo”: <“consignar”|”retirar”>, 
        #  “monto”: nMonto, 
        #  “cuentaDestino”: nCDestino, “cuentaOrigen”: nCOrigen}
        # acc_num = 1
        header = 'comienzo'
        # op_type = 'transaccion'
        # amount = 4000
        # code = self.sec_num
        message = {u'id':self.sec_num,
                   u'estado':header, 
                   u'tipo':info['op_type'],
                   u'monto':info['amount'],
                   u'cuentaOrigen':info['acc_local'],
                   u'cuentaDestino':info['acc_remote'],
                   u'idCliente':int(self.get_cookie("authcookie").split('-')[0])}
        print message
        self.application.outq.init_transaction(message)


        # self.application.pc.publish_message(message)asdsdfsdfsdfsdfs.jhdkhgdhhkghjghghjf
    def notify_client(self, msg):
        self.write_message(msg)
        self.application.outq.remove_listener(self.sec_num)

class WebSocketHandlerAssociate(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        # self.application.pc.add_event_listener(self)
        print("WebSocket opened")

 
    def on_close(self):
        print("WebSocket closed")
        self.application.outq.remove_listener(self.sec_num)
        # self.application.pc.remove_event_listener(self)

    def on_message(self, message):
        #"op_type;amount;acc_local;acc_remote"
        # print message

        self.sec_num = self.application.outq.add_listener(self)
        info = json.loads(message)
        #{“estado”: <”comienzo”|”confirmacion”|”error”>“id”: nId, “tipo”: “asociar”, “cuentaOrigen”: nCOrigen, 
        #“bancoOrigen”: <”bancandes”|”llamabank”> “cuentaDestino”: nCDestino, “bancoDestino”:  <”bancandes”|”llamabank”>, 
        #“nombreEmpleado”:nNombre, “valor”: nValor, “frecuencia”:<”mensual”|”quincenal”>}
        # acc_num = 1
        header = 'comienzo'
        # op_type = 'transaccion'
        # amount = 4000
        # code = self.sec_num
        if  info['frec'] is 1:
            frecuencia = 'mensual'
        else:
            frecuencia = 'quincenal'

        message = {u'id':self.sec_num,
                   u'estado':header, 
                   u'tipo':'asociar',
                   u'valor':info['salario'],
                   u'frecuencia':frecuencia,
                   u'cuentaOrigen':info['cuenta'],
                   'bancoOrigen':"llamabank",
                   'bancoDestino':'bancandes',
                   u'cuentaDestino':info['cuenta_empl'],
                   u'idCliente':int(self.get_cookie("authcookie").split('-')[0])}
        print message
        self.application.outq.init_associate(message)


        # self.application.pc.publish_message(message)asdsdfsdfsdfsdfs.jhdkhgdhhkghjghghjf
    def notify_client(self, msg):
        self.write_message(msg)
        self.application.outq.remove_listener(self.sec_num)

class WebSocketHandlerPay(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        # self.application.pc.add_event_listener(self)
        print("WebSocket opened")

 
    def on_close(self):
        print("WebSocket closed")
        self.application.outq.remove_listener(self.sec_num)
        # self.application.pc.remove_event_listener(self)

    def on_message(self, message):
        #"op_type;amount;acc_local;acc_remote"
        # print message
        self.sec_num = self.application.outq.add_listener(self)
        info = json.loads(message)
        #{“estado”: <”comienzo”|”confirmacion”|”error”>“id”: nId, “tipo”: “asociar”, “cuentaOrigen”: nCOrigen, 
        #“bancoOrigen”: <”bancandes”|”llamabank”> “cuentaDestino”: nCDestino, “bancoDestino”:  <”bancandes”|”llamabank”>, 
        #“nombreEmpleado”:nNombre, “valor”: nValor, “frecuencia”:<”mensual”|”quincenal”>}
        # acc_num = 1
        header = 'comienzo'
        # op_type = 'transaccion'
        # amount = 4000
        # code = self.sec_num
        # {u'numCuenta': 123, u'saldo': 6666666, u'estado': u'comienzo', u'id': u'fghiop', u'tipo': u'pagar'
        message = {u'id':self.sec_num,
                   u'estado':header, 
                   u'tipo':'pagar',
                   u'numCuenta':info['acc'],
                   u'idCliente':int(self.get_cookie("authcookie").split('-')[0])}
        print message
        self.application.outq.init_pay(message)


        # self.application.pc.publish_message(message)asdsdfsdfsdfsdfs.jhdkhgdhhkghjghghjf
    def notify_client(self, msg):
        self.write_message(msg)
        self.application.outq.remove_listener(self.sec_num)


class WebSocketHandlerOperations(tornado.websocket.WebSocketHandler):

    def open(self, *args, **kwargs):
        # self.application.pc.add_event_listener(self)
        print("WebSocket opened")
        self.sec_num = self.application.outq.add_listener(self)

    def on_close(self):
        print("WebSocket closed")
        self.application.outq.remove_listener(self.sec_num)

    def on_message(self, message):
        # print(message)
        # [{"name":"draw","value":1},
        #  {"name":"columns","value":
        # [{"data":"fecha","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"tipo","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"id_cliente","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"valor","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}}]},{"name":"order","value":[{"column":0,"dir":"asc"}]},{"name":"start","value":0},{"name":"length","value":10},
        #  {"name":"search","value":{"value":"","regex":false}}]
        full = json.loads(message)
        data = full['data']
        draw = data[0]
        columns = data[1]
        order = data[2]
        start = data[3]
        length = data[4]
        search = data[5]

        draw = draw['value']
        cols = columns['value']
        order_by = order['value'][0]
        column_name = cols[order_by['column']]
        order_s = order_by['dir']
        start = start['value']
        length = length['value']
        search = search['value']

        movInicio = full['uMovStart']
        movFin = full['uMovStop']
        saldoDesde = full['sumFrom']
        saldoHasta = full['sumTo']
        pa1 = full['pa1']
        pa2 = full['pa2']

        _type = 'consultaOp'
        if pa1 != '-1' and pa2 != '-1':
            _type = 'paOp'
            obj = {
                'estado':'comienzo',
                'draw':draw, 
                'ordenar_por':column_name, 
                'orden':order_s, 
                'inicio':start,
                'numero_tuplas':length,
                'tipo':_type,
                'pa1':pa1,
                'pa2':pa2,
                'por':'cuenta',
                'id':self.sec_num
            }
        else:
            obj = {
                    'estado':'comienzo',
                    'draw':draw, 
                    'ordenar_por':column_name, 
                    'orden':order_s, 
                    'inicio':start,
                    'numero_tuplas':length,
                    'tipo':_type,
                    'fechaIni':movInicio,
                    'fechaFin':movFin,
                    'valorMin':saldoDesde,
                    'valorMax':saldoHasta,
                    'por':'cuenta',
                    'id':self.sec_num
            }
        
        self.application.outq.init_operations(obj)
        # data = {"draw": draw,
        #         "recordsTotal": count,
        #         "recordsFiltered": search_count,
        #         'data':cuentas}

    def notify_client(self, msg):
        data = {"draw": msg['draw'],
                "recordsTotal": 100,
                "recordsFiltered": len(msg['operaciones']),
                'data':msg['operaciones']}
        self.write_message(data)
