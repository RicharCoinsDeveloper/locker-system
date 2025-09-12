# ------------------------------------------------------------
# PowerShell Script: Generar Fase 3 – API REST y Autenticación
# ------------------------------------------------------------
# Asume que estás en: C:\Users\Desarrollo\Desktop\CoinsSmartGuard\AppCSG\serverCoinsSmartGuard\locker-system
$root = Get-Location

# Definir rutas base
$coreDir    = Join-Path $root "backend\app\core"
$schemasDir = Join-Path $root "backend\app\schemas"
$apiDir     = Join-Path $root "backend\app\api"

# Crear carpetas si no existen
@($coreDir, $schemasDir, $apiDir) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# Archivos a generar y su contenido
$files = @{
    # Core
    "$coreDir\config.py" = @'
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        validate_assignment = True
        model_config = {"str_strip_whitespace": True}

settings = Settings()
'@

    "$coreDir\security.py" = @'
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from .config import settings

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return _pwd_ctx.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_ctx.verify(plain, hashed)

def create_access_token(sub: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
'@

    # Schemas
    "$schemasDir\auth_schemas.py" = @'
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
'@

    # API Router
    "$apiDir\auth_router.py" = @'
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schemas.auth_schemas import RegisterRequest, LoginRequest, TokenResponse
from ..core.security import hash_password, verify_password, create_access_token
from ..models.user import User
from ..core.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest, session: AsyncSession = Depends(get_session)):
    exists = await session.execute(select(User).filter_by(email=req.email))
    if exists.scalars().first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email ya registrado")
    user = User(
        id=str(uuid.uuid4()),
        name=req.name,
        email=req.email,
        phone=req.phone,
        password=hash_password(req.password)
    )
    session.add(user)
    await session.commit()
    token = create_access_token(user.id)
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(User).filter_by(email=req.email))
    user = res.scalars().first()
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    return TokenResponse(access_token=create_access_token(user.id))
'@
}

# Generar cada archivo
foreach ($path in $files.Keys) {
    $content = $files[$path]
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    $content | Out-File -FilePath $path -Encoding UTF8
    Write-Host "Creado $path"
}

Write-Host ""
Write-Host "✅ Fase 3 generada exitosamente"
Write-Host "📍 Actualiza backend/app/main.py para incluir 'auth_router'"
