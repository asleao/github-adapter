# github-adapter [![Build Status](https://travis-ci.org/asleao/github-service.svg?branch=master)](https://travis-ci.org/asleao/github-service)
Adapter para realizar a comunicação com a api do Github.

# Instalação

Configure as variáveis de ambiente abaixo:

    export FLASK_APP=githubms
    export FLASK_ENV=development

Clone o projeto, entre no diretorio e rode o comando:

    pip install -e . 

Para rodar o projeto execute o comando:

    flask run

Exemplo de requisição:

    curl -d '{"username":"value1", "password":"value2"}' -H "Content-Type: application/json" -X POST https://github-mservice.herokuapp.com/v1/auth
