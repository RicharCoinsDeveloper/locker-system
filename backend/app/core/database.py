# backend/app/core/database.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from .config import settings

# Crear el engine asíncrono
engine: AsyncEngine = create_async_engine(settings.MYSQL_URL, echo=False)

# Crear el sessionmaker asíncrono
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

# Dependencia para FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
