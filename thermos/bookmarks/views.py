from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user

from . import bookmarks
from .forms import BookmarkForm
from .. models import Bookmark, User, Tag
from .. import db


@bookmarks.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))
    # Render the add template giving it the empty form object.
    return render_template('bookmark_form.html', form=form)


@bookmarks.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
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
        # return render_template(url_for('.user', username=current_user.username)) ToDo: Fix This
        return render_template('user.html', user=current_user)
    return render_template('bookmark_form.html', form=form, title='Edit Bookmark')


@bookmarks.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash("Deleted '{}'".format(bookmark.description))
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash('Are you extra sure you want to delete this?')
    return render_template('confirm_delete.html', bookmark=bookmark, nolinks=True)


@bookmarks.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bookmarks.route('/tag/<name>')
def tag(name):
    # Try to retrieve a tag by that name. Then pass back the Tag model object we just got from the DB.
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)