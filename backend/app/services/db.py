from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configuración de la conexión a la base de datos
SQLALCHEMY_DATABASE_URL = settings.MYSQL_URL

# Crear engine de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

# Configurar SessionLocal para dependencias de FastAPI
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

def get_db():
    """
    Dependency de FastAPI que proporciona una sesión de DB y se encarga de cerrarla.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
