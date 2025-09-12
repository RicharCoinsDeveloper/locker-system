from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    telefono: str = Field(..., regex=r"^\+\d{1,3}\d{7,10}$")
    password: str = Field(..., min_length=8)
    role_id: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
