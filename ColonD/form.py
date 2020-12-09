from flask import Blueprint, request, redirect, session, current_app, Response
from datetime import datetime
from os import path

bp = Blueprint("api", __name__, url_prefix="/api")

# For google forms test
@bp.route("form", methods=["GET", "POST"])
def form():
    
    if request.method == "POST":
        # Saves it into an instance file
        data = request.form.get("data")
        # If only it exists
        if data:
            with current_app.open_instance_resource("form", "wt") as file:
                file.write(datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S\n"))
                file.write(data)
            
            return "Success!"

        return "Fail!"

    elif request.method == "GET":
        # Gets the latest time the item is posted.
        if path.exists(path.join(current_app.instance_path, "form")):
            with current_app.open_instance_resource("form", "r") as file:
                return Response(file.read(), content_type="text/plain") 

        return "Empty"