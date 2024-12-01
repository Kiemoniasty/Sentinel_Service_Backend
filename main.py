"""Main entry point for the application. """

from app.flask import app

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
