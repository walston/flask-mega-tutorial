import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    HOST = os.environ.get('FLASK_HOST') or '0.0.0.0'
    PORT = os.environ.get('FLASK_PORT') or 5000
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    POSTS_PER_PAGE = 25
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
