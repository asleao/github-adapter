import pika
import os
import logging
from app.github import controller


def setup():
    URL = os.environ.get('CLOUDAMQP_URL')
    return pika.URLParameters(URL)


def read_from_queue(msg):
    print(" Reading queue")
    print(" Received %r" % msg)
    print(" Created!")


def callback(ch, method, properties, body):
    #read_from_queue(body)
    controller.repository(body)
