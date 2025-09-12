# backend/alembic/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Agregar la carpeta 'backend' y 'backend/app' al path para importar modelos
here = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(here, '..')))
sys.path.insert(0, os.path.abspath(os.path.join(here, '..', 'app')))

# Importar Base y modelos directamente desde app.models
from app.models import Base  # Base metadata
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

# Configuración de Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de todos los modelos para autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecuta migraciones en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
