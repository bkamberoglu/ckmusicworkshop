import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_moment import Moment

from app.cache import cache
from config import config

import json


moment = Moment()
#db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
   # config[config_name].init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.permanent_session_lifetime = timedelta(minutes=60)

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production
        print ("I am in if not app.config['DEBUG'] and not app.config['TESTING'] =====> ")
        # email errors to the administrators
        if app.config.get('MAIL_ERROR_RECIPIENT') is not None:
            from logging.handlers import SMTPHandler
            credentials = None
            secure = None
            if app.config.get('MAIL_USERNAME') is not None:
                credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                if app.config['MAIL_USE_TLS'] is not None:
                    secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                toaddrs=[app.config['MAIL_ERROR_RECIPIENT']],
                subject='Application Error',
                credentials=credentials,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
            mail_handler.setFormatter(formatter)
            app.logger.addHandler(mail_handler)
  
        # send standard logs to syslog
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    cache.init_app(app)
    moment.init_app(app)
    #db.init_app(app)
    login_manager.init_app(app)

    
    #if not app.debug:
    app.config.from_pyfile('config.cfg', silent=True)
    # Configure logging

   # handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler = logging.FileHandler(find_logging_location(app, config_name))
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

  
    return app

def find_logging_location(app, config_name):
    configName = config[config_name]
    if configName == "config.DevelopmentConfig":
        return app.config['LOGGING_LOCATION_DEV']
    elif configName == "config.ProductionConfig":
        return app.config['LOGGING_LOCATION_PRO']
    elif configName == "config.TestingConfig":
        return app.config['LOGGING_LOCATION_TEST']
    else:
        return app.config['LOGGING_LOCATION_DEV']


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
moment = Moment(app)

db = SQLAlchemy(app)
db.init_app(app)




CLIENT_SECRETS = 'client_secrets.json'

GOOGLE_CLIENT_ID = json.loads(
    open(CLIENT_SECRETS, 'r').read())['web']['client_id']

from app import views, models
