import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for NOVA API integration."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # NOVA Assistant Configuration
    ASSISTANT_NAME = "NOVA"
    ASSISTANT_ID = "asst_XTd5ExJ9KUTLyrFkzkzPZa2f"
    DEFAULT_MODEL = "gpt-4o-mini"
    DEFAULT_TEMPERATURE = 0.7
    
    # API Settings
    MAX_TOKENS = 4000
    TIMEOUT = 30
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Please set it in your .env file or environment variables.")
        return True
