import os

# Determine the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Base configuration class; contains settings that apply to all environments
class Config:
    # Enable protection against Cross-Site Request Forgery (CSRF)
    WTF_CSRF_ENABLED = True
    
    # Define a secret key used for securely signing the session cookie
    SECRET_KEY = 'a-very-secret-key'
    
    # Disable Flask-SQLAlchemy event system, which can lead to overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configure session cookies to be transmitted only via HTTP (not JavaScript) for security
    SESSION_COOKIE_HTTPONLY = True
    
    # Restrict when cookies are sent to mitigate CSRF attacks
    SESSION_COOKIE_SAMESITE = 'Lax'

# Development environment configuration
class DevelopmentConfig(Config):
    # Enable debug mode for development to aid in debugging
    DEBUG = True
    
    # Define the SQLite database URI for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Testing environment configuration
class TestingConfig(Config):
    # Enable testing mode, which can change the behavior of some functions
    TESTING = True

    # Use an in-memory SQLite database for testing for faster tests without side effects
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Production environment configuration
class ProductionConfig(Config):
    # Define the SQLite database URI for production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Add additional production-specific configuration settings here
    # For example: logging levels, database connection pooling, etc.

# Dictionary mapping environment names to their respective configuration classes
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Set the default config to development for convenience
}
