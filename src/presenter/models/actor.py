from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, validates
from presenter.app import db
import datetime


class Actor(db.Model):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=True)
    filmography_movie_name = Column(String(255), nullable=True)
    filmography_url = Column(String(255), nullable=True)

    def __repr__(self):
        return "<Actor id=%s> %s %s" % (self.id, self.name, self.url)

    @validates(
        "name",
        "url",
        "filmography_movie_name",
        "filmography_url",
    )
    def validates_fields(self, keys, values):
        # ipdb.set_trace()
        if keys == "name":
            assert values != "", "Name is missing"
        if keys == "url":
            assert values != "", "URL is required"
        if keys == "filmography_movie_name":
            assert values != "", "Filmography: Movie name is required"
        if keys == "filmography_url":
            assert values != "", "Filmography: Movie URL is required"

        return values
