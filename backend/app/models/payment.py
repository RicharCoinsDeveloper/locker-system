from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from . import Base

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(String(36), primary_key=True)
    reservation_id = Column(String(36), ForeignKey('reservations.id'))
    customer_id = Column(String(36), ForeignKey('customers.id'))
    method_id = Column(String(36), ForeignKey('payment_methods.id'))
    cell_id = Column(String(36), ForeignKey('cells.id'))
    rate_id = Column(String(36), ForeignKey('rates.id'))
    amount = Column(Numeric(10,2))
    paid_at = Column(DateTime)
    status = Column(String(20))
    reference = Column(String(100))
