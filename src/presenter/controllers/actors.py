from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash
import ipdb
import json

actors_blueprint = Blueprint("actors", __name__)

from presenter.app import app, db, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from presenter.models.actor import Actor


actor_headers = ["name", "url", "filmography_movie_name", "filmography_url"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@actors_blueprint.route("/actors/", defaults={"page_nr": 1})
# @actors_blueprint.route("/actors/page=<int:page_nr>&items=<int:item_nr>", methods=["GET", "POST"])
def actors(page_nr):
    # get all entrance from DB
    all_actors = Actor.query.order_by(Actor.id).all()
    per_page = request.args.get("items", 5, type=int)
    current_page = request.args.get("page", 1, type=int)

    actor_count = len(all_actors)

    # Calculate how many items to be dispalyed on the page
    start = per_page * (current_page - 1)
    end = min(start + per_page, actor_count)
    actors = all_actors[start:end]
    mess = ""
    if len(actors) == 0:
        mess = "Warning message: no more actors"

    return render_template("actors/items.html", actors=actors, current_page=current_page, per_page=per_page, mess=mess)


def to_list(dbstring):
    dbstring = dbstring.strip("'][")
    li = dbstring.split(", ")
    result = []
    for item in li:
        result.append((item[1:-1]))
    return result


@actors_blueprint.route("/actors/<int:id>")
def show(id):
    item = Actor.query.get(id)
    filmography_name = item.filmography_movie_name
    filmography_url = item.filmography_url
    filmography = [x for x in zip(to_list(filmography_name), to_list(filmography_url))]
    return render_template("/actors/show.html", actor={"id": item.id, "name": item.name, "filmography": filmography})


@actors_blueprint.route("/actors/new")
def new():
    return render_template("/actors/new.html")


@actors_blueprint.route("/actors/new", methods=["POST"])
def create():
    actor = Actor()
    data = {
        "name": request.form.get("name"),
        "url": request.form.get("url"),
        "filmography_movie_name": request.form.get("filmography_movie_name"),
        "filmography_url": request.form.get("filmography_url"),
    }

    try:
        for item in actor_headers:
            setattr(actor, item, str(data.get(str(item))))

    except AssertionError as err:
        flash("Attention is required")
        return render_template("/actors/new.html", err=err)
    else:
        db.session.add(actor)
        db.session.flush()
        db.session.commit()

    flash("Successful actor insertion!")
    return render_template("/actors/new.html")


@actors_blueprint.route("/actors/<int:id>/edit")
def edit(id):
    item = Actor.query.get(id)
    return render_template("/actors/edit.html", actor=item)


@actors_blueprint.route("/actors/<int:id>", methods=["POST"])
def update(id):
    actor = Actor.query.get(id)
    data = {
        "name": request.form.get("name"),
        "url": request.form.get("url"),
        "filmography_movie_name": request.form.get("filmography_movie_name"),
        "filmography_url": request.form.get("filmography_url"),
    }

    try:
        for item in actor_headers:
            setattr(actor, item, str(data.get(str(item))))

    except AssertionError as err:
        flash("Attention is required!")
        return render_template("/actors/edit.html", actor=actor, err=err)
        # return redirect(url_for("actors.edit", id=actor.id))
    else:
        db.session.add(actor)
        db.session.flush()
        db.session.commit()
        flash("Success!")
    # return render_template("/actors/show.html", actor=actor)
    return redirect(url_for("actors.show", id=actor.id))


@actors_blueprint.route("/actors/upload")
def upload_page():
    return render_template("/actors/upload.html")


@actors_blueprint.route("/actors/upload", methods=["POST"])
def upload():
    # messg = ""
    # check if the post request has the file part
    if "file" not in request.files or request.files["file"].filename == "":
        flash("No file part")
        # return redirect("/movies/upload")
        return render_template("/actors/upload.html")

    file = request.files["file"]

    if file and allowed_file(file.filename):
        for row in file.readlines():
            temp = json.loads(row)
            actor = Actor()
            for item in actor_headers:
                try:
                    setattr(actor, item, str(temp.get(str(item))))
                except AssertionError as err:
                    flash("Attention is required!")
                    return render_template("/actors/upload.html", err=err)

            db.session.add(actor)
        db.session.flush()
        db.session.commit()

        flash("File uploaded successfully!")
    else:
        flash("Unallowed file type")

    return redirect(url_for("actors.upload_page"))
