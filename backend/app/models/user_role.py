from sqlalchemy import Column, String, ForeignKey
from . import Base

class UserRole(Base):
    __tablename__ = 'user_roles'
    user_id = Column(String(36), ForeignKey('users.id'), primary_key=True)
    role_id = Column(String(36), ForeignKey('roles.id'), primary_key=True)
