import os

from flask import Flask
# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='TdiKTNTzjx3iYIYbHSZAbw==',
    DATABASE=os.path.join(app.instance_path, 'githubms.sqlite')
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from githubms import github
app.register_blueprint(github.blueprint)
app.add_url_rule('/v1/auth', endpoint='authenticate')


# Configuration for deploy on Heroku
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
