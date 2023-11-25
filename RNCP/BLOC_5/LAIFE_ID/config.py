class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "_5\$&L[2D>b]J;f/b?]*"
    DATABASE_URI = "database_uri"

class ProductionConfig(Config):
    DATABASE_URI = "database_uri"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True