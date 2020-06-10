from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user

from thermos.forms import BookmarkForm, LoginForm, SignupForm
from thermos import app, db, login_manager
from thermos.models import User, Bookmark


# Flask-Login user loader (load_user implementation). Needs to return a user object given an ID in each session.
@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


# If the method is POST, process the form. If it's GET, create and show the form.
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    # Create a new BookmarkForm instance.
    form = BookmarkForm()
    # Validate the form, store the bookmarks and redirect to the index.
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored '{}'".format(description))
        return redirect(url_for('index'))
    # Render the add template giving it the empty form object.
    return render_template('add.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Create a new LoginForm FlaskForm instance from the forms.py
    form = LoginForm()
    # Validate the form, store the bookmarks and redirect to the index.
    if form.validate_on_submit():
        # Login and validate the user
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            # Redirect to the index page or the page the user was trying to access pulled from the next arg.
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash("Sorry, incorrect username or password. Please try again.")
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # ToDo: Change user variable names so there's no warning. Even though they're scope safe.
        new_user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Welcome to Thermos {}! Please login with the details you provided".format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
