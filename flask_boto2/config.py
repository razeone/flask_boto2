import os

# Define app directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    Common settings for the app
    """
    HOST = "0.0.0.0"
    PORT = 8080
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "secret"
    SECRET_KEY = "secret"
    GOOGLE_LOGIN_CLIENT_ID = ''
    GOOGLE_LOGIN_CLIENT_SECRET = ''
    GOOGLE_LOGIN_REDIRECT_SCHEME = 'http'
    GOOGLE_LOGIN_REDIRECT_PATH = '/'
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    REGION_LIST = {'eu-central-1', 'us-west-2'}
    DATABASE_CONNECT_OPTIONS = {}
    THREADS_PER_PAGE = 2
    DEBUG = False
    BROKER_URL = 'redis://localhost:6379/0'


class ProductionConfig(Config):
    """
    Configurations for production environment
    """
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_DATABASE_NAME = ''
    SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@%s/%s' % (
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_DATABASE_NAME
    )


class DevelopmentConfig(Config):
    """
    Configurations for development environment
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
