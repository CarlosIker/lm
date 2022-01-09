# /src/config.py

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    MAIL_SERVER     ='mail.kaibosmedia.com'
    MAIL_PORT       = 465
    MAIL_USERNAME   = os.getenv('SMTP_USERNAME')
    MAIL_PASSWORD   = os.getenv('SMTP_PASSWORD')
    MAIL_USE_TLS    = False
    MAIL_USE_SSL    = True

    WEBSITE_URL     = 'http://192.168.45.11/'

    RABBITMQ_USERNAME   = os.getenv('RABBITMQ_USERNAME')
    RABBITMQ_PASSWORD   = os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_HOST       = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT       = os.getenv('RABBITMQ_PORT')


class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class Testing(object):
    """
    Development environment configuration
    """
    TESTING = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=False

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
