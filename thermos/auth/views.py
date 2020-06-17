from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user

# From the current package, import the auth object, which is the blueprint object, which acts like the old app object.
from . import auth
from .. import db
# Import the User model from the parent package. Keeping models out of blueprints and centralized.
from .. models import User
from .forms import LoginForm, SignupForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Create a new LoginForm FlaskForm instance from the forms.py
    form = LoginForm()
    # Validate the form, store the bookmarks and redirect to the index.
    if form.validate_on_submit():
        # Login and validate the user
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            # Pass the user object and remember_me flag and register it with Flask-Login
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            # Redirect to the index page or the page the user was trying to access pulled from the next arg.
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("Sorry, incorrect username or password. Please try again.")
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        # ToDo: Change user variable names so there's no warning. Even though they're scope safe.
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Welcome to Thermos {}! Please login with the details you provided".format(new_user.username))
        return redirect(url_for('.login'))
    return render_template('signup.html', form=form)


