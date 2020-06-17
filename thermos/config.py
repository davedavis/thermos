import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # This project is not in production or live so safe to leave this on GitHub.
    SECRET_KEY = '\x83\xbf\x94\x19\x91\xd9:\x9a\x82\x12K\xbc\xa2\xc1f\xde\xc9\xbb\xa7\x82\xdd\t\xbb\xc7'
    DEBUG = False
    # This just removed the deprecation warning in the console.
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # This project is not in production or live so safe to leave this on GitHub.
    SQLALCHEMY_DATABASE_URI = 'mysql://thermos:thermosdev@localhost/thermosdev'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://thermos:thermosdev@localhost/thermosdev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    # Need to disable CSRF protection when running unit tests.
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "localhost.localdomain"


class ProductionConfig(Config):
    DEBUG = False
    # This project is not in production or live so safe to leave this on GitHub.
    SQLALCHEMY_DATABASE_URI = 'mysql://thermos:thermosdev@localhost/thermosdev'


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
