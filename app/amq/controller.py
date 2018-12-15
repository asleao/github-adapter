import pika
import os
import logging
import json

from dotenv.environ import getenv

from app.github import controller


def setup():
    URL = getenv('CLOUDAMQP_URL')
    return pika.URLParameters(URL)


def callback_repository(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    controller.repository(body)


def callback_collaborator(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    controller.manage_collaborators(body)
