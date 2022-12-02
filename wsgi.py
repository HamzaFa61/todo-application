"""
Application entry point
"""
from application import create_app
from application.shared.secrets import secrets

app = create_app()

if __name__ == "__main__":
    app.run(debug=secrets['dev_server'])
