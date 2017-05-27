import ast
import os
import signal
import sys

from bson.json_util import dumps

from application.translators import Translator
from infrastructure.amqp import client as amqp_client
from infrastructure.mongo import client as mongo_client

"""
Created on May 26, 2017

@author: Erick Cellani
"""


class Worker:

    def __init__(self, source=None, target=None):
        self.source_queue = source
        self.target_queue = target

        self.amqp_conn = amqp_client.connect('localhost')
        self.mongo_conn = mongo_client.connect('mongodb://localhost:27017/')

        self.amqp_ch = self.amqp_conn.channel()
        self.amqp_ch.queue_declare(target, durable=True)
        self.amqp_ch.queue_declare(self.source_queue, durable=True)

    def start(self):
        try:
            amqp_client.consumer(self.amqp_conn, self.source_queue, self.on_message)
        except Exception as e:
            raise e

    def on_message(self, channel, method, properties, body):
        try:
            translator = Translator(self.mongo_conn, 'ofertaDB')
            offer = ast.literal_eval(body)

            translator.translate_modality(offer)
            translator.translate_knowledge_area(offer)
            translator.translate_shift(offer)
            translator.translate_class(offer)
            translator.translate_week_day(offer)
            translator.translate_unity_brand(offer)

            amqp_client.send(self.amqp_ch, self.target_queue, dumps(offer))
            channel.basic_ack(method.delivery_tag)
        except Exception as e:
            raise e


if __name__ == '__main__':
    print '(PID) %r worker.py' % os.getpid()
    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))
    print('Press Ctrl+C to exit')
    Worker(source='ponte', target='drupal').start()
