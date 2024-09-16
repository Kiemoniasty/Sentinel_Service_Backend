"""Main entry point for the application. """

from app import flask as flask_app
from databases.init_postgres_db import InitPostgresDBs

app = flask_app.app

InitPostgresDBs.create_dbs()

if __name__ == "__main__":
    app.run(debug=True)
