from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError

from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(3, 80),
                                                   Regexp('^[A-Za-z0-9_]{3,}$',
                                                          message="Usernames can only be letters, numbers or "
                                                                  "underscores")])
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