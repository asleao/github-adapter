from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from github import Github
from flask import jsonify

blueprint = Blueprint('github', __name__)


@blueprint.route('/v1/auth')
def authenticate():
    username = ""
    password = ""

    github_object = Github(username, password)

    return jsonify(github_object.get_user().id)
