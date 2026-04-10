# app/auth/auth_handler.py

from datetime import datetime, timedelta
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.settings import settings

# 🔐 JWT config
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# ✅ USE ARGON2 (NO PASSWORD LENGTH LIMIT)
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

# ---------------------- Password Hashing ----------------------

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------- JWT Token Handling ----------------------

async def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )