# Import Flask extensions
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_user import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_option):
    app = Flask(__name__)

    # app configurations
    app.config.from_object(config_options[config_option])

    # initialise flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints

    return app
