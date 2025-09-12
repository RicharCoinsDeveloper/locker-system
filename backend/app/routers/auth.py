from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import UserRegister, UserLogin, Token
from app.models.user import User
from app.services.auth import hash_password, verify_password
from app.services.db import get_session
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(
    data: UserRegister,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_session)
):
    # Verificar si el correo ya está registrado
    result = await db.execute(select(User).filter_by(email=data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Crear nuevo usuario
    new_user = User(
        id=data.email,  # Asegúrate de que el campo `id` sea tipo str si usas el email como ID
        name=data.nombre,
        email=data.email,
        phone=data.telefono,
        role_id=data.role_id,
        password=hash_password(data.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # Refresca para asegurar que los datos estén actualizados

    # Generar token
    token = Authorize.create_access_token(
        subject=new_user.email,
        expires_time=settings.ACCESS_TOKEN_EXPIRES,
        user_claims={"role": new_user.role_id}
    )

    return {"access_token": token}

@router.post("/login", response_model=Token)
async def login(
    data: UserLogin,
    Authorize: AuthJWT = Depends(),
    db: AsyncSession = Depends(get_session)
):
    # Buscar usuario por email
    result = await db.execute(select(User).filter_by(email=data.email))
    user = result.scalars().first()

    # Validar existencia y contraseña
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Generar token
    token = Authorize.create_access_token(
        subject=user.email,
        expires_time=settings.ACCESS_TOKEN_EXPIRES,
        user_claims={"role": user.role_id}
    )

    return {"access_token": token}