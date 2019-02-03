import json

import pika
from dotenv.environ import getenv

from app.github import controller
from app.models.repository_data import RepositoryData


def setup():
    URL = getenv('CLOUDAMQP_URL')
    return pika.URLParameters(URL)


def callback_repository(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    repository_data = RepositoryData(body['name'],
                                     body['action'],
                                     body['token'],
                                     body['language'])
    controller.repository(repository_data)


def callback_collaborator(ch, method, properties, body):
    body = json.loads(body.decode('utf8').replace("'", '"'))
    collaborator_data = RepositoryData(body['name'],
                                       body['action'],
                                       body['token'],
                                       body['language'])
    collaborator_data.collaborators = body['collaborators']
    controller.manage_collaborators(collaborator_data)
