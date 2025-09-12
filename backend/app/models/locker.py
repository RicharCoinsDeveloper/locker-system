from sqlalchemy import Column, String, DateTime
from . import Base

class Locker(Base):
    __tablename__ = 'lockers'
    id = Column(String(36), primary_key=True)
    location = Column(String(100))
    status = Column(String(20))
    description = Column(String(255))
    installed_at = Column(DateTime)
