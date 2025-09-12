# backend/app/services/auth.py

from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.services.db import get_session
from pydantic import BaseModel

# Configurar PassLib para bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain, hashed)

async def get_permissions_by_role(role_id: str, db: AsyncSession):
    """
    Retorna una lista de nombres de permisos asociados a un id de rol, usando relaciones ORM.
    """
    stmt = (
        select(Permission.name)
        .join(RolePermission, Permission.id == RolePermission.permission_id)
        .where(RolePermission.role_id == role_id)
    )
    result = await db.execute(stmt)
    perms = result.scalars().all()
    return set(perms)

def require_permission(permission: str):
    """Decorator para requerir un permiso específico"""
    async def wrapper(
        Authorize: AuthJWT = Depends(),
        db: AsyncSession = Depends(get_session)
    ):
        Authorize.jwt_required()
        claims = Authorize.get_raw_jwt() or {}
        role_id = claims.get("role", None)
        if not role_id:
            raise HTTPException(status_code=403, detail="Role not found in token")
        
        # Verificar permisos del rol desde la base de datos dinámicamente
        perms = await get_permissions_by_role(role_id, db)
        if permission not in perms:
            raise HTTPException(status_code=403, detail="Not authorized")
    return wrapper

# Configuración JWT usando Pydantic
class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_access_token_expires: int = settings.ACCESS_TOKEN_EXPIRES

@AuthJWT.load_config
def get_jwt_config():
    return JWTSettings()