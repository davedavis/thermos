from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user

from thermos.forms import BookmarkForm, LoginForm, SignupForm
from thermos import app, db, login_manager
from thermos.models import User, Bookmark, Tag


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
        tags = form.tags.data
        # What we're passing to the model here in the tag parameter is just a comma separated list of words.
        # As that's all the HTML input receives in the form.
        bm = Bookmark(user=current_user, url=url, description=description, tags=tags)
        db.session.add(bm)
        db.session.commit()
        flash("Stored '{}'".format(description))
        return redirect(url_for('index'))
    # Render the add template giving it the empty form object.
    return render_template('bookmark_form.html', form=form)


@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        # Magic method provided by flask that copies the form data automatically, so no need to define tags.
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}'".format(bookmark.description))
        # return render_template(url_for('user', username=current_user.username))
        return render_template('user.html', user=current_user)
    return render_template('bookmark_form.html', form=form, title='Edit Bookmark')


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(request.args.get('next') or url_for('index'))
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
        flash("Welcome to Thermos {}! Please login with the details you provided".format(new_user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/tag/<name>')
def tag(name):
    # Try to retrieve a tag by that name. Then pass back the Tag model object we just got from the DB.
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)


@app.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash("Deleted '{}'".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    else:
        flash('Are you extra sure you want to delete this?')
    return render_template('confirm_delete.html', bookmark=bookmark, nolinks=True)


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


@app.errorhandler(403)
def not_authorized(e):
    return render_template('403.html'), 403


@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)


if __name__ == '__main__':
    app.run()
