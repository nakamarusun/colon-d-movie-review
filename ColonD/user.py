from flask import Blueprint, request
from flask.helpers import flash
from flask.templating import render_template
from ColonD import db
from werkzeug.security import (check_password_hash, generate_password_hash)

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("register", methods=["GET", "POST"])
def register_user():
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

        if not error:
            # If there is no errors in the list
            # Inserts the new user into the database
            cursor.execute("INSERT INTO user (username, email, password) VALUES ('{}', '{}', '{}')"
            .format(
                user,
                str(email),
                generate_password_hash(password, salt_length=20)
            ))
            db.mydb.commit()
            flash("Registration Succeeded!", "Success")
        else:
            # If error exists
            flash("\n".join(error), "Error")

    return render_template("user/register.html")

@bp.route("login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        
        user = request.form["user"]
        password = request.form["pass"]
        
        # Keep track of errors
        error = []

        # DB Cursor
        cursor = db.mydb.cursor()

        # See if the user exists in the db
        cursor.execute("SELECT * FROM user WHERE username='{user}' OR email='{user}'".format(user=user))
        if not cursor.fetchall():
            error.append("User/email not found!")

        else:
            cursor.execute("SELECT password FROM user WHERE username='{user}' OR email='{user}'".format(user=user))
            pass_hash = cursor.fetchall()[0][0]

            # Checks password hash
            if not check_password_hash(pass_hash, password):
                error.append("Wrong password!")
        
        if error:
            flash("\n".join(error), "Error")
        else:
            return "Welcome!"
    
    return render_template("user/login.html")