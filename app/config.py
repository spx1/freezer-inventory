import os
from app import BASE_DIRECTORY

class BaseConfig(object):
    Name = 'Default'
    Debug = False
    Testing = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIRECTORY}/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
    Name = 'Test'

class DevelopmentConfig(BaseConfig):
    Name = 'Development'
    Debug = True
    Testing = True
    TEMPLATES_AUTO_RELOAD = True
    SQL_USER = os.environ.get('SQL_USER','myuser')
    SQL_SERVER = os.environ.get('SQL_SERVER','locahlost')
    SQL_KEY = os.environ.get('SQL_PASSWORD','My not so secret password')
    SQL_DB = os.environ.get('SQL_DB','mydatabase')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqldb://{SQL_USER}:{SQL_KEY}@{SQL_SERVER}/{SQL_DB}'

class ProductionConfig(DevelopmentConfig):
    Name = 'Production'
    Debug = False
    Testing = False
    TEMPLATES_AUTO_RELAOD = False


EXPORT_CONFIGS = [
    DevelopmentConfig,
    ProductionConfig,
    TestConfig
]

config_by_name = {cfg.NAME: cfg for cfg in EXPORT_CONFIGS}
