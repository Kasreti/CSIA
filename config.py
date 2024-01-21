import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sahala'
    # This line is a configuration that allows SQLAlchemy to find the location of
    # the application's database.
    SQLALCHEMY_DATABASE_URI = os.environ.get('sqlite:////app.db') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
