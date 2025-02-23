"""Main entry point for the application. """

from app.flask import app

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
        # use_reloader=True,
        host="0.0.0.0",
        port=5000,
        # ssl_context=("certs/cert.pem", "certs/key.pem"),
    )
