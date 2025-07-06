"""
Configuration settings for the application.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Model Configuration
    MODEL_NAME = "gemini-pro"
    TEMPERATURE = 0.7
    
    # Memory Configuration
    MAX_HISTORY_LENGTH = 50
    
    # Storage Configuration
    DATA_DIR = "data"
    MEMORY_FILE = "memory.json"
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        return True