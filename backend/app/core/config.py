# backend/app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MYSQL_URL: str = "mysql+pymysql://user:pass@127.0.0.1:3308/locker_db"
    class Config:
        env_file = ".env"
        validate_assignment = True

settings = Settings()
