import os
from dotenv import load_dotenv


# Returns the full path of the executing script
basedir = os.path.abspath(os.path.dirname(__file__))

# Add all environment variable definitions in the .env file to os.environ
load_dotenv()


# Create default, development, testing and production configurations
# for Flask-SQLAlchemy configuration keys see: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# Default configuration
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    DB_USERNAME = os.environ.get('FLASK_DB_USERNAME')
    DB_PASSWORD = os.environ.get('FLASK_DB_PASSWORD')
    ITRACKER_ADMIN = os.environ.get('ITRACKER_ADMIN')
    # For SSL encryption see: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
    # SSL_REDIRECT = False

    @staticmethod
    # for now an empty init_app() method is implemented, it can take the application instance as an argument
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    ENV = "development"
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_TEST_DATABASE_URL')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
