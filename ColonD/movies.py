from functools import reduce
from flask import Blueprint, request, redirect, session, current_app, abort
from flask.helpers import flash, url_for
from flask.templating import render_template
from mysql.connector import cursor
from ColonD import db, user
from ColonD.util import util
from random import choice
from requests import get
from bs4 import BeautifulSoup
from math import ceil
from os import path
from datetime import datetime
from random import randint
import re

bp = Blueprint("movies", __name__, url_prefix="/movies")
flavor_words = ["Great", "Fine", "Marvelous", "Pretty", "Cool"]

def get_movie_poster(id, name, director):
    """
        Will return a link / base64 image based on
        the movie id entered. If it does not exist,
        returns a None.
    """

    image = None

    # Checks whether the image have been downloaded yet.
    poster_dir = path.join("poster_cache", id)
    if path.exists(path.join(current_app.instance_path, poster_dir)):
        
        # Tries to read from the file, and loads te image
        try:
            with current_app.open_instance_resource(poster_dir, "rt") as image_f:
                # Appends the image file to the list.
                image = image_f.read()

        except Exception:
            # If error, then load default image.
            pass
    
    else:     
        # Gets the image from google image scraping        
        image = util.scrape_g_image("{}+movie+poster+{}".format(name, director), current_app.config['SMALL_IMAGE'])

        # If the image is successfully loaded,
        if image:
            # Writes the image to a file for future caching.
            with current_app.open_instance_resource(poster_dir, "wt") as image_f:
                image_f.write(image)

    return image

@bp.route("/")
def home():

    content_per_page = int(request.args.get("amt", 10))
    content_per_page = content_per_page if content_per_page < 20 else 20
    page = int(request.args.get("pg", 1))

    query = None

    with db.mydb.cursor() as cursor:
    
        # Gets all the movie details from an offset (display as page)
        cursor.execute("SELECT movie_name, year_rel, runtime, director_name, m.id FROM movies m JOIN directors d ON m.director_id=d.id")
        query = cursor.fetchall()

    # The amount of movie available in the site.
    max_page = int(ceil(len(query) / content_per_page))

    # Gets the offset
    query = query[(page - 1) * content_per_page:(page - 1) * content_per_page + content_per_page]

    # Code snippet to get all the urls for scraping google images.
    images = []
    for row in query:

        image = get_movie_poster(row[4], row[0], row[3])

        if not image:
            # Load placeholder image
            images.append(url_for("static", filename="title.png"))
        else:
            images.append(image)

    query = [ list(query[i]) + [images[i]] for i in range(len(images)) ]

    return render_template("movies/index.html",
    flavor=choice(flavor_words),
    movies=query,
    page=page,
    max_page=max_page,
    movies_url=url_for('movies.home')
    )

def get_movie(id):
    cursor = db.mydb.cursor()
    # PENTING
    # Apparently, you have to insert ',' in the end at the parameters.
    cursor.execute("SELECT movie_name, year_rel, runtime, director_name, m.id FROM movies m JOIN directors d ON m.director_id=d.id WHERE m.id=%s", (id,))

    query = cursor.fetchall()
    if len(query) == 0:
        return None
    return query[0]

@bp.route("/<string:id>")
def movie(id):

    mov = get_movie(id)
    if not mov:
        # If there is no movie associated with that id
        abort(404)
    else:
        # If the movie exist.
        cursor = db.mydb.cursor()
        cursor.execute("SELECT title, created, body, star, username FROM review r JOIN user u ON r.author_id=u.id WHERE movie_id=%s ORDER BY created DESC;", (id,))

        query = cursor.fetchall()

        avg_star = float(reduce(lambda x, y : x + y[3], query, 0)) / len(query)

        return render_template("movies/movies.html",
        movie=mov,
        img=get_movie_poster(mov[4], mov[0], mov[3]),
        reviews=query,
        avg_star=avg_star)

@bp.route("/<string:id>/post", methods=["GET", "POST"])
@user.login_required
def movie_post(id):

    mov = get_movie(id)

    if request.method == "GET":
        # Get the forum posting thingy
        if not mov:
            # If there is no movie associated with that id
            abort(404)
        else:
            return render_template("movies/post.html",
            movie=mov,
            img=get_movie_poster(mov[4], mov[0], mov[3]))
    
    elif request.method == "POST":
        title = request.form["title"]
        content = request.form["review"]
        star = request.form["star"]

        if not mov:
            abort(404)
        else:
            user_id = session.get("user_id")
            if user_id:
                cursor = db.mydb.cursor()
                cursor.execute("INSERT INTO review (movie_id, author_id, created, title, body, star) VALUES(%s, %s, %s, %s, %s, %s);", (
                    id, user_id, datetime.now(), title, content, star
                ))
                cursor.execute("COMMIT;")

        return redirect(url_for("movies.movie", id=id))

@bp.route("/random")
def random():
    # Will lead the user to a random movie.
    cursor = db.mydb.cursor()
    cursor.execute("SELECT id FROM movies;")

    result = cursor.fetchall()

    return redirect(url_for("movies.movie", id=result[randint(0, len(result) - 1)][0]))

@bp.route("/posts")
def posts():

    # If the movie exist.
    cursor = db.mydb.cursor()
    cursor.execute("SELECT title, created, body, star, username FROM review r JOIN user u ON r.author_id=u.id ORDER BY created DESC;")

    query = cursor.fetchall()

    avg_star = float(reduce(lambda x, y : x + y[3], query, 0)) / len(query) if len(query) else 0

    return render_template("home/posts.html",
    reviews=query,
    avg_star=avg_star)