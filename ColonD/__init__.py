from flask import (Flask, render_template)
import mysql.connector as sql

def create_app():

    # Create the main app
    app = Flask(__name__)

    # Load config from a json file
    app.config.from_json('conf.json')

    # Checks whether the app is on development mode
    if (app.config['ENV'] == "development"):
        print("Running on development mode.")

    # Registers the index to the main html
    @app.route("/")
    def index():
        return render_template("home/index.html")

    @app.route("/favicon.ico")
    def img():
        return "yes"

    from ColonD.cache import reg_static_uncache
    
    # Registers the app so that the static will change cache properly.
    reg_static_uncache(app)

    # Register the blueprints
    from ColonD import user
    app.register_blueprint(user.bp)

    return app