from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from urllib.parse import quote_plus

class Settings(BaseSettings):
    # App
    APP_NAME: str = "NetOne AI Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "Lisa2021!"
    MYSQL_DATABASE: str = "netone_chat_db"
    
    # This field is needed to accept DATABASE_URL from .env
    DATABASE_URL: Optional[str] = None
    
    @property
    def database_url(self) -> str:
        """Construct database URL from components if not provided"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # URL-encode the password to handle special characters
        password_encoded = quote_plus(self.MYSQL_PASSWORD)
        return f"mysql+pymysql://{self.MYSQL_USER}:{password_encoded}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    USE_LOCAL_LLM: bool = False
    
    # Vector DB
    VECTOR_DB_PATH: str = "./data/embeddings/chroma_db"
    COLLECTION_NAME: str = "netone_docs"
    
    # Security
    JWT_SECRET: str = "your-super-secret-jwt-key-change-this"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # This ignores extra fields from .env

settings = Settings()