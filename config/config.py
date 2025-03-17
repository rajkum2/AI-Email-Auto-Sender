from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Keys
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    HUBSPOT_API_KEY: str = os.getenv("HUBSPOT_API_KEY", "")
    PIPEDRIVE_API_KEY: str = os.getenv("PIPEDRIVE_API_KEY", "")
    
    # Model Configuration
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "mistralai/Mistral-7B-v0.1")
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "./model_cache")
    
    # Email Configuration
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "")
    DEFAULT_REPLY_TO: str = os.getenv("DEFAULT_REPLY_TO", "")
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS: str = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "")
    SPREADSHEET_ID: str = os.getenv("SPREADSHEET_ID", "")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 