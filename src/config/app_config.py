import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8082))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_API_URL = os.getenv('OPENAI_API_URL', '')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
