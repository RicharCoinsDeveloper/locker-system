# app/routers/permissions.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.permission import Permission

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.post("/", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
async def create_permission(
    payload: PermissionCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    new_perm = Permission(id=str(uuid4()), **payload.dict())
    session.add(new_perm)
    await session.commit()
    await session.refresh(new_perm)
    return new_perm

@router.get("/", response_model=list[PermissionRead])
async def list_permissions(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    result = await session.execute(select(Permission))
    return result.scalars().all()

@router.get("/{perm_id}", response_model=PermissionRead)
async def get_permission(
    perm_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    perm = await session.get(Permission, perm_id)
    if not perm:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Permiso no encontrado")
    return perm

@router.put("/{perm_id}", response_model=PermissionRead)
async def update_permission(
    perm_id: str,
    payload: PermissionUpdate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    perm = await session.get(Permission, perm_id)
    if not perm:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Permiso no encontrado")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(perm, field, value)
    await session.commit()
    await session.refresh(perm)
    return perm

@router.delete("/{perm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    perm_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    perm = await session.get(Permission, perm_id)
    if not perm:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Permiso no encontrado")
    await session.delete(perm)
    await session.commit()
