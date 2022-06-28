from flask import Flask, render_template, session
from flask_sessionstore import Session
from flask_sqlalchemy import SQLAlchemy
import time
import sys
from presenter.configuration import config
import os

UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "json"}

app = Flask(__name__)
app.secret_key = "SQLAlchemySecret"
app.config.update(config().as_dict())

db = SQLAlchemy(app)


from presenter.controllers.movies import movies_blueprint
from presenter.controllers.actors import actors_blueprint
from presenter.controllers.home import home_blueprint
from presenter.controllers.users import users_blueprint

app.register_blueprint(movies_blueprint)
app.register_blueprint(actors_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(users_blueprint)


if __name__ == "__main__":

    os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_APP"] = "app"
    app.run(debug=True)
