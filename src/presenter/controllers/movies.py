from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename

import os
import ipdb
import json

movies_blueprint = Blueprint("movies", __name__)

from presenter.app import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from presenter.models.movie import Movie


headers = [
    "genre",
    "date_of_scraping",
    "director",
    "rating",
    "release_year",
    "title",
    "top_cast",
    "url",
    "image_urls",
    "images",
]


def to_list(dbstring):
    dbstring = dbstring.strip("'][")
    li = dbstring.split(", ")
    result = []
    for item in li:
        if item.startswith("\"['"):
            result.append((item[3:-1]))
        elif item.endswith("']\""):
            result.append((item[1:-3]))
        else:
            result.append((item[1:-1]))
    return result


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@movies_blueprint.route("/movies/")
def movies():
    # get all entries from DB
    all_movies = Movie.query.order_by(Movie.id).all()

    per_page = request.args.get("items", 5, type=int)
    current_page = request.args.get("page", 1, type=int)

    movie_count = len(all_movies)

    # Calculate how many items to be dispalyed on the page
    start = per_page * (current_page - 1)
    end = min(start + per_page, movie_count)
    movies = all_movies[start:end]
    mess = ""
    if len(movies) == 0:
        mess = "Error message, no more items"

    return render_template(
        "movies/items.html", movies=movies, current_page=current_page, items_per_page=per_page, mess=mess
    )


@movies_blueprint.route("/movies/results/")
def search_item():

    search_string = request.args.get("q")

    try:
        assert len(search_string) > 1
        # return redirect(url_for("movies.search"))

    except AssertionError as warning:
        return redirect(url_for("home.index"))
    else:
        search_result = Movie.query.filter(Movie.title.like("%" + search_string + "%")).all()
        per_page = request.args.get("items", 5, type=int)
        current_page = request.args.get("page", 1, type=int)

        movie_count = len(search_result)
        # Calculate how many items to be dispalyed on the page
        start = per_page * (current_page - 1)
        end = min(start + per_page, movie_count)
        movies = search_result[start:end]
        mess = ""
        if len(movies) == 0:
            mess = "Error message, no more items"
        return render_template(
            "movies/results.html",
            movies=movies,
            current_page=current_page,
            items_per_page=per_page,
            mess=mess,
            search_string=search_string,
        )


@movies_blueprint.route("/movies/new", methods=["GET", "POST"])
def create():
    movie = Movie()

    if request.method == "POST":
        try:
            title = request.form.get("title")
            genre = request.form.get("genre")
            rating = request.form.get("rating")
            url = request.form.get("url")
            date_of_scraping = request.form.get("date_of_scraping")
            director = request.form.get("director")
            release_year = request.form.get("release_year")
            top_cast = request.form.get("top_cast")
            image_urls = request.form.get("image_urls")
            images = request.form.get("images")

            movie.title = title
            movie.genre = genre
            movie.rating = rating
            movie.url = url
            movie.date_of_scraping = date_of_scraping
            movie.director = director
            movie.release_year = release_year
            movie.top_cast = top_cast
            movie.image_urls = image_urls
            movie.images = images
        except AssertionError as err:
            return render_template("/movies/new.html", err=err)
        else:
            db.session.add(movie)
            db.session.flush()
            db.session.commit()
            return render_template("home/index.html")

    return render_template("movies/new.html", new_movie=movie)


@movies_blueprint.route("/movies/<int:id>")
def show(id):
    item = Movie.query.get(id)
    movie = {
        "id": item.id,
        "title": item.title,
        "genre": to_list(item.genre),
        "date_of_scraping": item.date_of_scraping,
        "director": item.director,
        "rating": item.rating,
        "release_year": item.release_year,
        "top_cast": to_list(item.top_cast),
        "url": item.url,
        "image_urls": item.image_urls,
        "images": item.images,
    }
    return render_template("/movies/show.html", movie=movie)


@movies_blueprint.route("/movies/<int:id>", methods=["POST"])
def update(id):
    item = Movie.query.get(id)
    try:
        title = request.form.get("title")
        genre = request.form.get("genre")
        rating = request.form.get("rating")
        url = request.form.get("url")
        date_of_scraping = request.form.get("date_of_scraping")
        director = request.form.get("director")
        release_year = request.form.get("release_year")
        top_cast = request.form.get("top_cast")
        image_urls = request.form.get("image_urls")
        images = request.form.get("images")

        item.title = title
        item.genre = genre
        item.rating = rating
        item.url = url
        item.date_of_scraping = date_of_scraping
        item.director = director
        item.release_year = release_year
        item.top_cast = top_cast
        item.image_urls = image_urls
        item.images = images
    except AssertionError as err:
        flash("Your attention is required")
        return render_template("/movies/edit.html", movie=item, err=err)
        # return redirect(url_for("movies.edit", id=item.id, err=err))
    else:
        db.session.flush()
        db.session.commit()
        flash("Successfully registered!")
        return redirect(url_for("movies.show", id=item.id))
    # movie_url = "/movies/" + str(id) + "show.html"
    # return redirect(url_for("movies.edit", id=item.id))


@movies_blueprint.route("/movies/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    item = Movie.query.get(id)
    return render_template("/movies/edit.html", movie=item)


@movies_blueprint.route("/movies/upload")
def upload_page():
    return render_template("/movies/upload.html")


# delete from movies where genre is null
@movies_blueprint.route("/movies/upload", methods=["POST"])
def upload():
    # messg = ""
    # check if the post request has the file part
    if "file" not in request.files or request.files["file"].filename == "":
        # messg = "No file part"
        flash("No file part")
        # return redirect(request.url)
        # return redirect("/movies/upload")
        return render_template("/movies/upload.html")
    file = request.files["file"]

    if file and allowed_file(file.filename):
        for row in file.readlines():
            temp = json.loads(row)
            movie = Movie()
            for item in headers:
                try:
                    setattr(movie, item, str(temp.get(str(item))))
                    # ipdb.set_trace()
                    # movie.title = temp.get("title")
                except AssertionError as err:
                    flash("Attention is required!")
                    return render_template("/movies/upload.html", err=err)
            if movie.errors:
                return render_template("/movies/upload.html", err=movie.errors)

            db.session.add(movie)
        db.session.flush()
        db.session.commit()

        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        print(file)
        # ipdb.set_trace()
        flash("File uploaded successfully!")
        # messg = "Successfully uploaded file"
    else:
        flash("Unallowed file type")
        # messg = "Unallowed file type"

    # return redirect(url_for("movies.upload"))

    return render_template("/movies/upload.html")
