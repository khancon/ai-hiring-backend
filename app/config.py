import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file at the project root
load_dotenv()
logger = logging.getLogger(__name__)

class Config:
    # print(f"OpenAI API Key: {os.getenv('OPENAI_API_KEY')}")  # Debugging line to check if the key is loaded
    # Environment variables for configuration
    logger.info(f"Is OPENAI_API_KEY set? {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    logger.info(f"OPENAI_API_KEY Length: {len(os.getenv('OPENAI_API_KEY', ''))} characters")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # You can add more config variables here as needed
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    # Example: Add a default model name if you want
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    
    if not USERNAME or not PASSWORD:
        logger.warning("USERNAME or PASSWORD environment variables are not set. Basic auth will not be enabled.")
