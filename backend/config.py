import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AI Configuration
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'groq')
    
    # Flask Configuration
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')