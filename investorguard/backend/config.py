# Config file
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///investorguard.db'
    # API keys (set in env for real use)
    X_API_KEY = os.environ.get('X_API_KEY') or 'mock_key'
    