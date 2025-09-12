# backend/app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Base de datos
    MYSQL_URL: str = "mysql+pymysql://user:pass@127.0.0.1:3308/locker_db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 3600  # 1 hora en segundos
    
    # API
    API_VERSION: str = "v1"
    
    # Configuración del archivo .env
    class Config:
        env_file = ".env"  # Ruta CORREGIDA
        env_file_encoding = 'utf-8'

# Instancia global de configuración
settings = Settings()