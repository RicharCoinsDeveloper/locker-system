from sqlalchemy import Column, String, Numeric
from . import Base

class Rate(Base):
    __tablename__ = 'rates'
    id = Column(String(36), primary_key=True)
    description = Column(String(100))
    price = Column(Numeric(10,2))
    period = Column(String(50))
    status = Column(String(20))
