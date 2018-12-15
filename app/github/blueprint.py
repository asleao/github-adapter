"""
    TODO: Alterar nome da classe para blueprint.
"""
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from github import Github
from flask import jsonify, request
import json
import os
import requests
blueprint = Blueprint('github', __name__)


def authenticate(request):
    data = request.json
    if 'token' in data:
        return Github(data['token'])
    elif 'username' and 'password' in data:
        return Github(data['username'], data['password'])


@blueprint.route('/v1/repo', methods=['POST'])
def repository():
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    data = request.json
    github_object = authenticate(request=request)
    language = data['language']
    repository_name = data['repo_name']

    github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)

    return jsonify('{} created succesfully!'.format(repository_name))


@blueprint.route('/v1/repo/collaborators', methods=['POST'])
def add_collaborator():
    """
    Funcion responsable for adding a collaborator to specific repository.
    """
    data = request.json
    github_object = authenticate(request=request)
    collaborator = data['collaborator']
    repository_name = data['repo_name']
    repository = github_object.get_user().get_repo(repository_name)

    repository.add_to_collaborators(collaborator)

    return jsonify('{} added succesfully on {}!'.format(collaborator, repository_name))


@blueprint.route('/v1/repo/collaborators', methods=['DELETE'])
def remove_collaborator():
    """
    Funcion responsable for remove a collaborator from a repository.
    """
    data = request.json
    github_object = authenticate(request=request)
    collaborator = data['collaborator']
    repository_name = data['repo_name']
    repository = github_object.get_user().get_repo(repository_name)

    if repository.has_in_collaborators(collaborator) == False:
        # TODO: realizar um retorno http para usuário não existente
        return jsonify('{} doesn\'t exist in {}!'.format(collaborator, repository_name))
    else:
        repository.remove_from_collaborators(collaborator)
        return jsonify('{} removed succesfully from {}!'.format(collaborator, repository_name))

# TODO Criar formulário para o usuário preencher os dados.


@blueprint.route('/v1/authorization/callback', methods=['GET'])
def create_authorization():
    """
    Funcion responsable for create a authorization for the application.
    """

    params = {'client_id': current_app.config['GITHUB_CLIENT'],
              "client_secret": current_app.config['GITHUB_SECRET'],
              "code": request.args.get('code')
              }
    headers = {'accept': 'application/json'}
    url = "https://github.com/login/oauth/access_token"

    result = requests.post(url, params=params, headers=headers)

    data = result.json()
    access_token = data['access_token']
    return json.dumps(access_token)


@blueprint.route('/v1/authorization', methods=['GET'])
def login():
    scopes = "{user,read:org,public_repo,admin:repo_hook,admin:org,user:email}"
    client_id = current_app.config['GITHUB_CLIENT']
    url = "https://github.com/login/oauth/authorize?scope={}&client_id={}".format(scopes,
                                                                                  client_id)
    return redirect(url)
