"""
    TODO: Alterar nome da classe para blueprint.
"""
from github import Github


# TODO criar endpont para criar uma authorization e retornar um token para a fila do cloud AMQ.


def authenticate(data):
    if 'token' in data:
        return Github(data['token'])
    elif 'username' and 'password' in data:
        return Github(data['username'], data['password'])


def repository(data):
    """
    Funcion responsable for getting the credentials and create a repository.
    """
    github_object = authenticate(data=data)
    language = data['language']
    repository_name = data['name']
    if data['action'] == 'add':
        add_repository(github_object, language, repository_name)
    elif data['action'] == 'remove':
        username = github_object.get_user().login
        repository_slug = '{}/{}'.format(username, repository_name)
        repo = github_object.get_repo(repository_slug)
        if repo is not None:
            repo.delete()
            print('{} removed succesfully!'.format(repository_name))

    # TODO Enviar callback?


def add_repository(github_object, language, repository_name):
    repo = github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)
    print(repo.full_name)
    print('{} created succesfully!'.format(repository_name))


def manage_collaborators(data):
    """
        Funcion responsable for manage collaborators of the repository.
    """
    github_object = authenticate(data=data)
    collaborators = data['collaborators']
    repository_name = data['name']
    repository = github_object.get_user().get_repo(repository_name)

    for collaborator in collaborators:
        if data['action'] == 'add':
            add_collaborator(repository, collaborator, repository_name)
        elif data['action'] == 'remove':
            remove_collaborator(repository, collaborator, repository_name)


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
    if repository.has_in_collaborators(collaborator) == False:
        # TODO: realizar um retorno http para usuário não existente
        return print('{} doesn\'t exist in {}!'.format(collaborator, repository_name))
    else:
        repository.remove_from_collaborators(collaborator)
        return print('{} removed succesfully from {}!'.format(collaborator, repository_name))
