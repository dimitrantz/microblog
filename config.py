import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    # Posts per page configuration.
    POSTS_PER_PAGE = 5
    # Supported languages list.
    LANGUAGES = ['en', 'es']
    #Add Microsoft Translator API key to the configuration key value: 9fc365a267e84d6ca470aaec23128b70
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    # Elasticsearch configuration.
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    # Option to log to stdout.
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    # RQ integration.
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'