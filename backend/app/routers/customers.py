from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.customer import ClientCreate, ClientRead
from app.models.customer import Customer
from app.services.db import get_session
from app.services.auth import require_permission

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post(
    "/",
    response_model=ClientRead,
    dependencies=[Depends(require_permission("clients:write"))]
)
async def create_customer(
    data: ClientCreate,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(Customer).filter_by(email=data.email))
    if result.scalars().first():
        raise HTTPException(400, "Email already registered")
    customer = Customer(
        id=data.email,
        name=data.nombre,
        email=data.email,
        phone=data.telefono
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

@router.get(
    "/{customer_id}",
    response_model=ClientRead,
    dependencies=[Depends(require_permission("clients:read"))]
)
async def read_customer(
    customer_id: str,
    db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(Customer).filter_by(id=customer_id))
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(404, "Customer not found")
    return customer
