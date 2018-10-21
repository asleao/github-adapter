from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from github import Github
from flask import jsonify, request
import json

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


@blueprint.route('/v1/repo/collaborators', methods=['PUT'])
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
        #TODO: realizar um retorno http para usuário não existente
        return jsonify('{} doesn\'t exist in {}!'.format(collaborator, repository_name))
    else:
        repository.remove_from_collaborators(collaborator)
        return jsonify('{} removed succesfully from {}!'.format(collaborator, repository_name))
