""" Main entry point for the application. """

import app.flask as flask_app

app = flask_app.app

if __name__ == "__main__":
    app.run(debug=True)
