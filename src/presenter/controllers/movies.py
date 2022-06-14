from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect

movies_blueprint = Blueprint("movies", __name__)

from presenter.app import app, db
from presenter.models.movie import Movie


@movies_blueprint.route("/movies")
def index():
    all_movies = Movie.query.all()
    return render_template("movies/index.html", movies=all_movies)


@movies_blueprint.route("/movies", methods=["POST"])
def create():
    movie = Movie(
        title=request.form.get("title"), release_year=request.form.get("release_year"), url=request.form.get("url")
    )
    db.session.add(movie)
    db.session.commit()
    return redirect("/movies")
