# app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings

# ✅ ALWAYS use settings
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to False for production
    pool_size=10,  # Number of connections to keep in pool
    max_overflow=20,  # Max additional connections
    pool_timeout=30,  # Timeout for getting connection from pool
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Check connection before use
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session