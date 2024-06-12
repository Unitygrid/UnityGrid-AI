import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    WEB3_PROVIDER_URI = os.environ.get('WEB3_PROVIDER_URI') or 'http://127.0.0.1:7545'
    CONTRACT_ADDRESS = os.environ.get('CONTRACT_ADDRESS')
    CONTRACT_ABI = os.environ.get('CONTRACT_ABI')

config = Config()

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

config = Config()
test_config = TestConfig()
