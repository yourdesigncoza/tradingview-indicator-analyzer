import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

# Ensure required directories exist
def ensure_directories_exist():
    """Create necessary directories if they don't exist"""
    directories = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

# Create directories
ensure_directories_exist()

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str = 'sk-dummy-key-for-testing'

    # Rate Limiting
    REQUESTS_PER_MINUTE: int = 20

    # Environment
    ENVIRONMENT: str = 'development'

    # TradingView (optional)
    TRADINGVIEW_USERNAME: str = ''
    TRADINGVIEW_PASSWORD: str = ''

    # Database (optional)
    DB_NAME: str = ''
    DB_USER: str = ''
    DB_PASSWORD: str = ''
    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'

    # Paths (not from env)
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    LOGS_DIR: str = os.path.join(BASE_DIR, 'logs')
    DATA_DIR: str = os.path.join(BASE_DIR, 'data')

    @property
    def is_openai_key_valid(self) -> bool:
        """Check if the OpenAI API key is valid (not the dummy key)"""
        return self.OPENAI_API_KEY != 'sk-dummy-key-for-testing'

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'  # Ignore extra fields in .env

settings = Settings()