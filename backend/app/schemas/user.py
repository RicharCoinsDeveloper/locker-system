from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    telefono: str = Field(..., min_length=8)
    role_id: str = Field(..., min_length=1)
    

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserRead(UserBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
