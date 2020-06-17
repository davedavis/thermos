from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Regexp


# Class that uses the FlaskForm WTF class and and creates a simple form with two fields.
class BookmarkForm(FlaskForm):
    url = URLField('Please enter a URL', validators=[DataRequired(), url()])
    description = StringField('Add an optional description')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-Z0-9, ]*$',
                                                  message="Tags can only contain letters and numbers")])

    # Override the validate method to add some custom validation not included with WTForms.
    def validate(self):
        # TODO: Improve UX in validating when user doesn't enter a protocol. Fix reappending of incorrect URL form data.
        # if not self.url.data.startswith("http://") or self.url.data.startswith("https://"):
        #     self.url.data = "https://" + self.url.data
        # if not FlaskForm.validate(self):
        #     return False

        if not self.description.data:
            self.description.data = self.url.data

            # filter out empty and duplicate tag names
            # Split the input data at every comma, then remove all whitespace.
            stripped = [t.strip() for t in self.tags.data.split(',')]
            # Then remove all empty strings from the list.
            not_empty = [tag for tag in stripped if tag]
            # Put everything that remains in a set which removes all duplicates.
            tagset = set(not_empty)
            # Put the list of non-empty and non-duplicate tags into a comma separated string again.
            self.tags.data = ",".join(tagset)

        return True
