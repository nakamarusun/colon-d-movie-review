from flask import Blueprint
from flask.templating import render_template

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("register")
def register_user():
    return render_template("user/register.html")