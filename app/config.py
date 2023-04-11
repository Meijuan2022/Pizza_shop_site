import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Top secret key of website
    SECRET_KEY = 'DET-ÄR-EN-LÅNG-NYCKEL'

    # SET RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'EN-RECAPTCHA-NYCKEL'
    ECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'EN-RECAPTCHA-NYCKEL'
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
