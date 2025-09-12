import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schemas.auth_schemas import RegisterRequest, LoginRequest, TokenResponse
from ..core.security import hash_password, verify_password, create_access_token
from ..core.database import get_session
from ..models.user import User  # Asegúrate de que User está definido correctamente en models/user.py

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter_by(email=req.email))
    if result.scalars().first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Email ya registrado")
    user = User(
        id=str(uuid.uuid4()),
        name=req.name,
        email=req.email,
        phone=req.phone,
        password=hash_password(req.password)
    )
    session.add(user)
    await session.commit()
    token = create_access_token(str(user.id))  # Corrección aquí
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter_by(email=req.email))
    user = result.scalars().first()
    if not user or not verify_password(req.password, str(user.password)):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token(str(user.id))  # Corrección aquí
    return TokenResponse(access_token=token)