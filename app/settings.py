# app/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DB_TYPE: str = "sqlite"
    DB_NAME: str = "inventory.db"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DB_NAME}"

    class Config:
        extra = "ignore"

settings = Settings()