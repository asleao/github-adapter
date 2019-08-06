from github import Github
import asyncio


def authenticate(data):
    if 'token' in data:
        return Github(data['token'])
    elif 'username' and 'password' in data:
        return Github(data['username'], data['password'])


def repository(data):
    """
    Funcion responsable for getting the credentials and create a repository.
    """

    loop = asyncio.new_event_loop()
    loop.run_until_complete(manage_repository(data))
    loop.close()
    # TODO Enviar callback?


async def manage_repository(data):
    github_object = authenticate(data=data)
    language = data['language']
    repository_name = data['name']
    if data['action'] == 'add':
        asyncio.ensure_future(add_repository(github_object, language, repository_name))
    elif data['action'] == 'remove':
        asyncio.ensure_future(remove_repository(github_object, repository_name))


async def remove_repository(github_object, repository_name):
    username = github_object.get_user().login
    repository_slug = '{}/{}'.format(username, repository_name)
    repo = github_object.get_repo(repository_slug)
    if repo is not None:
        repo.delete()
        print('{} removed succesfully!'.format(repository_name))


async def add_repository(github_object, language, repository_name):
    github_object.get_user().create_repo(
        repository_name, gitignore_template=language, auto_init=True)
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
    if not repository.has_in_collaborators(collaborator):
        return print('{} doesn\'t exist in {}!'.format(collaborator, repository_name))
    else:
        repository.remove_from_collaborators(collaborator)
        return print('{} removed succesfully from {}!'.format(collaborator, repository_name))
