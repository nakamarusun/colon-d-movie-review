from flask import Blueprint, request
from flask.templating import render_template

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":

        user = request.form["user"]
        email = request.form["email"]
        password = request.form["pass"]
        
        print(user, email, password)

    return render_template("user/register.html")

@bp.route("login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        
        user = request.form["user"]
        password = request.form["pass"]
        
        print(user, password)
    
    return render_template("user/login.html")