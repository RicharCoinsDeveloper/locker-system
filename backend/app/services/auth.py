# backend/app/services/auth.py

from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from app.core.config import settings

# Configurar PassLib para bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# Permisos por rol
ROLE_PERMISSIONS = {
    "admin": ["customers:write", "customers:read", "users:write", "users:read"],
    "operator": ["customers:read", "users:read"]
}

def require_permission(permission: str):
    def wrapper(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        claims = Authorize.get_raw_jwt() or {}
        role = claims.get("role", "")
        if permission not in ROLE_PERMISSIONS.get(role, []):
            raise HTTPException(status_code=403, detail="Not authorized")
    return wrapper

# Cargar configuración de fastapi_jwt_auth
@AuthJWT.load_config
def get_jwt_config():
    class JWTSettings:
        authjwt_secret_key: str = settings.JWT_SECRET
        authjwt_algorithm: str = settings.JWT_ALGORITHM
        authjwt_access_token_expires: int = settings.ACCESS_TOKEN_EXPIRES
    return JWTSettings()
