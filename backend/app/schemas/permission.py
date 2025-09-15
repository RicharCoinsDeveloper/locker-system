from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .role import RoleRead

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class PermissionRead(PermissionBase):
    id: str
    
    class Config:
        from_attributes = True

# Para manejo de roles que tienen este permiso - usando Forward Reference
class PermissionWithRoles(PermissionRead):
    roles: List["RoleRead"] = []
