from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os


db = SQLAlchemy()
login_m = LoginManager()
login_m.login_view = 'login' 
login_m.login_message_category = 'info' 

def create_app():
    app = Flask(__name__,instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    db.init_app(app)
    login_m.init_app(app)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler  = RotatingFileHandler('logs/Myflaskblog.log',maxBytes=10240,backupCount=10)
        file_handler.setFormatter(logging.formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Myflaskblog startup')

    with app.app_context():

        from .main import main
        from .dashboard import dashboard
        from .gallery import gallery


        app.register_blueprint(dashboard,url_prefix='/dashboard')
        app.register_blueprint(main)
        app.register_blueprint(gallery,url_prefix='/dashboard')

        return app




