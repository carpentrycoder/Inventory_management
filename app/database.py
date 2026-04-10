# app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings

# ✅ ALWAYS use settings
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
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