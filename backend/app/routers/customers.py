from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.customer import ClientCreate, ClientRead
from app.models.customer import Customer
from app.services.db import get_db
from app.services.auth import require_permission

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post(
    "/",
    response_model=ClientRead,
    dependencies=[Depends(require_permission("clients:write"))]
)
def create_customer(
    data: ClientCreate,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(Customer.email == data.email).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    customer = Customer(
        id=data.email,
        name=data.nombre,
        email=data.email,
        phone=data.telefono
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get(
    "/{customer_id}",
    response_model=ClientRead,
    dependencies=[Depends(require_permission("clients:read"))]
)
def read_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
