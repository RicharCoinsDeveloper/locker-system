from sqlalchemy import Column, String
from . import Base

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
