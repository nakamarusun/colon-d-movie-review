from flask import g, current_app
import click
from flask.cli import with_appcontext
import mysql.connector as sql
from os import path

mydb = None

def connect_db(app):
    # Connects to the database server based on the json
    # configuration. and passes it to the global var.

    global mydb
    mydb = sql.connect(
        host=app.config['DATABASE_HOST'],
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASS'],
        allow_local_infile=True,
        # raise_on_warnings=True
    )
    # Enable loading data locally
    mydb.cursor().execute("SET GLOBAL local_infile=1;")

def init_database(app):
    # Initialize all the database and all the
    # tables and keep it empty.

    print("initializing tables...")
    with mydb.cursor() as cursor:
        # Creates the table here
        cursor.execute("USE " + app.config['DATABASE_NAME'])
        with app.open_resource("schema.sql", "rt") as file:
            for line in file.read().split(";"):

                string = line.strip().replace("\n", " ")
                cursor.execute(string)

        mydb.commit()
        print("Recreated the tables.")

def init_db_connection(app):
    # Initializes the first database connection,
    # and makes checks to ensure that the database
    # and all of the table schemas exists.

    connect_db(app)
    app.cli.add_command(init_db)
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
            init_database(app)

        # Don't forget to use the database for the whole duration of the db.
        cursor.execute("USE " + app.config['DATABASE_NAME'])

@click.command("init-db")
@with_appcontext
def init_db():
    # Initializes the database from the terminal.

    connect_db(current_app)
    cursor = mydb.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {}".format(current_app.config['DATABASE_NAME']))
    cursor.execute("CREATE DATABASE {}".format(current_app.config['DATABASE_NAME']))
    init_database(current_app)
    click.echo("Done initializing the Database!")