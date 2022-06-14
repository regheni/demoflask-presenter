from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
from presenter.configuration import config

app = Flask(__name__)


app.config.update(config().as_dict())
db = SQLAlchemy(app)

from presenter.controllers.movies import movies_blueprint

app.register_blueprint(movies_blueprint)
