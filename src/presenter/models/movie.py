from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from presenter.app import db
import datetime


class Movie(db.Model):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    release_year = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Movie id=%s %r>" % (self.id, self.title)
