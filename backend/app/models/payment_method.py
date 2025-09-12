from sqlalchemy import Column, String
from . import Base

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'
    id = Column(String(36), primary_key=True)
    description = Column(String(100))
