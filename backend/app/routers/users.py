from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.db import get_session
from app.services.auth import hash_password, require_permission

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=UserRead,
    dependencies=[Depends(require_permission("users:write"))]
)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).filter_by(email=data.email))
    if result.scalars().first():
        raise HTTPException(400, "Email already registered")
    user = User(
        id=data.email,
        name=data.nombre,
        email=data.email,
        phone=data.telefono,
        role_id=data.role_id,
        password=hash_password(data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_permission("users:read"))]
)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(404, "User not found")
    return user
