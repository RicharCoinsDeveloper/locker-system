from sqlalchemy import Column, String, DateTime, ForeignKey
from . import Base

class UserAccess(Base):
    __tablename__ = 'user_accesses'
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'))
    locker_id = Column(String(36), ForeignKey('lockers.id'))
    cell_id = Column(String(36), ForeignKey('cells.id'))
    accessed_at = Column(DateTime)
    access_type = Column(String(20))
