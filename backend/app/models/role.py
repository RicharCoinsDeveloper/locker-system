from sqlalchemy import Column, String
from . import Base

class Role(Base):
    __tablename__ = 'roles'
    id = Column(String(36), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
