import os
from os.path import dirname, abspath
db_path = dirname(dirname(dirname(abspath(__file__))))

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_path, 'prod.db')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(db_path, 'test.db')
    SQLALCHEMY_ECHO = False
