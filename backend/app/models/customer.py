# backend/app/models/customer.py
from sqlalchemy import Column, String, DateTime
from . import Base

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime)
