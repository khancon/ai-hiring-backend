import os
from dotenv import load_dotenv

# Load environment variables from .env file at the project root
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # You can add more config variables here as needed
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    # Example: Add a default model name if you want
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
