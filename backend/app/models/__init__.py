# backend/app/models/__init__.py

from sqlalchemy.orm import declarative_base

# UNA SOLA declaración de Base para todo el proyecto
Base = declarative_base()

# Importar todos los modelos para que estén registrados
from .user import User
from .role import Role
from .permission import Permission
from .role_permission import RolePermission
from .user_role import UserRole
from .customer import Customer
from .locker import Locker
from .cell import Cell
from .reservation import Reservation
from .qrcode import QRCode
from .customer_access import CustomerAccess
from .user_access import UserAccess
from .payment_method import PaymentMethod
from .rate import Rate
from .payment import Payment
from .invoice import Invoice