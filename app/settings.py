# app/settings.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # 🔐 JWT Configuration
    # =========================
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # =========================
    # 🗄️ Database Configuration
    # =========================
    DATABASE_URL: str | None = None  # ✅ Primary (Render / Neon)
    POSTGRES_DB: str = ""  # Fallback for local .env

    # Local fallback (ONLY for development)
    DB_TYPE: str = "sqlite"
    DB_NAME: str = "inventory.db"

    # =========================
    # 🌐 API Configuration
    # =========================
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # =========================
    # 🎨 Frontend (Optional)
    # =========================
    FRONTEND_BASE_URL: str = "http://localhost:8000"

    # =========================
    # 🔥 Database URL Builder
    # =========================
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        # ✅ PRODUCTION (Render / Neon / Supabase)
        db_url = self.DATABASE_URL or self.POSTGRES_DB
        if db_url:
            url = db_url

            # Fix postgres scheme for SQLAlchemy
            url = url.replace("postgres://", "postgresql://")

            # 🔥 IMPORTANT FIX for async/sync compatibility
            url = url.replace("postgresql://", "postgresql+asyncpg://")

            # Handle SSL for Neon
            if "sslmode=require" in url:
                url = url.replace("sslmode=require", "ssl=require")
            if "&channel_binding=require" in url:
                url = url.replace("&channel_binding=require", "")

            return url

        # ✅ LOCAL POSTGRES (rare case)
        if self.DB_TYPE == "postgres":
            return f"postgresql+asyncpg://{self.DB_NAME}"

        # ✅ DEFAULT LOCAL SQLITE
        return f"sqlite+aiosqlite:///./{self.DB_NAME}"

    # =========================
    # ⚙️ Pydantic Config
    # =========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Singleton instance
settings = Settings()