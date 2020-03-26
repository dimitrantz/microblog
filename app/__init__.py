import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    flaskapp = Flask(__name__)
    flaskapp.config.from_object(config_class)

    db.init_app(flaskapp)
    migrate.init_app(flaskapp, db)
    login.init_app(flaskapp)
    mail.init_app(flaskapp)
    bootstrap.init_app(flaskapp)
    moment.init_app(flaskapp)
    babel.init_app(flaskapp)
    #flaskapp.elasticsearch = Elasticsearch([flaskapp.config['ELASTICSEARCH_URL']]) \
     #   if flaskapp.config['ELASTICSEARCH_URL'] else None
    flaskapp.elasticsearch = Elasticsearch([flaskapp.config['ELASTICSEARCH_URL']]) \
        if flaskapp.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    flaskapp.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    flaskapp.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    flaskapp.register_blueprint(main_bp)

    if not flaskapp.debug and not flaskapp.testing:
        if flaskapp.config['MAIL_SERVER']:
            auth = None
            if flaskapp.config['MAIL_USERNAME'] or flaskapp.config['MAIL_PASSWORD']:
                auth = (flaskapp.config['MAIL_USERNAME'],
                        flaskapp.config['MAIL_PASSWORD'])
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
     
        if flaskapp.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            flaskapp.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                            maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            flaskapp.logger.addHandler(file_handler)

        flaskapp.logger.setLevel(logging.INFO)
        flaskapp.logger.info('Microblog startup')




    return flaskapp


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


from app import models