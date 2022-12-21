import os
import logging
from flask_compress import Compress
from logging.handlers import SMTPHandler

import smtplib


basedir = os.path.abspath(os.path.dirname(__file__))

# mail server settings
'''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USERNAME = 'ckmusicworkshop@gmail.com'
MAIL_PASSWORD = '#cengizkurt#'
MAIL_TO = 'ckmusicworkshopinfo@gmail.com'
'''

'''
FB_APP_ID='876652592469714'
FB_APP_SECRET='7522e91d4fd42dd87245c167887cf13e'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'musiccourse-dev.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

'''





class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SSL_DISABLE = True

    # sqlite :memory: identifier is the default if no filepath is present
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'musiccourse-dev.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    LOGGING_LOCATION_DEV = 'tmp/musiccourse_dev.log'
    LOGGING_LOCATION_PRO = 'tmp/musiccourse_pro.log'
    LOGGING_LOCATION_TEST = 'tmp/musiccourse_test.log'
    LOGGING_LEVEL = logging.DEBUG
    SECURITY_CONFIRMABLE = False
    CACHE_TYPE = 'simple'
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', \
'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500
    SUPPORTED_LANGUAGES = {'en': 'English', 'tr': 'Turkish'}
    BABEL_DEFAULT_LOCALE = 'tr'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    # slow database query threshold (in seconds)
    DATABASE_QUERY_TIMEOUT = 0.5

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_TO = os.environ.get('MAIL_TO')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_FLUSH_INTERVAL = 3600  # one hour
    MAIL_ERROR_RECIPIENT = os.environ.get('MAIL_ERROR_RECIPIENT')

    FB_APP_ID = os.environ.get('FB_APP_ID')
    FB_APP_SECRET = os.environ.get('FB_APP_SECRET')

    RECAPTCHA_SITEKEY = os.environ.get('RECAPTCHA_SITEKEY')

    ADMIN_EMAILS = ['bkamberoglu@gmail.com', 
                'b_kamberoglu@yahoo.com',
                'cengizkurtmusicworkshop@gmail.com',
                'ckmusicworkshop@gmail.com']



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'musiccourse-dev.db')
    SQLALCHEMY_RECORD_QUERIES = True
    #SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    MAIL_FLUSH_INTERVAL = 60 # one minute


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'musiccourse-test.db')
    #SECRET_KEY = 'secret'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    #DEBUG = False
    #TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'musiccourse-pro.db')
    



config = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig",

    "default": "config.DevelopmentConfig"
}



  