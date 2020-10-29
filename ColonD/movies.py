from flask import Blueprint, request, redirect, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from ColonD import db
from random import choice

bp = Blueprint("movies", __name__, url_prefix="/movies")
flavor_words = ["Great", "Fine", "Marvelous", "Pretty", "Cool"]

@bp.route("/")
def home():
    cursor = db.mydb.cursor()
    cursor.execute("SELECT movie_name, year_rel, runtime, director_name FROM movies m JOIN directors d ON m.director_id=d.id LIMIT 0, 10")
    query = cursor.fetchall()
    
    return render_template("movies/index.html", flavor=choice(flavor_words), movies=query)