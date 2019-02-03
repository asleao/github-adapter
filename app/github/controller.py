"""
    Class responsable for dealing with the github api requests.
"""
from github import Github

from app.models.repository_data import RepositoryData


def repository(repository_data: RepositoryData):
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    github_object = Github(repository_data.token)
    language = repository_data.language
    repository_name = repository_data.repository_name
    repository = github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)
    print('{} created succesfully!'.format(repository_name))

    # TODO Enviar callback?


def manage_collaborators(repository_data: RepositoryData):
    """
        Funcion responsable for manage collaborators of the repository.
    """
    github_object = Github(repository_data.token)
    repository = github_object.get_user().get_repo(repository_data.repository_name)

    for collaborator in repository_data.collaborators:
        if repository_data.action == 'add':
            add_collaborator(repository, collaborator, repository_data.repository_name)
        elif repository_data.action == 'remove':
            remove_collaborator(repository, collaborator, repository_data.repository_name)


def add_collaborator(repository, collaborator, repository_name):
    """
        Funcion responsable for adding collaborators to the repository.
    """
    repository.add_to_collaborators(collaborator, repository_name)
    print('{} added succesfully on {}!'.format(
        collaborator, repository_name))


def remove_collaborator(repository, collaborator, repository_name):
    """
        Funcion responsable to remove collaborators from the repository.
    """
    if not repository.has_in_collaborators(collaborator):
        # TODO: realizar um retorno http para usuário não existente
        return print('{} doesn\'t exist in {}!'.format(collaborator, repository_name))
    else:
        repository.remove_from_collaborators(collaborator)
        return print('{} removed succesfully from {}!'.format(collaborator, repository_name))
