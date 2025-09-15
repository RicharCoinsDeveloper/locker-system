from .customer import CustomerCreate, CustomerRead, CustomerUpdate
from .user import UserCreate, UserRead, UserUpdate, UserWithRole
from .role import RoleCreate, RoleRead, RoleUpdate, RoleWithPermissions
from .permission import PermissionCreate, PermissionRead, PermissionUpdate, PermissionWithRoles
from .role_permission import (
    RolePermissionAssign, 
    RolePermissionRemove, 
    RolePermissionResponse
)
from .user_role import (
    UserRoleAssign,
    UserRoleRemove, 
    UserRoleResponse
)
# Importar todos los esquemas de autenticación
from .auth import (
    Token, 
    TokenData, 
    RegisterRequest, 
    LoginRequest, 
    TokenResponse
)

# Actualizar forward references después de importar todos los esquemas
RoleWithPermissions.update_forward_refs()
PermissionWithRoles.update_forward_refs()
UserWithRole.update_forward_refs()

__all__ = [
    # Auth schemas
    "Token",
    "TokenData",
    "RegisterRequest", 
    "LoginRequest",
    "TokenResponse",
    
    # Customer schemas
    "CustomerCreate", 
    "CustomerRead", 
    "CustomerUpdate",
    
    # User schemas
    "UserCreate",
    "UserRead", 
    "UserUpdate",
    "UserWithRole",
    
    # Role schemas
    "RoleCreate",
    "RoleRead",
    "RoleUpdate",
    "RoleWithPermissions",
    
    # Permission schemas
    "PermissionCreate",
    "PermissionRead",
    "PermissionUpdate",
    "PermissionWithRoles",
    
    # Role-Permission relationship schemas
    "RolePermissionAssign",
    "RolePermissionRemove",
    "RolePermissionResponse",
    
    # User-Role relationship schemas
    "UserRoleAssign",
    "UserRoleRemove",
    "UserRoleResponse"
]
