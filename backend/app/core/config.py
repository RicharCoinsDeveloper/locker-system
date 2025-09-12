# backend/app/core/config.py

from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    SECRET_KEY: str = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600  # 60 minutos * 60 segundos
    MYSQL_URL: str = "mysql+pymysql://user:pass@127.0.0.1:3308/locker_db"

class Config:
        env_file = ".env"
        validate_assignment = True
        env_file_encoding = "utf-8"

settings = Settings()

