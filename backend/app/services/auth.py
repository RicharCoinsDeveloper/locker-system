# backend/app/services/auth.py

from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.config import settings
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.services.db import get_db  # ajustado para sesión síncrona

# Configurar PassLib para bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain, hashed)


def get_permissions_by_role(role_id: str, db: Session) -> set[str]:
    """
    Retorna un set de nombres de permisos asociados a un id de rol.
    """
    stmt = (
        select(Permission.name)
        .join(RolePermission, Permission.id == RolePermission.permission_id)
        .where(RolePermission.role_id == role_id)
    )
    result = db.execute(stmt)
    return set(r[0] for r in result.all())


def require_permission(permission: str):
    """Decorator para requerir un permiso específico"""
    def decorator(fn):
        async def wrapper(
            Authorize: AuthJWT = Depends(),
            db: Session = Depends(get_db),
        ):
            Authorize.jwt_required()
            claims = Authorize.get_raw_jwt() or {}
            role_id = claims.get("role")
            if not role_id:
                raise HTTPException(status_code=403, detail="Role missing in token")
            perms = get_permissions_by_role(role_id, db)
            if permission not in perms:
                raise HTTPException(status_code=403, detail="Not authorized")
            return await fn(Authorize=Authorize, db=db)
        return wrapper
    return decorator


from pydantic import BaseModel

class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET
    authjwt_algorithm: str = settings.JWT_ALGORITHM
    authjwt_access_token_expires: int = settings.ACCESS_TOKEN_EXPIRES

@AuthJWT.load_config
def get_config():
    return JWTSettings()
