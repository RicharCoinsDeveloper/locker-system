from sqlalchemy import Column, String, DateTime, ForeignKey
from . import Base

class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey('customers.id'))
    locker_id = Column(String(36), ForeignKey('lockers.id'))
    cell_id = Column(String(36), ForeignKey('cells.id'))
    start_at = Column(DateTime)
    end_at = Column(DateTime)
    status = Column(String(20))
