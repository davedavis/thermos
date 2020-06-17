from flask import render_template

# Load the blueprint object instead of the app object.
from . import main

# Flask-Login user loader (load_user implementation). Needs to return a user object given an ID in each session.
from .. import login_manager
from ..models import User, Bookmark, Tag


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


# Error handling.
@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@main.app_errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405


@main.app_errorhandler(403)
def not_authorized(e):
    return render_template('403.html'), 403


@main.app_context_processor
def inject_tags():
    return dict(all_tags=Tag.all)
