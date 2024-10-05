"""Main entry point for the application. """

from app.flask import app
from databases.init_postgres_db import InitPostgresDBs

InitPostgresDBs.create_dbs()

if __name__ == "__main__":
    app.run(debug=True)
