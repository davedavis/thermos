from thermos import app, db
from flask_script import Manager, prompt_bool
# Need to import ALL model classes so Alembic/Migrate can use them.
from thermos.models import User, Bookmark, Tag
from flask_migrate import Migrate, MigrateCommand

# Manager/Manage.py setup. ToDo: Upgrade to Click/Flask CLI
manager = Manager(app)

# Need to pass the app AND the db object.
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def insert_data():
    dave = User(username="Dave", email="dave@dave.com", password="dave")
    db.session.add(dave)
    sarah = User(username="Sarah", email="sarahe@sarah.com", password="sarah")
    db.session.add(sarah)
    karl = User(username="Karl", email="karl@karl.com", password="karl")
    db.session.add(karl)

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description, user=dave, tags=tags))

    for name in ["python", "flask", "webdev", "programming", "training", "news", "orm", "databases", "emacs"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark("http://www.davedavis.io", "My website", "training,programming,python,flask,webdev")
    add_bookmark("http://www.python.org", "Python - my favorite language", "python")
    add_bookmark("http://flask.pocoo.org", "Flask: Web development one drop at a time.", "python,flask,webdev")
    add_bookmark("http://www.reddit.com", "Reddit. Frontpage of the internet", "news,coolstuff,fun")
    add_bookmark("http://www.sqlalchemy.org", "Nice ORM framework", "python,orm,databases")

    db.session.commit()
    print('Initialized the DB with sample data')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop everything?"):
        db.drop_all()
        print('Dropped the entire Database!')


if __name__ == '__main__':
    manager.run()


# As per: https://github.com/cburmeister/flask-bones
# from thermos import create_app, config
# app = create_app(config.dev_config)
