from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app import models, schemas
from app.auth.auth_bearer import jwt_bearer
from app.auth.auth_handler import decode_access_token

router = APIRouter(prefix="/users", tags=["Users"])

async def get_current_user_role(token: str = Depends(jwt_bearer)) -> str:
    payload = await decode_access_token(token)
    return payload.get("role")

@router.get("/", response_model=list[schemas.User])
async def list_users(
    db: AsyncSession = Depends(get_db),
    role: str = Depends(get_current_user_role)
):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users
