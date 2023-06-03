import os
from flask_sqlalchemy import SQLAlchemy
import flask

BASE_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
APP_NAME = "Inventory"
TEMPLATE_DIRECTORY = f"{BASE_DIRECTORY}/app/templates"
STATIC_DIRECTORY = f"{BASE_DIRECTORY}/app/static"
db = SQLAlchemy()

def create_app(environment: str = 'Test') -> flask.Flask:
    '''Create the Flask application and bind the sqlalchemy objects'''
    from .config import config_by_name
    from .control import api

    app = flask.Flask(__name__)
    app.config.from_object( config_by_name[ environment ] )
    db.init_app(app)

    app.register_blueprint(api)
    
    @app.route("/health")
    def health():
        return flask.jsonify("Web server is healthy")

    return app