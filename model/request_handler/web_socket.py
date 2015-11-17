import os
import sys
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
        # self.application.pc.remove_event_listener(self)

    def on_message(self, message):
    	print message
    	self.application.pc.publish_message(message)
