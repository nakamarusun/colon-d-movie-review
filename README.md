# Welcome to Colon D
## Colon D Movie Reviewer: The best movie reviewer ever
#### TA Database Project by Group 3

<p align="center">
<img src=ColonD/static/title.png />
<div style="text-align: center;">*Author note: `Colon D` is typed as :<zero-width space>D</div>
</p>

<br>
This project is developed in flask and coded in python. Includes basic authentication that stores in the database. Password is hashed for safety. Movie and director database is adopted from https://www.imdb.com/interfaces/ . All posters from the movies are gotten from a webscraper looking for images in Google Images, and saved as cache. 

Available in jasoncoding.com/colond !

# How to install:

## For development
1.  Clone project and login
```bash
git clone https://github.com/nakamarusun/colon-d-movie-review.git
cd colon-d-movie-review
```
1.  Create a virtual environment for Python 3 (Google if don't know :<zero-width space>( )
```bash
python -m venv venv
```

3. Activate the virtual environment, and install libs
```bash
venv/Scripts/activate
pip install -r requirements.txt
```

3. Make environment variable for flask app
Windows:
```bash
set FLASK_APP=ColonD
```
Linux / Mac:
```bash
export FLASK_APP=ColonD
```

4. Copy and rename conf.json_template to conf.json and configure it by yourself
5. Create the database and tables using the command
```bash
flask init-db
```
6. Run the flask project, and access using http://127.0.0.1:5000/
```bash
flask run
```

## For operational server
wsgi.py is already made for the server, just have to select it in the server configuration page.