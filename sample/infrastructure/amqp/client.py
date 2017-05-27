import pika

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


def consumer(conn, queue, cb):
    try:
        channel = conn.channel()
        channel.queue_declare(queue, durable=True)
        channel.basic_consume(cb, queue=queue, no_ack=False)
        print ' [*] Consumer started'
        channel.start_consuming()
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
