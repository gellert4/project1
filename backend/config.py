"""
Configuration management
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = os.getenv('DEBUG', False)
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    VECTOR_DB_PATH = 'data/vectordb'
    UPLOAD_FOLDER = 'data/uploads'
