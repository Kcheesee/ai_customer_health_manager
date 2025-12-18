from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Customer Pulse"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/customer_pulse"
    
    # Security
    FERNET_KEY: str = "your-fernet-key-here-must-be-32-url-safe-base64-bytes" # e.g. from cryptography.fernet import Fernet; Fernet.generate_key()
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
