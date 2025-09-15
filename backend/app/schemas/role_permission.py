from typing import List
from pydantic import BaseModel

# Para asignar permisos a roles
class RolePermissionAssign(BaseModel):
    role_id: str
    permission_ids: List[str]

class RolePermissionRemove(BaseModel):
    role_id: str
    permission_ids: List[str]

# Para respuestas de asignación
class RolePermissionResponse(BaseModel):
    role_id: str
    permission_id: str
    
    class Config:
        from_attributes = True
