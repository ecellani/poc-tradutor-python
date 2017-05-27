import ast
import os

from bson.json_util import dumps

from application.translators import Translator
from infrastructure.amqp import client as amqp_client
from infrastructure.mongo import client as mongo_client

"""
Created on May 26, 2017

@author: Erick Cellani
"""


class Worker:

    def __init__(self):
        self.mongo_conn = mongo_client.connect('mongodb://localhost:27017/')
        self.amqp_conn = amqp_client.connect('localhost')
        self.amqp_ch = self.amqp_conn.channel()
        self.amqp_ch.queue_declare('drupal', durable=True)
        self.amqp_ch.queue_declare('ponte2', durable=True)

    def start(self):
        try:
            amqp_client.consumer(self.amqp_conn, 'ponte2', self.on_message)
        except Exception as e:
            raise e
        finally:
            if self.amqp_conn:
                print 'AMQP Connection closed'
                self.amqp_conn.close()
            if self.mongo_conn:
                print 'Mongo Connection closed'
                self.mongo_conn.close()

    def on_message(self, ch, method, properties, body):
        try:
            translator = Translator(self.mongo_conn, 'ofertaDB')
            doc = ast.literal_eval(body)

            translator.translate_modality(doc)
            translator.translate_knowledge_area(doc)
            translator.translate_shift(doc)
            translator.translate_class(doc)
            translator.translate_week_day(doc)
            translator.translate_unity_brand(doc)

            amqp_client.send(self.amqp_ch, 'drupal', dumps(doc))
        except Exception as e:
            raise e


if __name__ == '__main__':
    print "main: worker.py ", os.getpid()
    Worker().start()
