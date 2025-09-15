# backend/app/routers/users_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4
from datetime import datetime, timezone

from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.database import get_session
from app.core.security import get_current_user, hash_password
from app.models.user import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    new_user = User(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        **payload.dict(exclude={"password"})
    )
    new_user.hashed_password = hash_password(payload.password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: str,
    payload: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    data = payload.dict(exclude_none=True, exclude={"password"})
    for field, value in data.items():
        setattr(user, field, value)
    if payload.password:
        # If your User model uses a setter or private attribute for password, use it here
        # For example, if you have a set_password method:
        # user.set_password(payload.password)
        # Or if the column is named _password:
        # user._password = hash_password(payload.password)
        # Otherwise, assign directly if user.password is a Column[str]:
        user.hashed_password = hash_password(payload.password)
    await session.commit()
    await session.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Usuario no encontrado")
    await session.delete(user)
    await session.commit()
