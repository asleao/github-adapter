import os
import pika

from flask import Flask
# create and configure the app
app = Flask(__name__)
app.config.from_object('config')


# Blueprints
from .github.controller import blueprint
app.register_blueprint(blueprint)
app.add_url_rule('/v1/repo', endpoint='repository')
app.add_url_rule('/v1/repo/collaborators', endpoint='repository/collaborators')
app.add_url_rule('/v1/authorizations', endpoint='authorization')

# CloudAMQ
from .amq.amq import Amq
thread = Amq()

# Configuration for deploy on Heroku
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
