# backend/app/schemas/auth.py
from pydantic import BaseModel, EmailStr

# Esquemas JWT existentes
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None

# Nuevos esquemas para registro y login
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    password: str
    role_id: str  # ¡Importante: asegurar que se asigne un rol!

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Alias para compatibilidad
TokenResponse = Token
