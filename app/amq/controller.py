import json
import os

import pika

from app.github import controller


def setup():
    URL = os.environ.get('CLOUDAMQP_URL')
    return pika.URLParameters(URL)


def callback_repository(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    controller.repository(body)


def callback_collaborator(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    controller.manage_collaborators(body)
