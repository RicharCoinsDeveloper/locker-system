from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from app.schemas.auth import UserLogin, UserRegister, Token
from app.models.user import User
from app.services.auth import verify_password, hash_password
from app.services.db import get_db
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(
    data: UserRegister,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    # Verificar si el email ya está registrado
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear nuevo usuario
    new_user = User(
        id=data.email,
        name=data.nombre,
        email=data.email,
        phone=data.telefono,
        role_id=data.role_id,
        password=hash_password(data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generar token
    token = Authorize.create_access_token(
        subject=new_user.email,
        expires_time=settings.ACCESS_TOKEN_EXPIRES,
        user_claims={"role": new_user.role_id}
    )
    
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(
    data: UserLogin,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = Authorize.create_access_token(
        subject=user.email,
        expires_time=settings.ACCESS_TOKEN_EXPIRES,
        user_claims={"role": user.role_id}
    )
    return {"access_token": token}
