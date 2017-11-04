# Import Flask extensions
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_babelex import Babel
from flask_user import UserManager, UserMixin, SQLAlchemyAdapter

# initialise Flask extensions
bootstrap = Bootstrap()
babel = Babel()
db = SQLAlchemy()


def create_app(config_option):
    app = Flask(__name__)

    # app configurations
    app.config.from_object(config_options[config_option])

    # initialise flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    babel.init_app(app)

    # Setup flask_user to handle user account related forms
    from .models.user_models import User, MyRegisterForm
    from .views.misc_views import user_profile_page

    # Setup the SQLAlchemy DB Adapter
    db_adapter = SQLAlchemyAdapter(db, User)

    # Initialise Flask-User and bind to app
    user_manager = UserManager(
        db_adapter, app, register_form=MyRegisterForm, user_profile_view_function=user_profile_page)

    # Register Blueprints

    return app
