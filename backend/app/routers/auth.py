from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.schemas.auth import UserLogin, Token
from app.models.user import User
from app.services.auth import verify_password
from app.services.db import get_db
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(
    data: UserLogin,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password if isinstance(user.password, str) else getattr(user, "password")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = Authorize.create_access_token(
        subject=user.email if isinstance(user.email, str) else getattr(user, "email"),
        expires_time=settings.ACCESS_TOKEN_EXPIRES,
        user_claims={"role": user.role_id}
    )
    return {"access_token": token}
