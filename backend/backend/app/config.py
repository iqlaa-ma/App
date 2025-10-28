from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    MONGODB_URL: str = "mongodb://localhost:27017" #mongodb
    DATABASE_NAME: str = "auth_db" #mongodb
    # DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "Mobile Auth API"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cache settings to avoid reading .env multiple times"""
    return Settings()


settings = get_settings()