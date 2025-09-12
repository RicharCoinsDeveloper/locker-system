# backend/app/models/user.py
from sqlalchemy import Column, String, DateTime, ForeignKey
from . import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    role_id = Column(String(36), ForeignKey('roles.id'))
    created_at = Column(DateTime)
