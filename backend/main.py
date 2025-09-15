# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, customers, roles, permissions
from app.core.database import engine
from app.models import Base
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear UNA SOLA instancia de FastAPI
app = FastAPI(
    title="CoinsSmartGuard",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc", 
    openapi_url="/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(users.router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(customers.router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(roles.router, prefix=f"/api/{settings.API_VERSION}")
app.include_router(permissions.router, prefix=f"/api/{settings.API_VERSION}")

@app.on_event("startup")
async def startup_event():
    """Crear tablas de base de datos al iniciar la aplicación"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")

@app.get("/")
async def root():
    return {"message": "CoinsSmartGuard API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

