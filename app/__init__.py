import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config

flaskapp = Flask(__name__)
flaskapp.config.from_object(Config)
db = SQLAlchemy(flaskapp)
migrate = Migrate(flaskapp, db)
login = LoginManager(flaskapp)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
mail = Mail(flaskapp)
bootstrap = Bootstrap(flaskapp)
moment = Moment(flaskapp)
babel = Babel(flaskapp)


from app import routes, models, errors

if not flaskapp.debug:
    if flaskapp.config['MAIL_SERVER']:
        auth = None
        if flaskapp.config['MAIL_USERNAME'] or flaskapp.config['MAIL_PASSWORD']:
            auth = (flaskapp.config['MAIL_USERNAME'], flaskapp.config['MAIL_PASSWORD'])
        secure = None
        if flaskapp.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(flaskapp.config['MAIL_SERVER'], flaskapp.config['MAIL_PORT']),
            fromaddr='no-reply@' + flaskapp.config['MAIL_SERVER'],
            toaddrs=flaskapp.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        flaskapp.logger.addHandler(mail_handler)


    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        flaskapp.logger.addHandler(file_handler)

        flaskapp.logger.setLevel(logging.INFO)
        flaskapp.logger.info('Microblog startup')

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(flaskapp.config['LANGUAGES'])


