# app/auth/auth_bearer.py

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from app.auth.auth_handler import decode_access_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication scheme."
                )

            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Invalid or expired token."
                )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Authorization token missing."
            )

    async def verify_jwt(self, token: str) -> bool:
        try:
            await decode_access_token(token)
            return True
        except:
            return False

# ✅ Use this in your routes with: dependencies=[Depends(jwt_bearer)]
jwt_bearer = JWTBearer()
