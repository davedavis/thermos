from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import desc
from thermos import db

from werkzeug.security import check_password_hash, generate_password_hash

# This needs to be added to work on the command line, avoiding the redefining of models.
# db.metadata.clear()


# A bookmark can have any number of tags, and a tag can be associated with any number of bookmarks. So we need a m2m
# relationship. To do this, we set up a tags (plural) junction table, containing foreign keys to both models. Junction
# table is defined directly, using the db.table class as we're not going to need a model for this as tags won't be
# accessed. We only need the singular tag model.
tags = db.Table('bookmark_tag',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
                )


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Set the relationship with the Tag class, need to use a string as it's not defined until later. ToDo: Move it up
    # and replace it with the class name for future proofing. The second argument to the relationship call is the
    # argument 'secondary' which tells the relationship to use our junction table called "tags" above. We also defined
    # a backref called 'bookmarks' which will add an attribute called bookmarks to the other side of the relationship.
    # So each tag will get a bookmarks attribute containing a list of the associated bookmarks. Dynamic loading in case
    # there are a large number of bookmarks associated with each tag.
    # Underscore as I don't want to access this directly from other classes.
    _tags = db.relationship('Tag', secondary=tags, backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    # In the view and the form, we handle the list of tags as a comma separated string. So it's convenient to create a
    # tag property that provides a list of strings as well. The getter takes the contents of the _tags list which holds
    # actual Tag model objects. Then it takes the name from each and joins it into a string. So when we ask for the
    # value of the tags property on a bookmark, we get a string, with a list of tag names.
    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    # When we pass a string with a list of tags to be set to this property, we need to find out for each of those tags
    # whether it already exists in the database. If it doesn't, we need to insert a new tag into the tag table and then
    # add the new model object to the tag list for this bookmark. If it does exist, we can simply retrieve it and put it
    # in the list. So if it exists, we create a new method get_or_create that takes the name of a tag and returns a tag
    # model instance by either creating or retrieving a tag with that name. We then do a for loop over all the words in
    # the string we received and then call the method on each of those words. The resulting list is a list of tag model
    # objects and we can assign that to the _tags attribute. Assigning a list of tag objects is all we have to do and
    # SQLAlchemy will take it from there and create all the relevant rows in the database.
    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]

    def __repr__(self):
        return "Bookmark '{}': '{}'>".format(self.description, self.url)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(256))

    @property
    def password(self):
        raise AttributeError('Password: Write Only Field. Check the models file if you are unsure')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    # ToDo: Add a get_userid_by_user

    def __repr__(self):
        return '<User %r>' % self.username


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True, index=True)

    # Get_or_create uses a Try statement to retrieve a tag with a given name. If that throws an exception (tag doesn't
    # exist), we create a new tag and return that. So this way, we can convert strings to tags and back.
    # ToDo: Fix Exception warning
    @staticmethod
    def get_or_create(name):
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        return Tag.query.all()

    def __repr__(self):
        return self.name
