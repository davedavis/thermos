from flask_wtf import FlaskForm

from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Regexp, EqualTo, ValidationError, Email
from wtforms import PasswordField, BooleanField, SubmitField, StringField

# Class that uses the FlaskForm WTF class and and creates a simple form with two fields.
from thermos.models import User


class BookmarkForm(FlaskForm):
    url = URLField('Please enter a URL', validators=[DataRequired(), url()])
    description = StringField('Add an optional description')

    # Override the validate method to add some custom validation not included with WTForms.
    def validate(self):
        # TODO: Improve UX in validating when user doesn't enter a protocol. Fix reappending of incorrect URL form data.
        # if not self.url.data.startswith("http://") or self.url.data.startswith("https://"):
        #     self.url.data = "https://" + self.url.data
        # if not FlaskForm.validate(self):
        #     return False

        if not self.description.data:
            self.description.data = self.url.data

        return True


class LoginForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(3, 80),
                                                   Regexp('^[A-Za-z0-9_]{3,}$',
                                                   message="Usernames can only be letters, numbers or underscores")])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(4, 99),
                                                     EqualTo('password2', message="Passwords must match")])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(),
                                                     Length(1, 120),
                                                     Email()])

    # ToDo: Figure our a better way of doing this that's not a static method (Or add decorator)
    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already a user on this site with that email address')


    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken by somebody else. Sorry!')

