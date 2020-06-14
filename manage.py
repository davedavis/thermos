from thermos import app, db
from flask_script import Manager, prompt_bool
from thermos.models import User

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username="Dave", email="dave@dave.com", password="dave"))
    db.session.add(User(username="Sarah", email="sarahe@sarah.com", password="sarah"))
    db.session.add(User(username="Eimh", email="eimh@eimh.com", password="eimh"))
    db.session.add(User(username="Aido", email="aido@aido.com", password="aido"))
    db.session.add(User(username="Kerrie", email="kerrie@kerrie.com", password="kerrie"))
    db.session.add(User(username="Claire", email="claire@claire.com", password="claire"))
    db.session.commit()
    print('Initialized the DB')


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
