import pika
import json
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)

class PikaClient(object):
    def __init__(self, io_loop):
        logger.info('PikaClient: __init__')
        self.io_loop = io_loop
 
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = ''
 
        self.event_listeners = set([])
 
    def connect(self):
        if self.connecting:
            logger.info('PikaClient: Already connecting to RabbitMQ')
            return
 
        logger.info('PikaClient: Connecting to RabbitMQ')
        self.connecting = True
 
        cred = pika.PlainCredentials('llamabank', '123llama123')
        param = pika.ConnectionParameters(
            host='margffoy-tuay.com',
            port=5672,
            virtual_host='bancandesh',
            credentials=cred
        )
 
        self.connection = pika.TornadoConnection(param,
            on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)
 
    def on_connected(self, connection):
        logger.info('PikaClient: connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)
 
    def on_channel_open(self, channel):
        logger.info('PikaClient: Channel open, Declaring exchange')
        self.channel = channel
        # declare exchanges, which in turn, declare
        # queues, and bind exchange to queues
 
    def on_closed(self, connection):
        logger.info('PikaClient: rabbit connection closed')
        self.io_loop.stop()
 
    def on_message(self, channel, method, header, body):
        logger.info('PikaClient: message received: %s' % body)
        self.notify_listeners(event_factory(body))
 
    def notify_listeners(self, event_obj):
        # here we assume the message the sourcing app
        # post to the message queue is in JSON format
        event_json = json.dumps(event_obj)
 
        for listener in self.event_listeners:
            listener.write_message(event_json)
            logger.info('PikaClient: notified %s' % repr(listener))
 
    def add_event_listener(self, listener):
        self.event_listeners.add(listener)
        logger.info('PikaClient: listener %s added' % repr(listener))
 
    def remove_event_listener(self, listener):
        try:
            self.event_listeners.remove(listener)
            logger.info('PikaClient: listener %s removed' % repr(listener))
        except KeyError:
            pass

