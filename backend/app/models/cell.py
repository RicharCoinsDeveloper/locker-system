from sqlalchemy import Column, String, Integer, ForeignKey
from . import Base

class Cell(Base):
    __tablename__ = 'cells'
    id = Column(String(36), primary_key=True)
    locker_id = Column(String(36), ForeignKey('lockers.id'))
    number = Column(Integer)
    status = Column(String(20))
    description = Column(String(255))
