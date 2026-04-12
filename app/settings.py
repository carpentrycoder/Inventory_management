# app/settings.py

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # JWT Configuration
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database Configuration
    DB_TYPE: str = "sqlite"
    DB_NAME: str = "inventory.db"

    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    API_BASE_URL: str = "http://127.0.0.1:8000"

    # Frontend Configuration
    FRONTEND_PORT: int = 8000
    FRONTEND_BASE_URL: str = "http://127.0.0.1:8000"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()