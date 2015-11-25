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
        self.sec_num = self.application.outq.add_listener(self)

 
    def on_close(self):
        print("WebSocket closed")
        self.application.outq.remove_listener(self.sec_num)
        # self.application.pc.remove_event_listener(self)

    def on_message(self, message):
        #"op_type;amount;acc_local;acc_remote"
        # print message
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
                   u'cuentaDestino':info['acc_remote']}
        print message
        self.application.outq.init_transaction(message)


        # self.application.pc.publish_message(message)asdsdfsdfsdfsdfs.jhdkhgdhhkghjghghjf
    def notify_client(self, msg):
        self.write_message(msg)



