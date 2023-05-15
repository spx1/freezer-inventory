import os
from flask_sqlalchemy import SQLAlchemy
import flask

BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

def create_app(environment: str = 'Test') -> flask.Flask:
    '''Create the Flask application and bind the sqlalchemy objects'''
    from .config import config_by_name

    app = flask.Flask(__name__)
    app.config.from_object( config_by_name[ environment ] )
    db.init_app(app)

    @app.route("/health")
    def health():
        flask.jsonify("Web server is healthy")