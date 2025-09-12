# backend/app/services/db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import Base  # Importar Base desde models/__init__.py

# Crear motor de base de datos asíncrono
engine = create_async_engine(
    settings.MYSQL_URL.replace("mysql+pymysql://", "mysql+aiomysql://"),
    echo=True,
    future=True
)

# Configurar sesión asíncrona
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Dependencia para obtener sesión de base de datos
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()