""" 
users.py 
Users table

"""
from presenter.app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    pwhash = db.Column(db.String(255), nullable=False)

    def __init__(self, username="", email="", pwhash=""):
        self.username = username
        self.email = email
        self.pwhash = generate_password_hash(pwhash)

    def __repr__(self):
        return f"User: {self.username}"

    @property
    def password(self):
        raise AttributeError("Password error")

    @password.setter
    def password(self, password):
        self.pwhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwhash, password)
