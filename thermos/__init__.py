from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Store it in the apps config dict. This is needed for the flash function and and to access the session object.
app.config['SECRET_KEY'] = '\x83\xbf\x94\x19\x91\xd9:\x9a\x82\x12K\xbc\xa2\xc1f\xde\xc9\xbb\xa7\x82\xdd\t\xbb\xc7'
# SQLAlchemy setup.
# Suppress the annoying deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# ToDo: Switch between SQLite and MySQL in dev/production. Although I could do with experience in MySQL in dev.
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
# pip install mysqlclient to get the SQLAlchemy MySQL support.
# Local testing so it's OK for this to be on GitHub.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://thermos:thermos@localhost/thermosdev'
db = SQLAlchemy(app)

# Needs to go at the end to avoid circular import issues.
# import thermos.models
import views

