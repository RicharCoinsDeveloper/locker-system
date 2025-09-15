from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class CustomerRead(CustomerBase):
    id: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
