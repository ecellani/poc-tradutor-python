import os
from time import sleep

import pika
import psutil

"""
Created on May 26, 2017

@author: Erick Cellani
"""


def connect(host):
    try:
        credentials = pika.PlainCredentials('guest', 'guest')
        params = pika.ConnectionParameters(host, 5673, None, credentials)
        conn = pika.BlockingConnection(params)
        print ' [*] Connected to AMQP'
        return conn
    except Exception as e:
        raise e


def send(ch, queue, msg):
    try:
        ch.basic_publish(exchange='',
                         routing_key=queue,
                         body=msg,
                         properties=pika.BasicProperties(
                             content_type='application/json'
                         ))
    except Exception as e:
        raise e


def consumer(conn, queue, cb):
    try:
        channel = conn.channel()
        channel.queue_declare(queue, durable=True)
        channel.basic_consume(cb, queue=queue, no_ack=True)
        print ' [*] Waiting for messages.'
        channel.start_consuming()
    except Exception as e:
        raise e


def sync_consumer(conn, queue, cb):
    try:
        channel = conn.channel()
        channel.queue_declare(queue, durable=True)
        print ' [*] Waiting for messages.'
        _i = 500
        py = psutil.Process(os.getpid())
        while True:
            _i += 1
            if _i > 500:
                _i = 0
                print 'Memory usage: ', get_human_readable_size(py.memory_info()[0])

            msg = channel.basic_get(queue=queue, no_ack=False)
            if all(msg):
                cb(channel, msg)
            else:
                _i = 500
                print 'Channel empty'
                sleep(30)

    except Exception as e:
        raise e


def get_human_readable_size(num):
    exp_str = [(0, 'B'), (10, 'KB'), (20, 'MB'), (30, 'GB'), (40, 'TB'), (50, 'PB'), ]
    i = 0
    while i + 1 < len(exp_str) and num >= (2 ** exp_str[i + 1][0]):
        i += 1
        rounded_val = round(float(num) / 2 ** exp_str[i][0], 2)
    return '%s %s' % (int(rounded_val), exp_str[i][1])
