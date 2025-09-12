#from pydantic import BaseSettings  # type: ignore
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_URL: str
    REDIS_URL: str
    RABBITMQ_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES: int = 3600  # en segundos
    API_VERSION: str = "0.1.0"

    class Config:
        env_file = "../../.env"

settings = Settings()
