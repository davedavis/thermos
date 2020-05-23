from flask_wtf import FlaskForm

from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
from wtforms.fields.core import StringField


class BookmarkForm(FlaskForm):
    url = URLField('url', validators=[DataRequired(), url()])
    description = StringField('description')
