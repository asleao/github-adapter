import os
import pika
from .amq.controller import setup, callback

from flask import Flask
# create and configure the app
app = Flask(__name__)
app.config.from_object('config')


# CloudAMQ
params_amp = setup()
connection = pika.BlockingConnection(params_amp)
channel = connection.channel()  # start a channel
channel.queue_declare(queue='Github')
channel.basic_consume(callback,
                      queue='Github',
                      no_ack=True)
channel.start_consuming()
connection.close()

# Blueprints
from .github.controller import blueprint
app.register_blueprint(blueprint)
app.add_url_rule('/v1/repo', endpoint='repository')
app.add_url_rule('/v1/repo/collaborators', endpoint='repository/collaborators')

# Configuration for deploy on Heroku
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
