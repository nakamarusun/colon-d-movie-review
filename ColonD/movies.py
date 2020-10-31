from flask import Blueprint, request, redirect, session, current_app
from flask.helpers import flash, url_for
from flask.templating import render_template
from ColonD import db
from ColonD.util import util
from random import choice
from requests import get
from bs4 import BeautifulSoup
from math import ceil
from os import path
import re

bp = Blueprint("movies", __name__, url_prefix="/movies")
flavor_words = ["Great", "Fine", "Marvelous", "Pretty", "Cool"]

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

        image = None

        # Checks whether the image have been downloaded yet.
        poster_dir = path.join("poster_cache", row[4])
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
            image = util.scrape_g_image("{}+movie+poster+{}".format(row[0], row[3]), current_app.config['SMALL_IMAGE'])

            # If the image is successfully loaded,
            if image:
                # Writes the image to a file for future caching.
                with current_app.open_instance_resource(poster_dir, "wt") as image_f:
                    image_f.write(image)

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

@bp.route("/<string:id>")
def movie(id):
    return id