from flask import (g)
import mysql.connector as sql

mydb = None

def connect_db(app):
    # Connects to the database server based on the json
    # configuration. and passes it to the global var.

    global mydb
    mydb = sql.connect(
        host=app.config['DATABASE_HOST'],
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASS'],
    )


def init_database(app):
    # Initialize all the database and all the
    # tables and keep it empty.

    print("initializing tables...")
    with mydb.cursor() as cursor:
        with app.open_resource("schema.sql", "rt") as file:
            for line in file.read().split(";"):

                string = line.strip().replace("\n", " ")

                cursor.execute(string)

        print("Recreated the tables.")

def init_db_connection(app):
    # Initializes the first database connection,
    # and makes checks to ensure that the database
    # and all of the table schemas exists.

    connect_db(app)

    with mydb.cursor() as cursor:
        # Create cursor for future purposes
        cursor = mydb.cursor()

        cursor.execute("SHOW DATABASES")
        dbs = [ x[0] for x in cursor.fetchall() ]

        # Checks if database exists
        if app.config['DATABASE_NAME'] not in dbs:
            # Create it if it does not exist
            # Will throw sql.errors.ProgrammingError when user
            # does not have permission.
            cursor.execute("CREATE DATABASE " + app.config['DATABASE_NAME'])
            cursor.execute("USE " + app.config['DATABASE_NAME'])
            init_database(app)

    cursor.execute("USE " + app.config['DATABASE_NAME'])