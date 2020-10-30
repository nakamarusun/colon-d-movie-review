from flask import Blueprint, request, redirect, session, current_app
from flask.helpers import flash, url_for
from flask.templating import render_template
from ColonD import db
from ColonD.util import util
from random import choice
from requests import get
from bs4 import BeautifulSoup
import re

bp = Blueprint("movies", __name__, url_prefix="/movies")
flavor_words = ["Great", "Fine", "Marvelous", "Pretty", "Cool"]

@bp.route("/")
def home():

    content_per_page = int(request.args.get("amt", 10))
    content_per_page = content_per_page if content_per_page < 20 else 20
    page = int(request.args.get("pg", 1))

    cursor = db.mydb.cursor()
    
    # Gets all the movie details from an offset (display as page)
    cursor.execute("SELECT movie_name, year_rel, runtime, director_name FROM movies m JOIN directors d ON m.director_id=d.id LIMIT {}, {}"
    .format((page - 1) * content_per_page, content_per_page))

    query = cursor.fetchall()

    # The amount of movie available in the site.
    movies = len(query)

    small_image = current_app.config['SMALL_IMAGE']

    # Code snippet to get all the urls for scraping google images.

    images = []
    for row in query:
        # Gets the html page that the image is contained.

        # Here we can adjust what mode we want to retrieve the image.
        # If small_image is true, we get all the image based on their very small
        # thumbnail from google, and the user have to load the links individually.
        # If it is false, then the image got will be higher quality, and the user does
        # not have to load the link individually.
        if small_image:
            html = get('https://www.google.com/search?q={}+movie+poster+{}&tbm=isch'.format(row[0], row[3])).text
            bp = BeautifulSoup(html, 'html.parser')
            img = bp.find_all('img')
            
            images.append(img[1].get('src'))
        else:
            # The header is there so that as if a windows computer is accessing the website.
            # This will provide a different response from small_image=True.
            html = get('https://www.google.com/search?q={}+movie+poster+{}&tbm=isch'.format(row[0], row[3]), headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0", "Accept": "image/webp,*/*"
                }).text
            # Defines a RegEx pattern in which the image is contained
            pattern = re.compile(r"_setImgSrc\('[0-9]+','[^']+'\)", re.MULTILINE)

            # Searches the text
            raw_data = pattern.search(html)

            img = None
            if not raw_data:
                # Debugging purposes
                with open("failed_html.html", "wb+") as file:
                    file.write(html)
                # Placeholder image.
                img = url_for('static', filename='title.png')
            else:
                # Raw data
                img_str = raw_data.group()
                img = img_str.replace("\\", "")[util.findnth(img_str, "'", 3) + 1:-2]
            
            images.append(img)

    query = [ list(query[i]) + [images[i]] for i in range(len(images)) ]

    return render_template("movies/index.html", flavor=choice(flavor_words), movies=query)