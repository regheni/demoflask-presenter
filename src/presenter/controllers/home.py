from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from presenter.services.search import SearchItem

import os
import ipdb


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@home_blueprint.route("/results/", methods=["GET", "POST"])
def search_results():
    display = False
    search_string = request.args.get("q")
    movies = []
    actors = []
    service = SearchItem()
    results = service.search(search_string)

    per_page = request.args.get("items", 5, type=int)
    current_page = request.args.get("page", 1, type=int)

    count = len(results)
    start = per_page * (current_page - 1)
    end = min(start + per_page, count)
    movies = movies[start:end]
    actors = actors[start:end]

    mess = ""
    if len(results) <= per_page:
        display = True
    elif len(movies) == 0:
        mess = "Error message, no more items"

    return render_template(
        "services/search_results.html",
        results=results,
        current_page=current_page,
        items_per_page=per_page,
        search_string=search_string,
        display=display,
        mess=mess,
    )

    # return render_template("services/search_results.html", results=results)


# @services_blueprint.route("/results/")
# def search():
#     search_string = request.args.get("q")
#     count = 0
#     movies = []
#     actors = []
#     for item in (Movie, Actor):
#         if item == Movie:
#             movies.extend(Movie.query.filter(Movie.title.like("%" + search_string + "%")).all())
#             count += len(movies)

#         if item == Actor:
#             actors.extend(Actor.query.filter(Actor.name.like("%" + search_string + "%")).all())
#             count += len(actors)

#     per_page = request.args.get("items", 5, type=int)
#     current_page = request.args.get("page", 1, type=int)
#     # count = len(movies) + len(actors)
#     start = per_page * (current_page - 1)
#     end = min(start + per_page, count)
#     movies = movies[start:end]
#     actors = actors[start:end]
#     mess = ""
#     results = {
#         "movies": movies,
#         "actors": actors,
#     }
#     if count == 0:
#         mess = "Error message, no more items"
#     return render_template(
#         "services/search_results.html",
#         results=results,
#         current_page=current_page,
#         items_per_page=per_page,
#         mess=mess,
#         search_string=search_string,
#     )
