
import os
"""Set up environment configurations"""


class Config():
    """Parent configuration class"""
    secret_key = os.getenv("SECRET_KEY")
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")


class Development(Config):
    """Configuration for development environment"""
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_URL")


class Testing(Config):
    """Configuration for testing environment"""
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_TESTING_URL")

    
class Production(Config):
    """Configuration for production environment"""
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")


app_config = {
    "development": Development,
    "testing": Testing,
    "production": Production
}
