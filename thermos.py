from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from forms import BookmarkForm
from flask_sqlalchemy import SQLAlchemy
import os


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)


# Store it in the apps config dict. This is needed for the flash function and and to access the session object.
app.config['SECRET_KEY'] = '\x83\xbf\x94\x19\x91\xd9:\x9a\x82\x12K\xbc\xa2\xc1f\xde\xc9\xbb\xa7\x82\xdd\t\xbb\xc7'

# SQLAlchemy setup.
# Suppress the annoying deprecation warning in the console.
app.config ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ToDo: Switch between SQLite and MySQL in dev/production. Although I could do with experience in MySQL in dev.
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
# pip install mysqlclient to get the SQLAlchemy MySQL support.
# Local testing so it's OK for this to be on GitHub.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://thermos:thermos@localhost/thermosdev'
db = SQLAlchemy(app)


# Temporary structure to hold bookmarks, pending DB.
bookmarks = []


# Temporary method to store bookmarks in the temporary dict.
def store_bookmarks(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user="Dave",
        date=datetime.utcnow()
    ))


# Method that gets and sorts bookmarks to be displayed.
def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=new_bookmarks(5))


# If the method is POST, process the form. If it's GET, create and show the form.
@app.route('/add', methods=['GET', 'POST'])
def add():
    # Create a new BookmarkForm instance.
    form = BookmarkForm()
    # Validate the form, store the bookmarks and redirect to the index.
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        store_bookmarks(url, description)
        flash("Stored '{}'".format(description))
        return redirect(url_for('index'))
    # Render the add template giving it the empty form object.
    return render_template('add.html', form=form)


# Error handling.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('405.html'), 405


if __name__ == '__main__':
    app.run()
