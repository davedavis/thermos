from flask_wtf import FlaskForm

from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url
from wtforms.fields.core import StringField


# Class that uses the FlaskForm WTF class and and creates a simple form with two fields.
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
