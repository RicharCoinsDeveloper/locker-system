from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from .role import RoleRead

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role_id: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role_id: Optional[str] = None
    password: Optional[str] = None

class UserRead(UserBase):
    id: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        orm_mode = True

# Usuario con información de rol completa
class UserWithRole(UserRead):
    role: Optional["RoleRead"] = None
