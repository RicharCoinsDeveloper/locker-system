from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .permission import PermissionRead

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class RoleRead(RoleBase):
    id: str
    
    class Config:
        from_attributes = True

# Para manejo de permisos en roles - usando Forward Reference
class RoleWithPermissions(RoleRead):
    permissions: List["PermissionRead"] = []
