# backend/alembic/import_models.py

"""
Este archivo importa todos los modelos de SQLAlchemy para asegurar que
Alembic los detecte correctamente al generar migraciones.
"""
from app.models.customer import Customer
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user_role import UserRole
from app.models.locker import Locker
from app.models.cell import Cell
from app.models.reservation import Reservation
from app.models.qrcode import QRCode
from app.models.customer_access import CustomerAccess
from app.models.user_access import UserAccess
from app.models.payment_method import PaymentMethod
from app.models.rate import Rate
from app.models.payment import Payment
from app.models.invoice import Invoice

# Declarative Base
from app.models import Base
