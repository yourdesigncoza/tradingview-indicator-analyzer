from decouple import config
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str = config('OPENAI_API_KEY')
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = config('REQUESTS_PER_MINUTE', default=20, cast=int)
    
    # Environment
    ENVIRONMENT: str = config('ENVIRONMENT', default='development')
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    LOGS_DIR: str = os.path.join(BASE_DIR, 'logs')
    DATA_DIR: str = os.path.join(BASE_DIR, 'data')
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()