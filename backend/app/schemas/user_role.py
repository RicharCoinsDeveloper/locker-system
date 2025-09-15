from typing import List
from pydantic import BaseModel

# Para asignar roles a usuarios
class UserRoleAssign(BaseModel):
    user_id: str
    role_ids: List[str]

class UserRoleRemove(BaseModel):
    user_id: str
    role_ids: List[str]

# Para respuestas de asignación
class UserRoleResponse(BaseModel):
    user_id: str
    role_id: str
    
    class Config:
        from_attributes = True
