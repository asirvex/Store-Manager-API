
import os
"""Set up environment configurations"""

class Config():
    """Parent configuration class"""
    secret_key = os.getenv("SECRET_KEY")
    DEBUG = False

class Development(Config):
    """Configuration for development environment"""
    DEBUG = True

class Testing(Config):
    """Configuration for testing environment"""
    DEBUG = True

class Production(Config):
    """Configuration for production environment"""
    DEBUG = False

app_config = {
    "development": Development,
    "testing": Testing,
    "production": Production
}
