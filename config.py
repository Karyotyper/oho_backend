class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://ohodb:oho123@localhost:5432/ohodb'
    SECRET_KEY = 'otp'

    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = "pioneer21st@gmail.com"
    MAIL_PASSWORD = 'jkrmdjyqspxtbigb'

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    ##SQLALCHEMY_DATABASE_URI = ##


app_config = {
    'development': Development,
    'production': Production,
}