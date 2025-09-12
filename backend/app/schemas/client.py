from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ClientBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    telefono: str = Field(..., regex=r"^\+\d{1,3}\d{7,10}$")

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
