# backend/app/routers/clients_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
from app.core.database import get_session
from app.core.security import get_current_user
from app.models.customer import Customer

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_client(
    payload: CustomerCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    new_client = Customer(id=str(uuid4()), **payload.dict())
    session.add(new_client)
    await session.commit()
    await session.refresh(new_client)
    return new_client

@router.get("/", response_model=list[CustomerRead])
async def list_clients(
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    result = await session.execute(select(Customer))
    return result.scalars().all()

@router.get("/{client_id}", response_model=CustomerRead)
async def get_client(
    client_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    client = await session.get(Customer, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    return client

@router.put("/{client_id}", response_model=CustomerRead)
async def update_client(
    client_id: str,
    payload: CustomerUpdate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    client = await session.get(Customer, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    for field, value in payload.dict(exclude_none=True).items():
        setattr(client, field, value)
    await session.commit()
    await session.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: str,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    client = await session.get(Customer, client_id)
    if not client:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    await session.delete(client)
    await session.commit()
