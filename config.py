import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    HONEYPOT_API_KEY = os.getenv("HONEYPOT_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # GUVI Callback
    GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    
    # Agent Configuration
    AGENT_MODEL = "gemini-pro"
    MAX_CONVERSATION_TURNS = 50
    
    # Scam Detection Thresholds
    SCAM_CONFIDENCE_THRESHOLD = 0.6
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.HONEYPOT_API_KEY:
            raise ValueError("HONEYPOT_API_KEY is required")
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")

config = Config()
