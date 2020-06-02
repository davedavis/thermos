from thermos import app, db
from flask_script import Manager, prompt_bool
from thermos.models import User

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="Dave", email="dave@dave.com"))
    db.session.add(User(username="Sarah", email="sarahe@sarah.com"))
    db.session.add(User(username="Eimh", email="eimh@eimh.com"))
    db.session.add(User(username="Aido", email="aido@aido.com"))
    db.session.add(User(username="Kerrie", email="kerrie@kerrie.com"))
    db.session.add(User(username="Claire", email="claire@claire.com"))
    db.session.commit()
    print('Initialized the DB')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to drop everything?"):
        db.drop_all()
        print('Dropped the entire Database!')


if __name__ == '__main__':
    manager.run()
