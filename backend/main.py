# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, customers, roles, permissions
from app.services.db import engine
from app.models import Base

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
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(roles.router, prefix="/api/v1")
app.include_router(permissions.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Crear tablas si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "CoinsSmartGuard API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}