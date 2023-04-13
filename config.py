
class Config:
    TESTING = False
    DEBUG = False
    FLASK_ENV = 'development'
    SECRET_KEY = "my-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

class ProdConfig(Config):
    TESTING = False
    DEBUG = False

class StagConfig(Config):
    DEBUG = True

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True


