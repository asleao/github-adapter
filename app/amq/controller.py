import pika
import os
import logging


def setup():
    URL = os.environ.get('CLOUDAMQP_URL')
    PARAMS_AMQ = pika.URLParameters(URL)
    return PARAMS_AMQ


def read_from_queue(msg):
    print(" Reading queue")
    print(" Received %r" % msg)
    print(" Created!")

def callback(ch, method, properties, body):
    read_from_queue(body)
