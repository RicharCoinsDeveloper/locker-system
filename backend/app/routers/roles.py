# app/routers/roles.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.role import Role

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
async def create_role(
    payload: RoleCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    new_role = Role(id=str(uuid4()), **payload.dict())
    session.add(new_role)
    await session.commit()
    await session.refresh(new_role)
    return new_role

@router.get("/", response_model=list[RoleRead])
async def list_roles(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    result = await session.execute(select(Role))
    return result.scalars().all()

@router.get("/{role_id}", response_model=RoleRead)
async def get_role(
    role_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    role = await session.get(Role, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Rol no encontrado")
    return role

@router.put("/{role_id}", response_model=RoleRead)
async def update_role(
    role_id: str,
    payload: RoleUpdate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    role = await session.get(Role, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Rol no encontrado")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(role, field, value)
    await session.commit()
    await session.refresh(role)
    return role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    role = await session.get(Role, role_id)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Rol no encontrado")
    await session.delete(role)
    await session.commit()

