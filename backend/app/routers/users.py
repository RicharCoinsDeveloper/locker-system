from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.db import get_db
from app.services.auth import hash_password, require_permission

router = APIRouter(prefix="/users", tags=["users"])

@router.post(
    "/",
    response_model=UserRead,
    dependencies=[Depends(require_permission("users:write"))]
)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        id=data.email,
        name=data.nombre,
        email=data.email,
        phone=data.telefono,
        role_id=data.role_id,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_permission("users:read"))]
)
def read_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
