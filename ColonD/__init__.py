from flask import (Flask, render_template)

def create_app():

    # Create the main app
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("home/index.html")

    @app.route("/favicon.ico")
    def img():
        return "yes"

    from ColonD.cache import reg_static_uncache
    
    # Registers the app so that the static will change cache properly.
    reg_static_uncache(app)

    return app