# backend/main.py

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from app.core.config import settings
from alembic import command
from alembic.config import Config
import os

# Ejecutar migraciones automáticamente al arrancar
def run_migrations():
    script_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "alembic"))
    alembic_cfg = Config(os.path.join(script_dir, "alembic.ini"))
    alembic_cfg.set_main_option("script_location", script_dir)
    command.upgrade(alembic_cfg, "head")

# Arrancar migraciones antes de crear la app
run_migrations()

app = FastAPI(
    title="CoinsSmartGuard",
    version=settings.API_VERSION,
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc UI
    openapi_url="/openapi.json",
)

@app.get("/healthz", tags=["Health"], summary="Check API health")
async def health_check():
    """
    Endpoint para verificar que la API está funcionando.
    Devuelve el estado y la versión actual de la API.
    """
    return {"status": "ok", "version": settings.API_VERSION}

@AuthJWT.load_config
def get_jwt_config():
    return settings  # FastAPI-JWT-Auth buscará `JWT_SECRET` y podrá usar `JWT_ALGORITHM`

app = FastAPI(openapi_prefix=f"/api/{settings.API_VERSION}")