# Project Structure
# Models, Templates and Static files are all thermos package/root level.
# Functionality is broken down into views and forms in relevant package level blueprints.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_debugtoolbar import DebugToolbarExtension

# Import the config dictionary.
from .config import config_by_name

# SQLAlchemy setup.
# Suppress the annoying deprecation warning in the console.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # Local testing so it's OK for this to be on GitHub.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://thermos:thermosdev@localhost/thermosdev'
db = SQLAlchemy()

# Login/Authentication configuration setup
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"

# Create a Moment instance
moment = Moment()

# Create a DebugToolBar instance.
toolbar = DebugToolbarExtension()


# App factory function
def create_app(config_name):
    app = Flask(__name__)
    # Currently hardcoding the development configuration in as there's no deployment yet.
    # See https://github.com/cburmeister/flask-bones for more details on alternatives.
    # app.config.from_object(config_by_name[config_name])
    app.config.from_object(config.DevelopmentConfig)
    db.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)

    # Register blueprints. Do them here because some of them might depend on the db or login_manager when loading. So
    # we want to make sure that we don't load these modules before we have set up the entire application, including the
    # extensions.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .bookmarks import bookmarks as bookmarks_blueprint
    app.register_blueprint(bookmarks_blueprint, url_prefix='/bookmarks')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
