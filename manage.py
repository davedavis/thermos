import os
from thermos import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('THERMOS_ENV') or 'dev')

# Manager/Manage.py setup. ToDo: Upgrade to Click/Flask CLI
manager = Manager(app)

# Need to pass the app AND the db object.
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# For when migrations don't go so well.
# @manager.command
# def insert_data():
#     dave = User(username="Dave", email="dave@dave.com", password="dave")
#     db.session.add(dave)
#     sarah = User(username="Sarah", email="sarahe@sarah.com", password="sarah")
#     db.session.add(sarah)
#     karl = User(username="Karl", email="karl@karl.com", password="karl")
#     db.session.add(karl)
#
#
# @manager.command
# def dropdb():
#     if prompt_bool("Are you sure you want to drop everything?"):
#         db.drop_all()
#         print('Dropped the entire Database!')
