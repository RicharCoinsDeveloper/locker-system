from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserLogin, Token
from app.models.user import User
from app.services.auth import verify_password
from app.services.db import get_session
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).filter_by(email=data.email))
    user: User = result.scalars().first()
    if not user or not verify_password(data.password, user.password if isinstance(user.password, str) else user.password.value):
        raise HTTPException(401, "Invalid credentials")
    # Usar el atributo de la instancia
    token = Authorize.create_access_token(
        subject=user.email if isinstance(user.email, str) else user.email.value,  # Ensure subject is a str
        expires_time=settings.ACCESS_TOKEN_EXPIRES,
        user_claims={"role": user.role_id}
    )
    return {"access_token": token}
