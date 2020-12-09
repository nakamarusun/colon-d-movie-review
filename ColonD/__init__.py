from flask import (Flask, render_template)
from flask.templating import render_template_string
from ColonD import db, instances, form
from os import environ, makedirs
import os

def create_app():

    # Create the main app
    project_root = os.path.dirname(os.path.realpath('__file__'))
    app = Flask(__name__,
        template_folder=os.path.join(project_root, 'ColonD/templates'),
        static_folder=os.path.join(project_root, 'ColonD/static')
    )

    # Load config from a json file
    app.config.from_json(environ.get("FLASK_TEST_CONF", "conf.json"))
    app.config.from_mapping(SECRET_KEY="devsecret")

    # Checks whether the app is on development mode
    if (app.config['ENV'] == "development"):
        print("Running on development mode.")
    
    db.init_db_connection(app)

    # Initializes all the instance folder
    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    # Initializes all the instance folder
    instances.init_instances(app)

    # Registers the index to the main html
    @app.route("/")
    def index():
        return render_template("home/index.html")

    @app.route("/favicon.ico")
    def img():
        return "yes"

    @app.errorhandler(404)
    def page404(e):
        return render_template("404.html")

    from ColonD.cache import reg_static_uncache
    
    # Registers the app so that the static will change cache properly.
    reg_static_uncache(app)

    # Register the blueprints
    from ColonD import user, movies
    app.register_blueprint(user.bp)
    app.register_blueprint(movies.bp)
    app.register_blueprint(form.bp)

    if (app.config['ENV'] == "development"):
        print("App instantiation done!")

    return app