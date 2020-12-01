import functools
from flask import Blueprint, request, redirect, session
from flask.helpers import flash, url_for
from flask.templating import render_template
from ColonD import db
from werkzeug.security import (check_password_hash, generate_password_hash)

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("register", methods=["GET", "POST"])
def register_user():

    # Logs out the user if they are logged in
    if session.get("user", None) != None:
        flash("You are logged out.", "Success")
        session.clear()

    if request.method == "POST":
        # POST request when registering.
        user = request.form["user"]
        email = request.form["email"]
        password = request.form["pass"]

        # To keep track of errors.
        error = []
        
        # MySQL cursor
        cursor = db.mydb.cursor()

        cursor.execute("SELECT * FROM user WHERE username='{}'".format(user))
        if cursor.fetchall():
            # If username already exists
            error.append("Username already exists!")

        cursor.execute("SELECT * FROM user WHERE email='{}'".format(email))
        if cursor.fetchall():
            # If email already exists
            error.append("Email already exists!")

        if error:
            # If error exists
            flash("\n".join(error), "Error")

        else:
            # If there is no errors in the list
            # Inserts the new user into the database
            cursor.execute("INSERT INTO user (username, email, password) VALUES ('{}', '{}', '{}')"
            .format(
                user,
                str(email),
                generate_password_hash(password, salt_length=20)
            ))
            db.mydb.commit()
            flash("Registration Succeeded!, log in to enter the site.", "Success")
            return redirect(url_for("user.login_user"))

    return render_template("user/register.html")

@bp.route("login", methods=["GET", "POST"])
def login_user():

    # Logs out the user if they are logged in
    if session.get("user", None) != None:
        flash("You are logged out.", "Success")
        session.clear()

    if request.method == "POST":
        
        user = request.form["user"]
        password = request.form["pass"]
        
        # Keep track of errors
        error = []

        # DB Cursor
        cursor = db.mydb.cursor()

        username = None

        # See if the user exists in the db
        cursor.execute("SELECT * FROM user WHERE username='{user}' OR email='{user}'".format(user=user))
        query = cursor.fetchall()
        if not query:
            error.append("User/email not found!")

        else:
            query = query[0]
            username = query[1]
            pass_hash = query[3]

            # Checks password hash
            if not check_password_hash(pass_hash, password):
                error.append("Wrong password!")
        
        if error:
            flash("\n".join(error), "Error")
        else:
            session["user"] = username
            session["user_id"] = query[0]
            return redirect(url_for("index"))
    
    return render_template("user/login.html")

@bp.route("logout")
def logout_user():
    # Logs out the user from the website
    session.clear()
    return redirect(request.referrer)

def login_required(view):
    #View decorator that redirects anonymous users to the login page.

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("user") == None:
            flash("Login required!", "Error")
            return redirect(url_for("user.login_user"))

        return view(**kwargs)

    return wrapped_view