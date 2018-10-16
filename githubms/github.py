from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from github import Github
from flask import jsonify, request

blueprint = Blueprint('github', __name__)


@blueprint.route('/v1/auth', methods=['POST'])
def authenticate():
    data = request.json
    username = data['username']
    password = data['password']

    github_object = Github(username, password)

    # TODO:request permission for creating an authorization.
    return jsonify("User {} authenticated succesfully!".format(username))


@blueprint.route('/v1/repo', methods=['POST'])
def repository():
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    data = request.json
    if 'token' in data:
        github_object = Github(data['token'])
    elif 'username' and 'password' in data:
        github_object = Github(data['username'], data['password'])
    language = data['language']
    repository_name = data['repo_name']

    github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)

    return jsonify('{} created succesfully!'.format(repository_name))
