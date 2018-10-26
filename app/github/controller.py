"""
    TODO: Alterar nome da classe para blueprint.
"""
from werkzeug.exceptions import abort
from github import Github
from flask import jsonify, request
import json
from flask import current_app

# TODO criar endpont para criar uma authorization e retornar um token para a fila do cloud AMQ.


def authenticate(request):
    data = json.loads(request.decode('utf8').replace("'", '"'))
    if 'token' in data:
        return Github(data['token'])
    elif 'username' and 'password' in data:
        return Github(data['username'], data['password'])


def repository(request):
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    data = json.loads(request.decode('utf8').replace("'", '"'))
    github_object = authenticate(request=request)
    language = data['language']
    repository_name = data['name']

    github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)
    print('{} created succesfully!'.format(repository_name))
    #TODO Enviar callback?    

