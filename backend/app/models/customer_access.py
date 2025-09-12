from sqlalchemy import Column, String, DateTime, ForeignKey
from . import Base

class CustomerAccess(Base):
    __tablename__ = 'customer_accesses'
    id = Column(String(36), primary_key=True)
    customer_id = Column(String(36), ForeignKey('customers.id'))
    locker_id = Column(String(36), ForeignKey('lockers.id'))
    cell_id = Column(String(36), ForeignKey('cells.id'))
    accessed_at = Column(DateTime)
